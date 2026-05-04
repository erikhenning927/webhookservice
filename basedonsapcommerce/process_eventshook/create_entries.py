import time
from utils.utils import parse_order_date, commerce_date, commerce_boolean
from SQL.insert_update_entries import insert_entries_to_db

def process_entries(payload):
    startprocess = time.time()

    details = []
    ######### DATE ##############
    date_info = commerce_date(payload["creationtime"], payload["modifiedtime"])
    namedDeliveryDate_ = parse_order_date(payload.get("namedDeliveryDate", None))
    namedDeliveryDate = namedDeliveryDate_.get('datetime', None)
    ######### END DATE ##########

    ######### Bool ##########
    isReservedIn = commerce_boolean(payload.get("isReservedIn", None))
    isReservedIn = commerce_boolean(payload.get("isReservedIn", None))
    ######### END Bool ##########
    Promotions = payload.get("Promotions", [])
    Promotions_codes = [gp.get("code", None) for gp in Promotions]

    details.append({
        "orderId": (payload.get("order") or {}).get("code"),
        "refId": (payload.get("product") or {}).get("code"),
        "warehouseId": payload.get("warehouse", None),
        "courierId": (payload.get("shippingType") or {}).get("code"),
        "namedDeliveryDate": namedDeliveryDate,
        "sellingPrice": payload.get("sellingPrice", None),
        "deliveryQuotedCost": payload.get("deliveryQuotedCost", None),
        "calculated": payload.get("calculated", None),
        "pointOfService": payload.get("pointOfService", None),
        "basePrice": payload.get("basePrice", None),
        "quantity": payload.get("quantity", None),
        "price": payload.get("price", None),
        "selectedSla": payload.get("selectedSla", None),
        "entryNumber": payload.get("entryNumber", None),
        "info": payload.get("info", None),
        "deliveryCost": payload.get("deliveryCost", None),
        "totalPrice": payload.get("totalPrice", None),
        "costPrice": payload.get("costPrice", None),
        "quantityStatus": payload.get("quantityStatus", None),
        "Promotions": '|'.join(filter(None, Promotions_codes)),
        "creationDate": date_info["creationDate"],
        "creationTime": date_info["creationTime"],
        "modifiedDate": date_info["modifiedDate"],
        "modifiedTime": date_info["modifiedTime"]
    })
    print(f"entriesProcess tooks {(time.time() - startprocess) * 1000:.2f} ms")
    print(details)
    return details
