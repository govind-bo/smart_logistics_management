from src.database.run_sql_script import run_sql_script
from src.etl.etl_pipeline import etl_pipeline


POST_LOAD_SCRIPTS = [
    '02_indexes.sql',
    '03_route_normalization.sql'
]

def main() -> None:
    '''
    Main orchestration pipeline
    '''

    print('SMART LOGISTICS MANAGEMENT PIPELINE')

    print('\n[SCHEMA] Creating fresh database tables...')
    run_sql_script('01_table_creation.sql')

    # RUN ETL
    print('\n[ETL] Running ETL pipeline...')
    etl_pipeline()

    # POST-LOAD SQL SCRIPTS
    print('\n[POST-LOAD] Running SQL scripts...')

    for script in POST_LOAD_SCRIPTS:

        print(f'\nExecuting: {script}')
        run_sql_script(script)

    print('[SUCCESS] Main pipeline completed successfully')



if __name__ == '__main__':
    main()