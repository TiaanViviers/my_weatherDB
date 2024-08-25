import checkers_DB, get_weather
import sqlite3
from dotenv import load_dotenv
import os


def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('../data/checkers_shops.db')              
    cursor = conn.cursor()
    
    # Set up database
    checkers_DB.run(cursor)
    
    # Get latest forecast readings
    update_readings(cursor, conn)
    

def update_readings(cursor, conn):
    # Loop through all shops in the shops table
    cursor.execute("SELECT id, latitude, longitude FROM shops")
    shops = cursor.fetchall()
    
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("API_KEY")

    for shop in shops:
        shop_id, lat, lon = shop
        
        # Fetch weather data for the shop's location
        weather_data = get_weather_data(lat, lon)
        
        # Determine if a warning should be triggered
        warning = 1 if weather_data['rain_forecast'] > 70 or weather_data['wind_forecast'] > 30 else 0
        
        # Insert or update the weather data in the weather_forecast table
        checkers_DB.insert_weather_data(cursor, shop_id, warning,
                                        weather_data['date'], 
                                        weather_data['rain_forecast'], 
                                        weather_data['wind_forecast'])

    # Commit the changes
    conn.commit()
    conn.close()
    


if __name__ == '__main__':
    main()