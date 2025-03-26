import requests
import json
from datetime import datetime
import os
import sys


class WeatherFetcher:

    def __init__(self):
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.api_key = None
        self.city = None

    def get_user_input(self):
        print("\n===== Weather Information Fetcher =====\n")
        # Check if API key is stored in environment variable
        env_api_key = os.environ.get('OPENWEATHER_API_KEY')
        if env_api_key:
            use_env = input(f"API key found in environment variable. Use it? (y/n): ").lower()
            if use_env == 'y':
                self.api_key = env_api_key
            else:
                self.api_key = input("Enter your OpenWeatherMap API key: ").strip()
        else:
            self.api_key = input("Enter your OpenWeatherMap API key: ").strip()
            # Ask if user wants to save API key for future use
            save_key = input("Save API key for future use? (y/n): ").lower()
            if save_key == 'y':
                print("To save your API key, set the environment variable OPENWEATHER_API_KEY")
                if os.name == 'posix':  # Linux/Mac
                    print("  echo 'export OPENWEATHER_API_KEY=\"your-api-key\"' >> ~/.bashrc")
                elif os.name == 'nt':  # Windows
                    print("  setx OPENWEATHER_API_KEY \"your-api-key\"")
        # Get city name
        self.city = input("\nEnter city name (e.g., London, New York, Tokyo): ").strip()
        # Validate inputs
        if not self.api_key:
            print("Error: API key is required.")
            return False
        if not self.city:
            print("Error: City name is required.")
            return False
        return True

    def fetch_weather(self):
        print(f"\nFetching weather data for {self.city}...")
        # Parameters for the API request
        params = {
            'q': self.city,
            'appid': self.api_key,
            'units': 'metric'  # Use metric units for temperature in Celsius
        }
        try:
            # Make the API request
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            # Parse JSON response
            weather_data = response.json()
            print("Weather data retrieved successfully!\n")
            return weather_data
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                print(f"Error: City '{self.city}' not found. Please check the spelling and try again.")
            elif response.status_code == 401:
                print("Error: Invalid API key. Please check your API key and try again.")
            else:
                print(f"Error: HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError:
            print("Error: Connection error. Please check your internet connection.")
        except Exception as err:
            print(f"Error: An unexpected error occurred: {err}")
        return None

    def display_weather(self, weather_data):
        if not weather_data:
            return
        try:
            # Extract main weather information
            main_info = weather_data['main']
            weather_info = weather_data['weather'][0]
            wind_info = weather_data['wind']
            sys_info = weather_data['sys']
            # Format location information
            location = f"{weather_data['name']}, {sys_info['country']}"
            # Convert timestamps to readable format
            sunrise_time = datetime.fromtimestamp(sys_info['sunrise']).strftime('%H:%M:%S')
            sunset_time = datetime.fromtimestamp(sys_info['sunset']).strftime('%H:%M:%S')
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Create border with location name
            border = "=" * (len(location) + 12)
            # Display weather information
            print(border)
            print(f"== Weather in {location} ==")
            print(border + "\n")
            print(f"Weather Condition: {weather_info['description'].title()}")
            print(f"Temperature: {main_info['temp']}°C (Feels like: {main_info['feels_like']}°C)")
            print(f"Min Temperature: {main_info['temp_min']}°C")
            print(f"Max Temperature: {main_info['temp_max']}°C")
            print(f"Humidity: {main_info['humidity']}%")
            print(f"Pressure: {main_info['pressure']} hPa")
            print(f"Wind Speed: {wind_info['speed']} m/s")
            print(f"Wind Direction: {wind_info.get('deg', 'N/A')}°")
            print(f"Sunrise: {sunrise_time}")
            print(f"Sunset: {sunset_time}")
            print(f"\nLast Updated: {current_time}")
            # Save data to file option
            save_option = input("\nWould you like to save this weather data to a file? (y/n): ").lower()
            if save_option == 'y':
                self.save_weather_data(weather_data)
        except KeyError as key_err:
            print(f"Error: Missing data in API response: {key_err}")
        except Exception as err:
            print(f"Error displaying weather data: {err}")

    def save_weather_data(self, weather_data):
        try:
            filename = f"weather_{weather_data['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(weather_data, f, indent=2)
            print(f"Weather data saved to {filename}")
        except Exception as err:
            print(f"Error saving weather data: {err}")

    def run(self):
        if self.get_user_input():
            weather_data = self.fetch_weather()
            if weather_data:
                self.display_weather(weather_data)
                # Ask if user wants to check another city
                check_another = input("\nWould you like to check weather for another city? (y/n): ").lower()
                if check_another == 'y':
                    self.run()
                else:
                    print("Thank you for using the Weather Information Fetcher!")
            else:
                retry = input("\nWould you like to try again? (y/n): ").lower()
                if retry == 'y':
                    self.run()
                else:
                    print("Exiting Weather Information Fetcher.")
                    
weather_fetcher = WeatherFetcher()
weather_fetcher.run()
