import pandas as pd
import numpy as np

from src.etl.data_validation import (_check_pk_uniqueness, _fk_coverage,  _try_parse_date)

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx add fk null test depending on business logic

# ======================================================================= Primary Key tests function =======================================================================

def test_pk():                                  
    '''
    tests the _check_pk_uniqueness function on 4 criteria
    '''

    def test_valid_pk():
        '''
        This function will test src.etl.data_validation._check_pk_uniqueness for handling valid primary keys
        '''
        df = pd.DataFrame(
                {'id' : [1, 2, 3, 4, 8]}
        )
        test_result = _check_pk_uniqueness(df, 'id')

        assert test_result['valid'] is True
        print(f"\nvalid PK test result:")
        for key, value in test_result.items():
            print(f"{key} : {value}")

    def test_duplicate_in_pk():
        df = pd.DataFrame(
            {'id' : [1, 2, 3, 3, 4]}
        )
        test_result = _check_pk_uniqueness(df, 'id')

        assert test_result['valid'] is False
        print(f"\nduplicates in PK test result:")
        for key, value in test_result.items():
            print(f"{key} : {value}")

    def test_null_pk():
        df = pd.DataFrame(
            {'id':[1, 2, None, 4]}
        )
        test_result = _check_pk_uniqueness(df, 'id')
        assert test_result['valid'] is False
        print(f"\nnulls in PK test result:")
        for key, value in test_result.items():
            print(f"{key} : {value}")

    def test_missing_column_pk():
        df = pd.DataFrame(
            {'a':[1, 2, 3]}
        )
        test_result = _check_pk_uniqueness(df, 'id')
        assert test_result['valid'] is False
        print(f"\nmissing column PK test result:")
        for key, value in test_result.items():
            print(f"{key} : {value}")

    print('\n' + "=" * 90 + '\n')
    print()
    print('Primary key tests:\n')
    test_valid_pk()
    test_duplicate_in_pk()
    test_null_pk
    test_missing_column_pk()

# ======================================================================= Foreign Key tests function =======================================================================

def test_fk():                            
    '''
    tests the _fk_coverage function on 6 criteria - 3 valid 3 invalid
    '''

    def test_valid_fk_same():
        '''
        tests valid fk with exactly same and equal values as pk
        '''
        parent_df = pd.DataFrame(
            {'parent_pk':[1, 2, 3]}
        )
        child_df = pd.DataFrame(
            {'child_fk': [1, 2, 3]}
        )
        test_result = _fk_coverage(child_df, 'child_fk', parent_df, 'parent_pk')
        assert test_result['valid'] is True
        print(f"\nvalid FK with same and equal keys in PK & FK test result:")
        for key, value in test_result.items():
            print(f"{key} : {value}")

    def test_valid_fk_extra_pk_keys():
        '''
        tests valid fk with extra keys in pk (unused in FK)
        '''
        parent_df = pd.DataFrame(
            {'parent_pk':[1, 2, 3, 4]}
        )
        child_df = pd.DataFrame(
            {'child_fk': [1, 2, 3]}
        )
        test_result = _fk_coverage(child_df, 'child_fk', parent_df, 'parent_pk')
        assert test_result['valid'] is True
        print(f"\nvalid FK with extra keys in pk (unused in FK) test result:")
        for key, value in test_result.items():
            print(f"{key} : {value}")

    def test_valid_fk_keys_repeat():
        '''
        tests valid fk where fk keys repeat
        '''
        parent_df = pd.DataFrame(
            {'parent_pk':[1, 2, 3]}
        )
        child_df = pd.DataFrame(
            {'child_fk': [1, 2, 3, 2]}
        )
        test_result = _fk_coverage(child_df, 'child_fk', parent_df, 'parent_pk')
        assert test_result['valid'] is True
        print(f"\nvalid FK where FK keys repeat test result:")
        for key, value in test_result.items():
            print(f"{key} : {value}")

    def test_bad_key_fk():
        parent_df = pd.DataFrame(
            {'parent_pk':[1, 2, 3]}
        )
        child_df = pd.DataFrame(
            {'child_fk': [1, 2, 3, 4]}
        )
        test_result = _fk_coverage(child_df, 'child_fk', parent_df, 'parent_pk')
        assert test_result['valid'] is False
        print(f"\nbad keys in FK test result:")
        for key, value in test_result.items():
            print(f"{key} : {value}")

    def test_missing_fk():
        parent_df = pd.DataFrame(
            {'parent_pk':[1, 2, 3]}
        )
        child_df = pd.DataFrame(
            {'a': [1, 2, 3]}
        )
        test_result = _fk_coverage(child_df, 'child_fk', parent_df, 'parent_pk')
        assert test_result['valid'] is False
        print(f"\nmissing FK test result:")
        for key, value in test_result.items():
            print(f"{key} : {value}")

    def test_fk_missing_pk():
        parent_df = pd.DataFrame(
            {'a':[1, 2, 3]}
        )
        child_df = pd.DataFrame(
            {'child_fk': [1, 2, 3]}
        )
        test_result = _fk_coverage(child_df, 'child_fk', parent_df, 'parent_pk')
        assert test_result['valid'] is False
        print(f"\nvalid FK test result:")
        for key, value in test_result.items():
            print(f"{key} : {value}")

    print('\n' + "=" * 90 + '\n')
    print()
    print('Foreign key tests:\n')
    test_valid_fk_same()
    test_valid_fk_extra_pk_keys()
    test_valid_fk_keys_repeat()

    test_bad_key_fk()
    test_missing_fk()
    test_fk_missing_pk()


# ======================================================================= date parse test function =======================================================================
def test_dt_parse():
    '''
    test src.etl.data_validation._try_parse_date() for the following conditions:
    - no valid dates
    - missing date column
    - all valid dates
    - partial valid dates
    - 
    with only one date column and two date columns
    '''

    print('\n' + "=" * 90 + '\n')
    def test_dts(test_df : pd.DataFrame, dt_col_list : list, truthy_checks : list) -> None:
        # test with single date column2 

        test_result = _try_parse_date(test_df, dt_col_list)
        for idx, outer_key in enumerate(test_result):
            assert test_result[outer_key]['full_parse'] == truthy_checks[idx][0]
            assert test_result[outer_key]['missing_col'] == truthy_checks[idx][1]
            print()
            for inner_key, value in test_result[outer_key].items():
                print(f"{inner_key} : {value}")
        print()

    # --------------------- test cases -----------------------

    # 1. all valid dates tests ===============================
    print(f"\n1. All valid dates test result:\n{'-' * 50}")
    # 1.1. single column all valid dates ---------------------

    print(f"1.1. single column all valid dates test result:")
    
    test_df = pd.DataFrame({
            'dt1':[
            "2024-01-01",
            "2024-02-01", 
            "2024-03-01"
            ]
        })
    dt_col_list = ['dt1']
    truthy_checks = [[True, False]]
    test_dts(test_df, dt_col_list, truthy_checks)
 
    # 1.2. two columns column all valid dates ---------------------

    print(f"1.2. single column all valid dates test result:")
    test_df = pd.DataFrame(
        [
        ["2025-01-01", "2025-01-10"],
        ["2025-02-01", "2025-02-10"],
        ["2025-03-01", "2025-03-10"]
        ],
        columns = ['dt1', 'dt2']
        )

    dt_col_list = ['dt1', 'dt2']
    truthy_checks = [[True, False], [True, False]]
    test_dts(test_df, dt_col_list, truthy_checks)

    # 2. missing column tests ===============================
    print(f"\n2. missing date col test result:\n{'-' * 50}")
    # 2.1. single column missing dt col ---------------------

    print(f"2.1. all missing date col test result:")
    
    test_df = pd.DataFrame({
            'not_dt1':[
            "2024-01-01",
            "2024-02-01", 
            "2024-03-01"
            ]
        })
    dt_col_list = ['dt1']
    truthy_checks = [[False, True]]
    test_dts(test_df, dt_col_list, truthy_checks)
 
    # 2.2. two columns both missing dt col ---------------------

    print(f"2.2. two columns both missing dt col test result:")
    test_df = pd.DataFrame(
        [
        ["2025-01-01", "2025-01-10"],
        ["2025-02-01", "2025-02-10"],
        ["2025-03-01", "2025-03-10"]
        ],
        columns = ['not_dt1', 'not_dt2']
        )

    dt_col_list = ['dt1', 'dt2']
    truthy_checks = [[False, True], [False, True]]
    test_dts(test_df, dt_col_list, truthy_checks)

    #2.3. two cols - one present, one missing dt col test ------------

    print(f"2.3. two cols - one present, one missing dt col test result:")
    test_df = pd.DataFrame(
        [
        ["2025-01-01", "2025-01-10"],
        ["2025-02-01", "2025-02-10"],
        ["2025-03-01", "2025-03-10"]
        ],
        columns = ['dt1', 'not_dt2']                                                    # one criteria with one column present with bad dates
        )

    dt_col_list = ['dt1', 'dt2']
    truthy_checks = [[True, False], [False, True]]
    test_dts(test_df, dt_col_list, truthy_checks)

    # 3. Bad date values ===============================
    print(f"\n3. bad dates test result:\n{'-' * 50}")
    # 3 all bad dates and partial bad dates ---------------------
    test_df = pd.DataFrame(
        [
        ["2025-01-101", "2025-01-10"],
        [None, "2025-02-10"],
        ["bad date", None]
        ],
        columns = ['dt1', 'dt2']
        )

    dt_col_list = ['dt1', 'dt2']
    truthy_checks = [[False, False], [True, False]]
    test_dts(test_df, dt_col_list, truthy_checks)



if __name__ == '__main__':
    test_pk()
    test_fk()
    test_dt_parse()
    