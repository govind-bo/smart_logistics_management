import os
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.database.engine import get_engine

def run_sql_script(script: str) -> None:
    '''
    Executes SQL scripts
    '''
    script_path = os.path.join(
        'sql',
        script
    )
    try:
        with open(script_path, 'r', encoding = 'utf-8') as file:
            sql_script = file.read()
        db_engine = get_engine()
        with db_engine.begin() as conn:
            for query in sql_script.split(';'):
                query = query.strip()
                if query:
                    conn.execute(text(query))
        print(f"Successfully executed:  {os.path.basename(script_path)}")

    except SQLAlchemyError as error:
        print(f'\n[ERROR] Error executing SQL script:\n{error}')
        raise

if __name__ == '__main__':

    script = '02_indexes.sql'
    script = '03_route_normalization.sql'
    script = ''

    run_sql_script(script)

