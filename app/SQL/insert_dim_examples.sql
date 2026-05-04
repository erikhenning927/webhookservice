-- ============================================================================
-- DADOS DE EXEMPLO PARA TABELAS DIM (DIMENSÕES)
-- ============================================================================
-- Executar este script para popular as tabelas de dimensão com dados realistas
-- ============================================================================

-- ============================================================================
-- 1. dim_events - Tipos de eventos do sistema
-- ============================================================================
INSERT INTO dim_events (
    eventId, name, defaultDescription, openTicket, createdByIntegration,
    mustBeFilledRetroactively, dateWhenTypeDefined, queueType,
    creationDate, creationTime, modifiedDate, modifiedTime, blocked
) VALUES
('ORDER_CREATED', 'Pedido Criado', 'Um novo pedido foi criado no sistema', 1, 1, 0, '2024-01-01 10:00:00', 'COMMERCE_QUEUE', '2024-01-01', '10:00:00', '2024-01-01', '10:00:00', 0),
('ORDER_CONFIRMED', 'Pedido Confirmado', 'Pedido foi confirmado após validação', 1, 1, 0, '2024-01-01 10:00:00', 'COMMERCE_QUEUE', '2024-01-01', '10:00:00', '2024-01-01', '10:00:00', 0),
('PAYMENT_APPROVED', 'Pagamento Aprovado', 'Pagamento do pedido foi aprovado', 1, 1, 0, '2024-01-01 10:00:00', 'PAYMENT_QUEUE', '2024-01-01', '10:00:00', '2024-01-01', '10:00:00', 0),
('PAYMENT_PENDING', 'Pagamento Pendente', 'Aguardando confirmação do pagamento', 0, 1, 1, '2024-01-01 10:00:00', 'PAYMENT_QUEUE', '2024-01-01', '10:00:00', '2024-01-01', '10:00:00', 0),
('ORDER_SHIPPED', 'Pedido Enviado', 'Pedido foi despachado da origem', 1, 1, 0, '2024-01-01 10:00:00', 'LOGISTICS_QUEUE', '2024-01-01', '10:00:00', '2024-01-01', '10:00:00', 0),
('ORDER_DELIVERED', 'Pedido Entregue', 'Pedido foi entregue ao cliente', 0, 1, 0, '2024-01-01 10:00:00', 'LOGISTICS_QUEUE', '2024-01-01', '10:00:00', '2024-01-01', '10:00:00', 0),
('ORDER_CANCELLED', 'Pedido Cancelado', 'Pedido foi cancelado', 1, 1, 0, '2024-01-01 10:00:00', 'COMMERCE_QUEUE', '2024-01-01', '10:00:00', '2024-01-01', '10:00:00', 0),
('RETURN_INITIATED', 'Devolução Iniciada', 'Cliente iniciou processo de devolução', 1, 1, 1, '2024-01-01 10:00:00', 'RETURN_QUEUE', '2024-01-01', '10:00:00', '2024-01-01', '10:00:00', 0),
('RETURN_RECEIVED', 'Devolução Recebida', 'Item devolvido foi recebido no armazém', 0, 1, 0, '2024-01-01 10:00:00', 'RETURN_QUEUE', '2024-01-01', '10:00:00', '2024-01-01', '10:00:00', 0),
('REFUND_PROCESSED', 'Reembolso Processado', 'Reembolso foi processado para o cliente', 0, 1, 0, '2024-01-01 10:00:00', 'PAYMENT_QUEUE', '2024-01-01', '10:00:00', '2024-01-01', '10:00:00', 0);

-- ============================================================================
-- 2. dim_salesChannel - Canais de venda/plataformas
-- ============================================================================

INSERT INTO dim_salesChannel (
    stateRegistration, ownStore, cnpj, applyEmployeeCommercialRule,
    name, active, creationDate, creationTime, modifiedDate, modifiedTime
)
VALUES
('MG123456', 1, '12345678000101', 1, 'Loja Própria - Web', 1, '2024-01-01', '08:00:00', '2024-01-01', '08:00:00');

-- =====
-- ============================================================================
-- 3. dim_paymentModes - Modalidades de pagamento
-- ============================================================================
INSERT INTO dim_paymentModes (
    paymentModeId, name, description, active, refundBy, findFinancialTitles,
    creationDate, creationTime, modifiedDate, modifiedTime
) VALUES
('CREDIT_CARD', 'Cartão de Crédito', 'Pagamento via cartão de crédito', 1, 1, 1, '2024-01-01', '09:00:00', '2024-01-01', '09:00:00'),
('DEBIT_CARD', 'Cartão de Débito', 'Pagamento via cartão de débito', 1, 1, 1, '2024-01-01', '09:00:00', '2024-01-01', '09:00:00'),
('BANK_TRANSFER', 'Transferência Bancária', 'Pagamento via transferência bancária', 1, 1, 1, '2024-01-01', '09:00:00', '2024-01-01', '09:00:00'),
('PIX', 'PIX', 'Pagamento instantâneo via PIX', 1, 1, 1, '2024-01-01', '09:00:00', '2024-01-01', '09:00:00'),
('BOLETO', 'Boleto Bancário', 'Pagamento via boleto bancário', 1, 0, 1, '2024-01-01', '09:00:00', '2024-01-01', '09:00:00'),
('GIFT_CARD', 'Gift Card', 'Pagamento via gift card pré-pago', 1, 1, 0, '2024-01-01', '09:00:00', '2024-01-01', '09:00:00'),
('INSTALLMENT', 'Parcelado em Até 12x', 'Pagamento parcelado em até 12 vezes', 1, 1, 1, '2024-01-01', '09:00:00', '2024-01-01', '09:00:00');

-- ============================================================================
-- 4. dim_productBrand - Marcas de produtos
-- ============================================================================
INSERT INTO dim_productBrand (
    brandId, name, creationDate, creationTime, modifiedDate, modifiedTime
) VALUES
('BRAND001', 'Samsung', '2024-01-01', '09:30:00', '2024-01-01', '09:30:00'),
('BRAND002', 'LG', '2024-01-01', '09:30:00', '2024-01-01', '09:30:00'),
('BRAND003', 'Sony', '2024-01-01', '09:30:00', '2024-01-01', '09:30:00'),
('BRAND004', 'Apple', '2024-01-01', '09:30:00', '2024-01-01', '09:30:00'),
('BRAND005', 'Positivo', '2024-01-01', '09:30:00', '2024-01-01', '09:30:00');

-- ============================================================================
-- 5. dim_productFamily - Famílias de produtos
-- ============================================================================
INSERT INTO dim_productFamily (
    familyId, name, creationDate, creationTime, modifiedDate, modifiedTime
) VALUES
('FAMILY001', 'Eletrônicos', '2024-01-01', '09:45:00', '2024-01-01', '09:45:00'),
('FAMILY002', 'Informática', '2024-01-01', '09:45:00', '2024-01-01', '09:45:00'),
('FAMILY003', 'Eletrodomésticos', '2024-01-01', '09:45:00', '2024-01-01', '09:45:00'),
('FAMILY004', 'TVs e Monitores', '2024-01-01', '09:45:00', '2024-01-01', '09:45:00'),
('FAMILY005', 'Celulares e Tablets', '2024-01-01', '09:45:00', '2024-01-01', '09:45:00'),
('FAMILY006', 'Áudio e Vídeo', '2024-01-01', '09:45:00', '2024-01-01', '09:45:00');

-- ============================================================================
-- 6. dim_productLine - Linhas de produtos
-- ============================================================================
INSERT INTO dim_productLine (
    lineId, name, creationDate, creationTime, modifiedDate, modifiedTime
) VALUES
('LINE001', 'Linha Premium', '2024-01-01', '10:00:00', '2024-01-01', '10:00:00'),
('LINE002', 'Linha Standard', '2024-01-01', '10:00:00', '2024-01-01', '10:00:00'),
('LINE003', 'Linha Econômica', '2024-01-01', '10:00:00', '2024-01-01', '10:00:00'),
('LINE004', 'Linha Gaming', '2024-01-01', '10:00:00', '2024-01-01', '10:00:00'),
('LINE005', 'Linha Profissional', '2024-01-01', '10:00:00', '2024-01-01', '10:00:00'),
('LINE006', 'Linha Smart Home', '2024-01-01', '10:00:00', '2024-01-01', '10:00:00');

-- ============================================================================
-- 7. dim_courier - Transportadoras/Courieres
-- ============================================================================
INSERT INTO dim_courier (
    courierId, retrieveShippingLabel, name, idSalesforce,
    creationDate, creationTime, modifiedDate, modifiedTime
) VALUES
('COURIER001', 1, 'Correios', 'SF_CORREIOS_001', '2024-01-01', '10:15:00', '2024-01-01', '10:15:00'),
('COURIER002', 1, 'Sedex', 'SF_SEDEX_001', '2024-01-01', '10:15:00', '2024-01-01', '10:15:00'),
('COURIER003', 1, 'PAC', 'SF_PAC_001', '2024-01-01', '10:15:00', '2024-01-01', '10:15:00'),
('COURIER004', 1, 'Loggi', 'SF_LOGGI_001', '2024-01-01', '10:15:00', '2024-01-01', '10:15:00'),
('COURIER005', 1, 'Rapido Fresh', 'SF_RAPIDO_001', '2024-01-01', '10:15:00', '2024-01-01', '10:15:00'),
('COURIER006', 1, 'JadLog', 'SF_JADLOG_001', '2024-01-01', '10:15:00', '2024-01-01', '10:15:00'),
('COURIER007', 1, 'Total Express', 'SF_TOTAL_001', '2024-01-01', '10:15:00', '2024-01-01', '10:15:00'),
('COURIER008', 1, 'Via Brasil', 'SF_VIABR_001', '2024-01-01', '10:15:00', '2024-01-01', '10:15:00');

-- ============================================================================
-- 8. dim_warehouse - Depósitos/Armazéns
-- ============================================================================
INSERT INTO dim_warehouse (warehouseId, name) VALUES
('WH-01', 'Armazém São Paulo - SP'),
('WH-02', 'Armazém Minas Gerais - MG'),
('WH-03', 'Armazém Rio de Janeiro - RJ'),
('WH-04', 'Armazém Bahia - BA'),
('WH-05', 'Armazém Santa Catarina - SC'),
('WH-06', 'Armazém Rio Grande do Sul - RS');

-- ============================================================================
-- 9. dim_variantProducts - Produtos Variantes
-- ============================================================================
INSERT INTO dim_variantProducts (
    refId, name, displayName, commercialId, completeProduct, weight, height, width, length,
    packageWeight, packageHeight, packageWidth, packageLength, unit, ean, version,
    familyId, lineId, brandId, creationDate, creationTime, modifiedDate, modifiedTime
) VALUES
('PROD001', 'Smart TV 55" 4K UHD', 'Samsung Smart TV 55" 4K UHD - Neo QLED', 'SAMSUNG55QLED', 1, 18.5, 123.5, 97.2, 25.4, 20.5, 128.0, 104.0, 32.0, 'UN', '8806090123456', 'V1.0', 'FAMILY004', 'LINE001', 'BRAND002', '2024-01-01', '10:30:00', '2024-01-01', '10:30:00'),
('PROD002', 'Notebook I7 16GB', 'Notebook Core i7 16GB SSD 512GB Tela 15.6"', 'NB-I7-16GB-512', 1, 2.1, 1.8, 36.0, 25.0, 2.5, 5.0, 38.0, 27.0, 'UN', '8806090123457', 'V2.1', 'FAMILY002', 'LINE001', 'BRAND007', '2024-01-01', '10:30:00', '2024-01-01', '10:30:00'),
('PROD003', 'Smartphone 128GB', 'Samsung Galaxy A12 64GB 4G Azul', 'GALA12-128GB', 1, 0.185, 16.5, 7.6, 0.8, 0.250, 18.0, 10.0, 3.0, 'UN', '8806090123458', 'V1.2', 'FAMILY005', 'LINE002', 'BRAND002', '2024-01-01', '10:30:00', '2024-01-01', '10:30:00'),
('PROD004', 'Geladeira Frost Free', 'Geladeira Brastemp Frost Free 500L Inox', 'BRA-FF-500L', 1, 85.0, 193.0, 82.0, 65.0, 90.0, 198.0, 87.0, 72.0, 'UN', '8806090123459', 'V1.0', 'FAMILY003', 'LINE002', 'BRAND001', '2024-01-01', '10:30:00', '2024-01-01', '10:30:00'),
('PROD005', 'Smart Watch', 'Samsung Galaxy Watch4 Classic 42mm', 'WATCH4-42MM', 1, 0.052, 4.2, 4.2, 1.2, 0.180, 7.5, 7.5, 4.0, 'UN', '8806090123460', 'V1.1', 'FAMILY005', 'LINE001', 'BRAND002', '2024-01-01', '10:30:00', '2024-01-01', '10:30:00'),
('PROD006', 'Soundbar 2.1', 'Soundbar LG 2.1 Canais 100W RMS', 'LG-SB-2.1-100W', 1, 2.8, 5.8, 86.5, 9.5, 3.5, 12.0, 92.0, 16.0, 'UN', '8806090123461', 'V1.0', 'FAMILY006', 'LINE002', 'BRAND003', '2024-01-01', '10:30:00', '2024-01-01', '10:30:00'),
('PROD007', 'Console Gaming', 'PlayStation 5 1TB com Controle', 'PS5-1TB-STD', 1, 4.5, 15.0, 39.0, 10.4, 5.2, 18.0, 43.0, 15.0, 'UN', '8806090123462', 'V1.0', 'FAMILY002', 'LINE004', 'BRAND001', '2024-01-01', '10:30:00', '2024-01-01', '10:30:00'),
('PROD008', 'iPad 10.2"', 'Apple iPad 10.2" 64GB WiFi Prata', 'IPAD-10.2-64GB', 1, 0.483, 25.0, 17.2, 0.75, 0.550, 28.0, 20.0, 5.0, 'UN', '8806090123463', 'V2.0', 'FAMILY005', 'LINE001', 'BRAND005', '2024-01-01', '10:30:00', '2024-01-01', '10:30:00'),
('PROD009', 'Fone Bluetooth', 'Sony WH-CH720 Fone Bluetooth', 'SONY-CH720-BT', 1, 0.192, 19.2, 17.4, 8.6, 0.350, 22.0, 20.0, 12.0, 'UN', '8806090123464', 'V1.0', 'FAMILY006', 'LINE002', 'BRAND004', '2024-01-01', '10:30:00', '2024-01-01', '10:30:00'),
('PROD010', 'Micro-ondas Digital', 'Consul Micro-ondas 30L 1000W Inox', 'CONS-MO-30L', 1, 15.0, 30.0, 53.0, 42.0, 16.5, 33.0, 56.0, 45.0, 'UN', '8806090123465', 'V1.0', 'FAMILY003', 'LINE002', 'BRAND001', '2024-01-01', '10:30:00', '2024-01-01', '10:30:00');

-- ============================================================================
-- ✅ INSERÇÃO CONCLUÍDA
-- ============================================================================
-- Próximas ações recomendadas:
-- 1. Executar script SQL para validar dados
-- 2. Executar queries para verificar integridade referencial
-- 3. Atualizar dados conforme necessário para seu ambiente
-- ============================================================================
