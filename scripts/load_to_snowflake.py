import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import snowflake.connector
from config.config import (
    SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD,
    SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA
)

def load_to_snowflake():
    # 1. Connect to Snowflake
    conn = snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )
    cursor = conn.cursor()

    # 2. Absolute path to CSV
    csv_path = os.path.abspath("data/weather_data.csv")
    print(f"Uploading {csv_path} to stage...")

    # 3. PUT command – upload to internal stage
    put_cmd = f"PUT file://{csv_path} @WEATHER_STAGE AUTO_COMPRESS=TRUE;"
    cursor.execute(put_cmd)
    print("✅ CSV uploaded to stage.")

    # 4. COPY INTO – load into raw table
    copy_cmd = """
        COPY INTO WEATHER_RAW
        FROM @WEATHER_STAGE
        FILE_FORMAT = (FORMAT_NAME = CSV_FORMAT)
        ON_ERROR = 'SKIP_FILE';
    """
    cursor.execute(copy_cmd)
    print("✅ Data loaded into WEATHER_RAW.")

    # 5. Clean up stage (optional)
    remove_cmd = "REMOVE @WEATHER_STAGE;"
    cursor.execute(remove_cmd)
    print("🧹 Stage cleaned.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    load_to_snowflake()