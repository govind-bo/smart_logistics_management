SELECT DISTINCT s.status AS shipment_status
FROM shipments s
WHERE s.order_date BETWEEN :start_date AND :end_date


/*
SELECT DISTINCT status AS shipment_status
    FROM shipments
    ORDER BY shipment_status;
    */


