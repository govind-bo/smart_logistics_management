# Smart Logistics Management & Analytics Platform

## Project Overview

In modern logistics operations, companies manage thousands of shipments daily across multiple routes, warehouses, and courier personnel. Operational inefficiencies such as delivery delays, high transportation costs, underutilized warehouses, and inconsistent courier performance can significantly impact profitability and customer satisfaction.

This project is an end-to-end Data Engineering and Business Intelligence solution designed to solve this problem. It consolidates raw, fragmented operational data into a normalized MySQL database via a robust ETL pipeline, and layers a high-performance Streamlit dashboard on top to provide real-time analytics, SLA tracking, and operational insights.

## Key Features & Dashboard Modules

The presentation layer is divided into seven dedicated modules, each designed to answer specific business questions:

1. Operations Overview
* Tracks high-level KPIs: Total shipments, delivery success rates, and average durations.
* Visualizes shipment status mix and chronological cost trends.


2. Route Performance
* Compares expected delivery times (baseline) against actual delivery times to identify severe SLA breaches.
* Maps network density and correlates route distance with delivery delays.


3. Courier Performance
* Analyzes workforce efficiency by tracking volume handled per courier.
* Correlates customer ratings with actual delivery success rates to evaluate personnel effectiveness.


4. Cost Analytics
* Breaks down operational expenses (Fuel, Labor, Miscellaneous).
* Identifies high-cost shipments and evaluates how cost scales with package weight and route distance.


5. Warehouse Utilization
* Compares individual warehouse capacity against actual shipment activity.
* Highlights utilization risks (bottlenecks vs. underutilized hubs).


6. Cancellation Analytics
* Identifies failure hotspots by mapping cancellation rates to specific origin cities and couriers.


7. Shipment Explorer
* A micro-investigation tool for customer support agents.
* Allows targeted lookup of individual Shipment IDs to audit tracking timelines and specific cost breakdowns.



## Technical Architecture

This application strictly adheres to a 3-Tier Architecture, ensuring a clear separation of concerns.

### 1. Data Ingestion & ETL Layer

The backend features an idempotent, custom-built ETL pipeline (`main_pipeline.py`) that processes over 280,000 raw records (CSVs/JSONs).

* Extraction: Automatically parses mixed file formats from a raw data landing zone.
* Validation: Performs pre-load Quality Assurance, checking for Primary Key uniqueness, Foreign Key coverage, and proper Date parsing.
* Transformation & Cleaning: Resolves duplicate anomalies in memory. Handles 1-to-Many route mapping relationships deterministically by assigning the optimal (shortest distance) route to unstructured shipments before they hit the database.
* Loading: Executes a safe, reverse-dependency table truncation (disabling FK checks temporarily) for a clean bulk insert via SQLAlchemy, followed by automated indexing (`02_indexes.sql`) for read optimization.

### 2. Caching & Processing Layer

Follows a "Let SQL Fetch, Let Python Analyze" methodology.

* Database Connection: Utilizes SQLAlchemy connection pooling.
* Caching: Streamlit's `@st.cache_data` wraps the query execution layer. Mutable parameters (lists from multiselects) are securely cast to tuples before caching to prevent memory reference errors.
* Processing Logic: Pandas handles heavy statistical aggregations, sorting, and percentage calculations in memory. `.copy()` is used explicitly during dataframe slicing to prevent Pandas `SettingWithCopyWarning` memory leaks.

### 3. Presentation Layer

* Context-Aware Cascading Filters: A multi-directional filtering engine that dynamically updates available dropdown options (Origin, Destination, Status, Courier) based on database realities, preventing "Zero Data" dead-ends.
* Defensive UI: The interface intercepts empty dataframes before they cause runtime exceptions (e.g., `ZeroDivisionError` or `KeyError`), rendering clean "No Data Available" annotations on Plotly charts instead.

## Dataset Scale

* Shipment Records: ~70,000 active shipments
* Tracking Events: ~209,000 granular status logs
* Cost Records: ~70,000 shipment cost breakdowns
* Network & Workforce: 1,000 couriers, 500 distinct routes, and 50 warehouse distribution centers

---

## Setup & Installation Instructions

### 1. Prerequisites

* Python 3.10 or higher
* MySQL Server (running locally or remotely)
* Git

### 2. Clone the Repository

Open your terminal and run:
`git clone https://github.com/your-username/smart-logistics-management.git`
`cd smart-logistics-management`

### 3. Set Up Virtual Environment & Dependencies

Create and activate your virtual environment:
`python -m venv venv`

**On Windows:**
`venv\Scripts\activate`

**On Mac/Linux:**
`source venv/bin/activate`

Install the required packages:
`pip install -r requirements.txt`

### 4. Database Configuration

Create a `.env` file in the root directory of the project and define your MySQL credentials:
MYSQL_USER="your_mysql_username"
MYSQL_PASSWORD="your_mysql_password"
MYSQL_HOST="localhost"
MYSQL_PORT="3306"
MYSQL_DB="smart_logistics"

### 5. Run the ETL Pipeline

Ensure your raw data files are placed in `data/raw_data/`. Execute the orchestrator to build the schema, run the ETL validations, load the database, and apply indexes:
`python -m src.main_pipeline`

### 6. Launch the Dashboard

Start the Streamlit web application:
`streamlit run app.py`

---

## Repository Structure
├── config/
│   ├── db_config.py           
│   └── schema_config.py       
├── data/
│   ├── raw_data/              
│   └── processed_data/        
├── sql/
│   ├── analytics_sql/         
│   └── etl_sql/               
├── src/
│   ├── dashboard/             
│   │   ├── components/        
│   │   ├── processors/        
│   │   ├── tabs/              
│   │   └── utils.py           
│   ├── database/              
│   └── etl/                   
├── app.py                     
└── main_pipeline.py