import pandas as pd
from modules.market_map_os_to_bst import get_market_mapping
from modules.market_map_ga_to_bst import get_ga_market_mapping
import os
from IPython.display import display
from pathlib import Path
import numpy as np

def clean_local_data(df: pd.DataFrame) -> pd.DataFrame:

    # --- Type Conversion and Renaming ---
    df['Date'] = pd.to_datetime(df['EVENT_DATE'], errors = "coerce")
    df = df[df['Date'].notna()]
    df['Start_Date'] = pd.to_datetime(df['START_DATE'], errors = "coerce")
    df = df[df['Start_Date'].notna()]
    df['End_Date'] = pd.to_datetime(df['END_DATE'], errors = "coerce")
    df = df[df['End_Date'].notna()]
    df['Market'] = df['REPORTING_MARKET']

    df = df.rename(columns={'EVENT_TYPE': 'Tactic'})

    # --- Feature Engineering ---
    # Convert per-door spend to total market-level spend
    df['Spend'] = df['DAILY_SPEND_ACTUAL_PER_OPEN_DOOR'] * df['OPEN_DOORS_IN_REPORTING_MARKET']
    
    # Expand date ranges to daily observations
    df['Date'] = [pd.date_range(start, end) for start, end in zip(df['Start_Date'], df['End_Date'])]
    df = df.explode('Date')
    
    # --- Reshaping Data ---
    # Pivot to get unique spend columns by local tactic
    cleaned_df = df.pivot_table(
        index=['Date', 'Market'],
        columns='Tactic',
        values='Spend',
        aggfunc='sum',
        fill_value=0
    ).reset_index()
    cleaned_df.columns.name = None

    # Replace specified market names with "New York City"
    cleaned_df['Market'] = cleaned_df['Market'].replace(
        ['Central Jersey', 'NYC / NJ', 'New Jersey', 'Northern Jersey'],
        'New York City'
    )

    cleaned_df = cleaned_df.rename(columns={'Other': 'Other_Local'})

    print("Local Data Description")
    display(cleaned_df.describe())
    return cleaned_df

def clean_national_data(df: pd.DataFrame) -> pd.DataFrame:

    # --- Type Conversion and Renaming ---
    df['Date'] = pd.to_datetime(df['DATE'])
    df = df.rename(columns={
        'PLATFORM': 'Platform',
        'ACTUAL_SPEND': 'Spend',
        'FUNNEL_LEVEL': 'Funnel',
        'CHANNEL': 'Sales_Channel'
    })
    
    # --- Column Selection ---
    cols_to_keep = ['Date', 'Platform', 'Spend', 'Funnel', 'Sales_Channel']
    cleaned_df = df[cols_to_keep]
    cleaned_df['Date'] = pd.to_datetime(cleaned_df['Date'])

    print("National Data Description")
    display(cleaned_df.describe())
    return cleaned_df

def clean_opensignal_data(df: pd.DataFrame) -> pd.DataFrame:

    # --- Type Conversion and Filtering ---
    df['Date'] = pd.to_datetime(df['DATE'])
    df['Population'] = pd.to_numeric(df['MONTHLY_VALUE'])
    
    df_filtered = df[
        (df['METRIC'] == 'Subscribers') &
        (df['SEGMENT'] != 'Overall (Prepaid and Postpaid)') &
        (df['Date'].dt.year > 2023) &
        (df['GEO_DMA'] != 'National') 
    ].copy()

    # --- Aggregation ---
    df_grouped = df_filtered.groupby(['Date', 'GEO_DMA'])['Population'].sum().reset_index()
    df_grouped['Market'] = df_grouped['GEO_DMA']

    # --- Market Mapping ---
    mapping_dict = get_market_mapping()
    df_grouped['Market'] = df_grouped['Market'].map(mapping_dict).fillna(df_grouped['Market'])

    # --- Population %s ---
    totals = df_grouped.groupby('Date', as_index=False)['Population'].sum().rename(
        columns={'Population': 'Population_Total'}
    )
    df_grouped = df_grouped.merge(totals, on='Date', how='left')

    df_grouped['Population_Percent'] = (
        df_grouped['Population'] / df_grouped['Population_Total']
    )

    # --- Column Selection ---
    cols_to_keep = ['Date', 'Population', 'Market', 'Population_Percent']
    cleaned_df = df_grouped[cols_to_keep]

    print("OpenSignal Data Description")
    display(cleaned_df.describe())
    return cleaned_df

def clean_ga_data(df: pd.DataFrame) -> pd.DataFrame:
    
    df = df.rename(columns={
        'DATE': 'Date',
        'CHANNEL': 'Sales_Channel',
        'NET_REPORTING_GAS': 'GA',
        'MARKET': 'Market'
    })

    cols_to_keep = ['Date', 'Sales_Channel', 'GA', 'Market']
    df_filtered = df[cols_to_keep]
    df_filtered['Date'] = pd.to_datetime(df_filtered['Date'])

    mapping_dict = get_ga_market_mapping()
    df_filtered['Market'] = df_filtered['Market'].map(mapping_dict).fillna(df_filtered['Market'])

    cleaned_df = df_filtered.groupby(["Date", "Market", "Sales_Channel"]).sum().reset_index()

    print("GA Data Description")
    display(cleaned_df.describe())
    return cleaned_df

def clean_new_national(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(
        columns={
            'DATE': 'Date',
            'PLATFORM': 'Platform',
            'TACTIC': 'Tactic',
            'FUNNEL': 'Funnel',
            'CHANNEL': 'Sales_Channel',
            'SPEND': 'Spend'
        }
    )

    cols_to_keep = ['Date', 'Platform', 'Spend', 'Funnel', 'Sales_Channel']
    cleaned_df = df[cols_to_keep]
    cleaned_df['Date'] = pd.to_datetime(cleaned_df['Date'])

    print("New National Data Description")
    display(cleaned_df.describe())
    return cleaned_df


    # --- Master Wrapper to Call Previous Cleaning Fns
def clean_all_data():

    # Reading Cached Data 
    local_raw = pd.read_parquet("./data/cache/local.parquet")
    national_raw = pd.read_parquet("./data/cache/national.parquet")
    opensignal_raw = pd.read_parquet("./data/cache/opensignal.parquet")
    ga_raw = pd.read_parquet("./data/cache/ga.parquet")
    new_national_raw = pd.read_parquet("./data/cache/new_national.parquet")
    
    #  Cleaning 
    local_cleaned = clean_local_data(local_raw)
    national_cleaned = clean_national_data(national_raw)
    opensignal_cleaned = clean_opensignal_data(opensignal_raw)
    ga_cleaned = clean_ga_data(ga_raw)
    new_national_cleaned = clean_new_national(new_national_raw)
    
        # Merging Spend Data here 
        # --- Update to merge national and new_national ---
    new_start = new_national_cleaned['Date'].min()
    national_cleaned = national_cleaned[national_cleaned['Date'] < new_start]
    spend = pd.concat([national_cleaned, new_national_cleaned], ignore_index=True)
    spend = spend.sort_values(['Date', 'Platform']).reset_index(drop=True)


    # --- Saving Cleaned Data ---
    CLEAN_PATH = Path("./data/clean")
    CLEAN_PATH.mkdir(parents=True, exist_ok=True)

    local_cleaned.to_parquet(CLEAN_PATH / 'local_cleaned.parquet', index=False)
    opensignal_cleaned.to_parquet(CLEAN_PATH / 'opensignal_cleaned.parquet', index=False)
    ga_cleaned.to_parquet(CLEAN_PATH / 'ga_cleaned.parquet', index=False)
    spend.to_parquet(CLEAN_PATH / 'spend_cleaned.parquet', index=False)
    print("All data has been cleaned and saved successfully.")

    return None