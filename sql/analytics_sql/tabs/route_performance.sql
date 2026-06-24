SELECT
    s.shipment_id,
    s.order_date,
    s.delivery_date,
    s.status,
    s.weight,
    r.route_id,
    r.origin,
    r.destination,
    r.distance_km,
    r.avg_time_hours AS expected_time_hrs,
    TIMESTAMPDIFF(HOUR, s.order_date, s.delivery_date) AS actual_time_hrs
FROM shipments s
LEFT JOIN routes r ON s.route_id = r.route_id
WHERE s.status = 'Delivered'
