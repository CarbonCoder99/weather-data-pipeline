import requests
import json
import os
import time
from datetime import datetime
import pandas as pd

# CONFIGURATION
#OpenWeatherMap API key
API_KEY = "b26f75bdebdc6d8d6f1246b772464fa0" 

# List of 5 cities you want to track
CITIES = ["Lagos", "London", "New York", "Tokyo", "Nairobi"]

def fetch_weather_data(city_name):
    # We update the URL dynamically for each city
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        weather_summary = {
            "city": data.get("name"),
            "temp_celsius": data["main"].get("temp"),
            "humidity": data["main"].get("humidity"),
            "description": data["weather"][0].get("description"),
            "timestamp": datetime.now().isoformat()
        }
        return weather_summary

    except Exception as err:
        print(f"Error fetching {city_name}: {err}")
        return None




if __name__ == "__main__":
    all_weather_data = []

    print(f"--- Starting Daily Extraction: {datetime.now()} ---")

    for city in CITIES:
        result = fetch_weather_data(city)
        if result:
            all_weather_data.append(result)
            print(f"Successfully fetched: {city}")
        time.sleep(1)

    # --- PARQUET STORAGE CODE ---
    # 1. Create a timestamp string (Year-Month-Day_Hour-Minute)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    # 2. Create a dynamic filename using an "f-string"
    # Create a 'data' directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    file_in_json = f"weather_data_{timestamp}.json"
    filename_parquet = f"data/weather_data_{timestamp}.parquet"

    # 3. Convert to DataFrame and save
    with open(file_in_json, "w") as f:
        json.dump(all_weather_data, f, indent=4)
    
    df = pd.DataFrame(all_weather_data)
    df.to_parquet(filename_parquet, engine='pyarrow', index=False)

    print(f"--- Successfully saved to: {filename_parquet} ---")


    def quality_check(df):
        if df.empty:
            print("CRITICAL: Dataframe is empty!")
            return False
        if df['temp_celsius'].isnull().any():
            print("WARNING: Found missing temperatures!")
        print(f"Quality Check Passed: {len(df)} records verified.")
        return True
    
    def validate_data(file_path):
        df = pd.read_parquet(file_path)
        
        # 1. Check if we have all 5 cities
        city_count = df['city'].nunique()
        
        # 2. Check for missing values
        missing_temps = df['temp'].isnull().sum()
        
        if city_count == 5 and missing_temps == 0:
            print("✅ DATA QUALITY PASS: All cities present, no missing data.")
        else:
            print(f"❌ DATA QUALITY FAIL: Cities: {city_count}/5, Missing: {missing_temps}")
    
    # Run the check after saving
    validate_data(filename_parquet)
    
    
    
    # --- DATABASE SYNC SECTION ---
    print("--- Starting Database Sync Check ---")
    DB_URL = os.getenv('SUPABASE_DB_URL')
    
    if DB_URL:
        print("✅ Found Database URL, attempting to connect...")
        try:
            engine = create_engine(DB_URL)
            df.to_sql('weather_history', engine, if_exists='append', index=False)
            print("🚀 DATABASE SUCCESS: Data pushed to Supabase!")
        except Exception as e:
            print(f"❌ DATABASE ERROR: {e}")
    else:
        print("⚠️ DATABASE SKIPPED: The environment variable SUPABASE_DB_URL is empty or missing.")
    
    print(f"--- Pipeline Finished: {datetime.now()} ---")    # --- END OF PIPELINE ---
