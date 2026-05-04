UPDATE commerce_orders
    SET 
    [Type] = ?,
    [OrderIsIncomplete] = ?
WHERE [orderId] = ?