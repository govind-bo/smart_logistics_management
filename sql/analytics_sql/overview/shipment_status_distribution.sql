SELECT status,
        COUNT(*) AS shipment_count
FROM shipments
WHERE order_date BETWEEN :start_date AND :end_date
GROUP BY status
ORDER BY shipment_count DESC;