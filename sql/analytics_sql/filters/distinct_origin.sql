SELECT DISTINCT s.origin 
FROM shipments s
LEFT JOIN courier_staff cs ON s.courier_id = cs.courier_id
WHERE 1=1