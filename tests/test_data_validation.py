import pandas as pd
import numpy as np

from src.etl.data_validation import (_check_pk_uniqueness, _fk_coverage, validate_data)

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx add fk null test depending on business logic

# ======================================================================= Primary Key tests functions =======================================================================

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


def test_pk():                                  # ------------------------ calls other functions ------------------------
    '''
    tests the _check_pk_uniqueness function on 4 criteria
    '''
    print('\n' + "=" * 90 + '\n')
    print()
    print('Primary key tests:\n')
    test_valid_pk()
    test_duplicate_in_pk()
    test_null_pk
    test_missing_column_pk()

# ======================================================================= Foreign Key tests functions =======================================================================

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


def test_fk():                                  # ------------------------ calls other functions ------------------------
    '''
    tests the _fk_coverage function on 6 criteria - 3 valid 3 invalid
    '''
    print('\n' + "=" * 90 + '\n')
    print()
    print('Foreign key tests:\n')
    test_valid_fk_same()
    test_valid_fk_extra_pk_keys()
    test_valid_fk_keys_repeat()

    test_bad_key_fk()
    test_missing_fk()
    test_fk_missing_pk()



if __name__ == '__main__':
    test_pk()
    test_fk()
 