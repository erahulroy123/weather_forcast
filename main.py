#api key = a612116ff3018aa4cae2884314f84e49

import requests

class WeatherFetcher:
    def __init__(self, api_key, city):
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.api_key = api_key
        self.city = city

    def fetch_weather(self):
        params = {
            'q': self.city,
            'appid': self.api_key,
            'units': 'metric'
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                print(f"Error: City '{self.city}' not found.")
            elif response.status_code == 401:
                print("Error: Invalid API key.")
            else:
                print(f"HTTP error: {http_err}")
        except requests.exceptions.ConnectionError:
            print("Error: Connection failed. Check your internet.")
        except Exception as err:
            print(f"Unexpected error: {err}")
        return None

    def display_weather(self, weather_data):
        try:
            main_info = weather_data['main']
            weather_info = weather_data['weather'][0]
            city_name = weather_data['name']
            
            print(f"Weather in {city_name}")
            print(f"Condition: {weather_info['description']}")
            print(f"Temperature: {main_info['temp']}°C")
        except KeyError as key_err:
            print(f"Error: Missing data in API response: {key_err}")

    def run(self):
        weather_data = self.fetch_weather()
        if weather_data:
            self.display_weather(weather_data)

api_key = input("Enter your OpenWeatherMap API key: ").strip()
city = input("Enter city name (e.g., London, New York, Tokyo): ").strip()

if api_key and city:
    WeatherFetcher(api_key, city).run()
else:
    print("Error: Both API key and city name are required.")
