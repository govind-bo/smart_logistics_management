import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
        "user":os.getenv("MYSQL_USER"),
        "password":os.getenv("MYSQL_PASSWORD"),
        "host":os.getenv("MYSQL_HOST"),
        "port":int(os.getenv('MYSQL_PORT', 3306)),
        "database":os.getenv("MYSQL_DB") 
            }