from db import get_connection
from utils.chunk import chunked_iterable
from datetime import datetime

def insert_paymentInfos_to_db(all_paymentInfos):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tentar usar fast_executemany se disponível (MSSQL com pyodbc)
    if hasattr(cursor, 'fast_executemany'):
        cursor.fast_executemany = True

    inserted_total = 0
    updated_total = 0
    try:
        update_query = """
        UPDATE commerce_paymentInfo
        SET
            paymentModeId = ?, Connector = ?, transactionId = ?, GiftCardId = ?, duplicate = ?, 
            ReferenceValue = ?, Acquirer = ?, Installments = ?, [Group] = ?, MerchantName = ?, 
            paidValue = ?, Nsu = ?, pixRefundId = ?, saved = ?, AuthId = ?, CardHolder = ?, 
            RedemptionCode = ?, Tid = ?, returnCode = ?, ExpiryYear = ?, ReturnMessage = ?, 
            DueDate = ?, LastDigits = ?, ExpiryMonth = ?, InstallmentsValue = ?, FirstDigits = ?, 
            refund = ?, creationDate = ?, creationTime = ?, modifiedDate = ?, modifiedTime = ?
        WHERE paymentId = ?;
        """

        insert_query = """
        INSERT INTO commerce_paymentInfo (
            paymentId, paymentModeId, Connector, transactionId, GiftCardId, duplicate, 
            ReferenceValue, Acquirer, Installments, [Group], MerchantName, 
            paidValue, Nsu, pixRefundId, saved, AuthId, CardHolder, RedemptionCode, 
            Tid, returnCode, ExpiryYear, ReturnMessage, DueDate, LastDigits, 
            ExpiryMonth, InstallmentsValue, FirstDigits, refund, creationDate, creationTime, 
            modifiedDate, modifiedTime
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        for chunk in chunked_iterable(all_paymentInfos, 10000):
            update_data = [
                (
                    info.get('paymentModeId'),
                    info.get('Connector'),
                    info.get('transactionId'),
                    info.get('GiftCardId'),
                    info.get('duplicate'),
                    info.get('ReferenceValue'),
                    info.get('Acquirer'),
                    info.get('Installments'),
                    info.get('Group'),
                    info.get('MerchantName'),
                    info.get('paidValue'),
                    info.get('Nsu'),
                    info.get('pixRefundId'),
                    info.get('saved'),
                    info.get('AuthId'),
                    info.get('CardHolder'),
                    info.get('RedemptionCode'),
                    info.get('Tid'),
                    info.get('returnCode'),
                    info.get('ExpiryYear'),
                    info.get('ReturnMessage'),
                    info.get('DueDate'),
                    info.get('LastDigits'),
                    info.get('ExpiryMonth'),
                    info.get('InstallmentsValue'),
                    info.get('FirstDigits'),
                    info.get('refund'),
                    info.get('creationDate'),
                    info.get('creationTime'),
                    info.get('modifiedDate'),
                    info.get('modifiedTime'),
                    info.get('paymentId')
                )
                for info in chunk
            ]
            cursor.executemany(update_query, update_data)
            conn.commit()
            updated_rows = cursor.rowcount if cursor.rowcount != -1 else len(update_data)
            updated_total += updated_rows
            print(f"🟡 Atualizados {updated_rows} modos de pagamento no batch.")

            insert_data = [
                (
                    info.get('paymentId'),
                    info.get('paymentModeId'),
                    info.get('Connector'),
                    info.get('transactionId'),
                    info.get('GiftCardId'),
                    info.get('duplicate'),
                    info.get('ReferenceValue'),
                    info.get('Acquirer'),
                    info.get('Installments'),
                    info.get('Group'),
                    info.get('MerchantName'),
                    info.get('paidValue'),
                    info.get('Nsu'),
                    info.get('pixRefundId'),
                    info.get('saved'),
                    info.get('AuthId'),
                    info.get('CardHolder'),
                    info.get('RedemptionCode'),
                    info.get('Tid'),
                    info.get('returnCode'),
                    info.get('ExpiryYear'),
                    info.get('ReturnMessage'),
                    info.get('DueDate'),
                    info.get('LastDigits'),
                    info.get('ExpiryMonth'),
                    info.get('InstallmentsValue'),
                    info.get('FirstDigits'),
                    info.get('refund'),
                    info.get('creationDate'),
                    info.get('creationTime'),
                    info.get('modifiedDate'),
                    info.get('modifiedTime')
                )
                for info in chunk
                if not paymentInfo_exists(cursor, info.get('paymentId'))
            ]

            if insert_data:
                cursor.executemany(insert_query, insert_data)
                conn.commit()
                inserted_rows = cursor.rowcount if cursor.rowcount != -1 else len(insert_data)
                inserted_total += inserted_rows
                print(f"🟢 Inseridos {inserted_rows} modos de pagamento no batch.")

        print(f"✅ Finalizado: {inserted_total} inseridos e {updated_total} atualizados.")
    except Exception as e:
        order_id = all_paymentInfos[0].get('paymentId', 'Unknown')
        error_message = str(e)
        domain = 'commerce_paymentInfo'
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Erro ao inserir pagament: {e}")
        conn.rollback()
    finally:
        print("Conexão fechada. Finalizando inserção de pagamentos.")
        cursor.close()
        conn.close()


def paymentInfo_exists(cursor, paymentId):
    if not paymentId:
        return False
    cursor.execute(
        "SELECT 1 FROM commerce_paymentInfo WHERE paymentId = ?",
        (paymentId,)
    )
    return cursor.fetchone() is not None
