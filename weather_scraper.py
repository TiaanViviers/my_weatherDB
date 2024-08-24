"""
Weather scraper using OpenWeatherMap API key

Program takes longitude and latitude as command line input parameters
and produces temperature, wind, and rain metrics of the next 3 hours

to execute:
python3 weather_scraper.py <longitude> <latitude>

"""
import requests
import sys
from datetime import datetime


# Function to retrieve weather forecast from OpenWeatherMap Forecast API
def get_forecast(longitude, latitude, api_key):
    # Define the API endpoint
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    
    # Send a GET request to the API
    response = requests.get(url)
    
    if response.status_code == 200:
        forecast_data = response.json()
        return forecast_data
    else:
        print(f"Response Text: {response.text}")
        return None


# Function to extract and print forecast information
def print_forecast_info(forecast):
    if forecast:
        print("Weather forecast for the next 3 hours:")
        print()
        
        # Get the forecast for the next 3 hours (first entry)
        next_3_hours_forecast = forecast['list'][0]  # The first entry is the forecast for the next 3 hours
        
        # Wind data
        wind_speed = next_3_hours_forecast['wind']['speed']
        print(f"Wind Speed: {wind_speed} m/s")
        print()
        
        # Rain data
        rain_3h = next_3_hours_forecast.get('rain', {}).get('3h', 0)
        print(f"Rain Volume (next 3 hours): {rain_3h} mm")
        print()

        # General weather description
        weather_description = next_3_hours_forecast['weather'][0]['description']
        print(f"Weather Description: {weather_description}")

    else:
        print("Failed to retrieve forecast data")

def main():
    # Read command-line args for lon, lat
    if len(sys.argv) == 3:
        longitude = sys.argv[1]  # Example: 18.647499
        latitude = sys.argv[2]   # Example: -33.832500
    else:
        print("Please enter valid Longitude, Latitude arguments")
        sys.exit()

    api_key = "b21fc0b0e6006ec6b0c62372da738631"

    forecast = get_forecast(longitude, latitude, api_key)
    print_forecast_info(forecast)


if __name__ == "__main__":
    main()
