from app.db import get_connection
from app.utils.chunk import chunked_iterable
from app.utils.utils import load_sql
from datetime import datetime

def insert_consignment_to_db(all_consigment):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tentar usar fast_executemany se disponível (MSSQL com pyodbc)
    if hasattr(cursor, 'fast_executemany'):
        cursor.fast_executemany = True

    inserted_total = 0
    updated_total = 0
    try:
        update_query = """
        UPDATE commerce_consignments
        SET 
            orderId = ?,
            romaneioNumber = ?,
            trackingUrl = ?,
            isReturnInTransit = ?,
            departureDate = ?,
            trackingCode = ?,
            manifestNumber = ?,
            transportadora = ?,
            exchangeReason = ?,
            invoiceSent = ?,
            deliveryForecastDate = ?,
            statusDisplay = ?,
            shippingLabelProcess = ?,
            warehouseId = ?,
            consignmentProcesses = ?,
            status = ?,
            modifiedDate = ?,
            modifiedTime = ?
        WHERE consigmentId = ?;
        """

        insert_query = """
        INSERT INTO commerce_consignments (
            consigmentId,
            orderId,
            romaneioNumber,
            trackingUrl,
            isReturnInTransit,
            departureDate,
            trackingCode,
            manifestNumber,
            transportadora,
            exchangeReason,
            invoiceSent,
            deliveryForecastDate,
            statusDisplay,
            shippingLabelProcess,
            warehouseId,
            consignmentProcesses,
            status,
            creationDate,
            creationTime,
            modifiedDate,
            modifiedTime
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        for chunk in chunked_iterable(all_consigment, 5000):
            update_data = [
                (
                    consignment.get('orderId', None),
                    consignment.get('romaneioNumber', None),
                    consignment.get('trackingUrl', None),
                    consignment.get('isReturnInTransit', None),
                    consignment.get('departureDate', None),
                    consignment.get('trackingCode', None),
                    consignment.get('manifestNumber', None),
                    consignment.get('transportadora', None),
                    consignment.get('exchangeReason', None),
                    consignment.get('invoiceSent', None),
                    consignment.get('deliveryForecastDate', None),
                    consignment.get('statusDisplay', None),
                    consignment.get('shippingLabelProcess', None),
                    consignment.get('warehouseId', None),
                    consignment.get('consignmentProcesses', None),
                    consignment.get('status', None),
                    consignment.get('modifiedDate', None),
                    consignment.get('modifiedTime', None),
                    consignment.get('consigmentId', None)
                )
                for consignment in chunk
            ]

            cursor.executemany(update_query, update_data)
            conn.commit()
            updated_rows = cursor.rowcount if cursor.rowcount != -1 else len(update_data)
            updated_total += updated_rows
            print(f"🟡 Atualizados {updated_rows} registros no batch.")

            insert_data = [
                (
                    consignment.get('consigmentId', None),
                    consignment.get('orderId', None),
                    consignment.get('romaneioNumber', None),
                    consignment.get('trackingUrl', None),
                    consignment.get('isReturnInTransit', None),
                    consignment.get('departureDate', None),
                    consignment.get('trackingCode', None),
                    consignment.get('manifestNumber', None),
                    consignment.get('transportadora', None),
                    consignment.get('exchangeReason', None),
                    consignment.get('invoiceSent', None),
                    consignment.get('deliveryForecastDate', None),
                    consignment.get('statusDisplay', None),
                    consignment.get('shippingLabelProcess', None),
                    consignment.get('warehouseId', None),
                    consignment.get('consignmentProcesses', None),
                    consignment.get('status', None),
                    consignment.get('creationDate', None),
                    consignment.get('creationTime', None),
                    consignment.get('modifiedDate', None),
                    consignment.get('modifiedTime', None)
                )
                for consignment in chunk
                if not record_exists(cursor, consignment.get('consigmentId', None))
            ]

            if insert_data:
                cursor.executemany(insert_query, insert_data)
                conn.commit()
                inserted_rows = cursor.rowcount if cursor.rowcount != -1 else len(insert_data)
                inserted_total += inserted_rows
                print(f"🟢 Inseridos {inserted_rows} registros no batch.")

        print(f"✅ Finalizado: {inserted_total} inseridos e {updated_total} atualizados.")
    except Exception as e:
        order_id = all_consigment[0].get('consigmentId', 'Unknown')
        error_message = str(e)
        domain = 'commerce_consignments'
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Erro ao inserir consignment: {e}")
        conn.rollback()
    finally:
        print("Conexão fechada. Finalizando inserção de consignment.")
        cursor.close()
        conn.close()

def record_exists(cursor, consigmentId):
    if not consigmentId:
        return False
    cursor.execute(
        "SELECT 1 FROM commerce_consignments WHERE consigmentId = ?",
        (consigmentId,)
    )
    return cursor.fetchone() is not None


def update_order_type(all_consignment):
    conn = get_connection()
    cursor = conn.cursor()

    update_query = load_sql('commerce_order/update_type.sql', 'Queries')

    update_batch = []
    for order in all_consignment:
        try:
            update_values = (
                'Order',
                '1',
                order['orderId']
            )
            update_batch.append(update_values)
        except KeyError as e:
            print(f"Missing key {e} in orderId: {order['orderId']}")

    if update_batch:
        cursor.executemany(update_query, update_batch)
        print(f"{len(update_batch)} pedidos atualizados com tipo no banco com sucesso.")

    conn.commit()
    cursor.close()
    conn.close()