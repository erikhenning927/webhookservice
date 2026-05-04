from app.db import get_connection
from app.utils.chunk import chunked_iterable
from datetime import datetime


def insert_address_to_db(all_addresses):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tentar usar fast_executemany se disponível (MSSQL com pyodbc)
    if hasattr(cursor, 'fast_executemany'):
        cursor.fast_executemany = True

    inserted_total = 0
    updated_total = 0
    try:
        update_query = """
        UPDATE commerce_deliveryAddresses
        SET
            postalcode = ?,
            unloadingAddress = ?,
            streetnumber = ?,
            complement = ?,
            remarks = ?,
            addressType = ?,
            contactAddress = ?,
            shippingAddress = ?,
            addressId = ?,
            building = ?,
            cellphone = ?,
            town = ?,
            appartment = ?,
            company = ?,
            typeQualifier = ?,
            streetname = ?,
            department = ?,
            billingAddress = ?,
            country = ?,
            title = ?,
            region = ?,
            district = ?
        WHERE orderId = ?;
        """

        insert_query = """
        INSERT INTO commerce_deliveryAddresses (
            orderId, postalcode, unloadingAddress, streetnumber, complement, remarks, addressType, 
            contactAddress, shippingAddress, addressId, building, cellphone, town, appartment, company, 
            typeQualifier, streetname, department, billingAddress, country, title, region, district
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        for chunk in chunked_iterable(all_addresses, 10000):
            update_data = [
                (
                    address.get('postalcode'),
                    address.get('unloadingAddress'),
                    address.get('streetnumber'),
                    address.get('complement'),
                    address.get('remarks'),
                    address.get('addressType'),
                    address.get('contactAddress'),
                    address.get('shippingAddress'),
                    address.get('addressId'),
                    address.get('building'),
                    address.get('cellphone'),
                    address.get('town'),
                    address.get('appartment'),
                    address.get('company'),
                    address.get('typeQualifier'),
                    address.get('streetname'),
                    address.get('department'),
                    address.get('billingAddress'),
                    address.get('country'),
                    address.get('title'),
                    address.get('region'),
                    address.get('district'),
                    address.get('orderId')
                )
                for address in chunk
            ]

            cursor.executemany(update_query, update_data)
            conn.commit()
            updated_rows = cursor.rowcount if cursor.rowcount != -1 else len(update_data)
            updated_total += updated_rows
            print(f"🟡 Atualizados {updated_rows} addresses no batch.")

            insert_data = [
                (
                    address.get('orderId'),
                    address.get('postalcode'),
                    address.get('unloadingAddress'),
                    address.get('streetnumber'),
                    address.get('complement'),
                    address.get('remarks'),
                    address.get('addressType'),
                    address.get('contactAddress'),
                    address.get('shippingAddress'),
                    address.get('addressId'),
                    address.get('building'),
                    address.get('cellphone'),
                    address.get('town'),
                    address.get('appartment'),
                    address.get('company'),
                    address.get('typeQualifier'),
                    address.get('streetname'),
                    address.get('department'),
                    address.get('billingAddress'),
                    address.get('country'),
                    address.get('title'),
                    address.get('region'),
                    address.get('district')
                )
                for address in chunk
                if not address_exists(cursor, address.get('orderId'))
            ]

            if insert_data:
                cursor.executemany(insert_query, insert_data)
                conn.commit()
                inserted_rows = cursor.rowcount if cursor.rowcount != -1 else len(insert_data)
                inserted_total += inserted_rows
                print(f"Inseridos {inserted_rows} addresses no batch.")

        print(f"Finalizado: {inserted_total} inseridos e {updated_total} atualizados.")
    except Exception as e:
        order_id = all_addresses[0].get('orderId', 'Unknown')
        error_message = str(e)
        domain = 'commerce_deliveryAddresses'
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Erro ao inserir endereço: {e}")
        conn.rollback()
    finally:
        print("Conexão fechada. Finalizando inserção de endereços de entrega.")
        cursor.close()
        conn.close()


def address_exists(cursor, orderId):
    if not orderId:
        return False
    cursor.execute(
        "SELECT 1 FROM commerce_deliveryAddresses WHERE orderId = ?",
        (orderId,)
    )
    return cursor.fetchone() is not None