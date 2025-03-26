import requests
from datetime import datetime

class WeatherFetcher:
    def __init__(self):
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.api_key = None
        self.city = None

    def get_user_input(self):
        print("\n===== Weather Information Fetcher =====")
        self.api_key = input("Enter your OpenWeatherMap API key: ").strip()
        self.city = input("Enter city name (e.g., London, New York, Tokyo): ").strip()
        
        # Basic input validation
        if not self.api_key or not self.city:
            print("Error: Both API key and city name are required.")
            return False
        return True

    def fetch_weather(self):
        print(f"\nFetching weather data for {self.city}...")
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
        if not weather_data:
            return
        
        try:
            main_info = weather_data['main']
            weather_info = weather_data['weather'][0]
            wind_info = weather_data['wind']
            sys_info = weather_data['sys']
            
            location = f"{weather_data['name']}, {sys_info['country']}"
            print(f"\nWeather in {location}")
            print("-" * 30)
            print(f"Condition: {weather_info['description'].title()}")
            print(f"Temperature: {main_info['temp']}°C")
            print(f"Feels like: {main_info['feels_like']}°C")
            print(f"Humidity: {main_info['humidity']}%")
            print(f"Wind Speed: {wind_info['speed']} m/s")
            
        except KeyError as key_err:
            print(f"Error: Missing data in API response: {key_err}")

    def run(self):
        while True:
            if self.get_user_input():
                weather_data = self.fetch_weather()
                if weather_data:
                    self.display_weather(weather_data)
            
            # Ask to continue or exit
            if input("\nCheck another city? (y/n): ").lower() != 'y':
                print("Thank you for using the Weather Information Fetcher!")
                break


WeatherFetcher().run()
