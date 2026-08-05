
# 🌦️ Live Weather Data Pipeline

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Snowflake](https://img.shields.io/badge/Snowflake-Data%20Cloud-56B9EB)](https://www.snowflake.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B)](https://streamlit.io/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-2088FF)](https://github.com/features/actions)

## 📌 Overview

A **production-grade data engineering pipeline** that fetches real-time weather data from the OpenWeatherMap API, loads it into Snowflake, and visualizes it through an interactive Streamlit dashboard. The entire pipeline is automated using GitHub Actions, making it a complete end-to-end data solution.

### 🎯 Key Features

- **Automated Data Ingestion**: Fetches weather data hourly for multiple cities
- **Cloud Data Warehouse**: Snowflake for scalable storage and analytics
- **Incremental Loading**: Streams + Tasks for automatic data transformation
- **Interactive Dashboard**: Real-time visualizations with Streamlit
- **CI/CD Pipeline**: GitHub Actions for scheduled execution
- **Production-Ready**: Error handling, logging, and secure secret management

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     OpenWeatherMap API                          │
│                        (Free Tier)                              │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│              GitHub Actions (Scheduled Hourly)                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  fetch_weather.py        load_to_snowflake.py           │    │
│  │  - HTTP Request          - Upload CSV to Stage          │    │
│  │  - Parse JSON            - COPY INTO Table              │    │
│  │  - Save to CSV           - Stage Cleanup                │    │
│  └─────────────────────────────────────────────────────────┘    │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Snowflake Data Cloud                       │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ WEATHER_RAW  │───▶│  WEATHER_    │───▶│   Analytics │       │
│  │   (Staging)  │    │   CLEAN      │    │   Views      │       │
│  └──────────────┘    │(Transformed) │    └──────────────┘       │
│                      └──────────────┘                           │
│                           ▲                                     │
│                           │                                     │
│                     ┌──────────────┐                            │
│                     │   STREAMS    │                            │
│                     │  + TASKS     │                            │
│                     └──────────────┘                            │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│              Streamlit Dashboard (Live Visualization)           │
│  - Temperature Trends         - Weather Distribution            │
│  - Humidity & Pressure        - City Filters                    │
│  - KPI Metrics                - Data Table                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technologies Used

| Category | Technology |
|----------|------------|
| **Orchestration** | GitHub Actions |
| **Data Extraction** | Python, Requests, Pandas |
| **Data Warehouse** | Snowflake (Cloud Data Platform) |
| **Data Transformation** | SQL (Streams, Tasks, Views) |
| **Visualization** | Streamlit, Plotly |
| **Version Control** | Git, GitHub |
| **Secret Management** | Environment Variables, GitHub Secrets, Streamlit Secrets |

---

## 📁 Project Structure

```
snowflake-weather-pipeline/
│
├── .github/
│   └── workflows/
│       └── weather_pipeline.yml    # GitHub Actions workflow
│
├── .streamlit/
│   └── secrets.toml                # Streamlit secrets (local)
│
├── config/
│   └── config.py                   # Configuration loader
│
├── data/
│   └── weather_data.csv            # Temporary CSV (auto-generated)
│
├── scripts/
│   ├── fetch_weather.py            # Fetch data from OpenWeatherMap
│   └── load_to_snowflake.py        # Load data into Snowflake
│
├── sql/
│   ├── 01_create_objects.sql       # Warehouse, DB, Tables, Stage
│   ├── 02_transform.sql            # Create WEATHER_CLEAN table
│   ├── 03_views.sql                # Analytics views
│   └── 04_stream_task.sql          # Streams and Tasks
│
├── app.py                          # Streamlit dashboard
├── requirements.txt                # Python dependencies
├── .env                            # Local environment variables
├── .gitignore                      # Git ignore file
└── README.md                       # Project documentation
```

---

## 🚀 Quick Start

### Prerequisites

1. **OpenWeatherMap API Key** - [Get free API key](https://openweathermap.org/api)
2. **Snowflake Account** - [Free trial](https://signup.snowflake.com/)
3. **Python 3.10+** installed locally

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/snowflake-weather-pipeline.git
   cd snowflake-weather-pipeline
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials:
   # OPENWEATHER_API_KEY=your_key
   # CITIES=Pune,Mumbai,Delhi
   # SNOWFLAKE_ACCOUNT=your_account
   # SNOWFLAKE_USER=your_username
   # SNOWFLAKE_PASSWORD=your_password
   ```

5. **Set up Snowflake objects**
   ```sql
   -- Run SQL files in Snowflake in this order:
   sql/01_create_objects.sql
   sql/02_transform.sql
   sql/03_views.sql
   sql/04_stream_task.sql
   ```

6. **Run the pipeline locally**
   ```bash
   python scripts/fetch_weather.py
   python scripts/load_to_snowflake.py
   ```

7. **Launch the dashboard**
   ```bash
   streamlit run app.py
   ```

---

## ☁️ Deployment

### Deploy on GitHub Actions (Automated Pipeline)

1. Push code to GitHub repository
2. Add required secrets in repo → Settings → Secrets and variables → Actions:
   - `OPENWEATHER_API_KEY`
   - `CITIES`
   - `SNOWFLAKE_ACCOUNT`
   - `SNOWFLAKE_USER`
   - `SNOWFLAKE_PASSWORD`
   - `SNOWFLAKE_WAREHOUSE`
   - `SNOWFLAKE_DATABASE`
   - `SNOWFLAKE_SCHEMA`
3. The workflow will automatically run every hour

### Deploy on Streamlit Cloud (Dashboard)

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app" and connect your GitHub repository
3. Set main file path: `app.py`
4. Add Streamlit secrets (same Snowflake credentials)
5. Deploy and get your public URL

---

## 📊 Dashboard Features

- **Real-time KPIs**: Average temperature, humidity, latest readings
- **Interactive Filters**: Select cities and date ranges
- **Temperature Trends**: Line charts by city with hover details
- **Weather Distribution**: Pie charts showing weather conditions
- **Humidity & Pressure**: Scatter plots with sizing
- **Data Table**: Sortable, filterable recent weather data

---

## 🔄 Data Pipeline Workflow

1. **GitHub Actions** triggers every hour (or manually)
2. **fetch_weather.py** calls OpenWeatherMap API for all cities
3. Data is saved as CSV with timestamp
4. **load_to_snowflake.py** uploads CSV to Snowflake stage
5. `COPY INTO` loads data into `WEATHER_RAW` table
6. **Snowflake Stream** captures new rows
7. **Snowflake Task** (hourly) transforms and inserts into `WEATHER_CLEAN`
8. **Streamlit Dashboard** reads from `WEATHER_CLEAN` for live visualization

---

## 📈 Sample Queries

```sql
-- Check latest weather for each city
SELECT CITY, DATE, TIME, TEMPERATURE, WEATHER 
FROM WEATHER_CLEAN 
QUALIFY ROW_NUMBER() OVER (PARTITION BY CITY ORDER BY DATE DESC, TIME DESC) = 1;

-- Average temperature by city for last 7 days
SELECT CITY, AVG(TEMPERATURE) AS AVG_TEMP
FROM WEATHER_CLEAN
WHERE DATE >= DATEADD(day, -7, CURRENT_DATE())
GROUP BY CITY;

-- Weather condition frequency
SELECT WEATHER, COUNT(*) AS COUNT
FROM WEATHER_CLEAN
GROUP BY WEATHER
ORDER BY COUNT DESC;
```

---

## 🎓 Learning Outcomes

This project demonstrates:

- ✅ **Data Engineering**: Building end-to-end ETL pipelines
- ✅ **Cloud Computing**: Working with Snowflake (Data Cloud)
- ✅ **API Integration**: Extracting data from REST APIs
- ✅ **Orchestration**: Scheduling with GitHub Actions (CI/CD)
- ✅ **Data Visualization**: Building interactive dashboards
- ✅ **Python**: Requests, Pandas, Snowflake connector
- ✅ **SQL**: Complex queries, streams, tasks, views
- ✅ **Best Practices**: Error handling, secret management, version control

---

## 🔮 Future Enhancements

- [ ] Add data quality checks and validation
- [ ] Implement dbt for transformation layer
- [ ] Add alerting (Slack/Email for failures)
- [ ] Historical weather data analysis (ML predictions)
- [ ] Power BI integration
- [ ] Multiple data sources (weather + air quality)
- [ ] Dockerize the application

---


