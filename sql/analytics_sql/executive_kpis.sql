-- =====================================================
-- SMART LOGISTICS MANAGEMENT PROJECT
-- EXECUTIVE KPI ANALYTICS
-- =====================================================


-- =====================================================
-- KPI: TOTAL SHIPMENTS
-- =====================================================

SELECT COUNT(shipment_id) AS total_shipment
        FROM shipments;

-- =====================================================
-- KPI: DELIVERED SHIPMENT PERCENTAGE
-- =====================================================

SELECT ROUND(
           100 * SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END)/
                    COUNT(*), 
                    2
) AS delivered_shipment_percentage
FROM shipments;

-- =====================================================
-- KPI: CANCELLED SHIPMENT PERCENTAGE
-- =====================================================

SELECT ROUND(
            100 * SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END)/
            COUNT(*),
            2
) AS cancelled_shipment_percentage
FROM shipments;

-- =====================================================
-- KPI: IN-TRANSIT SHIPMENT PERCENTAGE
-- =====================================================

SELECT ROUND(
            100 * SUM(CASE WHEN status = 'In Transit' THEN 1 ELSE 0 END)/
            COUNT(*),
            2
) AS in_transit_shipment_percentage
FROM shipments;

-- =====================================================
-- KPI: AVERAGE DELIVERY DURATION
-- =====================================================

SELECT ROUND(
        AVG(DATEDIFF(delivery_date, order_date)),
            2)
AS average_delivery_duration
FROM shipments;

-- =====================================================
-- KPI: TOTAL OPERATIONAL COST
-- =====================================================

SELECT ROUND(
        SUM(
            COALESCE(fuel_cost, 0) +
            COALESCE(labor_cost, 0) +
            COALESCE(misc_cost, 0)),
        2)
AS total_operational_cost
FROM costs;

-- =====================================================
-- KPI: AVERAGE SHIPMENT COST
-- =====================================================

SELECT ROUND(
        AVG(
            COALESCE(fuel_cost, 0) +
            COALESCE(labor_cost, 0) +
            COALESCE(misc_cost, 0)),
        2)
AS average_operational_cost
FROM costs;

-- =====================================================
-- KPI: AVERAGE SHIPMENT WEIGHT
-- =====================================================

SELECT ROUND(
        AVG(
            COALESCE(weight, 0)
            ), 2
        )
AS average_shipment_weight
FROM shipments;


-- =====================================================
-- KPI: ON-TIME DELIVERY PERCENTAGE
-- =====================================================

SELECT ROUND(
        100 * SUM(
                CASE WHEN
                    TIMESTAMPDIFF(
                        HOUR,
                        s.order_date,
                        s.delivery_date
                                ) 
                            <= r.avg_time_hours
                    THEN 1
                    ELSE 0
                END
                )/ COUNT(*), 
            2) AS on_time_delivery_percentage
FROM shipments s JOIN
     routes r
     ON
     s.route_id = 
     c.route_id
WHERE s.status = 'Delivered'
      AND s.delivery_date IS NOT NULL;

-- =====================================================
-- KPI: DELAYED SHIPMENT PERCENTAGE
-- =====================================================





-- =====================================================
-- KPI: COST PER KG
-- =====================================================



-- =====================================================
-- KPI: ACTIVE COURIER COUNT
-- =====================================================


-- =====================================================
-- KPI: ROUTE COVERAGE
-- =====================================================



/*
Delayed Shipment %
On-Time Delivery %
Cost Per KG
Active Courier Count
Route Coverage
*/