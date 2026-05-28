DROP DATABASE IF EXISTS smart_logistics;

CREATE DATABASE smart_logistics;

USE smart_logistics;

SHOW TABLES;

-- Create tables
-- dimension tables:

CREATE TABLE IF NOT EXISTS courier_staff (
		courier_id VARCHAR(50) PRIMARY KEY COMMENT 'UID for courier employee',
        name VARCHAR(150) NOT NULL,
        rating DECIMAL(3, 1) COMMENT 'Performance rating',
        vehicle_type VARCHAR(50)
        ) COMMENT = 'Stores courier employees details';
  
CREATE TABLE IF NOT EXISTS routes (
		route_id VARCHAR(50) PRIMARY KEY COMMENT 'UID for route',
        origin VARCHAR(100) COMMENT 'Starting city/location of route',
        destination VARCHAR(100) COMMENT 'Ending city/location of route',
        distance_km DECIMAL(10,2) COMMENT 'Distance between origin and destination in kilometers ',
        avg_time_hours DECIMAL(5,2) COMMENT 'Average travel time expected for this route'
        ) COMMENT = 'Stores transport route information';
        
CREATE TABLE IF NOT EXISTS warehouses (
		warehouse_id VARCHAR(50) PRIMARY KEY COMMENT 'UID for warehouse',
        city VARCHAR(100) COMMENT 'City where warehouse is located',
        state VARCHAR(50) COMMENT 'State or region of warehouse',
        capacity INT COMMENT 'Maximum shipment capacity warehouse can handle'
        ) COMMENT = 'Stores warehouse location and capacity details';

-- fact tables:
        
CREATE TABLE IF  NOT EXISTS shipments(
		shipment_id VARCHAR(50) PRIMARY KEY,
        order_date DATE COMMENT 'Date when the shipment order was created ',
        origin VARCHAR(100) COMMENT 'City/location where shipment starts ',
        destination VARCHAR(100) COMMENT 'Delivery city/location',
        weight DECIMAL(10, 2) COMMENT 'Weight of the shipment in kg',
        courier_id VARCHAR(50) COMMENT 'courier responsible for delivery (FK to courier_staff)',
        status VARCHAR(50) COMMENT 'Current shipment status (Delivered, In Transit, Cancelled, etc.)',
        delivery_date DATE NULL COMMENT 'Date when shipment was delivered (NULL if not delivered yet)',
        
        CONSTRAINT fk_shipments_courier
			FOREIGN KEY (courier_id)
			REFERENCES courier_staff(courier_id)
        ) COMMENT'Stores all shipment/order details';
       
CREATE TABLE IF NOT EXISTS shipment_tracking (
		tracking_id INT PRIMARY KEY COMMENT 'UID for tracking event',
        shipment_id VARCHAR(50) COMMENT 'Shipment linked to this event (FK to shipments)',
        status VARCHAR(50) COMMENT 'Status update at this stage (Picked Up, In Transit, Delivered, etc.)',
        timestamp DATETIME COMMENT 'Date & time when this tracking event  occurred',
        
        CONSTRAINT fk_tracking_shipment
			FOREIGN KEY (shipment_id)
            REFERENCES shipments(shipment_id)
		) COMMENT 'Tracks status updates for each shipment over time';
       
CREATE TABLE IF NOT EXISTS costs (
		shipment_id VARCHAR(50) PRIMARY KEY COMMENT 'Shipment linked to cost record (FK to shipments)',
		fuel_cost DECIMAL(15,2) COMMENT 'Fuel cost incurred for shipment delivery',
		labor_cost DECIMAL(15,2) COMMENT 'Courier labor cost for shipment',
		misc_cost DECIMAL(15,2) COMMENT 'Additional operational costs (handling, packaging, etc.)',
	
		CONSTRAINT fk_costs_shipments
			FOREIGN KEY (shipment_id) 
			REFERENCES shipments(shipment_id)
		) COMMENT = 'Stores cost breakdown per shipment';

SHOW TABLES;

