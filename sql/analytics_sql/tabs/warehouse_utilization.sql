SELECT 
    s.shipment_id,
    s.order_date,
    s.origin,
    s.destination,
    cs.vehicle_type,
    s.weight,
    w_orig.warehouse_id AS orig_wh_id,
    w_orig.city AS orig_wh_city,
    w_orig.capacity AS orig_capacity,
    w_dest.warehouse_id AS dest_wh_id,
    w_dest.city AS dest_wh_city,
    w_dest.capacity AS dest_capacity
FROM shipments s
LEFT JOIN courier_staff cs ON s.courier_id = cs.courier_id
LEFT JOIN warehouses w_orig ON s.origin = w_orig.city
LEFT JOIN warehouses w_dest ON s.destination = w_dest.city
WHERE 1=1