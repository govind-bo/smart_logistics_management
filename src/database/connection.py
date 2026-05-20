import mysql.connector
from mysql.connector import Error
from config.db_config import DB_CONFIG

def get_connection():
    '''
    This function connects to the MySQL database, if connection fails it prints the error
    '''
    try:
        conn = mysql.connector.connect(**DB_CONFIG)

        if conn.is_connected():
            print("Database connection successful")
            return conn
        return None
    except Error as e:
        print(f'Database connection failed : {e}')
        return None