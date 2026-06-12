SELECT DISTINCT s.destination
FROM shipments s
WHERE s.order_date BETWEEN :start_date AND :end_date


/*
SELECT DISTINCT destination
FROM shipments
ORDER BY destination;
*/