import requests

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 23.2599,
    "longitude": 77.4126,
    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
}

response = requests.get(url, params=params)

print("Status code:", response.status_code)

data = response.json()

print(data)