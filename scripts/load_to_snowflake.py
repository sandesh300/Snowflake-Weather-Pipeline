import sys
import os
# Adds the project root folder to Python's module search path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os
import snowflake.connector
from config.config import (
    SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD,
    SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA
)

def load_to_snowflake():
    # Connect to Snowflake
    conn = snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )
    cursor = conn.cursor()

    # 1. Upload CSV to stage using PUT
    csv_path = "data/weather_data.csv"
    put_cmd = f"PUT file://{os.path.abspath(csv_path)} @WEATHER_STAGE AUTO_COMPRESS=TRUE;"
    cursor.execute(put_cmd)
    print("CSV uploaded to stage.")

    # 2. Copy into raw table (only load if not already present, using a unique constraint)
    # We'll use a simple approach: load everything and rely on a unique key later.
    # For now, we'll load without duplicate check; we'll handle duplicates via task logic.
    copy_cmd = """
        COPY INTO WEATHER_RAW
        FROM @WEATHER_STAGE
        FILE_FORMAT = (FORMAT_NAME = CSV_FORMAT)
        ON_ERROR = 'SKIP_FILE';
    """
    cursor.execute(copy_cmd)
    print("Data loaded into WEATHER_RAW.")

    # 3. (Optional) Remove staged file to keep stage clean
    remove_cmd = "REMOVE @WEATHER_STAGE;"
    cursor.execute(remove_cmd)
    print("Stage cleaned.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    load_to_snowflake()