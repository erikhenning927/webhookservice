import re
import time
import logging
from typing import Any, Dict, Optional
from fastapi import APIRouter, Request, BackgroundTasks, Header, HTTPException

from app.services.create_cart import process_cart, insert_orderCustomer_to_db, insert_paymentInfos_to_db, insert_address_to_db, insert_order_to_db
from app.services.create_consignment import process_consignment, insert_consignment_to_db, update_order_type
from app.services.event_history import process_event, insert_eventHistory_to_db, update_order_status
from app.services.create_entries import process_entries, insert_entries_to_db

router = APIRouter()
logger = logging.getLogger(__name__)

def process_payload(payload: Dict[str, Any], hook_type: Optional[str]):
    """Background task to process the incoming webhook payload."""
    try:
        if hook_type in ('inboundCartEntry', 'inboundOrderEntry'):
            logger.info(f"Processando entrada! {hook_type}")
            details = process_entries(payload)
            insert_entries_to_db(details)
            
        elif hook_type in ('inboundConsignment', 'inboundConsignmentReturn'):
            logger.info(f"Processando Consignment! {hook_type}")
            details = process_consignment(payload)
            insert_consignment_to_db(details)
            update_order_type(details)

        elif hook_type in ('inboundCart', 'inboundOrder'):
            logger.info(f"Processando order! {hook_type}")
            details = process_cart(payload, hook_type)
            insert_orderCustomer_to_db(details)
            insert_paymentInfos_to_db(details)
            insert_address_to_db(details)
            insert_order_to_db(details)
            
        elif hook_type == 'inboundEventHistory':
            logger.info(f"Processando event history! {hook_type}")
            details = process_event(payload)
            insert_eventHistory_to_db(details)
            update_order_status(details)

    except Exception as e:
        logger.error(f"Erro no processamento em background: {e}", exc_info=True)


@router.post("/api")
async def hook_service(
    request: Request,
    background_tasks: BackgroundTasks,
    ce_type: Optional[str] = Header(None, alias="Ce-Type")
):
    try:
        start = time.time()
        hook_type = None

        if ce_type:
            match = re.search(r'\.(inbound[^.]+)\.', ce_type)
            if match:
                hook_type = match.group(1)
                
        payload = await request.json()

        # Adiciona o processamento em background usando a feature nativa do FastAPI
        background_tasks.add_task(process_payload, payload, hook_type)

        process_time = (time.time() - start) * 1000
        logger.info(f"Response time took {process_time:.2f} ms")

        return {"message": "Recebido com sucesso"}

    except Exception as e:
        logger.error("Erro ao processar request", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
