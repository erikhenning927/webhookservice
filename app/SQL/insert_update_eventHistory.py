from app.db import get_connection
from app.utils.chunk import chunked_iterable
from datetime import datetime


def insert_eventHistory_to_db(all_eventHistory):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tentar usar fast_executemany se disponível (MSSQL com pyodbc)
    if hasattr(cursor, 'fast_executemany'):
        cursor.fast_executemany = True

    inserted_total = 0
    updated_total = 0
    try:
        update_query = """
        UPDATE commerce_eventHistory
        SET 
            attempts = ?,
            lastExecutionDate = ?,
            consignment = ?
        WHERE orderId = ?
        AND eventId = ?;
        """

        insert_query = """
        INSERT INTO commerce_eventHistory (
            orderId,
            consignment,
            eventId,
            description,
            lastExecutionDate,
            attempts,
            date,
            sourceSystem,
            creationDate,
            creationTime,
            modifiedDate,
            modifiedTime,
            trackingDescription,
            romaneioNumber,
            send,
            trackingCourier,
            trackingUrl,
            manifestNumber,
            trackingCode,
            trackingState,
            trackingCity,
            trackingDispatchedDate,
            departureDate
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        for chunk in chunked_iterable(all_eventHistory, 5000):
            update_data = [
                (
                    eventH['attempts'],
                    eventH['lastExecutionDate'],
                    eventH['consignmentId'],
                    eventH['orderId'],
                    eventH['eventId']
                )
                for eventH in chunk
            ]

            cursor.executemany(update_query, update_data)
            conn.commit()
            updated_rows = cursor.rowcount if cursor.rowcount != -1 else len(update_data)
            updated_total += updated_rows
            print(f"🟡 Atualizados {updated_rows} registros no batch.")

            insert_data = [
                (
                    eventH['orderId'],
                    eventH['consignmentId'],
                    eventH['eventId'],
                    eventH['description'],
                    eventH['lastExecutionDate'],
                    eventH['attempts'],
                    eventH['date'],
                    eventH['sourceSystem'],
                    eventH['creationDate'],
                    eventH['creationTime'],
                    eventH['modifiedDate'],
                    eventH['modifiedTime'],
                    eventH.get('trackingDescription', None),
                    eventH.get('romaneioNumber', None),
                    eventH.get('send', None),
                    eventH.get('trackingCourier', None),
                    eventH.get('trackingUrl', None),
                    eventH.get('manifestNumber', None),
                    eventH.get('trackingCode', None),
                    eventH.get('trackingState', None),
                    eventH.get('trackingCity', None),
                    eventH.get('trackingDispatchedDate', None),
                    eventH.get('departureDate', None)
                )
                for eventH in chunk
                if not record_exists(cursor, eventH['orderId'], eventH['eventId'])
            ]

            if insert_data:
                cursor.executemany(insert_query, insert_data)
                conn.commit()
                inserted_rows = cursor.rowcount if cursor.rowcount != -1 else len(insert_data)
                inserted_total += inserted_rows
                print(f"🟢 Inseridos {inserted_rows} registros no batch.")

        print(f"✅ Finalizado: {inserted_total} inseridos e {updated_total} atualizados.")
    except Exception as e:
        order_id = all_eventHistory[0].get('orderId', 'Unknown')
        error_message = str(e)
        domain = 'commerce_eventHistory'
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Erro ao inserir evento: {e}")
        conn.rollback()
    finally:
        print("Conexão fechada. Finalizando inserção de eventos.")
        cursor.close()
        conn.close()

def record_exists(cursor, orderId, eventId):
    cursor.execute(
        "SELECT 1 FROM commerce_eventHistory WHERE orderId = ? AND eventId = ?",
        (orderId, eventId)
    )
    return cursor.fetchone() is not None

