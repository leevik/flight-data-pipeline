import os
from pathlib import Path

import snowflake.connector
from dotenv import load_dotenv


load_dotenv()

SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "FLIGHT_DATA_DEMO")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "RAW")
SNOWFLAKE_PRIVATE_KEY_PATH = os.getenv(
    "SNOWFLAKE_PRIVATE_KEY_PATH",
    "/app/keys/dbt_rsa_key.p8",
)

STAGE_NAME = os.getenv("SNOWFLAKE_STAGE_NAME", "flights_stage")
TABLE_NAME = os.getenv("SNOWFLAKE_RAW_TABLE", "FLIGHTS")


def get_connection():
    return snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        role=SNOWFLAKE_ROLE,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
        private_key_file=SNOWFLAKE_PRIVATE_KEY_PATH,
    )


def load_flights_to_snowflake() -> None:
    if not Path(SNOWFLAKE_PRIVATE_KEY_PATH).exists():
        raise FileNotFoundError(f"Private key not found: {SNOWFLAKE_PRIVATE_KEY_PATH}")

    copy_sql = f"""
        COPY INTO {SNOWFLAKE_SCHEMA}.{TABLE_NAME}
        FROM @{STAGE_NAME}
        FILE_FORMAT = (TYPE = JSON)
        ON_ERROR = CONTINUE;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"USE DATABASE {SNOWFLAKE_DATABASE}")
            cur.execute(f"USE SCHEMA {SNOWFLAKE_SCHEMA}")

            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {SNOWFLAKE_SCHEMA}.{TABLE_NAME} (
                    data VARIANT
                )
            """)

            cur.execute(copy_sql)
            results = cur.fetchall()

            print("Snowflake COPY INTO completed.")
            for row in results:
                print(row)


if __name__ == "__main__":
    load_flights_to_snowflake()