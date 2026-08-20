import requests
import pandas as pd
from datetime import datetime

# Bhopal coordinates
city = "Bhopal"
latitude = 23.2599
longitude = 77.4126

url = "https://air-quality-api.open-meteo.com/v1/air-quality"

params = {
    "latitude": latitude,
    "longitude": longitude,
    "current": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone"
}

response = requests.get(url, params=params)

if response.status_code == 200:

    data = response.json()

    current = data["current"]

    record = {
        "city": city,
        "timestamp": current["time"],
        "pm10": current["pm10"],
        "pm2_5": current["pm2_5"],
        "carbon_monoxide": current["carbon_monoxide"],
        "nitrogen_dioxide": current["nitrogen_dioxide"],
        "sulphur_dioxide": current["sulphur_dioxide"],
        "ozone": current["ozone"]
    }

    df = pd.DataFrame([record])

    print("\nAir Quality Data:")
    print(df)

else:
    print("API request failed")
    print("Status code:", response.status_code)

df.to_csv("data/air_quality.csv", index=False)

print("\nData saved successfully.")