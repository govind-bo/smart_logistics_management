SELECT 
    s.shipment_id,
    s.order_date,
    s.status,
    s.origin,
    s.destination,
    s.weight,
    s.route_id,
    s.courier_id,
    cs.name AS courier_name,
    r.distance_km
FROM shipments s
LEFT JOIN courier_staff cs ON s.courier_id = cs.courier_id
LEFT JOIN routes r ON s.route_id = r.route_id
WHERE 1=1