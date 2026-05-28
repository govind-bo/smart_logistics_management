'''
import mysql.connector
from mysql.connector import Error
from config.db_config import DB_CONFIG

def get_connection():
    '''
    # This function connects to the MySQL database, if connection fails it prints the error
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
'''

from sqlalchemy import create_engine
from config.db_config import DB_CONFIG
from sqlalchemy.engine import URL

def get_engine():
    '''
    Creates and returns a SQLAlchemy engine for MySQL.
    '''
    db_url = URL.create(
        drivername="mysql+pymysql",
        username=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        database=DB_CONFIG["database"]
    )

    engine = create_engine(db_url)


    return engine