import os
import pyodbc
from sqlalchemy import create_engine, inspect, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()

class Database:
    """
    Gerenciador de conexão com banco de dados usando SQLAlchemy.
    Similar ao comportamento do TypeORM em aplicações Node.js.
    """
    
    def __init__(self, database_url: str = None):
        """
        Inicializa a conexão com o banco de dados.
        
        Args:
            database_url: String de conexão do banco. Se None, usa variável de ambiente.
        """
        if database_url is None:
            database_url = os.getenv(
                "DATABASE_URL",
                None
            )
        
        self.database_url = database_url
        
        # Configurar engine baseado no tipo de banco
        if database_url and "sqlite" in database_url.lower():
            self.engine = create_engine(
                database_url,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
            )
        elif database_url and "mssql" in database_url.lower():
            # Para SQL Server via URL do SQLAlchemy
            self.engine = create_engine(
                database_url,
                pool_size=10,
                max_overflow=20,
                pool_recycle=3600,
                echo=False
            )
        else:
            # Conexão direta com pyodbc (quando DATABASE_URL não é fornecida)
            # Usa variáveis de ambiente user_db, pass_db, etc
            user_db = os.getenv('user_db', 'sa')
            pass_db = os.getenv('pass_db', '')
            host_db = os.getenv('host_db', 'localhost,1433')
            db_name = os.getenv('db_name', 'master')
            
            try:
                connection_string = (
                    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
                    f"SERVER={host_db};"
                    f"DATABASE={db_name};"
                    f"UID={user_db};"
                    f"PWD={pass_db};"
                    f"TrustServerCertificate=yes"
                )
                
                # Testa conexão com pyodbc primeiro
                test_conn = pyodbc.connect(connection_string)
                test_conn.close()
                
                # Se funcionou, criar engine com pyodbc
                self.database_url = connection_string
                self.engine = create_engine(
                    f"mssql+pyodbc:///?odbc_connect={connection_string}",
                    pool_size=10,
                    max_overflow=20,
                    pool_recycle=3600,
                )
                
            except Exception as e:
                logger.error(f"Erro ao conectar com pyodbc: {e}")
                raise
        
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
    
    def create_all_tables(self):
        """Cria todas as tabelas definidas nos modelos."""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("✅ Todas as tabelas foram criadas com sucesso!")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao criar tabelas: {e}")
            raise
    
    def drop_all_tables(self):
        """Remove todas as tabelas (cuidado ao usar!)."""
        try:
            Base.metadata.drop_all(bind=self.engine)
            logger.info("Todas as tabelas foram removidas")
            return True
        except Exception as e:
            logger.error(f"Erro ao remover tabelas: {e}")
            raise
    
    def get_session(self):
        """Retorna uma nova sessão do banco de dados."""
        return self.SessionLocal()
    
    def get_connection(self):
        """
        Retorna uma conexão raw do banco de dados para execução de SQL direto.
        Útil para INSERT/UPDATE em batch com executemany().
        
        Para MSSQL: Retorna conexão pyodbc
        Para SQLite: Retorna conexão sqlite3
        Para outros: Retorna conexão raw do engine
        
        Returns:
            Conexão do banco de dados.
        """
        try:
            if "mssql" in self.database_url.lower():
                # Extrai a string de conexão ODBC da URL
                if "odbc_connect=" in self.database_url:
                    # URL SQLAlchemy: mssql+pyodbc:///?odbc_connect=...
                    import urllib.parse
                    odbc_string = self.database_url.split("odbc_connect=", 1)[1]
                    odbc_string = urllib.parse.unquote(odbc_string)
                    return pyodbc.connect(odbc_string)
                else:
                    # String de conexão direta
                    return pyodbc.connect(self.database_url)
            elif "sqlite" in self.database_url.lower():
                # Para SQLite, usar conexão raw do engine
                return self.engine.raw_connection()
            else:
                # Para outros bancos, usar conexão raw do engine
                return self.engine.raw_connection()
        except Exception as e:
            logger.error(f"Erro ao obter conexão: {e}")
            raise
    
    def check_tables_exist(self) -> dict:
        """
        Verifica quais tabelas já existem no banco de dados.
        
        Returns:
            Dicionário com informações das tabelas existentes.
        """
        inspector = inspect(self.engine)
        existing_tables = inspector.get_table_names()
        
        return {
            "existing_tables": existing_tables,
            "count": len(existing_tables)
        }
    
    def close(self):
        """Fecha todas as conexões do pool."""
        self.engine.dispose()


# Instância global do banco de dados
_db_instance = None

def get_db(database_url: str = None) -> Database:
    """
    Obtém a instância singleton do gerenciador de banco de dados.
    
    Args:
        database_url: String de conexão (usado apenas na primeira chamada).
    
    Returns:
        Instância do Database.
    """
    global _db_instance
    
    if _db_instance is None:
        _db_instance = Database(database_url)
    
    return _db_instance
