import requests
from dotenv import load_dotenv
import os


def get_full_forecast(longitude, latitude, api_key):
    """
    Function to retrieve weather forecast from OpenWeatherMap Forecast API

    Args:
        longitude (float): longitude of a location (N | S)
        latitude (float): latitude of a location (E | W)
        api_key (string): OpenWeatherMap API key

    Returns:
        list: list containing all the forecast data
    """
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

        
def get_weather(api_key, longitude, latitude):
    """
    Function used to return date, wind_speed and rain reading to client

    Args:
        api_key (string): OpenWeatherMap API key
        longitude (float): longitude of a location (N | S)
        latitude (float): latitude of a location (E | W)

    Returns:
        date (string): "YYYY-MM-DD HH:MM:SS" format date string
        wind_speed (float): wind speed forecast in km/h
        rain (float): rain forecast in mm
    """
    full_forecast = get_full_forecast(longitude, latitude, api_key)
    
    if full_forecast is not None:
        # Get the forecast for the next 3 hours
        next_3_hours_forecast = full_forecast['list'][0]
        date = next_3_hours_forecast['dt_txt']
        wind_speed = next_3_hours_forecast['wind']['speed'] * 3.6 # Convert to km/h
        rain = next_3_hours_forecast.get('rain', {}).get('3h', 0)

        return date, wind_speed, rain
    else:
        return None, None, None
    

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("API_KEY")
    date, wind_speed, rain = get_weather(api_key, 18.647499, -33.832500)
    print(f"date: {date} ; date type {type(date)}")
    print(f"wind_speed: {wind_speed} ; wind type {type(wind_speed)}")
    print(f"rain: {rain} ; rain type {type(rain)}")
