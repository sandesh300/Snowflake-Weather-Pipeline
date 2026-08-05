import streamlit as st
import pandas as pd
import plotly.express as px
import snowflake.connector
from datetime import datetime, timedelta

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="🌦️ Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

st.title("🌦️ Live Multi-City Weather Dashboard")
st.markdown("Data updated hourly from OpenWeatherMap via automated pipeline")

# ---------- SNOWFLAKE CONNECTION (cached) ----------
@st.cache_resource
def get_snowflake_connection():
    # For Streamlit Cloud, use st.secrets
    # For local testing, falls back to environment variables
    try:
        # Streamlit Cloud secrets
        conn = snowflake.connector.connect(
            account=st.secrets["SNOWFLAKE_ACCOUNT"],
            user=st.secrets["SNOWFLAKE_USER"],
            password=st.secrets["SNOWFLAKE_PASSWORD"],
            warehouse=st.secrets["SNOWFLAKE_WAREHOUSE"],
            database=st.secrets["SNOWFLAKE_DATABASE"],
            schema=st.secrets["SNOWFLAKE_SCHEMA"]
        )
        return conn
    except:
        # Fallback for local .env testing
        import os
        from dotenv import load_dotenv
        load_dotenv()
        return snowflake.connector.connect(
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA")
        )

# ---------- LOAD DATA (cached) ----------
@st.cache_data(ttl=300)  # cache for 5 minutes
def load_data():
    conn = get_snowflake_connection()
    
    query = """
    SELECT 
        CITY,
        DATE,
        TIME,
        TEMPERATURE,
        HUMIDITY,
        PRESSURE,
        WIND_SPEED,
        WEATHER,
        TEMP_STATUS
    FROM WEATHER_CLEAN
    WHERE DATE >= DATEADD(day, -7, CURRENT_DATE())  -- Last 7 days
    ORDER BY DATE DESC, TIME DESC
    """
    
    df = pd.read_sql(query, conn)
    conn.close()
    
    # Convert DATE to datetime for plotting
    df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str) + ' ' + df['TIME'])
    
    return df

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("🔍 Filters")

df = load_data()

if df.empty:
    st.warning("⚠️ No data found in WEATHER_CLEAN. Please run your pipeline first.")
    st.stop()

# City multiselect
cities = df['CITY'].unique().tolist()
selected_cities = st.sidebar.multiselect(
    "Select Cities",
    cities,
    default=cities[:3]  # select first 3 by default
)

# Date range
min_date = df['DATE'].min()
max_date = df['DATE'].max()
date_range = st.sidebar.date_input(
    "Date Range",
    [min_date, max_date],   
    min_value=min_date,
    max_value=max_date
)


# Filter data
filtered_df = df[df['CITY'].isin(selected_cities)]
if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df['DATE'] >= date_range[0]) &
        (filtered_df['DATE'] <= date_range[1])
    ]

# ---------- MAIN DASHBOARD ----------
if filtered_df.empty:
    st.warning("No data matches your filters. Try adjusting the selection.")
    st.stop()

# ---- KPI ROW ----
latest_df = filtered_df.sort_values('DATETIME', ascending=False).drop_duplicates('CITY')

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_temp = filtered_df['TEMPERATURE'].mean()
    st.metric("🌡️ Avg Temperature", f"{avg_temp:.1f}°C")

with col2:
    avg_humidity = filtered_df['HUMIDITY'].mean()
    st.metric("💧 Avg Humidity", f"{avg_humidity:.0f}%")

with col3:
    latest_temp = latest_df['TEMPERATURE'].mean()
    st.metric("🔴 Latest Avg Temp", f"{latest_temp:.1f}°C")

with col4:
    city_count = filtered_df['CITY'].nunique()
    st.metric("🏙️ Cities", city_count)

# ---- TEMPERATURE TREND ----
st.subheader("🌡️ Temperature Trend by City")

fig_temp = px.line(
    filtered_df,
    x='DATETIME',
    y='TEMPERATURE',
    color='CITY',
    title='Temperature Over Time',
    markers=True
)
fig_temp.update_layout(height=400)
st.plotly_chart(fig_temp, use_container_width=True)

# ---- TWO-COLUMN LAYOUT ----
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("💧 Humidity & Pressure")
    
    fig_humidity = px.scatter(
        filtered_df,
        x='DATETIME',
        y='HUMIDITY',
        color='CITY',
        title='Humidity Trend',
        size='PRESSURE',
        hover_data=['WEATHER']
    )
    fig_humidity.update_layout(height=350)
    st.plotly_chart(fig_humidity, use_container_width=True)

with col_right:
    st.subheader("☁️ Weather Condition Breakdown")
    
    weather_counts = filtered_df.groupby(['CITY', 'WEATHER']).size().reset_index(name='COUNT')
    fig_pie = px.pie(
        weather_counts,
        values='COUNT',
        names='WEATHER',
        facet_col='CITY',
        title='Weather Distribution by City',
        hole=0.3
    )
    fig_pie.update_layout(height=350)
    st.plotly_chart(fig_pie, use_container_width=True)

# ---- DATA TABLE ----
st.subheader("📊 Recent Weather Data")
st.dataframe(
    filtered_df[['CITY', 'DATE', 'TIME', 'TEMPERATURE', 'HUMIDITY', 'WEATHER', 'TEMP_STATUS']],
    use_container_width=True,
    hide_index=True
)

# ---- FOOTER ----
st.markdown("---")
st.caption(f"Data refreshed from Snowflake. Pipeline runs hourly via GitHub Actions. Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")