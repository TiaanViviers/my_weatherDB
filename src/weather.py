"""
Weather scraper using OpenWeatherMap API key

Program takes longitude and latitude as command line input parameters
and produces temperature, wind, and rain metrics of the next 3 hours

to execute:
python3 weather_scraper.py <longitude> <latitude>

"""
import requests
import sys
from dotenv import load_dotenv
import os


# Function to retrieve weather forecast from OpenWeatherMap Forecast API
def get_full_forecast(longitude, latitude, api_key):
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
        
        
def get_weather(api_key, longitude, latitude):
    full_forecast = get_full_forecast(longitude, latitude, api_key)
    
    if full_forecast is not None:
        # Get the forecast for the next 3 hours
        next_3_hours_forecast = full_forecast['list'][0]
        date = next_3_hours_forecast['dt_txt']  # "YYYY-MM-DD HH:MM:SS" format
        wind_speed = next_3_hours_forecast['wind']['speed']
        rain = next_3_hours_forecast.get('rain', {}).get('3h', 0)

        return date, wind_speed, rain
    else:
        return None, None, None
    
    
    

def main():

    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("API_KEY")
    
    date, wind_speed, rain = get_full_forecast(api_key, 18.647499, -33.832500)
    

    #forecast = get_full_forecast(longitude, latitude, api_key)
    #print_forecast_info(forecast)


if __name__ == "__main__":
    main()
