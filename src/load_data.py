import requests
from database import get_connection


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


def collect_data():

    connection = get_connection()
    cursor = connection.cursor()

    for city, coordinates in cities.items():

        latitude, longitude = coordinates

        # -------------------------
        # AIR QUALITY API
        # -------------------------

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

        # -------------------------
        # WEATHER API
        # -------------------------

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

        if (
            air_response.status_code != 200
            or weather_response.status_code != 200
        ):
            print(f"{city}: API request failed")
            continue

        air_data = air_response.json()["current"]
        weather_data = weather_response.json()["current"]

        # -------------------------
        # GET CITY ID
        # -------------------------

        cursor.execute(
            """
            SELECT city_id
            FROM cities
            WHERE city_name = %s
            """,
            (city,)
        )

        result = cursor.fetchone()

        if result is None:
            print(f"{city}: city not found in database")
            continue

        city_id = result[0]

        # -------------------------
        # INSERT DATA
        # -------------------------

        insert_query = """
        INSERT INTO air_quality (
            city_id,
            timestamp,
            us_aqi,
            pm10,
            pm2_5,
            carbon_monoxide,
            nitrogen_dioxide,
            sulphur_dioxide,
            ozone,
            temperature,
            humidity,
            wind_speed,
            surface_pressure
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )

        ON CONFLICT (city_id, timestamp)
        DO UPDATE SET
        us_aqi = EXCLUDED.us_aqi,
        pm10 = EXCLUDED.pm10,
        pm2_5 = EXCLUDED.pm2_5,
        carbon_monoxide = EXCLUDED.carbon_monoxide,
        nitrogen_dioxide = EXCLUDED.nitrogen_dioxide,
        sulphur_dioxide = EXCLUDED.sulphur_dioxide,
        ozone = EXCLUDED.ozone,
        temperature = EXCLUDED.temperature,
        humidity = EXCLUDED.humidity,
        wind_speed = EXCLUDED.wind_speed,
        surface_pressure = EXCLUDED.surface_pressure;
        """

        values = (
            city_id,
            air_data["time"],
            air_data["us_aqi"],
            air_data["pm10"],
            air_data["pm2_5"],
            air_data["carbon_monoxide"],
            air_data["nitrogen_dioxide"],
            air_data["sulphur_dioxide"],
            air_data["ozone"],
            weather_data["temperature_2m"],
            weather_data["relative_humidity_2m"],
            weather_data["wind_speed_10m"],
            weather_data["surface_pressure"]
        )

        cursor.execute(
            insert_query,
            values
        )

        print(f"{city}: data inserted")

    connection.commit()

    cursor.close()
    connection.close()

    print("\nAll data inserted successfully!")


if __name__ == "__main__":
    collect_data()