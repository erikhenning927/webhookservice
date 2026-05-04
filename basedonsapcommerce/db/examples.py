"""
Exemplo de integração do módulo DB com os processos existentes.

Este arquivo mostra como usar o ORM em lugar de queries SQL diretas.
"""

from db.migrations import get_session
from db import (
    CommerceOrders,
    CommerceOrderCustomer,
    CommercePaymentInfo,
    CommerceCartEntry,
    CommerceConsignments,
    CommerceEventHistory,
    CommerceOrderBlock,
)
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)


class OrderService:
    """Serviço para operações com pedidos."""
    
    @staticmethod
    def create_order(order_data: dict) -> bool:
        """
        Cria um novo pedido usando ORM.
        
        Exemplo de uso:
        ```python
        order_data = {
            'orderId': '12345',
            'customerId': 'CUST001',
            'status': 'pending',
            'subtotal': 150.50,
            'totalDiscounts': 0,
            'salesChannelId': 1
        }
        OrderService.create_order(order_data)
        ```
        """
        session = get_session()
        try:
            new_order = CommerceOrders(
                orderId=order_data.get('orderId'),
                customerId=order_data.get('customerId'),
                status=order_data.get('status', 'pending'),
                subtotal=order_data.get('subtotal'),
                totalDiscounts=order_data.get('totalDiscounts', 0),
                salesChannelId=order_data.get('salesChannelId'),
                date=datetime.now(),
                creationDate=date.today(),
                **{k: v for k, v in order_data.items() 
                   if k not in ['orderId', 'customerId', 'status', 'subtotal', 'totalDiscounts', 'salesChannelId']}
            )
            session.add(new_order)
            session.commit()
            logger.info(f"✅ Pedido {order_data['orderId']} criado com sucesso")
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Erro ao criar pedido: {e}")
            return False
        finally:
            session.close()
    
    @staticmethod
    def get_order(order_id: str) -> CommerceOrders:
        """Busca um pedido pelo ID."""
        session = get_session()
        try:
            order = session.query(CommerceOrders).filter_by(orderId=order_id).first()
            return order
        finally:
            session.close()
    
    @staticmethod
    def update_order_status(order_id: str, new_status: str) -> bool:
        """Atualiza o status de um pedido."""
        session = get_session()
        try:
            order = session.query(CommerceOrders).filter_by(orderId=order_id).first()
            if order:
                order.status = new_status
                order.statusUpdatedAt = datetime.now()
                session.commit()
                logger.info(f"✅ Pedido {order_id} status atualizado para {new_status}")
                return True
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Erro ao atualizar status: {e}")
            return False
        finally:
            session.close()
    
    @staticmethod
    def get_pending_orders() -> list:
        """Retorna todos os pedidos pendentes."""
        session = get_session()
        try:
            orders = session.query(CommerceOrders).filter_by(status='pending').all()
            return orders
        finally:
            session.close()


class PaymentService:
    """Serviço para operações com pagamentos."""
    
    @staticmethod
    def create_payment(payment_data: dict) -> bool:
        """
        Cria uma nova informação de pagamento.
        
        Exemplo de uso:
        ```python
        payment_data = {
            'paymentId': 'PAY001',
            'paymentModeId': 'CREDIT_CARD',
            'paidValue': 150.50,
            'status': 'approved'
        }
        PaymentService.create_payment(payment_data)
        ```
        """
        session = get_session()
        try:
            new_payment = CommercePaymentInfo(
                paymentId=payment_data.get('paymentId'),
                paymentModeId=payment_data.get('paymentModeId'),
                paidValue=payment_data.get('paidValue'),
                creationDate=date.today(),
                **{k: v for k, v in payment_data.items() 
                   if k not in ['paymentId', 'paymentModeId', 'paidValue']}
            )
            session.add(new_payment)
            session.commit()
            logger.info(f"✅ Pagamento {payment_data['paymentId']} criado com sucesso")
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Erro ao criar pagamento: {e}")
            return False
        finally:
            session.close()
    
    @staticmethod
    def get_payment(payment_id: str) -> CommercePaymentInfo:
        """Busca um pagamento pelo ID."""
        session = get_session()
        try:
            payment = session.query(CommercePaymentInfo).filter_by(paymentId=payment_id).first()
            return payment
        finally:
            session.close()


class CustomerService:
    """Serviço para operações com clientes de pedidos."""
    
    @staticmethod
    def create_order_customer(customer_data: dict) -> bool:
        """
        Cria um novo cliente associado a um pedido.
        
        Exemplo de uso:
        ```python
        customer_data = {
            'orderId': '12345',
            'customerId': 'CUST001',
            'customerFirstName': 'João',
            'customerLastName': 'Silva',
            'customerEmail': 'joao@email.com'
        }
        CustomerService.create_order_customer(customer_data)
        ```
        """
        session = get_session()
        try:
            new_customer = CommerceOrderCustomer(
                orderId=customer_data.get('orderId'),
                customerId=customer_data.get('customerId'),
                customerFirstName=customer_data.get('customerFirstName'),
                customerLastName=customer_data.get('customerLastName'),
                customerEmail=customer_data.get('customerEmail'),
                **{k: v for k, v in customer_data.items() 
                   if k not in ['orderId', 'customerId', 'customerFirstName', 'customerLastName', 'customerEmail']}
            )
            session.add(new_customer)
            session.commit()
            logger.info(f"✅ Cliente criado para pedido {customer_data['orderId']}")
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Erro ao criar cliente: {e}")
            return False
        finally:
            session.close()


class ConsignmentService:
    """Serviço para operações com consignações/remessas."""
    
    @staticmethod
    def create_consignment(consignment_data: dict) -> bool:
        """
        Cria uma nova consignação.
        
        Exemplo de uso:
        ```python
        consignment_data = {
            'consigmentId': 'CONS001',
            'orderId': '12345',
            'status': 'pending',
            'trackingCode': 'BR123456789'
        }
        ConsignmentService.create_consignment(consignment_data)
        ```
        """
        session = get_session()
        try:
            new_consignment = CommerceConsignments(
                consigmentId=consignment_data.get('consigmentId'),
                orderId=consignment_data.get('orderId'),
                status=consignment_data.get('status', 'pending'),
                creationDate=date.today(),
                **{k: v for k, v in consignment_data.items() 
                   if k not in ['consigmentId', 'orderId', 'status']}
            )
            session.add(new_consignment)
            session.commit()
            logger.info(f"✅ Consignação {consignment_data['consigmentId']} criada")
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Erro ao criar consignação: {e}")
            return False
        finally:
            session.close()
    
    @staticmethod
    def update_consignment_status(consignment_id: str, new_status: str) -> bool:
        """Atualiza o status de uma consignação."""
        session = get_session()
        try:
            consignment = session.query(CommerceConsignments).filter_by(
                consigmentId=consignment_id
            ).first()
            if consignment:
                consignment.status = new_status
                session.commit()
                logger.info(f"✅ Consignação {consignment_id} status: {new_status}")
                return True
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Erro ao atualizar consignação: {e}")
            return False
        finally:
            session.close()


class EventService:
    """Serviço para operações com histórico de eventos."""
    
    @staticmethod
    def create_event(event_data: dict) -> bool:
        """
        Cria um novo evento no histórico.
        
        Exemplo de uso:
        ```python
        event_data = {
            'orderId': '12345',
            'eventId': 'EVENT_001',
            'description': 'Pedido aprovado',
            'eventType': 'order_approved'
        }
        EventService.create_event(event_data)
        ```
        """
        session = get_session()
        try:
            new_event = CommerceEventHistory(
                orderId=event_data.get('orderId'),
                eventId=event_data.get('eventId'),
                description=event_data.get('description'),
                eventType=event_data.get('eventType'),
                date=datetime.now(),
                creationDate=date.today(),
                **{k: v for k, v in event_data.items() 
                   if k not in ['orderId', 'eventId', 'description', 'eventType']}
            )
            session.add(new_event)
            session.commit()
            logger.info(f"✅ Evento criado para pedido {event_data['orderId']}")
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Erro ao criar evento: {e}")
            return False
        finally:
            session.close()


# ============================================================================
# INTEGRAÇÃO COM CÓDIGO EXISTENTE
# ============================================================================

# Em lugar de chamar insert_order_to_db(details) diretamente,
# você pode agora fazer:
#
# from db_examples import OrderService
#
# order_data = extract_order_data(details)
# OrderService.create_order(order_data)


# Exemplos de uso nos processos existentes:

def integrate_with_create_cart():
    """Exemplo de integração com create_cart.py"""
    # Antes (SQL direto):
    # insert_order_to_db(details)
    
    # Depois (ORM):
    # order_data = {
    #     'orderId': details['orderId'],
    #     'customerId': details['customerId'],
    #     'status': 'pending',
    #     'subtotal': details['subtotal']
    # }
    # OrderService.create_order(order_data)
    pass


def integrate_with_event_history():
    """Exemplo de integração com event_history.py"""
    # Antes (SQL direto):
    # insert_eventHistory_to_db(details)
    
    # Depois (ORM):
    # event_data = {
    #     'orderId': details['orderId'],
    #     'eventId': details['eventId'],
    #     'description': details['description']
    # }
    # EventService.create_event(event_data)
    pass


if __name__ == '__main__':
    # Exemplos de teste
    logger.basicConfig(level=logger.INFO)
    
    print("✨ Exemplos de uso do módulo DB")
    print("\nVeja os exemplos acima para integrar com seu código!")
