from flask import Flask, request, jsonify
import threading
import logging
import re
import time
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

from process_eventshook.create_cart import *
from process_eventshook.create_consignment import *
from process_eventshook.event_history import *
from process_eventshook.create_entries import *
from db.migrations import run_migrations


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

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

@app.route('/hook_service/api', methods=['POST'])
def hook_service():

    try:
        start = time.time()
        ce_type = request.headers.get('Ce-Type')
        hook_type = None

        if ce_type:
            match = re.search(r'\.(inbound[^.]+)\.', ce_type)
            print(match, 'match')
            if match:
                hook_type = match.group(1)
        payload = request.get_json()
        # print("Received payload:", payload)

        # processamento em background
        threading.Thread(target=process_payload, args=(payload, hook_type)).start()

        print(f"Response time took {(time.time() - start) * 1000:.2f} ms")


        return "Recebido com sucesso", 200

    except Exception as e:
        logging.error("Erro ao processar request", exc_info=True)
        print(f"Erro ao processar request{e}")
        return str(e), 400


def process_payload(payload, hook_type):
    try:
        event_code = (payload.get("britaniaEvent") or {}).get("code", None)


        if hook_type == 'inboundCartEntry' or hook_type == 'inboundOrderEntry':
            print("Processando entrada!", hook_type)
            details = process_entries(payload)
            insert_entries_to_db(details)
        if hook_type in ('inboundConsignment', 'inboundBritaniaConsignmentReturn'):
            print("Processando Consignment!", hook_type)
            details = process_consignment(payload)
            insert_consignment_to_db(details)
            update_order_type(details)

        if hook_type in ('inboundCart', 'inboundOrder'):
            print("Processando order!", hook_type)
            details = process_cart(payload, hook_type)
            insert_orderCustomer_to_db(details)
            insert_paymentInfos_to_db(details)
            insert_address_to_db(details)
            insert_order_to_db(details)
        if hook_type == 'inboundEventHistory':
            details = process_event(payload)
            insert_eventHistory_to_db(details)
            update_order_status(details)

    except Exception as e:
       logging.error(f"Erro no processamento em background: {e}", exc_info=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)