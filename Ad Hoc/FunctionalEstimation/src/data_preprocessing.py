print("Starting preprocessing script...")
import sys
print("Python Executable", sys.executable)

import pandas as pd
import pandas_datareader.data as web
from datetime import datetime
print("Imported Files")


# --- Read in 2024 Marketing Spend and Outcomes

mkt_2h_2024 = pd.read_csv("data/raw/2H2024_Marketing_Long.csv")
print(mkt_2h_2024.head())


# --- Read in Door Data

ds_2h_2024 = pd.read_csv("data/raw/DS_Door.csv")
print(ds_2h_2024.head())


# --- Import CPI Data from FRED API ---

start = datetime(2024, 7, 1)
end = datetime.today()

cpi = web.DataReader('CPIAUCSL', 'fred', start, end)
cpi = cpi.reset_index().rename(columns={'DATE': 'Date', 'CPIAUCSL': 'CPI'})
print(cpi.head())
print("Read API")




# --- Variable Cleaning

dataframes = {
    "Marketing": mkt_2h_2024,
    "CPI": cpi,
    "DoorSwing": ds_2h_2024
}


for name, df in dataframes.items():
    print(f"\n{name} DataFrame")
    print(df.dtypes)


mkt_2h_2024['Date'] = pd.to_datetime(mkt_2h_2024['Date'])
ds_2h_2024 = pd.to_datetime(ds_2h_2024['Date'])
cpi['Date'] = pd.to_datetime(cpi['Date'])


