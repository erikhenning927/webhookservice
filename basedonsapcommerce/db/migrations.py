"""
Módulo de migrações do banco de dados.
Responsável por gerenciar a criação e atualização de esquemas.
"""

import logging
import os
from .database import get_db, Base
from .models import *  # Importa todos os modelos para registrá-los no Base

logger = logging.getLogger(__name__)


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
