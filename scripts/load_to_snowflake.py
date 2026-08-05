import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

from config.config import (
    SNOWFLAKE_ACCOUNT,
    SNOWFLAKE_USER,
    SNOWFLAKE_PASSWORD,
    SNOWFLAKE_WAREHOUSE,
    SNOWFLAKE_DATABASE,
    SNOWFLAKE_SCHEMA,
)


def load_to_snowflake():
    # Read CSV
    csv_path = "data/weather_data.csv"
    df = pd.read_csv(csv_path)

    print(f"Read {len(df)} rows from CSV.")

    # Connect to Snowflake
    conn = snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
    )

    try:
        success, nchunks, nrows, output = write_pandas(
            conn=conn,
            df=df,
            table_name="WEATHER_RAW",
            auto_create_table=False,
            overwrite=False,
        )

        if success:
            print(f"Successfully loaded {nrows} rows into WEATHER_RAW.")
            print(f"Chunks uploaded: {nchunks}")
        else:
            print("Data load failed.")

    finally:
        conn.close()


if __name__ == "__main__":
    load_to_snowflake()