SELECT 
    s.shipment_id,
    s.order_date,
    s.status,
    s.origin,
    s.destination,
    s.weight,
    s.delivery_date,
    s.courier_id,
    cs.name AS courier_name,
    cs.vehicle_type,
    st.tracking_id,
    st.status AS tracking_status,
    st.timestamp,
    COALESCE(c.fuel_cost, 0) AS fuel_cost,
    COALESCE(c.labor_cost, 0) AS labor_cost,
    COALESCE(c.misc_cost, 0) AS misc_cost
FROM shipments s
LEFT JOIN courier_staff cs ON s.courier_id = cs.courier_id
LEFT JOIN shipment_tracking st ON s.shipment_id = st.shipment_id
LEFT JOIN costs c ON s.shipment_id = c.shipment_id
WHERE 1=1