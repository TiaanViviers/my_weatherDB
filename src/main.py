import checkers_DB, weather
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
    
    
    
# Loop through all shops in the shops table
def update_readings(cursor, conn):
    """
    Function for updating the weather_forecast table using the weather API
    
    Args:
        cursor (sqlite3.Cursor): The cursor object used to execute SQL commands in the database.
        conn (sqlite3.connect): Connection to the sqlite3 Database
    """
    # Load environment variables from .env file
    load_dotenv()  
    api_key = os.getenv("API_KEY")
    
    
    cursor.execute("SELECT id, latitude, longitude FROM shops")
    shops = cursor.fetchall()
    

    for shop in shops:
        shop_id, lat, lon = shop
        
        # Fetch weather data for the shop's location
        date, wind_speed, rain = weather.get_weather(api_key, lon, lat)
        
        # Determine if a warning should be triggered
        if (rain > 0) or (wind_speed > 35):
            warning = 1
        else: warning = 0
        
        # Insert or update the weather data in the weather_forecast table
        checkers_DB.insert_weather_data(cursor, shop_id, warning, date, rain, wind_speed)

    checkers_DB.display_table(cursor, "weather_forecast")
    conn.commit()
    conn.close()
    


if __name__ == '__main__':
    main()