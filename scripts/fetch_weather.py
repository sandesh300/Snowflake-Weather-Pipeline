import sys
import os
# Adds the project root folder to Python's module search path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import pandas as pd
from datetime import datetime
from config.config import API_KEY, CITY

def fetch_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    response.raise_for_status()   # raise exception for HTTP errors
    data = response.json()

    record = {
        "CITY": data["name"],
        "DATE": datetime.now().strftime("%Y-%m-%d"),
        "TIME": datetime.now().strftime("%H:%M:%S"),
        "TEMPERATURE": data["main"]["temp"],
        "HUMIDITY": data["main"]["humidity"],
        "PRESSURE": data["main"]["pressure"],
        "WIND_SPEED": data["wind"]["speed"],
        "WEATHER": data["weather"][0]["main"]
    }
    df = pd.DataFrame([record])
    
    # ✅ CREATE THE DATA DIRECTORY IF IT DOES NOT EXIST
    os.makedirs("data", exist_ok=True)
    
    df.to_csv("data/weather_data.csv", index=False)
    print(f"Weather data for {CITY} saved at {datetime.now()}")

if __name__ == "__main__":
    fetch_weather()