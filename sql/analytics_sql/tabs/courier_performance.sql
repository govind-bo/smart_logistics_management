SELECT 
    s.shipment_id,
    s.order_date,
    s.status,
    s.weight,
    s.courier_id,
    cs.name AS courier_name,
    cs.rating AS courier_rating,
    cs.vehicle_type
FROM shipments s
LEFT JOIN courier_staff cs ON s.courier_id = cs.courier_id
WHERE 1=1