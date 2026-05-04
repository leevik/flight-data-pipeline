# airflow/dags/flight_pipeline_dag.py

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "leevio",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="flight_data_pipeline",
    description="Fetch flight data, upload to S3, load Snowflake, run dbt",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["flights", "s3", "snowflake", "dbt"],
) as dag:

    fetch_flights = BashOperator(
        task_id="fetch_flights",
        bash_command="python -m src.extract.fetch_flights",
    )

    upload_to_s3 = BashOperator(
        task_id="upload_to_s3",
        bash_command="python -m src.load.upload_to_s3",
    )

    load_to_snowflake = BashOperator(
        task_id="load_to_snowflake",
        bash_command="python -m src.load.load_to_snowflake",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="dbt run --project-dir /app/dbt --profiles-dir /app/dbt",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="dbt test --project-dir /app/dbt --profiles-dir /app/dbt",
    )

    fetch_flights >> upload_to_s3 >> load_to_snowflake >> dbt_run >> dbt_test