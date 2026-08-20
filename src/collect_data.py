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


air_quality_url = "https://air-quality-api.open-meteo.com/v1/air-quality"

weather_url = "https://api.open-meteo.com/v1/forecast"

records = []


for city, coordinates in cities.items():

    latitude, longitude = coordinates

    # -----------------------------
    # AIR QUALITY
    # -----------------------------

    air_params = {
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

    air_response = requests.get(
        air_quality_url,
        params=air_params
    )

    # -----------------------------
    # WEATHER
    # -----------------------------

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m,"
            "surface_pressure"
        ),
        "timezone": "Asia/Kolkata"
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params
    )

    # -----------------------------
    # CHECK API RESPONSES
    # -----------------------------

    if (
        air_response.status_code == 200
        and weather_response.status_code == 200
    ):

        air_data = air_response.json()["current"]
        weather_data = weather_response.json()["current"]

        record = {
            "city": city,
            "latitude": latitude,
            "longitude": longitude,

            "timestamp": air_data["time"],

            # Air quality
            "us_aqi": air_data["us_aqi"],
            "pm10": air_data["pm10"],
            "pm2_5": air_data["pm2_5"],
            "carbon_monoxide": air_data["carbon_monoxide"],
            "nitrogen_dioxide": air_data["nitrogen_dioxide"],
            "sulphur_dioxide": air_data["sulphur_dioxide"],
            "ozone": air_data["ozone"],

            # Weather
            "temperature": weather_data["temperature_2m"],
            "humidity": weather_data["relative_humidity_2m"],
            "wind_speed": weather_data["wind_speed_10m"],
            "surface_pressure": weather_data["surface_pressure"]
        }

        records.append(record)

        print(f"{city}: data collected")

    else:

        print(
            f"{city}: API request failed"
        )


# -----------------------------
# CREATE DATAFRAME
# -----------------------------

df = pd.DataFrame(records)


# -----------------------------
# DISPLAY DATA
# -----------------------------

print("\nCombined Dataset:")
print(df)


# -----------------------------
# SAVE DATA
# -----------------------------

df.to_csv(
    "data/air_quality_weather.csv",
    index=False
)

print(
    "\nData saved to "
    "data/air_quality_weather.csv"
)