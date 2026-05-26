import pandas as pd
from config.schema_config import (PK_MAP, FK_MAP, DATE_COL_MAP)

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


def _fk_coverage(child: pd.DataFrame, child_fk: str, parent: pd.DataFrame, parent_pk: str) -> dict:         # realization - it should have been parent followed by child, as that is how tables are also created.
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

def _try_parse_date(df: pd.DataFrame, cols: list) -> dict:
    '''
    This function checks dates parsing and identifies and returns bad entries
    '''
    test_result = {}            # it will generate a dict of dict. the inside dictionary will have test result of a column whose key will be the column name
    for col in cols:
        test_col_result = {
        'full_parse': False,
        'missing_col':False,
        'msg':'',
        'total_rows': 0,
        'null_count': 0,
        'bad_dates_count' : 0,
        'bad_dates_index': []
        }
        if col not in df.columns:
            test_col_result['msg'] = f"{col} missing in the dataframe"
            test_col_result['missing_col'] = True
            test_result[col] = test_col_result
            continue
        test_col_result['total_rows'] = df[col].size
        test_col_result['null_count'] = df[col].isna().sum()
        parsed = pd.to_datetime(df[col], errors = 'coerce')
        bad_dates_mask = parsed.isna() & df[col].notna()     
        bad_dates_count = bad_dates_mask.sum()
        bad_dates_index = df.index[bad_dates_mask].tolist()
        if bad_dates_count == 0:
            test_col_result['full_parse'] = True
            test_col_result['msg'] = f"all dates parsed successfully in col - {col}"
        else:
            test_col_result['msg'] = f"parsing incomplete, bad dates present in col - {col}"
            test_col_result['bad_dates_count'] = bad_dates_count
            test_col_result['bad_dates_index'] = bad_dates_index
        test_result[col] = test_col_result
    return test_result


def validate_data(dataframes: pd.DataFrame) -> None:
    '''
    to perform data quality checks before loading into SQL, checks:
    - primary key uniqueness
    - foreign key coverage
    - checks if date columns could be parsed to datetime successfully and identifies and returns bad date entries
    '''

    # ----------------------------------------------------- SHOULD I RAISE ALERT WHEN A DF NAME PRESENT IN OUR MAPS IS MISSING IN dataframes ????????????????------------------------------------------------------?
    print('\n' + "=" * 90 + '\n')
    # PK uniqueness checks (skips any table extracted from raw_data folder which is not meant to be used)
    for table_name, pk_col in PK_MAP.items():
        if table_name in dataframes:
            pk_check = _check_pk_uniqueness(dataframes[table_name], pk_col)
            
            print(f"\nPK uniqueness check for:")
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
    for child_t_name, child_fk, parent_t_name, parent_pk in FK_MAP:
        child_table = dataframes[child_t_name]
        parent_table = dataframes[parent_t_name]
        if child_t_name in dataframes and parent_t_name in dataframes:
            fk_check = _fk_coverage(child_table, child_fk, parent_table, parent_pk)
            print(f'\nFK coverage check for:')
            print(f'Foreign key {child_t_name}.{child_fk} referencing {parent_t_name}.{parent_pk}')
            print(f'status = {'passed' if fk_check['valid'] else 'failed'}')
            if not fk_check['valid']: 
                if not fk_check['missing_count']:
                    print(f"reason = {fk_check['msg']}")
                else:
                    print(f'count of values missing in ref key = {fk_check['missing_count']}')
                    print(f'sample bad keys:\n {fk_check['sample_bad_keys']}')
                

    print('\n' + ' ' * 20 + '-' * 50 + ' ' * 20 + '\n')
    # date parsing checks
    for table_name, cols in DATE_COL_MAP.items():
        if table_name in dataframes:
            date_parse_check = _try_parse_date(dataframes[table_name], cols)
            for _, each_date_parse_check in date_parse_check.items():
                print(each_date_parse_check['msg'])
                print(f"total rows = {each_date_parse_check['total_rows']}")
                print(f"null count = {each_date_parse_check['null_count']}")
                if not each_date_parse_check['full_parse']:
                    print(f"total rows = {each_date_parse_check['total_rows']}")
                    print(f"null count = {each_date_parse_check['null_count']}")
                    print(f"bad dates count = {each_date_parse_check['bad_dates_count']}")
                    print(f"bad dates index: {each_date_parse_check['bad_dates_index']}")
                    
                          