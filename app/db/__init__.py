from .database import Database, get_db
from .models import (
    DimEvents,
    DimSalesChannel,
    DimPaymentModes,
    DimProductBrand,
    DimProductFamily,
    DimProductLine,
    DimCourier,
    DimWarehouse,
    DimVariantProducts,
    CommercePaymentInfo,
    CommerceOrderCustomer,
    CommerceOrders,
    CommerceConsignments,
    CommerceConsignmentEntry,
    CommerceCartEntry,
    CommerceBillingAddress,
    CommerceDeliveryAddresses,
    CommerceEventHistory,
    CommerceInvoices,
    CommerceOrderBlock,
)


def get_connection():
    """
    Helper para obter uma conexão raw do banco de dados.
    Útil para INSERT/UPDATE em batch com executemany().
    
    Returns:
        Conexão raw pronta para uso.
    """
    db = get_db()
    return db.get_connection()


def execute_batch(connection, query, data, batch_size=1000):
    """
    Executa um INSERT/UPDATE em batch, compatível com múltiplos bancos.
    Detecta automaticamente o tipo de banco e executa de forma otimizada.
    
    Args:
        connection: Conexão obtida via get_connection()
        query: Query SQL com placeholders (?)
        data: Lista de tuplas com os dados
        batch_size: Tamanho de cada batch (padrão: 1000)
    
    Returns:
        Tupla (total_inseridos, total_atualizados) ou (total_afetados, 0)
    """
    cursor = connection.cursor()
    total_affected = 0
    
    try:
        # Detectar tipo de banco pelo driver/module
        is_mssql = hasattr(cursor, 'fast_executemany')
        
        if is_mssql:
            # SQL Server com pyodbc - usar fast_executemany
            cursor.fast_executemany = True
        
        # Processar em batches
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            
            try:
                cursor.executemany(query, batch)
                connection.commit()
                
                # Contar registros afetados
                if cursor.rowcount > 0:
                    total_affected += cursor.rowcount
                else:
                    total_affected += len(batch)
                    
            except Exception as e:
                connection.rollback()
                print(f"❌ Erro no batch {i//batch_size + 1}: {e}")
                raise
        
        return (total_affected, 0)
        
    except Exception as e:
        connection.rollback()
        print(f"❌ Erro geral na execução em batch: {e}")
        raise
    finally:
        cursor.close()


__all__ = [
    "Database",
    "get_db",
    "get_connection",
    "execute_batch",
    "DimEvents",
    "DimSalesChannel",
    "DimPaymentModes",
    "DimProductBrand",
    "DimProductFamily",
    "DimProductLine",
    "DimCourier",
    "DimWarehouse",
    "DimVariantProducts",
    "CommercePaymentInfo",
    "CommerceOrderCustomer",
    "CommerceOrders",
    "CommerceConsignments",
    "CommerceConsignmentEntry",
    "CommerceCartEntry",
    "CommerceBillingAddress",
    "CommerceDeliveryAddresses",
    "CommerceEventHistory",
    "CommerceInvoices",
    "CommerceOrderBlock",
]
