import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.migrations import run_migrations
from app.api.endpoints import webhook
from app.core.config import settings

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Executar migrações ao iniciar a aplicação
    try:
        logger.info("🚀 Iniciando aplicação...")
        logger.info("📊 Tentando conectar ao banco de dados...")
        
        if run_migrations():
            logger.info("✅ Banco de dados pronto!")
        else:
            logger.warning("⚠️  Falha ao executar migrações - Verifique as credenciais do SQL Server no arquivo .env")
            logger.warning("   Se você não configurou o .env, copie de .env.example e adicione suas credenciais")
            logger.warning("   A aplicação continuará rodando, mas sem persistência de dados")
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar aplicação: {e}", exc_info=True)
        
    yield
    # Lógica de shutdown (se necessário)
    logger.info("🛑 Encerrando aplicação...")

app = FastAPI(
    title="Webhook Service API",
    description="API for processing webhooks built with FastAPI",
    version="1.0.0",
    lifespan=lifespan
)

# Registrar rotas
app.include_router(webhook.router, prefix="/hook_service", tags=["Webhooks"])

# Para rodar usando uvicorn:
# uvicorn app.main:app --host 0.0.0.0 --port 5005
