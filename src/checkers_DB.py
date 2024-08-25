import sqlite3
import csv


def create_tables(cursor):
    """
    Function to create the "shops" and "weather_forecast" Tables

    shops Table:
        stores the following variables of shops in the shops.csv file:
        id | store_name | province | latitude | longitude | address

    weather_forecast Table:
        store the following variables of each weather reading:
        id | shop_id | date | rain_forecast | wind_forecast | warning

    Args:
        cursor (sqlite3.Cursor): The cursor object used to execute SQL commands in the database.
    """
    # Create the shops table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS shops (
        id INTEGER PRIMARY KEY,
        store_name TEXT,
        province TEXT,
        latitude REAL,
        longitude REAL,
        address TEXT
    )
    ''')
    
    # Create the weather_forecast table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_forecast (
        id INTEGER PRIMARY KEY,
        shop_id INTEGER,
        date TEXT,
        rain_forecast REAL,
        wind_forecast REAL,
        warning BOOLEAN,
        FOREIGN KEY (shop_id) REFERENCES shops(id)
    )
    ''')
    return


def load_csv(csv_file):
    """
    Simple function to read csv file into a list

    Args:
        csv_file (string): Path to csv file.

    Returns:
        list: list containing all the shops and the information
                of each shop observation
    """
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)
    

def insert_shop_data(cursor, shop_data):
    """
    Function to add new additions in the shops.csv file to the "shops" Table

    Itterates through shop_data array to check if there are any shops
    that are not in the table already.
    If new shop is found, a new observation in the "shops" Table is created

    Args:
        cursor (sqlite3.Cursor): The cursor object used to execute SQL commands in the database.
        shop_data (list): list containing all the shops and the information
                of each shop observation
    """
    for shop in shop_data:
        # Check if the shop already exists (based on name and coordinates)
        cursor.execute('''
        SELECT * FROM shops WHERE store_name = ? AND latitude = ? AND longitude = ?
        ''', (shop['store_name'], shop['latitude'], shop['longitude']))

        if cursor.fetchone() is None:
            # Insert new shop
            cursor.execute('''
            INSERT INTO shops (store_name, province, latitude, longitude, address)
            VALUES (?, ?, ?, ?, ?)
            ''', (shop['store_name'], shop['province'], shop['latitude'], shop['longitude'],
                  shop['address']))
            print(f"Added new shop: {shop['store_name']}")
    
    return


def insert_weather_data(cursor, shop_id, warning, date, rain_forecast, wind_forecast):
    """
    Inserts a weather reading into the "weather_forecast" table in the SQLite database.

    Args:
        cursor (sqlite3.Cursor): The cursor object used to execute SQL commands in the database.
        shop_id (int): The ID of the shop for which the weather forecast is being recorded. 
                       This ID should correspond to an entry in the "shops" table.
        warning (bool): A boolean value (0 or 1) indicating whether a warning should be triggered
                        based on the weather conditions.
        date (str): The date for which the weather forecast is relevant,
                    in "YYYY-MM-DD HH:MM:SS" format.
        rain_forecast (float): The amount of rain forecasted for the next 3 hours in mm.
        wind_forecast (float): The wind speed forecasted for the next 3 hours in km/h. 
    """
    cursor.execute('''
        INSERT INTO weather_forecast (shop_id, date, rain_forecast, wind_forecast, warning)
        VALUES (?, ?, ?, ?, ?)
    ''', (shop_id, date, rain_forecast, wind_forecast, warning))


def display_table(cursor, table_name):
    """
    Function to print Tables.

    For debugging and visualisation purposes.

    Args:
        cursor (sqlite3.Cursor): The cursor object used to execute SQL commands in the database.
        table_name (string): Name of the table you want to print
    """
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()

    if rows:
        # Print the table headers
        print(f"\n--- {table_name.upper()} TABLE ---")
        for column in cursor.description:
            print(f"{column[0]:<15}", end="")
        print()

        # Print each row
        for row in rows:
            for value in row:
                print(f"{str(value):<15}", end="")
            print()
    else:
        print(f"\nNo data found in {table_name}.")

    return


def run(cursor):
    """
    Main Function to connect, set up and populate the Database.

    Creates the shops and weather_forecast tables
    Reads the shop locations from csv file and adds it to the shops table
    Optionally display the tables
    
    Args:
        cursor (sqlite3.Cursor): The cursor object used to execute SQL commands in the database.
    """
    
    create_tables(cursor)                        # Create tables
    shop_data = load_csv('../data/shops.csv')    # Load shop data from the CSV file
    insert_shop_data(cursor, shop_data)          # Insert shop data into the database

    # Visualize tables
    #display_table(cursor, "shops")
    #display_table(cursor, "weather_forecast")
    
    
if __name__ == '__main__':
    run()