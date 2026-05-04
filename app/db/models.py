from sqlalchemy import (
    Column, String, Integer, Float, DateTime, Date, Time, 
    DECIMAL, Text, Boolean, ForeignKey, LargeBinary, func
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class DimEvents(Base):
    """Tabela de eventos."""
    __tablename__ = "dim_events"
    
    eventId = Column(String(150), primary_key=True)
    name = Column(String(150))
    defaultDescription = Column(String(255))
    openTicket = Column(Integer)
    createdByIntegration = Column(Integer)
    mustBeFilledRetroactively = Column(Integer)
    dateWhenTypeDefined = Column(DateTime)
    queueType = Column(String(80))
    creationDate = Column(Date)
    creationTime = Column(Time)
    modifiedDate = Column(Date)
    modifiedTime = Column(Time)
    blocked = Column(Boolean)


class DimSalesChannel(Base):
    """Tabela de canais de venda."""
    __tablename__ = "dim_salesChannel"
    
    salesChannelId = Column(Integer, primary_key=True)
    stateRegistration = Column(String(50))
    ownStore = Column(Integer)
    cnpj = Column(String(20))
    applyEmployeeCommercialRule = Column(Integer)
    name = Column(String(255))
    active = Column(Integer)
    creationDate = Column(Date)
    creationTime = Column(Time)
    modifiedDate = Column(Date)
    modifiedTime = Column(Time)


class DimPaymentModes(Base):
    """Tabela de modalidades de pagamento."""
    __tablename__ = "dim_paymentModes"
    
    paymentModeId = Column(String(20), primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    active = Column(Integer)
    refundBy = Column(Integer)
    findFinancialTitles = Column(Integer)
    creationDate = Column(Date)
    creationTime = Column(Time)
    modifiedDate = Column(Date)
    modifiedTime = Column(Time)


class DimProductBrand(Base):
    """Tabela de marcas de produtos."""
    __tablename__ = "dim_productBrand"
    
    brandId = Column(String(50), primary_key=True)
    name = Column(String(100))
    creationDate = Column(Date)
    creationTime = Column(Time)
    modifiedDate = Column(Date)
    modifiedTime = Column(Time)


class DimProductFamily(Base):
    """Tabela de famílias de produtos."""
    __tablename__ = "dim_productFamily"
    
    familyId = Column(String(100), primary_key=True)
    name = Column(String(100))
    creationDate = Column(Date)
    creationTime = Column(Time)
    modifiedDate = Column(Date)
    modifiedTime = Column(Time)


class DimProductLine(Base):
    """Tabela de linhas de produtos."""
    __tablename__ = "dim_productLine"
    
    lineId = Column(String(100), primary_key=True)
    name = Column(String(100))
    creationDate = Column(Date)
    creationTime = Column(Time)
    modifiedDate = Column(Date)
    modifiedTime = Column(Time)


class DimCourier(Base):
    """Tabela de transportadoras."""
    __tablename__ = "dim_courier"
    
    courierId = Column(String(100), primary_key=True)
    retrieveShippingLabel = Column(Integer)
    name = Column(String(255))
    idSalesforce = Column(String(255))
    creationDate = Column(Date)
    creationTime = Column(Time)
    modifiedDate = Column(Date)
    modifiedTime = Column(Time)


class DimWarehouse(Base):
    """Tabela de depósitos/armazéns."""
    __tablename__ = "dim_warehouse"
    
    warehouseId = Column(String(10), primary_key=True)
    name = Column(String(255))


class DimVariantProducts(Base):
    """Tabela de produtos variantes."""
    __tablename__ = "dim_variantProducts"
    
    refId = Column(String(20), primary_key=True)
    name = Column(String(255))
    displayName = Column(String(255))
    commercialId = Column(String(50))
    completeProduct = Column(Integer)
    lastValidationDiagnostic = Column(Text)
    weight = Column(Float)
    height = Column(Float)
    width = Column(Float)
    length = Column(Float)
    packageWeight = Column(Float)
    packageHeight = Column(Float)
    packageWidth = Column(Float)
    packageLength = Column(Float)
    masterBoxWeight = Column(Float)
    amountMasterBox = Column(Integer)
    masterBoxHeight = Column(Float)
    masterBoxLength = Column(Float)
    masterBoxWidth = Column(Float)
    dunMasterBox = Column(String(50))
    manufacturerCode = Column(String(255))
    manufacturerName = Column(String(100))
    ean = Column(String(20))
    obsolete = Column(Integer)
    outOfLine = Column(Integer)
    outOfLineWithArrival = Column(Integer)
    onlineDate = Column(Date)
    offlineDate = Column(Date)
    version = Column(String(50))
    unit = Column(String(10))
    approvalStatus = Column(String(50))
    familyId = Column(String(100), ForeignKey("dim_productFamily.familyId"))
    lineId = Column(String(100), ForeignKey("dim_productLine.lineId"))
    brandId = Column(String(50), ForeignKey("dim_productBrand.brandId"))
    groupingProducts = Column(String(255))
    baseProductcode = Column(String(50))
    catalogVersion = Column(String(100))
    categoryCode = Column(String(100))
    creationDate = Column(Date)
    creationTime = Column(Time)
    modifiedDate = Column(Date)
    modifiedTime = Column(Time)


class CommercePaymentInfo(Base):
    """Tabela de informações de pagamento de comércio."""
    __tablename__ = "commerce_paymentInfo"
    
    paymentId = Column(String(50), primary_key=True)
    paymentModeId = Column(String(20), ForeignKey("dim_paymentModes.paymentModeId"))
    Connector = Column(String(255))
    transactionId = Column(String(50))
    GiftCardId = Column(String(50))
    duplicate = Column(Integer)
    ReferenceValue = Column(DECIMAL(10, 2))
    Acquirer = Column(String(50))
    Installments = Column(Integer)
    Group = Column(String(50))
    MerchantName = Column(String(255))
    paidValue = Column(DECIMAL(10, 2))
    Nsu = Column(String(20))
    pixRefundId = Column(String(50))
    saved = Column(Integer)
    AuthId = Column(String(50))
    CardHolder = Column(String(100))
    RedemptionCode = Column(String(50))
    Tid = Column(String(50))
    returnCode = Column(String(50))
    ExpiryYear = Column(String(4))
    ReturnMessage = Column(String(255))
    DueDate = Column(DateTime)
    LastDigits = Column(String(10))
    ExpiryMonth = Column(String(2))
    InstallmentsValue = Column(DECIMAL(10, 2))
    FirstDigits = Column(String(10))
    refund = Column(String(255))
    creationDate = Column(Date)
    creationTime = Column(Time)
    modifiedDate = Column(Date)
    modifiedTime = Column(Time)


class CommerceOrderCustomer(Base):
    """Tabela de cliente de pedido de comércio."""
    __tablename__ = "commerce_orderCustomer"
    
    customerId = Column(String(20), primary_key=True)
    orderId = Column(String(20), primary_key=True)
    customerDocument = Column(String(20))
    customerFirstName = Column(String(100))
    customerLastName = Column(String(100))
    customerDocumentType = Column(String(20))
    customerPhone = Column(String(50))
    customerEmail = Column(String(100))
    customerTradeName = Column(String(100))
    customerCorporateDocument = Column(String(20))
    customerStateInscription = Column(String(50))
    customerCorporatePhone = Column(String(50))
    customerIsCorporate = Column(Integer)
    customerUserProfileId = Column(String(50))
    customerUserProfileVersion = Column(String(50))
    customerClass = Column(String(50))
    customerCode = Column(String(50))


class CommerceOrders(Base):
    """Tabela principal de pedidos de comércio."""
    __tablename__ = "commerce_orders"
    
    orderId = Column(String(20), primary_key=True)
    paymentId = Column(String(50), ForeignKey("commerce_paymentInfo.paymentId"))
    customerId = Column(String(20))
    salesChannelId = Column(Integer, ForeignKey("dim_salesChannel.salesChannelId"))
    Sequence = Column(String(20))
    SellerOrderId = Column(String(50))
    MarketplaceOrderId = Column(String(50))
    Origin = Column(String(50))
    AffiliateId = Column(String(50))
    Description = Column(String(255))
    deliveryQuotedCost = Column(DECIMAL(10, 2))
    isComplete = Column(Integer)
    OrderIsIncomplete = Column(Integer)
    invoiceShippedDate = Column(DateTime)
    invoiceDeliveryDate = Column(DateTime)
    authorizedDate = Column(DateTime)
    UtmSource = Column(String(100))
    UtmPartner = Column(String(100))
    UtmMedium = Column(String(100))
    UtmCampaign = Column(String(100))
    UtmiCampaign = Column(String(100))
    UtmiPage = Column(String(100))
    UtmiPart = Column(String(100))
    date = Column(DateTime)
    statusUpdatedAt = Column(DateTime)
    paymentRefundOn = Column(Integer)
    paymentRefundAttempts = Column(Integer)
    subtotal = Column(DECIMAL(10, 2))
    totalDiscounts = Column(DECIMAL(10, 2))
    cancelledIn = Column(Integer)
    status = Column(String(50))
    exportStatus = Column(String(50))
    blockCart = Column(Integer)
    Type = Column(String(10))
    creationDate = Column(Date)
    creationTime = Column(Time)
    modifiedDate = Column(Date)
    modifiedTime = Column(Time)


class CommerceConsignments(Base):
    """Tabela de remessas/consignações de comércio."""
    __tablename__ = "commerce_consignments"
    
    consigmentId = Column(String(20), primary_key=True)
    orderId = Column(String(20), ForeignKey("commerce_orders.orderId"))
    romaneioNumber = Column(String(20))
    trackingUrl = Column(String(255))
    isReturnInTransit = Column(Integer)
    departureDate = Column(DateTime)
    namedDeliveryDate = Column(DateTime)
    trackingCode = Column(String(50))
    shippingDate = Column(DateTime)
    trackingID = Column(String(50))
    manifestNumber = Column(String(20))
    transportadora = Column(String(255))
    carrier = Column(String(100))
    invoiceSent = Column(Integer)
    deliveryForecastDate = Column(DateTime)
    statusDisplay = Column(String(50))
    shippingLabelProcess = Column(String(155))
    warehouseId = Column(String(50))
    consignmentProcesses = Column(String(255))
    status = Column(String(50))
    shippingAddress = Column(String(255))
    exchangeReason = Column(String(255))
    creationDate = Column(Date)
    creationTime = Column(Time)
    modifiedDate = Column(Date)
    modifiedTime = Column(Time)


class CommerceConsignmentEntry(Base):
    """Tabela de entradas de consignação de comércio."""
    __tablename__ = "commerce_ConsignmentEntry"
    
    consigmentId = Column(String(20), ForeignKey("commerce_consignments.consigmentId"), primary_key=True)
    refId = Column(String(20), primary_key=True)
    quantityPending = Column(Integer)
    quantityShipped = Column(Integer)
    quantityDeclined = Column(Integer)
    shippedQuantity = Column(Integer)
    quantity = Column(Integer)


class CommerceCartEntry(Base):
    """Tabela de entradas de carrinho de comércio."""
    __tablename__ = "commerce_cartEntry"
    
    orderId = Column(String(50), primary_key=True)
    refId = Column(String(20), primary_key=True)
    warehouseId = Column(String(10), ForeignKey("dim_warehouse.warehouseId"))
    courierId = Column(String(100), ForeignKey("dim_courier.courierId"))
    namedDeliveryDate = Column(DateTime)
    sellingPrice = Column(DECIMAL(18, 2))
    deliveryQuotedCost = Column(DECIMAL(18, 2))
    calculated = Column(Integer)
    pointOfService = Column(String(255))
    basePrice = Column(DECIMAL(18, 2))
    quantity = Column(Integer)
    price = Column(DECIMAL(18, 2))
    selectedSla = Column(String(255))
    entryNumber = Column(Integer)
    info = Column(Text)
    deliveryCost = Column(DECIMAL(18, 2))
    totalPrice = Column(DECIMAL(18, 2))
    isReservedInErp = Column(Integer)
    costPrice = Column(DECIMAL(18, 2))
    quantityStatus = Column(String(255))
    Promotions = Column(Text)
    costCenter = Column(String(255))
    chosenVendor = Column(String(255))
    creationDate = Column(Date)
    creationTime = Column(Time)
    modifiedDate = Column(Date)
    modifiedTime = Column(Time)


class CommerceBillingAddress(Base):
    """Tabela de endereço de cobrança de comércio."""
    __tablename__ = "commerce_billingAddress"
    
    orderId = Column(String(20), primary_key=True)
    postalcode = Column(String(20))
    unloadingAddress = Column(Integer)
    streetnumber = Column(String(50))
    complement = Column(String(255))
    remarks = Column(String(255))
    addressType = Column(String(50))
    contactAddress = Column(Integer)
    shippingAddress = Column(Integer)
    addressId = Column(String(50))
    building = Column(String(100))
    cellphone = Column(String(20))
    town = Column(String(50))
    appartment = Column(String(100))
    company = Column(String(100))
    typeQualifier = Column(String(10))
    streetname = Column(String(255))
    department = Column(String(100))
    billingAddress = Column(Integer)
    country = Column(String(10))
    title = Column(String(50))
    region = Column(String(100))
    district = Column(String(255))


class CommerceDeliveryAddresses(Base):
    """Tabela de endereço de entrega de comércio."""
    __tablename__ = "commerce_deliveryaddresses"
    
    orderId = Column(String(20), primary_key=True)
    postalcode = Column(String(20))
    unloadingAddress = Column(Integer)
    streetnumber = Column(String(50))
    complement = Column(String(255))
    remarks = Column(String(255))
    addressType = Column(String(50))
    contactAddress = Column(Integer)
    shippingAddress = Column(Integer)
    addressId = Column(String(50))
    building = Column(String(100))
    cellphone = Column(String(20))
    town = Column(String(50))
    appartment = Column(String(100))
    company = Column(String(100))
    typeQualifier = Column(String(10))
    streetname = Column(String(255))
    department = Column(String(100))
    billingAddress = Column(Integer)
    country = Column(String(10))
    title = Column(String(50))
    region = Column(String(100))
    district = Column(String(255))


class CommerceEventHistory(Base):
    """Tabela de histórico de eventos de comércio."""
    __tablename__ = "commerce_eventHistory"
    
    orderId = Column(String(20), primary_key=True)
    consignment = Column(String(20))
    eventId = Column(String(150), ForeignKey("dim_events.eventId"), primary_key=True)
    description = Column(String(255), primary_key=True)
    trackingCode = Column(String(50))
    trackingDispatchedDate = Column(DateTime)
    trackingCity = Column(String(100))
    trackingDescription = Column(String(255))
    lastExecutionDate = Column(DateTime)
    manifestNumber = Column(String(50))
    origin = Column(String(100))
    trackingCourier = Column(String(100))
    attempts = Column(Integer)
    sendCRM = Column(Integer)
    departureDate = Column(DateTime)
    trackingUrl = Column(String(255))
    trackingState = Column(String(50))
    send = Column(Integer)
    romaneioNumber = Column(String(50))
    date = Column(DateTime)
    eventType = Column(String(50))
    sourceSystem = Column(String(50))
    creationDate = Column(Date)
    creationTime = Column(Time)
    modifiedDate = Column(Date)
    modifiedTime = Column(Time)
    createdAt = Column(DateTime, default=datetime.utcnow)


class CommerceInvoices(Base):
    """Tabela de faturas de comércio."""
    __tablename__ = "commerce_invoices"
    
    invoiceNumber = Column(String(20), primary_key=True)
    invoiceSerie = Column(String(5), primary_key=True)
    consigmentId = Column(String(20), ForeignKey("commerce_consignments.consigmentId"))
    establishment = Column(String(10))
    invoiceValue = Column(DECIMAL(10, 2))
    issuanceDate = Column(DateTime)
    orderAuthorizedDate = Column(DateTime)
    invoiceUrl = Column(String(255))
    invoiceKey = Column(String(100))
    invoiceSendTo = Column(Integer)
    invoiceSedtToSalesforce = Column(Integer)
    xml = Column(Integer)
    volumes = Column(Integer)
    courier = Column(String(100))
    reasonEntry = Column(String(255))
    reasonReturn = Column(String(255))
    type = Column(String(20))
    stockReleased = Column(Integer)
    creationDate = Column(Date)
    creationTime = Column(Time)
    modifiedDate = Column(Date)
    modifiedTime = Column(Time)


class CommerceOrderBlock(Base):
    """Tabela de bloqueios de pedidos de comércio."""
    __tablename__ = "commerce_orderBlock"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    orderId = Column(String(20), ForeignKey("commerce_orders.orderId"))
    refId = Column(String(20), ForeignKey("dim_variantProducts.refId"))
    date = Column(DateTime)
    description = Column(String(255))
    receivedPrice = Column(DECIMAL(10, 2))
    calculatedPrice = Column(DECIMAL(10, 2))
    blockReason = Column(String(100))
    blockType = Column(String(100))
    status = Column(String(100))
    salesChannelId = Column(Integer, ForeignKey("dim_salesChannel.salesChannelId"))
    creationDate = Column(Date)
    creationTime = Column(Time)
    modifiedDate = Column(Date)
    modifiedTime = Column(Time)
