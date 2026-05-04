from app.db import get_connection
from app.utils.chunk import chunked_iterable
from app.utils.utils import load_sql
from datetime import datetime


def insert_entries_to_db(all_entries):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tentar usar fast_executemany se disponível (MSSQL com pyodbc)
    if hasattr(cursor, 'fast_executemany'):
        cursor.fast_executemany = True

    inserted_total = 0
    updated_total = 0
    try:
        update_query = """
        UPDATE commerce_cartEntry
        SET 
            warehouseId = ?,
            courierId = ?,
            namedDeliveryDate = ?,
            sellingPrice = ?,
            isReservedInErp = ?,
            deliveryQuotedCost = ?,
            calculated = ?,
            pointOfService = ?,
            basePrice = ?,
            quantity = ?,
            price = ?,
            selectedSla = ?,
            entryNumber = ?,
            info = ?,
            deliveryCost = ?,
            totalPrice = ?,
            costPrice = ?,
            quantityStatus = ?,
            Promotions = ?,
            creationDate = ?,
            creationTime = ?,
            modifiedDate = ?,
            modifiedTime = ?
        WHERE orderId = ? and refId = ?;
        """

        insert_query = """
        INSERT INTO commerce_cartEntry (
            orderId,
            refId,
            warehouseId,
            courierId,
            namedDeliveryDate,
            sellingPrice,
            isReservedInErp,
            deliveryQuotedCost,
            calculated,
            pointOfService,
            basePrice,
            quantity,
            price,
            selectedSla,
            entryNumber,
            info,
            deliveryCost,
            totalPrice,
            costPrice,
            quantityStatus,
            Promotions,
            creationDate,
            creationTime,
            modifiedDate,
            modifiedTime
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        for chunk in chunked_iterable(all_entries, 5000):
            update_data = [
                (
                    entry.get('warehouseId', None),
                    entry.get('courierId', None),
                    entry.get('namedDeliveryDate', None),
                    entry.get('sellingPrice', None),
                    entry.get('isReservedInErp', None),
                    entry.get('deliveryQuotedCost', None),
                    entry.get('calculated', None),
                    entry.get('pointOfService', None),
                    entry.get('basePrice', None),
                    entry.get('quantity', None),
                    entry.get('price', None),
                    entry.get('selectedSla', None),
                    entry.get('entryNumber', None),
                    entry.get('info', None),
                    entry.get('deliveryCost', None),
                    entry.get('totalPrice', None),
                    entry.get('costPrice', None),
                    entry.get('quantityStatus', None),
                    entry.get('Promotions', None),
                    entry.get('creationDate', None),
                    entry.get('creationTime', None),
                    entry.get('modifiedDate', None),
                    entry.get('modifiedTime', None),
                    entry.get('orderId', None),
                    entry.get('refId', None)
                )
                for entry in chunk
            ]

            cursor.executemany(update_query, update_data)
            conn.commit()
            updated_rows = cursor.rowcount if cursor.rowcount != -1 else len(update_data)
            updated_total += updated_rows
            print(f"🟡 Atualizados {updated_rows} registros no batch.")

            insert_data = [
                (
                    entry.get('orderId', None),
                    entry.get('refId', None),
                    entry.get('warehouseId', None),
                    entry.get('courierId', None),
                    entry.get('namedDeliveryDate', None),
                    entry.get('sellingPrice', None),
                    entry.get('isReservedInErp', None),
                    entry.get('deliveryQuotedCost', None),
                    entry.get('calculated', None),
                    entry.get('pointOfService', None),
                    entry.get('basePrice', None),
                    entry.get('quantity', None),
                    entry.get('price', None),
                    entry.get('selectedSla', None),
                    entry.get('entryNumber', None),
                    entry.get('info', None),
                    entry.get('deliveryCost', None),
                    entry.get('totalPrice', None),
                    entry.get('costPrice', None),
                    entry.get('quantityStatus', None),
                    entry.get('Promotions', None),
                    entry.get('creationDate', None),
                    entry.get('creationTime', None),
                    entry.get('modifiedDate', None),
                    entry.get('modifiedTime', None)
                )
                for entry in chunk
                if not record_exists(cursor, entry.get('orderId', None), entry.get('refId', None))
            ]

            if insert_data:
                cursor.executemany(insert_query, insert_data)
                conn.commit()
                inserted_rows = cursor.rowcount if cursor.rowcount != -1 else len(insert_data)
                inserted_total += inserted_rows
                print(f"🟢 Inseridos {inserted_rows} registros no batch.")

        print(f"✅ Finalizado: {inserted_total} inseridos e {updated_total} atualizados.")
    except Exception as e:
        order_id = all_entries[0].get('orderId', 'Unknown')
        error_message = str(e)
        domain = 'commerce_cartEntry'
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Erro ao inserir entrada: {e}")
        conn.rollback()
    finally:
        print("Conexão fechada. Finalizando inserção de entrada.")
        cursor.close()
        conn.close()

def record_exists(cursor, orderId, refId):
    if not orderId or not refId:
        return False
    cursor.execute(
        "SELECT 1 FROM commerce_cartEntry WHERE orderId = ? AND refId = ?",
        (orderId, refId)
    )
    return cursor.fetchone() is not None

