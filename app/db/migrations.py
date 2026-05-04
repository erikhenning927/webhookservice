"""
Módulo de migrações do banco de dados.
Responsável por gerenciar a criação e atualização de esquemas.
"""

import logging
import os
from .database import get_db, Base
from .models import *  # Importa todos os modelos para registrá-los no Base

logger = logging.getLogger(__name__)

def seed_database(db):
    """Lê e executa o arquivo SQL de inserção de dimensões iniciais."""
    try:
        from sqlalchemy import text
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        sql_path = os.path.join(base_dir, 'SQL', 'insert_dim_examples.sql')
        
        if not os.path.exists(sql_path):
            logger.warning(f"⚠️ Script SQL não encontrado em: {sql_path}")
            return
            
        with open(sql_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()
            
        # Pega a conexão raw ou a engine para executar o script
        # Separando os inserts em blocos se houver mais de um, ou rodando tudo de uma vez
        with db.engine.begin() as conn:
            # Verifica se já existem dados em dim_events (usado como referência)
            result = conn.execute(text("SELECT COUNT(*) FROM dim_events"))
            count = result.scalar()
            if count > 0:
                logger.info("ℹ️ Banco de dados já possui dados de exemplo. Seed ignorado.")
                return

            logger.info("🌱 Populando tabelas de dimensões com dados iniciais...")
            # O SQLAlchemy engine.execute ou conn.execute lida com múltiplas queries no SQL Server.
            # Mas se falhar, podemos tentar dividir por blocos.
            conn.execute(text(sql_script))
            logger.info("✅ Dados de exemplo inseridos com sucesso!")
            
    except Exception as e:
        logger.warning(f"⚠️ Falha ao executar script de seed (talvez os dados já existam): {e}")

def run_migrations(database_url: str = None) -> bool:
    """
    Executa as migrações do banco de dados.
    Cria todas as tabelas se não existirem.
    
    Esta função deve ser chamada quando a aplicação inicia.
    
    Args:
        database_url: URL de conexão do banco (opcional).
    
    Returns:
        True se bem-sucedido, False caso contrário.
    """
    try:
        db = get_db(database_url)
        
        # Verifica tabelas existentes
        existing = db.check_tables_exist()
        logger.info(f"Tabelas existentes: {existing['count']}")
        
        if existing['count'] > 0:
            logger.info(f"Tabelas encontradas: {', '.join(existing['existing_tables'][:5])}...")
        
        # Cria todas as tabelas
        logger.info("🔄 Iniciando migração do banco de dados...")
        db.create_all_tables()
        
        # Verifica novamente
        existing_after = db.check_tables_exist()
        logger.info(f"✅ Migração concluída! Total de tabelas: {existing_after['count']}")
        
        # Opcional: Popular as tabelas com os dados de exemplo se o banco for novo (ou ignorar erros)
        seed_database(db)
        
        return True
        
    except Exception as e:
        error_str = str(e).lower()
        
        # Erro de autenticação (Login failed)
        if "login failed" in error_str or "28000" in error_str:
            logger.error("❌ ERRO DE AUTENTICAÇÃO: Falha no login do usuário SQL Server")
            logger.error("   Verifique suas credenciais no arquivo .env")
            logger.error(f"   DATABASE_URL deve ter o formato:")
            logger.error(f"   mssql+pyodbc://usuario:senha@host:porta/banco?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes")
            logger.error(f"\n   Exemplo:")
            logger.error(f"   DATABASE_URL=mssql+pyodbc://sa:sua_senha@localhost:1433/webhookservice?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes")
            
        # Erro de conexão
        elif "connection refused" in error_str or "connection" in error_str or "08001" in error_str:
            logger.error("❌ ERRO DE CONEXÃO: Não foi possível conectar ao SQL Server")
            logger.error("   Verifique se:")
            logger.error("   1. O SQL Server está rodando e acessível")
            logger.error("   2. O host e porta estão corretos no .env")
            logger.error("   3. Firewall não está bloqueando a porta (padrão: 1433)")
            
        else:
            logger.error(f"❌ Erro durante migração: {e}")
        
        # Não retorna traceback completo para não poluir logs
        return False


def rollback_migrations(database_url: str = None) -> bool:
    """
    Remove todas as tabelas do banco de dados (CUIDADO!).
    
    Args:
        database_url: URL de conexão do banco (opcional).
    
    Returns:
        True se bem-sucedido, False caso contrário.
    """
    try:
        db = get_db(database_url)
        
        logger.warning("⚠️  Iniciando rollback de todas as tabelas...")
        db.drop_all_tables()
        
        logger.info("✅ Rollback concluído!")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro durante rollback: {e}", exc_info=True)
        return False


def get_session():
    """
    Obtém uma nova sessão do banco de dados.
    
    Returns:
        Sessão SQLAlchemy.
    """
    db = get_db()
    return db.get_session()
