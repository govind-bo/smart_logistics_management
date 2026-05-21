import pandas as pd
from config.schema_config import PK_MAP, FK_MAP

# msg in test result dicts is unused... use it to tell reason for invalidity, not just valid or invalid
# should have named variable as result instead of test_result

def _check_pk_uniqueness(df: pd.DataFrame, pk: str) -> dict:
    '''
    Checks whether a column is a valid primary key.
    '''
    
    test_result = {
        "valid": False,
        "msg" : '',
        "total_rows" : len(df),
        "unique_non_null": 0,
        "null_count": 0,
        "duplicate_count": 0
        }
    
    if pk in df.columns:
        nulls = df[pk].isnull().sum()
        dupes = df[pk].dropna().duplicated().sum()
        
        if (nulls == 0) and (dupes == 0):
            test_result['valid'] = True
            test_result['msg'] = f'valid primary key {pk}'                  #unused
            test_result['unique_non_null'] = df[pk].nunique()
        else:
            test_result['msg'] = f"{'Nulls and duplicates' if (dupes !=0 and nulls!=0) else 'Null' if nulls != 0 else 'Duplicates'} found in {pk}"
            test_result['unique_non_null'] = df[pk].nunique(dropna = True)
            test_result['null_count'] = nulls
            test_result['duplicate_count'] = dupes
    else:
        test_result['msg'] = f'{pk} column missing in table'

    return test_result       


def _fk_coverage(child: pd.DataFrame, child_fk: str, parent: pd.DataFrame, parent_pk: str) -> dict:
    '''
    checks fk coverage/validity on three conditions:
    - fk present in child table
    - pk present in parent table
    - fk items are covered in parent table 
    '''
    test_result = {'valid' : False,
                   'msg' : '',
                   'missing_count' : 0,
                   'sample_bad_keys' : []
                   }
          
    if child_fk in child.columns and parent_pk in parent.columns:
        child_vals = set(child[child_fk].dropna())
        parent_vals = set(parent[parent_pk].dropna())
        missing = child_vals - parent_vals

        if missing:
            test_result['msg'] = f'{child_fk} has bad keys'
            test_result['missing_count'] = len(missing)
            test_result['sample_bad_keys'] = list(missing)[:10]
            return test_result
        
        test_result['valid'] = True
        test_result['msg'] = f'valid foreign key {child_fk}'                # unused
        return test_result
    
    test_result['msg'] = f"{'FK' if child_fk not in child.columns else 'PK'} column missing"
    return test_result


def validate_data(dataframes: pd.DataFrame) -> None:
    '''
    to perform data quality checks before loading into SQL, checks:
    - primary key uniqueness
    - foreign key coverage

    '''
    print('\n' + "=" * 90 + '\n')
    # PK uniqueness checks (skips any table extracted from raw_data folder which is not meant to be used)
    for table_name, pk_col in PK_MAP.items():
        if table_name in dataframes:
            pk_check = _check_pk_uniqueness(dataframes[table_name], pk_col)
            
            print(f"PK uniqueness check for:")
            print(f'Primary key {table_name}.{pk_col}:')
            print(f'status = {'passed' if pk_check['valid'] else 'failed'}')
            if not pk_check['valid']:
                print(f"reason = {pk_check['msg']}")
                print(f'total rows = {pk_check['total_rows']}')
                print(f'unique non null count = {pk_check['unique_non_null']}')
                print(f'null count = {pk_check['null_count']}')
                print(f"duplicate counts = {pk_check['duplicate_count']}")
                

    print('\n' + ' ' * 20 + '-' * 50 + ' ' * 20 + '\n')
    # FK coverage checks (based on relationships in schema_config)
    for child_table, child_fk, parent_table, parent_pk in FK_MAP:
        if child_table in dataframes and parent_table in dataframes:
            fk_check = _fk_coverage(child_table, child_fk, parent_table, parent_pk)
            print(f'FK coverage check for:')
            print(f'Foreign key {child_table}.{child_fk} referencing {parent_table}.{parent_pk} :')
            print(f'status = {'passed' if fk_check['valid'] else 'failed'}')
            if not fk_check['valid']: 
                if not fk_check['missing_count']:
                    print(f"reason = {fk_check['msg']}")
                else:
                    print(f'count of values missing in ref key = {fk_check['missing_count']}')
                    print(f'sample bad keys:\n {fk_check['sample_bad_keys']}')
                