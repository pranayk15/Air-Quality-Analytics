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


AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def collect_data():

    print("Starting data collection...", flush=True)

    # -----------------------------------
    # Prepare coordinates
    # -----------------------------------

    city_names = list(cities.keys())

    latitudes = ",".join(
        str(cities[city][0])
        for city in city_names
    )

    longitudes = ",".join(
        str(cities[city][1])
        for city in city_names
    )

    # -----------------------------------
    # AIR QUALITY API
    # -----------------------------------

    print("Requesting air quality data...", flush=True)

    air_params = {
        "latitude": latitudes,
        "longitude": longitudes,
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
        AIR_QUALITY_URL,
        params=air_params,
        timeout=60
    )

    air_response.raise_for_status()

    air_results = air_response.json()

    print("Air quality data received.", flush=True)

    # -----------------------------------
    # WEATHER API
    # -----------------------------------

    print("Requesting weather data...", flush=True)

    weather_params = {
        "latitude": latitudes,
        "longitude": longitudes,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m,"
            "surface_pressure"
        ),
        "timezone": "Asia/Kolkata"
    }

    weather_response = requests.get(
        WEATHER_URL,
        params=weather_params,
        timeout=60
    )

    weather_response.raise_for_status()

    weather_results = weather_response.json()

    print("Weather data received.", flush=True)

    # -----------------------------------
    # DATABASE
    # -----------------------------------

    print("Connecting to database...", flush=True)

    connection = get_connection()
    cursor = connection.cursor()

    # -----------------------------------
    # PROCESS EACH CITY
    # -----------------------------------

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
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s
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
            surface_pressure = EXCLUDED.surface_pressure
    """

    try:

        for index, city in enumerate(city_names):

            print(
                f"Processing {city}...",
                flush=True
            )

            air_data = air_results[index]["current"]

            weather_data = weather_results[index]["current"]

            # Get city ID
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

                print(
                    f"{city}: city not found in database",
                    flush=True
                )

                continue

            city_id = result[0]

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

            print(
                f"{city}: inserted successfully",
                flush=True
            )

        connection.commit()

        print(
            "\nAll data committed successfully!",
            flush=True
        )

    except Exception:

        connection.rollback()

        raise

    finally:

        cursor.close()
        connection.close()


if __name__ == "__main__":
    collect_data()
