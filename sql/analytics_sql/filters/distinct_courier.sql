SELECT DISTINCT c.courier_id, c.name AS courier_name
FROM courier_staff c
JOIN shipments s
    ON c.courier_id = s.courier_id
WHERE s.order_date BETWEEN :start_date AND :end_date

/*
SELECT courier_id, name
FROM courier_staff
ORDER BY name;
*/

