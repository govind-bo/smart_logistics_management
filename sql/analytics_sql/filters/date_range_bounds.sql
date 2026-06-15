-- This query finds the minimum and maximum date in shipments - 
-- to use for the order date filter

SELECT
    MIN(order_date) AS min_date,
    MAX(order_date) AS max_date
FROM shipments
WHERE 1 = 1