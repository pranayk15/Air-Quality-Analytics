import requests
import pandas as pd


cities = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Bengaluru": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Hyderabad": (17.3850, 78.4867),
    "Pune": (18.5204, 73.8567),
    "Ahmedabad": (23.0225, 72.5714),
    "Bhopal": (23.2599, 77.4126),
    "Indore": (22.7196, 75.8577)
}


url = "https://air-quality-api.open-meteo.com/v1/air-quality"

records = []


for city, coordinates in cities.items():

    latitude, longitude = coordinates

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "pm10,"
            "pm2_5,"
            "carbon_monoxide,"
            "nitrogen_dioxide,"
            "sulphur_dioxide,"
            "ozone,"
            "us_aqi"
        ),
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:

        data = response.json()
        current = data["current"]

        record = {
            "city": city,
            "latitude": latitude,
            "longitude": longitude,
            "timestamp": current["time"],
            "us_aqi": current["us_aqi"],
            "pm10": current["pm10"],
            "pm2_5": current["pm2_5"],
            "carbon_monoxide": current["carbon_monoxide"],
            "nitrogen_dioxide": current["nitrogen_dioxide"],
            "sulphur_dioxide": current["sulphur_dioxide"],
            "ozone": current["ozone"]
        }

        records.append(record)

        print(f"{city}: Data collected successfully")

    else:

        print(
            f"{city}: API request failed "
            f"with status {response.status_code}"
        )


df = pd.DataFrame(records)


print("\nFinal Dataset:")
print(df)


df.to_csv(
    "data/air_quality.csv",
    index=False
)

print("\nData saved to data/air_quality.csv")