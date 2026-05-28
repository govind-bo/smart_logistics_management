-- =====================================================
-- SHIPMENTS TABLE INDEXES
-- =====================================================

CREATE INDEX idx_shipments_status
            ON shipments(status);

CREATE INDEX idx_shipments_order_date
            ON shipments(order_date);

CREATE INDEX idx_shipments_origins_destination
            ON shipments(origin, destination);
        
CREATE INDEX idx_shipments_courier_id
            ON shipments(courier_id);

CREATE INDEX idx_shipments_delivery_date
            ON shipments(delivery_date);

-- =====================================================
-- SHIPMENT TRACKING TABLE INDEXES
-- =====================================================

CREATE INDEX idx_tracking_shipment_id
ON shipment_tracking(shipment_id);

CREATE INDEX idx_tracking_status
ON shipment_tracking(status);

CREATE INDEX idx_tracking_timestamp
ON shipment_tracking(timestamp);

-- =====================================================
-- ROUTES TABLE INDEXES
-- =====================================================

CREATE INDEX idx_routes_origin_destination
ON routes(origin, destination);




