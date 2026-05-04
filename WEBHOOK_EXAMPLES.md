# Webhook Service - Exemplos de Payload

Base URL: `http://localhost:5004/hook_service/api`

---

## 1️⃣ **inboundCart** (Carrinho)

```bash
curl -X POST http://localhost:5004/hook_service/api \
  -H "Content-Type: application/json" \
  -H "Ce-Type: com.example.commercechannel.inboundCart.v1" \
  -d '{
    "code": "CART-001",
    "creationtime": "/Date(1714827000000)/",
    "modifiedtime": "/Date(1714827300000)/",
    "customerDocument": "12345678900",
    "Sequence": 123456,
    "SellerOrderId":12335677,
    "MarketplaceOrderId": 123468798,
    "customerDocumentType": "CPF",
    "customerFirstName": "João",
    "customerLastName": "Silva",
    "customerPhone": "11999999999",
    "customerEmail": "joao@example.com",
    "customerClass": "REGULAR",
    "customerIsCorporate": false,
    "salesChannel": {
      "Id": 1
    },
    "user": {
      "uid": "joao@example.com"
    },
    "status": {
      "code": "CREATED"
    },
    "exportStatus": {
      "code": "PENDING"
    },
    "paymentInfos": [
      {
        "code": "CREDIT_CARD"
      }
    ],
    "deliveryAddress": {
      "streetnumber": "123",
      "streetname": "Rua das Flores",
      "postalcode": "01234-567"
    },
    "date": "/Date(1714827000000)/",
    "statusUpdatedAt": "/Date(1714827300000)/",
    "subtotal": 299.90,
    "totalDiscounts": 30.00,
    "isComplete": false,
    "OrderIsIncomplete": false,
    "paymentRefundOn": false,
    "cancelledInErp": false,
    "cancelledInCommerce": false,
    "blockCart": false
  }'
```

---

## 2️⃣ **inboundOrder** (Pedido)

```bash
curl -X POST http://localhost:5004/hook_service/api \
  -H "Content-Type: application/json" \
  -H "Ce-Type: com.example.commercechannel.inboundOrder.v1" \
  -d '{
    "code": "CART-001",
    "creationtime": "/Date(1714827000000)/",
    "modifiedtime": "/Date(1714827300000)/",
    "customerDocument": "12345678900",
    "Sequence": 123456,
    "SellerOrderId":12335677,
    "MarketplaceOrderId": 123468798,
    "customerDocumentType": "CPF",
    "customerFirstName": "João",
    "customerLastName": "Silva",
    "customerPhone": "11999999999",
    "customerEmail": "joao@example.com",
    "customerClass": "REGULAR",
    "customerIsCorporate": false,
    "salesChannel": {
      "Id": 1
    },
    "user": {
      "uid": "joao@example.com"
    },
    "status": {
      "code": "CREATED"
    },
    "exportStatus": {
      "code": "PENDING"
    },
    "paymentInfos": [
      {
        "code": "CREDIT_CARD"
      }
    ],
    "deliveryAddress": {
      "streetnumber": "123",
      "streetname": "Rua das Flores",
      "postalcode": "01234-567"
    },
    "date": "/Date(1714827000000)/",
    "statusUpdatedAt": "/Date(1714827300000)/",
    "subtotal": 299.90,
    "totalDiscounts": 30.00,
    "isComplete": false,
    "OrderIsIncomplete": false,
    "paymentRefundOn": false,
    "cancelledInErp": false,
    "cancelledInCommerce": false,
    "blockCart": false
  }'
```

---

## 3️⃣ **inboundCartEntry** (Entrada do Carrinho)

```bash
curl -X POST http://localhost:5004/hook_service/api \
  -H "Content-Type: application/json" \
  -H "Ce-Type: com.example.commercechannel.inboundCartEntry.v1" \
  -d '{
    "creationtime": "/Date(1714827000000)/",
    "modifiedtime": "/Date(1714827120000)/",
    "order": {
      "code": "CART-001"
    },
    "product": {
      "code": "PROD-001"
    },
    "warehouse": "WH-01",
    "shippingType": {
      "code": "COURIER001"
    },
    "quantity": 2,
    "basePrice": 149.95,
    "sellingPrice": 149.95,
    "price": 299.90,
    "totalPrice": 299.90,
    "costPrice": 100.00,
    "deliveryQuotedCost": 15.00,
    "deliveryCost": 15.00,
    "selectedSla": "STANDARD",
    "entryNumber": 1,
    "quantityStatus": "AVAILABLE",
    "calculated": true,
    "namedDeliveryDate": "/Date(1715211599000)/",
    "Promotions": [
      {
        "code": "PROMO-001"
      }
    ]
  }'
```

---

## 4️⃣ **inboundOrderEntry** (Entrada do Pedido)

```bash
curl -X POST http://localhost:5004/hook_service/api \
  -H "Content-Type: application/json" \
  -H "Ce-Type: com.example.commercechannel.inboundOrderEntry.v1" \
  -d '{
    "creationtime": "/Date(1714827600000)/",
    "modifiedtime": "/Date(1714827720000)/",
    "order": {
      "code": "ORDER-001"
    },
    "product": {
      "code": "PROD-002"
    },
    "warehouse": "WH-02",
    "shippingType": {
      "code": "COURIER001"
    },
    "quantity": 1,
    "basePrice": 599.90,
    "sellingPrice": 599.90,
    "price": 599.90,
    "totalPrice": 599.90,
    "costPrice": 400.00,
    "deliveryQuotedCost": 30.00,
    "deliveryCost": 30.00,
    "selectedSla": "EXPRESS",
    "entryNumber": 1,
    "quantityStatus": "CONFIRMED",
    "calculated": true,
    "namedDeliveryDate": "/Date(1715040599000)/",
    "isReservedIn": true,
    "Promotions": []
  }'
```

---

## 5️⃣ **inboundConsignment** (Consignação/Envio)

```bash
curl -X POST http://localhost:5004/hook_service/api \
  -H "Content-Type: application/json" \
  -H "Ce-Type: com.example.commercechannel.inboundConsignment.v1" \
  -d '{
    "code": "CONSIGN-001",
    "creationtime": "/Date(1714840800000)/",
    "modifiedtime": "/Date(1714841100000)/",
    "order": {
      "code": "CART-001"
    },
    "warehouse": {
      "code": "WH-02"
    },
    "status": {
      "code": "SHIPPED"
    },
    "romaneioNumber": "ROM-001",
    "trackingCode": "BR123456789BR",
    "trackingUrl": "https://tracking.example.com/BR123456789BR",
    "manifestNumber": "MANI-001",
    "transportadora": "SEDEX",
    "statusDisplay": "Em Transito",
    "isReturnInTransit": false,
    "invoiceSent": true,
    "exchangeReason": null,
    "departureDate": "/Date(1714903200000)/",
    "deliveryForecastDate": "/Date(1715211599000)/",
    "shippingLabelProcess": [
      {
        "code": "LABEL-PROCESS-001"
      }
    ],
    "consignmentProcesses": [
      {
        "code": "PROCESS-001"
      }
    ]
  }'
```

---

## 6️⃣ **inboundConsignmentReturn** (Retorno de Consignação)

```bash
curl -X POST http://localhost:5004/hook_service/api \
  -H "Content-Type: application/json" \
  -H "Ce-Type: com.example.commercechannel.inboundConsignmentReturn.v1" \
  -d '{
    "code": "CONSIGN-RETURN-001",
    "creationtime": "/Date(1714851600000)/",
    "modifiedtime": "/Date(1714851900000)/",
    "order": {
      "code": "CART-001"
    },
    "warehouse": {
      "code": "WH-02"
    },
    "status": {
      "code": "RETURNED"
    },
    "romaneioNumber": "ROM-RETURN-001",
    "trackingCode": "BR987654321BR",
    "trackingUrl": "https://tracking.example.com/BR987654321BR",
    "manifestNumber": "MANI-RETURN-001",
    "transportadora": "PAC",
    "statusDisplay": "Retorno em Transito",
    "isReturnInTransit": true,
    "invoiceSent": true,
    "exchangeReason": "DEFECTIVE_PRODUCT",
    "departureDate": "/Date(1715040000000)/",
    "deliveryForecastDate": "/Date(1715127599000)/",
    "shippingLabelProcess": [
      {
        "code": "LABEL-PROCESS-RETURN-001"
      }
    ],
    "consignmentProcesses": [
      {
        "code": "PROCESS-RETURN-001"
      }
    ]
  }'
```



---

## 8️⃣ **inboundEventHistory** (Histórico de Eventos)

```bash
curl -X POST http://localhost:5004/hook_service/api \
  -H "Content-Type: application/json" \
  -H "Ce-Type: com.example.commercechannel.inboundEventHistory.v1" \
  -d '{
    "creationtime": "/Date(1714848600000)/",
    "modifiedtime": "/Date(1714848720000)/",
    "order": {
      "code": "ORDER-001",
      "status": {
        "code": "SHIPPED"
      }
    },
    "consignment": {
      "code": "CONSIGN-001"
    },
    "eventId": {
      "code": "ORDER_SHIPPED"
    },
    "sourceSystem": {
      "code": "COMMERCE"
    },
    "description": "Pedido foi enviado para transporte",
    "attempts": 1,
    "send": true,
    "date": "/Date(1714848600000)/",
    "lastExecutionDate": "/Date(1714848660000)/",
    "trackingDescription": "Pacote enviado da origem",
    "trackingCourier": "SEDEX",
    "trackingUrl": "https://tracking.example.com/BR123456789BR",
    "trackingCode": "BR123456789BR",
    "trackingState": "SHIPPED",
    "trackingCity": "São Paulo",
    "trackingDispatchedDate": "/Date(1714840800000)/",
    "departureDate": "/Date(1714843400000)/",
    "romaneioNumber": "ROM-001",
    "manifestNumber": "MANI-001"
  }'
```

---

## 📋 Resumo dos Hook Types

| Hook Type | Descrição | Status |
|-----------|-----------|--------|
| `inboundCart` | Carrinho criado | ✅ Ativo |
| `inboundOrder` | Pedido criado | ✅ Ativo |
| `inboundCartEntry` | Entrada do carrinho | ✅ Ativo |
| `inboundOrderEntry` | Entrada do pedido | ✅ Ativo |
| `inboundConsignment` | Consignação/Envio | ✅ Ativo |
| `inboundConsignmentReturn` | Retorno de consignação | ✅ Ativo |
| `inboundEventHistory` | Histórico de eventos | ✅ Ativo |

---

## 🔧 Como Usar

### 1. Teste Individual
Copie um dos exemplos acima e execute no terminal:

```bash
curl -X POST http://localhost:5004/hook_service/api \
  -H "Content-Type: application/json" \
  -H "Ce-Type: com.example.commercechannel.inboundOrder.v1" \
  -d '{...}'
```

### 2. Teste com Insomnia/Postman
- **URL**: `http://localhost:5004/hook_service/api`
- **Método**: POST
- **Headers**: 
  - `Content-Type: application/json`
  - `Ce-Type: com.example.commercechannel.{hookType}.v1`
- **Body**: JSON do exemplo

### 3. Teste com Python Requests
```python
import requests
import json

url = "http://localhost:5004/hook_service/api"
headers = {
    "Content-Type": "application/json",
    "Ce-Type": "com.example.commercechannel.inboundOrder.v1"
}
payload = { ... }

response = requests.post(url, headers=headers, json=payload)
print(response.status_code, response.text)
```

---

## ✅ Resposta Esperada

Todas as requisições devem retornar:

```
Status 200: Recebido com sucesso
```

Os dados são processados em background (thread assíncrona), então a resposta é imediata.

---

## 📝 Notas Importantes

1. **Ce-Type Header**: Deve conter o hook type no padrão `com.example.commercechannel.{hookType}.v1`
2. **Processamento Assíncrono**: Os dados são processados em uma thread separada
3. **Banco de Dados**: Os dados são persistidos no SQL Server configurado em `.env`
4. **Validação**: Os campos são processados conforme implementado em `process_eventshook/`
