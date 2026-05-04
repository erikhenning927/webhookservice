from app.db import get_connection
from app.utils.chunk import chunked_iterable
from app.utils.utils import load_sql
from datetime import datetime


def insert_order_to_db(all_orders):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tentar usar fast_executemany se disponível (MSSQL com pyodbc)
    if hasattr(cursor, 'fast_executemany'):
        cursor.fast_executemany = True
    try:
        update_query = """
        UPDATE commerce_orders
        SET
            paymentId = ?,
            customerId = ?,
            salesChannelId = ?,
            OrderId = ?,
            Sequence = ?,
            SellerOrderId = ?,
            MarketplaceOrderId = ?,
            Origin = ?,
            AffiliateId = ?,
            Description = ?,
            deliveryQuotedCost = ?,
            isComplete = ?,
            authorizedDate = ?,
            OrderIsIncomplete = ?,
            invoiceShippedDate = ?,
            invoiceDeliveryDate = ?,
            UtmSource = ?,
            UtmPartner = ?,
            UtmMedium = ?,
            UtmCampaign = ?,
            UtmiCampaign = ?,
            UtmiPage = ?,
            UtmiPart = ?,
            date = ?,
            statusUpdatedAt = ?,
            paymentRefundOn = ?,
            paymentRefundAttempts = ?,
            subtotal = ?,
            totalDiscounts = ?,
            cancelledIn = ?,
            status = ?,
            exportStatus = ?,
            blockCart = ?,
            Type = ?,
            creationDate = ?,
            creationTime = ?,
            modifiedDate = ?,
            modifiedTime = ?
        WHERE orderId = ?
        """

        insert_query = """
        INSERT INTO commerce_orders (
            orderId, paymentId, customerId, salesChannelId, Sequence, SellerOrderId, MarketplaceOrderId, Origin, AffiliateId, 
            Description, deliveryQuotedCost, isComplete, authorizedDate, OrderIsIncomplete, invoiceShippedDate, 
            invoiceDeliveryDate, UtmSource, UtmPartner, UtmMedium, UtmCampaign, UtmiCampaign, UtmiPage, 
            UtmiPart, date, statusUpdatedAt, paymentRefundOn, paymentRefundAttempts, subtotal, totalDiscounts, cancelledIn, status, exportStatus, blockCart, Type, 
            creationDate, creationTime, modifiedDate, modifiedTime
        )
        SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        WHERE NOT EXISTS (SELECT 1 FROM commerce_orders WHERE orderId = ?)
        """

        for chunk in chunked_iterable(all_orders, 10000):
            update_values = []
            insert_values = []
            for order in chunk:
                try:
                    # Combinar cancelledInErp e cancelledInCommerce: se qualquer um for 1, cancelledIn = 1
                    cancelled_in = 1 if (order.get('cancelledInErp') or order.get('cancelledInCommerce')) else 0
                    
                    values = (
                        order['paymentId'], order['customerId'], order['salesChannelId'], order['OrderId'],
                        order['Sequence'], order['SellerOrderId'], order['MarketplaceOrderId'], order['Origin'], order['AffiliateId'], order['Description'],
                        order['deliveryQuotedCost'], order['isComplete'], order['authorizedDate'], order['OrderIsIncomplete'],
                        order['invoiceShippedDate'], order['invoiceDeliveryDate'], order['UtmSource'], order['UtmPartner'],
                        order['UtmMedium'], order['UtmCampaign'], order['UtmiCampaign'], order['UtmiPage'],
                        order['UtmiPart'], order['date'], order['statusUpdatedAt'], order['paymentRefundOn'], 
                        order['paymentRefundAttempts'], order['subtotal'], order['totalDiscounts'],
                        cancelled_in,
                        order['status'], order['exportStatus'], order['blockCart'], order['Type'], order['creationDate'], 
                        order['creationTime'], order['modifiedDate'], order['modifiedTime'], order['orderId']
                    )
                    update_values.append(values)

                    insert_values.append((
                        order['orderId'], order['paymentId'], order['customerId'], order['salesChannelId'],
                        order['Sequence'], order['SellerOrderId'], order['MarketplaceOrderId'], order['Origin'], order['AffiliateId'], order['Description'],
                        order['deliveryQuotedCost'], order['isComplete'], order['authorizedDate'], order['OrderIsIncomplete'],
                        order['invoiceShippedDate'], order['invoiceDeliveryDate'], order['UtmSource'], order['UtmPartner'],
                        order['UtmMedium'], order['UtmCampaign'], order['UtmiCampaign'], order['UtmiPage'],
                        order['UtmiPart'], order['date'], order['statusUpdatedAt'], order['paymentRefundOn'],
                        order['paymentRefundAttempts'], order['subtotal'], order['totalDiscounts'],
                        cancelled_in,
                        order['status'], order['exportStatus'], order['blockCart'], order['Type'], order['creationDate'],
                        order['creationTime'], order['modifiedDate'], order['modifiedTime'], order['orderId']
                    ))
                except KeyError as e:
                    print(f"Missing key {e} in orderId: {order.get('orderId', 'Unknown')}")

            if update_values:
                cursor.executemany(update_query, update_values)
            if insert_values:
                cursor.executemany(insert_query, insert_values)

            print(f"{len(update_values)} pedidos atualizados, {len(insert_values)} pedidos inseridos.")

        conn.commit()
    except Exception as e:
        order_id = order.get('orderId', 'Unknown')
        error_message = str(e)
        domain = 'commerce_orders'
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Erro ao inserir order: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def update_order_status(all_events):
    conn = get_connection()
    cursor = conn.cursor()

    update_query = load_sql('commerce_order/update_order_status.sql', 'Queries')

    # Agrupar eventos por orderId
    latest_events = {}
    for event in all_events:
        order_id = event.get('orderId')
        if not order_id:
            continue

        # Se já existe, comparar datas para pegar o mais recente
        current_event = latest_events.get(order_id)
        if not current_event or event.get('statusUpdatedAt', '') > current_event.get('statusUpdatedAt', ''):
            latest_events[order_id] = event

    update_batch = []
    for order_id, event in latest_events.items():
        try:
            update_values = (
                event['status'],
                order_id
            )
            update_batch.append(update_values)
        except KeyError as e:
            print(f"Missing key {e} in orderId: {order_id}")

    if update_batch:
        cursor.executemany(update_query, update_batch)
        print(f"{len(update_batch)} pedidos atualizados com status no banco com sucesso.")

    conn.commit()
    cursor.close()
    conn.close()