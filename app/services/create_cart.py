import time
from app.utils.utils import parse_order_date, commerce_date, commerce_boolean
from app.SQL.insert_update_orderCustomer import insert_orderCustomer_to_db
from app.SQL.insert_update_order import insert_order_to_db
from app.SQL.insert_update_deliveryAddress import insert_address_to_db
from app.SQL.insert_update_PaymentInfo import insert_paymentInfos_to_db

def process_cart(payload, hookType):
    startprocess = time.time()

    details = []
    ######### DATE ##############
    date_info = commerce_date(payload["creationtime"], payload["modifiedtime"])
    invoiceShippedDate_ = parse_order_date(payload.get("invoiceShippedDate", None))
    invoiceShippedDate = invoiceShippedDate_.get("datetime", None)
    invoiceDeliveryDate_ = parse_order_date(payload.get("invoiceDeliveryDate", None))
    invoiceDeliveryDate = invoiceDeliveryDate_.get("datetime", None)
    date_ = parse_order_date(payload.get("date", None))
    date = date_.get("datetime", None)
    authorizedDate_ = parse_order_date(payload.get("authorizedDate", None))
    authorizedDate = authorizedDate_.get("datetime", None)
    statusUpdatedAt_ = parse_order_date(payload.get("statusUpdatedAt", None))
    statusUpdatedAt = statusUpdatedAt_.get("datetime", None)

    ######### END DATE ##########

    ######### Bool ##########
    isComplete = commerce_boolean(payload.get("isComplete", None))
    OrderIsIncomplete = commerce_boolean(payload.get("OrderIsIncomplete", None))
    paymentRefundOn = commerce_boolean(payload.get("paymentRefundOn", None))
    cancelledInErp = commerce_boolean(payload.get("cancelledInErp", None))
    cancelledInCommerce = commerce_boolean(payload.get("cancelledInCommerce", None))
    customerIsCorporate = commerce_boolean(payload.get("customerIsCorporate", None))
    if customerIsCorporate == 0:
        customerId = payload.get("customerDocument", None)
    else:
        customerId = payload.get("customerCorporateDocument", None)
    
    ######### END Bool ##########

    deliveryAddress = payload.get("deliveryAddress") or {}
    paymentId = [p.get("code") for p in payload.get("paymentInfos", [])]
    if hookType == 'inboundCart':
        hookType = 'Cart'
    else:
        hookType = 'Order'
    details.append({
        'orderId': payload.get("code", None),
        "paymentId": paymentId[0] if paymentId else '123',
        'customerId': customerId,
        'salesChannelId': (payload.get("salesChannel") or {}).get("Id"),
        'cartProcessId': payload.get("cartProcessId", None),
        'OrderId': payload.get("OrderId", None),
        'Sequence': payload.get("Sequence", None),
        'SellerOrderId': payload.get("SellerOrderId", None),
        'MarketplaceOrderId': payload.get("MarketplaceOrderId", None),
        'Origin': payload.get("Origin", None),
        'AffiliateId': payload.get("AffiliateId", None),
        'Description': (payload.get("Description") or "")[:255],
        'deliveryQuotedCost': payload.get("deliveryQuotedCost", None),
        'isComplete':  isComplete,
        'OrderIsIncomplete': OrderIsIncomplete,
        'invoiceShippedDate': invoiceShippedDate,
        'invoiceDeliveryDate': invoiceDeliveryDate,
        'authorizedDate': authorizedDate,
        'UtmSource': (payload.get("UtmSource") or "")[:100],
        'UtmPartner': (payload.get("UtmPartner") or "")[:100],
        'UtmMedium': (payload.get("UtmMedium") or "")[:100],
        'UtmCampaign': (payload.get("UtmCampaign") or "")[:100],
        'UtmSource': (payload.get("UtmSource") or "")[:100],
        'UtmiCampaign': (payload.get("UtmiCampaign") or "")[:100],
        'UtmiPage': (payload.get("UtmiPage") or "")[:100],
        'UtmiPart': (payload.get("UtmiPart") or "")[:100],
        'date': date,
        'statusUpdatedAt':statusUpdatedAt,
        'paymentRefundOn': paymentRefundOn,
        'paymentRefundAttempts': payload.get("paymentRefundAttempts", None),
        'subtotal': payload.get("subtotal", None),
        'totalDiscounts': payload.get("totalDiscounts", None),
        'ErrorMessage': payload.get("ErrorMessage", None),
        'cancelledInErp': cancelledInErp,
        'cancelledInCommerce': cancelledInCommerce,
        'status': (payload.get("status") or {}).get("code"),
        'exportStatus': (payload.get("exportStatus") or {}).get("code"),
        'blockCart': commerce_boolean(payload.get("blockCart", None)),
        'Type': hookType,
        'customerDocument': payload.get("customerDocument", None),
        'customerFirstName': payload.get("customerFirstName", None),
        'customerLastName': payload.get("customerLastName", None),
        'customerDocumentType': payload.get("customerDocumentType", None),
        'customerPhone': payload.get("customerPhone", None),
        'customerEmail': (payload.get("user") or {}).get("uid"),
        'customerTradeName': payload.get("customerTradeName", None),
        'customerCorporateDocument': payload.get("customerCorporateDocument", None),
        'customerStateInscription': payload.get("customerStateInscription", None),
        'customerCorporatePhone': payload.get("customerCorporatePhone", None),
        'customerIsCorporate': customerIsCorporate,
        'customerUserProfileId': payload.get("customerUserProfileId", None),
        'customerUserProfileVersion': payload.get("customerUserProfileVersion", None),
        'customerClass': payload.get("customerClass", None),
        'customerCode': payload.get("customerCode", None),
        "addressId": (deliveryAddress.get("addressId") or "")[:50],
        "postalcode": deliveryAddress.get("postalcode", None),
        "unloadingAddress": commerce_boolean(deliveryAddress.get("unloadingAddress", None)),
        "streetnumber": (deliveryAddress.get("streetnumber") or "")[:50],
        "complement": (deliveryAddress.get("complement") or "")[:255],
        "remarks": deliveryAddress.get("remarks", None),
        "addressType": (deliveryAddress.get("complement") or "")[:50],
        "contactAddress": commerce_boolean(deliveryAddress.get("contactAddress", None)),
        "shippingAddress": commerce_boolean(deliveryAddress.get("shippingAddress", None)),
        "building": deliveryAddress.get("building", None),
        "cellphone": deliveryAddress.get("cellphone", None),
        "town": deliveryAddress.get("town", None),
        "district": deliveryAddress.get("district", None),
        "appartment": deliveryAddress.get("appartment", None),
        "company": deliveryAddress.get("company", None),
        "typeQualifier": deliveryAddress.get("typeQualifier", None),
        "streetname": deliveryAddress.get("streetname", None),
        "department": deliveryAddress.get("department", None),
        "billingAddress": commerce_boolean(deliveryAddress.get("billingAddress", None)),
        "country": (deliveryAddress.get("country") or {}).get("isocode", None),
        "title": (deliveryAddress.get("title") or {}).get("code", None),
        "region": (deliveryAddress.get("region") or {}).get("isocode", None),
        "creationDate": date_info["creationDate"],
        "creationTime": date_info["creationTime"],
        "modifiedDate": date_info["modifiedDate"],
        "modifiedTime": date_info["modifiedTime"]
    })
    print(f"cartProcess tooks {(time.time() - startprocess) * 1000:.2f} ms")
    print(details)
    return details

