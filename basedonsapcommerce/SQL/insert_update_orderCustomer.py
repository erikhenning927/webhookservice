from db import get_connection
from utils.chunk import chunked_iterable
from datetime import datetime


def insert_orderCustomer_to_db(all_orderCustomers):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tentar usar fast_executemany se disponível (MSSQL com pyodbc)
    if hasattr(cursor, 'fast_executemany'):
        cursor.fast_executemany = True

    inserted_total = 0
    updated_total = 0
    try:
        update_query = """
        UPDATE commerce_orderCustomer
        SET
            customerDocument = ?,
            customerFirstName = ?,
            customerLastName = ?,
            customerDocumentType = ?,
            customerPhone = ?,
            customerEmail = ?,
            customerTradeName = ?,
            customerCorporateDocument = ?,
            customerStateInscription = ?,
            customerCorporatePhone = ?,
            customerIsCorporate = ?,
            customerUserProfileId = ?,
            customerUserProfileVersion = ?,
            customerClass = ?,
            customerCode = ?
        WHERE orderId = ? AND customerId = ?;
        """

        insert_query = """
        INSERT INTO commerce_orderCustomer (
            customerId, orderId, customerDocument, customerFirstName, customerLastName,
            customerDocumentType, customerPhone, customerEmail, customerTradeName,
            customerCorporateDocument, customerStateInscription, customerCorporatePhone,
            customerIsCorporate, customerUserProfileId, customerUserProfileVersion,
            customerClass, customerCode
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        for chunk in chunked_iterable(all_orderCustomers, 10000):
            
            update_data = [
                (
                    customer.get('customerDocument'),
                    customer.get('customerFirstName'),
                    customer.get('customerLastName', '')[:100],
                    customer.get('customerDocumentType'),
                    customer.get('customerPhone'),
                    customer.get('customerEmail'),
                    customer.get('customerTradeName'),
                    customer.get('customerCorporateDocument'),
                    customer.get('customerStateInscription'),
                    customer.get('customerCorporatePhone'),
                    customer.get('customerIsCorporate'),
                    customer.get('customerUserProfileId'),
                    customer.get('customerUserProfileVersion'),
                    customer.get('customerClass'),
                    customer.get('customerCode'),
                    customer.get('orderId'),
                    customer.get('customerId')
                )
                for customer in chunk
            ]
            cursor.executemany(update_query, update_data)
            conn.commit()
            updated_rows = cursor.rowcount if cursor.rowcount != -1 else len(update_data)
            updated_total += updated_rows
            print(f"🟡 Atualizados {updated_rows} clientes no batch.")

            insert_data = [
                (
                    customer.get('customerId'),
                    customer.get('orderId'),
                    customer.get('customerDocument'),
                    customer.get('customerFirstName'),
                    customer.get('customerLastName', '')[:100],
                    customer.get('customerDocumentType'),
                    customer.get('customerPhone'),
                    customer.get('customerEmail'),
                    customer.get('customerTradeName'),
                    customer.get('customerCorporateDocument'),
                    customer.get('customerStateInscription'),
                    customer.get('customerCorporatePhone'),
                    customer.get('customerIsCorporate'),
                    customer.get('customerUserProfileId'),
                    customer.get('customerUserProfileVersion'),
                    customer.get('customerClass'),
                    customer.get('customerCode')
                )
                for customer in chunk
                if not orderCustomer_exists(cursor, customer.get('orderId'), customer.get('customerId'))
            ]

            if insert_data:
                cursor.executemany(insert_query, insert_data)
                conn.commit()
                inserted_rows = cursor.rowcount if cursor.rowcount != -1 else len(insert_data)
                inserted_total += inserted_rows
                print(f"Inseridos {inserted_rows} clientes no batch.")

        print(f"Finalizado: {inserted_total} inseridos e {updated_total} atualizados.")
    except Exception as e:
        order_id = all_orderCustomers[0].get('orderId', 'Unknown')
        error_message = str(e)
        domain = 'commerce_orderCustomer'
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Erro ao inserir clientes: {e}")
        conn.rollback()
    finally:
        print("Conexão fechada. Finalizando inserção de clientes.")
        cursor.close()
        conn.close()

def orderCustomer_exists(cursor, orderId, customerId):
    if not orderId or not customerId:
        return False
    cursor.execute(
        "SELECT 1 FROM commerce_orderCustomer WHERE orderId = ? AND customerId = ?",
        (orderId, customerId)
    )
    return cursor.fetchone() is not None
