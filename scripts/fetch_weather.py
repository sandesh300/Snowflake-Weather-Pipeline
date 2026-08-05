import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import pandas as pd
from datetime import datetime
from config.config import API_KEY, CITIES

def fetch_weather():
    all_records = []
    
    for city in CITIES:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()
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
            all_records.append(record)
            print(f"✅ Fetched data for {city}")
            
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP error for {city}: {e}")
        except KeyError as e:
            print(f"❌ Missing key in response for {city}: {e}")
        except Exception as e:
            print(f"❌ Unexpected error for {city}: {e}")
    
    if not all_records:
        raise RuntimeError("No weather data fetched for any city. Check API key or city names.")
    
    df = pd.DataFrame(all_records)
    
    # Create data folder if needed
    os.makedirs("data", exist_ok=True)
    
    # Save to CSV (overwrite with all cities)
    df.to_csv("data/weather_data.csv", index=False)
    print(f"\n✅ Saved weather data for {len(all_records)} cities at {datetime.now()}")

if __name__ == "__main__":
    fetch_weather()