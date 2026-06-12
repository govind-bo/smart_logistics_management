SELECT 
    s.shipment_id,
    s.order_date,
    s.delivery_date,
    s.origin,
    s.destination,
    s.status,
    s.weight,
    s.route_id,
    s.courier_id,
    cs.name AS courier_name,
    r.distance_km,
    r.avg_time_hours,
    COALESCE(c.fuel_cost, 0) AS fuel_cost,
    COALESCE(c.labor_cost, 0) AS labor_cost,
    COALESCE(c.misc_cost, 0) AS misc_cost,
    (COALESCE(c.fuel_cost, 0) + COALESCE(c.labor_cost, 0) + COALESCE(c.misc_cost, 0)) AS total_cost,
    w.warehouse_id,
    w.city AS warehouse_city,
    w.capacity AS warehouse_capacity
FROM shipments s
LEFT JOIN courier_staff cs ON s.courier_id = cs.courier_id
LEFT JOIN routes r ON s.route_id = r.route_id
LEFT JOIN costs c ON s.shipment_id = c.shipment_id
LEFT JOIN warehouses w ON s.origin = w.city
WHERE s.order_date BETWEEN :start_date AND :end_date