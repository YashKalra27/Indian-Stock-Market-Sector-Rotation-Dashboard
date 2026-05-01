# Sector Rotation Analytics: Cloud-Native Data Engineering Pipeline

## 1. Project Objective
The **Sector Rotation Analytics** project is a comprehensive data engineering and analytics platform designed to track the flow of capital across different sectors of the Indian Stock Market. By analyzing **Relative Strength (RS)** and **Momentum** against the Nifty 50 benchmark, the project identifies sector leadership shifts and mean reversion opportunities.

---

## 2. Technical Stack
| Category | Technologies |
| :--- | :--- |
| **Cloud Infrastructure** | AWS (S3, Lambda, Glue, Athena) |
| **Data Processing** | Python, Pandas, NumPy, SQL |
| **Orchestration** | AWS Lambda (Serverless ETL) |
| **Frontend/Analytics** | Streamlit, Plotly, Streamlit Components |
| **DevOps/Sync** | AWS CLI, Boto3, S3FS |

---

## 3. Step-by-Step Architecture

### Phase 1: Data Ingestion (The Bronze Layer)
The pipeline begins with raw data extraction from financial sources (NSE/BSE). 
- **Storage**: Raw data is staged in an **AWS S3 Bucket** (`sector-rotation-project-yashkalra`) under the `raw/` prefix.
- **Datasets**: 
  - **Prices**: Historical closing prices for all sectoral indices.
  - **Valuation**: Historical PE, PB, and Dividend Yield data.
  - **Indicators**: Macro data such as INDIA VIX (Volatility) and Gold prices (USD/INR).

### Phase 2: Automated Serverless ETL (The Silver Layer)
A Python-based **AWS Lambda Function** acts as the engine of the pipeline.
1. **Column Sanitization**: Raw files often have inconsistent headers (e.g., "Index Name", "index_name", "IndexName"). The Lambda uses **Regex** to strip special characters and lowercase all columns into a unified `snake_case` format.
2. **Temporal Alignment**: Since valuation data (PE/PB) is often reported on different schedules than price data, the Lambda identifies overlapping dates to ensure a precise "Apple-to-Apples" comparison.
3. **Indicator Unification**: Macro indicators like VIX and Gold are transformed into a long-format `master_indicators.csv` for easy querying.

### Phase 3: Feature Engineering (The Gold Layer)
The Lambda function calculates sophisticated financial metrics used for the final visualization:
- **Relative Strength (RS)**: Calculated as `[Sector Price] / [Nifty 50 Price]`. This isolates sector performance from general market noise.
- **Momentum (20-Bar)**: Calculated as the percentage change in the RS ratio over a 20-period lookback window.
- **Rank Tracking**: Sectors are dynamically ranked daily based on their RS and Momentum values.
- **Rank Change**: A specific feature that tracks the "delta" in rank to identify sectors quickly climbing the leadership ladder.
- **Output**: The refined data is saved back to S3 as `final_dataset.csv`.

### Phase 4: Data Cataloging (AWS Glue)
To transform our processed CSV files into a queryable relational structure, we implemented **AWS Glue**:
- **Glue Crawler**: A crawler is configured to automatically scan the `processed/` S3 directory. It identifies the data schema (headers, data types) and registers the datasets as tables.
- **Data Catalog**: The crawler populates a centralized metadata repository, allowing other AWS services to "understand" our dataset without manual schema definitions.

### Phase 5: Interactive SQL Analysis (Amazon Athena)
With the data cataloged, we utilized **Amazon Athena** for advanced analytical discovery:
- **Serverless SQL**: Athena allows us to run complex SQL queries (e.g., `SELECT * FROM sector_data WHERE momentum > 0.1`) directly against the files in S3.
- **Ad-hoc Insights**: This phase was critical for verifying the feature engineering results (RS/Momentum calculations) before pushing them to the live dashboard.

### Phase 6: Analytical Dashboard (The Delivery Layer)
The final stage is a **Streamlit Web Application** that provides a premium, interactive interface for end-users.
- **Glassmorphism UI**: Uses custom CSS/HTML to implement a dark-mode gradient interface with Inter typography and micro-animations.
- **Real-Time S3 Integration**: Utilizes `s3fs` to stream the processed Gold-layer data directly from AWS without needing a persistent database.
- **Visualizations**:
  - **Rotation Scatter**: A 2x2 quadrant (Improving, Leading, Weakening, Lagging) visualizing sector shifts.
  - **Macro Overlay**: Overlays sector performance against VIX or Gold to see how sectors react to volatility.
  - **Momentum Rank Tracker**: Interactive tables showing sector rankings with color-coded status tags.

---

## 4. Key Engineering Decisions
- **Serverless First**: By using AWS Lambda, we eliminated the need for a 24/7 server, significantly reducing infrastructure costs while maintaining high performance.
- **Regex-Driven Cleaning**: Implemented a flexible "Clean Function" that makes the pipeline resilient to changes in source CSV formats from financial providers.
- **Stateless Analytics**: The Streamlit dashboard remains stateless by fetching only what it needs from S3, ensuring the app remains fast and responsive even with thousands of rows of data.

---

## 5. Repository Structure
```text
/project
├── app.py                # Main Streamlit Dashboard (Premium UI)
├── lambda_function.py     # AWS Lambda Script (ETL & Feature Engineering)
├── raw/                   # Local raw data mirror
├── processed/             # Local processed data mirror
├── scripts/               # Modularized ETL Python scripts
└── requirements.txt       # Project dependencies
```
