SELECT 
    s.order_date,
    c.fuel_cost,
    c.labor_cost,
    c.misc_cost,
    s.shipment_id,
    s.weight,
    r.route_id,
    r.distance_km,
    r.avg_time_hours,
    r.origin,
    r.destination
FROM shipments s
LEFT JOIN costs c ON s.shipment_id = c.shipment_id
LEFT JOIN routes r on s.route_id = r.route_id
WHERE 1=1