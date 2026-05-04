import time
import asyncio
from utils.utils import parse_order_date, commerce_date, commerce_boolean
from SQL.insert_update_consignment import insert_consignment_to_db, update_order_type



def process_consignment(payload):
    startprocess = time.time()

    details = []
    ######### DATE ##############
    date_info = commerce_date(payload["creationtime"], payload["modifiedtime"])
    departureDate_ = parse_order_date(payload.get("departureDate", None))
    departureDate = departureDate_.get('datetime', None)
    deliveryForecastDate_ = parse_order_date(payload.get("deliveryForecastDate", None))
    deliveryForecastDate = deliveryForecastDate_.get('datetime', None)
    ######### END DATE ##########

    ######### Bool ##########
    isReturnInTransit = commerce_boolean(payload.get("isReturnInTransit", None))
    invoiceSent = commerce_boolean(payload.get("invoiceSent", None))
    ######### END Bool ##########
    shippingLabelProcess = payload.get("shippingLabelProcess", [])
    code_shipping = None

    if shippingLabelProcess and isinstance(shippingLabelProcess, list):
        code_shipping = shippingLabelProcess[0].get("code")

    consignmentProcesses = payload.get("consignmentProcesses", [])
    code_consignment = None

    if consignmentProcesses and isinstance(consignmentProcesses, list):
        code_consignment = consignmentProcesses[0].get("code")
    details.append({
        "orderId": (payload.get("order") or {}).get("code"),
        "consigmentId": payload.get("code", None),
        "romaneioNumber": payload.get("romaneioNumber", None),
        "trackingUrl": payload.get("trackingUrl", None),
        "isReturnInTransit": isReturnInTransit,
        "departureDate": departureDate,
        "trackingCode": payload.get("trackingCode", None),
        "manifestNumber": payload.get("manifestNumber", None),
        "transportadora": payload.get("transportadora", None),
        "exchangeReason": payload.get("exchangeReason", None),
        "invoiceSent": invoiceSent,
        "deliveryForecastDate": deliveryForecastDate,
        "statusDisplay": payload.get("statusDisplay", None),
        "warehouseId": (payload.get("warehouse") or {}).get("code"),
        "status": (payload.get("status") or {}).get("code"),
        "shippingLabelProcess": code_shipping,
        "consignmentProcesses": code_consignment,
        "creationDate": date_info["creationDate"],
        "creationTime": date_info["creationTime"],
        "modifiedDate": date_info["modifiedDate"],
        "modifiedTime": date_info["modifiedTime"]
    })
    print(f"consignmentProcess tooks {(time.time() - startprocess) * 1000:.2f} ms")
    print(details)
    return details
