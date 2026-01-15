def preprocess_data():
    print("Starting preprocessing script...")
    
    import sys
    print("Python Executable:", sys.executable)
    
    import pandas as pd
    from datetime import datetime
    
    # --- Read in Data ---
    mkt = pd.read_csv("data/raw/2H2024_Marketing_Long.csv")
    ds = pd.read_csv("data/raw/DS_Door.csv")
    cpi = pd.read_csv("data/raw/CPIAUCSL.csv").rename(columns={'DATE': 'Date'})
    
    # --- Print Heads ---
    print("Marketing Data:\n", mkt.head())
    print("DoorSwing Data:\n", ds.head())
    print("CPI Data:\n", cpi.head())
    
    # --- Convert 'Date' Columns ---
    mkt['Date'] = pd.to_datetime(mkt['Date'])
    ds['Date'] = pd.to_datetime(ds['Date'])
    cpi['Date'] = pd.to_datetime(cpi['Date'])
    
    # --- Fill Missing Values ---
    mkt = mkt.fillna(0)
    ds = ds.fillna(0)
    
    # --- Resample CPI to Daily Frequency and Fill ---
    cpi = cpi.set_index('Date').resample('D').ffill().reset_index()
    cpi = cpi.fillna(0)
    
    # --- Merge DataFrames ---
    final_df = mkt.merge(ds, how='left', on='Date')
    final_df = final_df.merge(cpi, how='left', on='Date')
    
    # --- Save Cleaned Data ---
    final_df.to_csv("data/processed/mkt_2h_2024.csv", index=False)
    
    return final_df

if __name__ == "__main__":
    df = preprocess_data()
    print("Preprocessing complete. Cleaned data saved and ready for analysis.")
