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