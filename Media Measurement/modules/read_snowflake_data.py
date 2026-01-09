import pandas as pd
from pathlib import Path
from datetime import datetime
import os
import pyarrow as pa
import pyarrow.parquet as pq
from snowflake.snowpark.functions import col


# --- This Script Reads Datasets from Snowflake: local marketing $, national marketing $, opensignal, and GAs

def fetch_and_cache_data(session):
    parquet_names = {
        os.getenv("POPULATION_TABLE") : "opensignal.parquet",    # Overall Population by Market
        os.getenv("OLD_SPENDING_TABLE") : "national.parquet",    # Deprecated Sales Table
        os.getenv("GEO_SPEND_DAILY") : "local.parquet",          # Regional Specific Spending by Market
        os.getenv("GEO_MARKET_MAP") : "market_mapping.parquet",  # Deprecated / Reference Map for Company Market Codes
        os.getenv("SALES_TABLE") : "ga.parquet",                 # Sales Data
        os.getenv("SPENDING_TABLE") : "new_national.parquet"     # Current  Level Spending
    }

    CACHE_PATH = Path("./data/cache")
    CACHE_PATH.mkdir(parents=True, exist_ok=True) 
    tables_to_query = []
    tables_to_check_age = []

    stale_age = 48 # Hour count to re-pull old tables

    for table_name, parquet_file in parquet_names.items():
        file_cache = CACHE_PATH / parquet_file
        if not file_cache.exists():
            tables_to_query.append(table_name)
        else:
            tables_to_check_age.append(parquet_file)       

    for parquet_file in tables_to_check_age:
        file_path = CACHE_PATH / parquet_file
        file_age_hours = (datetime.now() - datetime.fromtimestamp(os.path.getctime(file_path))).total_seconds() / 3600
        if file_age_hours > stale_age:
            for table_name, file_name in parquet_names.items():
                if file_name == parquet_file:
                    tables_to_query.append(table_name)
                    break
    
    if not tables_to_query:
        print("All data caches are fresh. No queries needed.")
        return

    print(f"Querying fresh data for: {tables_to_query}")

        # Parametrize for anonymity
    sales_table = os.getenv("SALES_TABLE")
    dim_schema = os.getenv("DIM_SCHEMA")
    
    start_date = '2024-07-01'

    for snowflake_name in set(tables_to_query):
        parquet_file = parquet_names[snowflake_name]
        
        if snowflake_name == os.getenv("SALES_TABLE"):
            query = f"""
            SELECT
                DATE(ACTIVATION_DATE) as DATE,
                
                -- 1. ADDED MARKET COLUMN HERE
                geo.geo_market_description as Market,

                case
                    when level2_channel_description IN ('Direct', 'AXIOM-DIRECT', 'AXIOM-INDIRECT') THEN 'Telesales'
                    when level2_channel_description = 'Amazon' then 'Amazon'
                    when level2_channel_description = 'Apple' then 'Apple'
                    when level2_channel_description in ('Alternate Distribution Channel','Dish Internal','Unknown',
                        'University Bookstore','Legacy','Small and Medium Business') or level2_channel_description is null then 'Other' 
                    when level2_channel_description = 'TikTok' THEN 'Web'
                    when level3_channel_description = 'WEB/DIGITAL' then 'Web'
                    when level3_channel_description = 'Dealer Channel' then 'Indirect'
                    else level3_channel_description 
                end as channel,
                
                SUM(GROSS_ACTIVATION_QUANTITY) AS GAs,
                
                -- This logic still works per-row: if the row is 'Denver', PR_GAs is 0. If 'PR / VI', it equals GAs.
                SUM(iff(geo.geo_market_description = 'PR / VI', rad.gross_activation_quantity ,0)) AS PR_GAs,
                GAs-PR_GAs AS NET_Reporting_GAs

            FROM {sales_table} AS rad
            left {dim_schema}.subscriber_dimension sub 
                on rad.subscriber_dimension_sk = sub.subscriber_dimension_sk
            left join {dim_schema}.npanxx_geographic_dimension geo 
                on left(sub.subscriber_telephone_number,6) = geo.npanxx_code
            WHERE 1=1
                AND ACTIVATION_DATE >= {start_date}
                AND rad.revenue_generating_ind = 'TRUE'
            
            -- 2. UPDATED GROUP BY TO INCLUDE MARKET (Column 2)
            GROUP BY 1, 2, 3
            ORDER BY 1, 2, 3
            ;
            """
            df = session.sql(query = query)
        else:
            df = session.table(snowflake_name)

        print(f"  -> Writing cache for {parquet_file}...")
        df.to_pandas().to_parquet(CACHE_PATH / parquet_file, index=False)

