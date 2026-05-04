# Flight Data ELT Pipeline (Airflow + Snowflake + dbt)

## Overview
<b>These instructions do not cover every step to recreate this pipeline.</b><br/>
This tech stack was used because they were requirements in a Data engineer job ad.
This pipeline utilizes AWS S3 which has costs and requires configurations not shown here.<br/>
Snowflake requires subscription also, but it offers free trial which was used in this project.<br/>
OpenSky API was chosen because it was free. <br/>
Apache Airflow is used here even though it was overkill for this project.<br/>
This project could be created without Snowflake and AWS S3 with free solutions like MinIO instead of S3 and PostgreSQL instead of Snowflake.<br/>

Data pipeline for flight data

The pipeline:
1. Extracts flight data from the OpenSky API  
2. Stores raw data locally and uploads it to AWS S3
3. Loads data into Snowflake (raw layer)  
4. Transforms data using dbt (staging and marts layers)  
5. Validates data quality with dbt tests  
6. Orchestrates the workflow using Apache Airflow  
7. Visualizes results in Power BI  

---

## Tech Stack

Python, Apache Airflow, Snowflake, dbt, AWS S3, Docker, Power BI

## Architecture
OpenSky API <-- Python (Extract) --> Local JSON --> AWS S3 --> Snowflake (Raw) --> dbt (STAGING -> MARTS) --> Power BI

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/leevik/flight-data-pipeline.git
cd flight-data-pipeline
```

### 2. Configure environment variables

Copy the example file:

```bash
cp .env.example .env
```

Fill in the required values:
- Snowflake account and user
- AWS credentials and S3 bucket
- OpenSky API credentials

### 3. Configure dbt profile

```bash
cp dbt/flight_analytics/profiles.yml.example dbt/flight_analytics/profiles.yml
```

### 4. Add Snowflake private key

Place your private key file in:

```
keys/dbt_rsa_key.p8
```

Ensure the path matches the value in your `.env` file.

### 5. Start the services

```bash
docker compose up --build
```

### 6. Access Airflow

Open in browser:

```
http://localhost:8080
```

Default credentials:
Check password from logs

```
username: admin
password: <check logs>
```

## Running the Pipeline

If services are already built, you can start only Airflow:

```bash
docker compose up airflow
```
Open in browser:
```
http://localhost:8080
```
Default credentials:
Check password from logs
```
username: admin
password: <check logs>
```

### Trigger the pipeline

1. Navigate to the DAGs page  
2. Find the DAG named:

```
flight_data_pipeline
```

3. Enable the DAG (toggle switch)  
4. Click "Trigger DAG"

---

### Pipeline steps

The pipeline executes the following tasks:

```
fetch_flights → upload_to_s3 → load_to_snowflake → dbt_run → dbt_test
```

- **fetch_flights**: Extracts flight data from OpenSky API  
- **upload_to_s3**: Uploads JSON data to AWS S3  
- **load_to_snowflake**: Loads raw data into Snowflake  
- **dbt_run**: Transforms data into staging and marts models  
- **dbt_test**: Runs data quality checks  

---

## Power BI
Connect snowflake to Power BI with same keypair & username you used earlier

Example visualizations:
    2 bar charts:
        1. X-axis arrival airport & Y-axis flight count
        2. X-axis arrival airport & Y-axis avg flight duration