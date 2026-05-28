-- =====================================================
-- ADD route_id COLUMN
-- =====================================================

ALTER TABLE shipments
ADD COLUMN route_id VARCHAR(50);

-- =====================================================
-- POPULATE route_id USING routes TABLE
-- =====================================================

UPDATE shipments s

JOIN routes r
ON s.origin = r.origin
AND s.destination = r.destination

SET s.route_id = r.route_id
WHERE s.route_id IS NULL;

-- =====================================================
-- ADD FOREIGN KEY
-- =====================================================

ALTER TABLE shipments

ADD CONSTRAINT fk_shipments_route_id

FOREIGN KEY (route_id)
REFERENCES routes(route_id);