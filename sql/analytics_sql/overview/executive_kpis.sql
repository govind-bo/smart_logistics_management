SELECT 
    s.shipment_id,
    s.order_date,
    s.delivery_date,
    s.origin,
    s.destination,
    s.status,
    cs.name AS courier_name,
    s.weight,
    s.route_id,
    r.avg_time_hours,
    COALESCE(c.fuel_cost, 0) + COALESCE(c.labor_cost, 0) + COALESCE(c.misc_cost, 0) AS total_cost
FROM shipments s
LEFT JOIN costs c ON s.shipment_id = c.shipment_id
LEFT JOIN routes r ON s.route_id = r.route_id
LEFT JOIN courier_staff cs ON s.courier_id = cs.courier_id
WHERE s.order_date BETWEEN :start_date AND :end_date