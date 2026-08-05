import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from config.config import (
    SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD,
    SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA
)

def load_to_snowflake():
    # 1. Read the CSV with all cities
    df = pd.read_csv("data/weather_data.csv")
    print(f"Read {len(df)} rows from CSV.")

    # 2. Connect to Snowflake
    conn = snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )

    # 3. Append directly to the table
    success, nrows, ncols = write_pandas(
        conn,
        df,
        table_name="WEATHER_RAW",
        quote_identifiers=False
    )

    if success:
        print(f"✅ Successfully inserted {nrows} rows into WEATHER_RAW.")
    else:
        print("❌ Failed to write to Snowflake.")

    conn.close()

if __name__ == "__main__":
    load_to_snowflake()