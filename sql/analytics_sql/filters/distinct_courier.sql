SELECT DISTINCT cs.name AS courier_name
FROM courier_staff cs
JOIN shipments s
    ON cs.courier_id = s.courier_id
    WHERE 1 = 1