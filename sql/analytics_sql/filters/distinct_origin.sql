
SELECT DISTINCT s.origin
FROM shipments s
WHERE s.order_date BETWEEN :start_date AND :end_date

/*
SELECT DISTINCT origin
FROM shipments
ORDER BY origin;
*/