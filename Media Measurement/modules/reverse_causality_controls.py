import pandas as pd
from typing import List, Optional

def create_lagged_features(
    df: pd.DataFrame,
    target_col: str,
    lag_days: List[int],
    date_col: str = 'Date',
    group_col: Optional[str] = None,
    dropna: bool = True
) -> pd.DataFrame:

    if date_col not in df.columns:
        raise ValueError(f"Date column '{date_col}' not found in DataFrame.")
    
    # --- 1. Preparation ---
    data = df.copy()
    data[date_col] = pd.to_datetime(data[date_col])
    
    # Sort data to ensure correct shifting
    sort_keys = [group_col, date_col] if group_col else [date_col]
    data = data.sort_values(by=sort_keys).reset_index(drop=True)

    # --- 2. Create Lags ---
    for lag in lag_days:
        new_col_name = f'{target_col}_lag_{lag}d'
        print(f"Creating lag: {new_col_name}")

        if group_col:
            if group_col not in data.columns:
                raise ValueError(f"Grouping column '{group_col}' not found in DataFrame.")
            data[new_col_name] = data.groupby(group_col)[target_col].shift(lag)
        else:
            data[new_col_name] = data[target_col].shift(lag)

    # --- 3. Handle NaNs ---
    if dropna:
        original_rows = len(data)
        data = data.dropna().reset_index(drop=True)
        print(f"Dropped {original_rows - len(data)} rows with NaN values.")

    return data