import os
import pandas as pd

# def inspect_data

def inspect_dataframes(dataframes: dict, n_rows:int = 3, top_n:int = 10) -> None:
    '''
    Quick structure check: shape, columns, dtypes, sample rows, followed by missing and duplicates (if any)
    '''
    for name, df in dataframes.items():
        print("\n\n" + "=" * 90)
        print(f"\nDATASET: {name}")
        print(f"\nRows: {len(df)} | Cols: {df.shape[1]}")
        print("\nColumns:", df.columns.tolist())
        print("\nDtypes:\n",df.dtypes.to_string())
        print(f"\nHead({n_rows}):\n", df.head(n_rows).to_string())
        print(f"\nSample({n_rows}):\n", df.sample(min(n_rows, len(df))).to_string())
        print()

        miss = df.isna().sum()
        miss = miss[miss>0].sort_values(ascending = False)
        if miss.empty:
            print("No missing values")
        else:
            print(f"Columns with missing values - {miss.size if miss.size < top_n else ('top ', top_n)}")       
            print(miss.head(top_n).to_string())
        print()

        dup = df.duplicated().sum()
        if dup == 0:
            print("No duplicate rows present")    
        else:
            print(f"Duplicate rows found: {dup}")
            print(f"First {min(top_n, dup)} duplicate rows:")
            print(df[df.duplicated()].head(min(top_n, dup)))
        print()

        df_numeric = df.select_dtypes(include = 'number')
        if not df_numeric.empty:
            print("Summary statistics of numerical columns:")
            print(df_numeric.describe().round(2).to_string())
