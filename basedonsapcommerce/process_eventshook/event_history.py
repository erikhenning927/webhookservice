import time
import asyncio
from utils.utils import parse_order_date, commerce_date, commerce_boolean
from SQL.insert_update_eventHistory import insert_eventHistory_to_db
from  SQL.insert_update_order import update_order_status



def process_event(payload):
    startprocess = time.time()

    details = []
    ######### DATE ##############
    date_info = commerce_date(payload["creationtime"], payload["modifiedtime"])
    date_ = parse_order_date(payload.get("date", None))
    date = date_.get('datetime', None)
    lastExecutionDate_ = parse_order_date(payload.get("lastExecutionDate", None))
    lastExecutionDate = lastExecutionDate_.get('datetime', None)
    trackingDispatchedDate_ = parse_order_date(payload.get("trackingDispatchedDate", None))
    trackingDispatchedDate = trackingDispatchedDate_.get('datetime', None)
    departureDate_ = parse_order_date(payload.get("departureDate", None))
    departureDate = departureDate_.get('datetime', None)
    send = commerce_boolean(payload.get("send", None))
    ######### END DATE ##########

    order = payload.get("order", {})
    details.append({
        "orderId": (payload.get("order") or {}).get("code"),
        "consignmentId": (payload.get("consignment") or {}).get("code"),
        "eventId": (payload.get("britaniaEvent") or {}).get("code"),
        "description": (payload.get("description") or "")[:255],
        "attempts": payload.get("attempts", None),
        "sourceSystem": (payload.get("sourceSystem") or {}).get("code"),
        "status": (order.get("status") or {}).get("code"),
        "status": (order.get("status") or {}).get("code"),
        "status": (order.get("status") or {}).get("code"),
        "date": date,
        "lastExecutionDate": lastExecutionDate,
        "trackingDescription": payload.get("trackingDescription", None),
        "romaneioNumber": payload.get("romaneioNumber", None),
        "send": send,
        "trackingCourier": payload.get("trackingCourier", None),
        "trackingUrl": payload.get("trackingUrl", None),
        "manifestNumber": payload.get("manifestNumber", None),
        "trackingCode": payload.get("trackingCode", None),
        "trackingState": payload.get("trackingState", None),
        "trackingCity": payload.get("trackingCity", None),
        "trackingDispatchedDate": trackingDispatchedDate,
        "departureDate": departureDate,
        "creationDate": date_info["creationDate"],
        "creationTime": date_info["creationTime"],
        "modifiedDate": date_info["modifiedDate"],
        "modifiedTime": date_info["modifiedTime"]
    })
    print(f"ProcessEvent levou {(time.time() - startprocess) * 1000:.2f} ms")
    print(details)
    return details
