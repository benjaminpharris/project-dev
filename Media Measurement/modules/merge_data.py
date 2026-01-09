def create_master_panel():
    import pandas as pd
    from pathlib import Path
    import numpy as np

    # --- Read-In Cleaned Data ---
    local = pd.read_parquet('./data/clean/local_cleaned.parquet')
    opensignal = pd.read_parquet('./data/clean/opensignal_cleaned.parquet')
    ga = pd.read_parquet('./data/clean/ga_cleaned.parquet')
    spend = pd.read_parquet('./data/clean/spend_cleaned.parquet')

    # === Imputing Opensignal Data for New Dates ===

    dfs = {
        "local": local,
        "spend": spend,
        "opensignal": opensignal,
        "ga": ga
    }

    # 1. Common start date across everything (including opensignal)
    start_date = max(df["Date"].min() for df in dfs.values())

    # 2. End date based only on *non-problematic* data (exclude opensignal)
    non_problematic = {k: v for k, v in dfs.items() if k != "opensignal"}
    end_date = min(df["Date"].max() for df in non_problematic.values())

    print(f"Using intersecting date range (excluding opensignal lag at end): "
          f"{start_date.date()} to {end_date.date()}")

    # Work on a copy of opensignal, then put it back into dfs
    opensignal = dfs["opensignal"].copy()
    opensignal["Date"] = pd.to_datetime(opensignal["Date"])

    # --- Month range we want OpenSignal to reach ---
    target_end_month = pd.to_datetime(end_date).to_period("M").to_timestamp()
    last_os_month = opensignal["Date"].max().to_period("M").to_timestamp()

    if last_os_month >= target_end_month:
        print("OpenSignal up-to-date; no need to extrapolate.")
        extrapolated = pd.DataFrame(columns=opensignal.columns)
        months_to_add = pd.DatetimeIndex([])
    else:
        print(f"Imputing OpenSignal from {last_os_month.date()} → {target_end_month.date()}")

        months_to_add = pd.date_range(
            start=last_os_month + pd.offsets.MonthBegin(1),
            end=target_end_month,
            freq="MS"
        )

    # --- Extrapolate Population forward using last 3 months of data for one Market. ---
        def extrapolate_market(group: pd.DataFrame) -> pd.DataFrame:
            group = group.sort_values("Date").copy()

            # Month index (0..n) within this market
            t_idx = group["Date"].dt.to_period("M").astype(int)
            group["t"] = t_idx - t_idx.min()

            # last three points for regression
            last3 = group.tail(3)

            # If insufficient data, fallback to flat forward-fill
            if len(last3) < 2:
                slope = 0.0
                intercept = float(last3["Population"].iloc[-1])
            else:
                x = last3["t"].values
                y = last3["Population"].values
                b, a = np.polyfit(x, y, 1)  # slope b, intercept a
                slope = b
                intercept = a

            new_rows = []
            if len(months_to_add) > 0:
                last_t = group["t"].max()
                for i, m in enumerate(months_to_add, start=1):
                    t_new = last_t + i
                    pop_pred = intercept + slope * t_new
                    new_rows.append({
                        "Market": group["Market"].iloc[0],
                        "Date": m,
                        "Population": max(pop_pred, 0),  # guard against negative
                    })

            return pd.DataFrame(new_rows)

        markets = opensignal["Market"].unique()
        if len(markets) > 0:
            extrapolated = pd.concat(
                [extrapolate_market(opensignal[opensignal["Market"] == m]) for m in markets],
                ignore_index=True
            )
        else:
            extrapolated = pd.DataFrame(columns=opensignal.columns)

    # --- Combine original + extrapolated & recompute Population_Percent ---
    if not extrapolated.empty:
        opensignal = pd.concat([opensignal, extrapolated], ignore_index=True)

    # Ensure Date is datetime
    opensignal["Date"] = pd.to_datetime(opensignal["Date"])

    # Recompute Population_Percent for all months
    opensignal["Population_Percent"] = (
        opensignal.groupby(opensignal["Date"].dt.to_period("M"))["Population"]
                  .transform(lambda x: x / x.sum())
    )

    # Push updated opensignal back into dfs
    dfs["opensignal"] = opensignal

    # --- Apply common date filter to all dfs ---
    filtered_dfs = [
        df[(df['Date'] >= start_date) & (df['Date'] <= end_date)].copy()
        for df in dfs.values()
    ]

    local, spend, opensignal, ga = filtered_dfs

    # --- Data Pre-processing ---
    key = ["Date", "Market"]

    # Aggregate local to one row per Date/Market
    num_cols = local.select_dtypes("number").columns.difference(key)
    non_num = local.columns.difference(num_cols.union(key))
    local = local.groupby(key, as_index=False).agg(
        {**{c: "sum" for c in num_cols}, **{c: "first" for c in non_num}}
    )

    # Aggregate opensignal to one row per Date/Market
    num = opensignal.select_dtypes("number").columns.difference(key)
    non = opensignal.columns.difference(num.union(key))
    opensignal = opensignal.groupby(key, as_index=False).agg(
        {**{c: "sum" for c in num}, **{c: "first" for c in non}}
    )

    # --- Expand opensignal to daily with forward-fill ---
    opensignal = (
        opensignal.sort_values(key)
                  .set_index("Date")
                  .groupby("Market")[["Population", "Population_Percent"]]
                  .apply(lambda g: g.asfreq("D").ffill())
                  .reset_index()
    )

    # --- Master Panel Containing all Dates and Markets ---
    markets = pd.Index(opensignal['Market'].unique(), name="Market")
    dates = pd.Index(pd.date_range(start_date, end_date, freq="D"), name="Date")
    master = pd.MultiIndex.from_product([dates, markets], names=["Date", "Market"]).to_frame(index=False)

    master = master.merge(opensignal, on=key, how="left")
    master[['Population', 'Population_Percent']] = (
        master.groupby('Market')[['Population', 'Population_Percent']]
              .transform(lambda x: x.ffill().bfill())
    )

    master = master.merge(local, on=key, how="left")

    # --- MERGE IN GA DATA ---
    master = master.merge(ga, on=key, how="left")

    # --- Merge In spend Data & Create Instruments ---
    spend = spend.pivot_table(
        index="Date", columns="Platform", values="Spend",
        aggfunc="sum", fill_value=0
    ).reset_index()

    spend = spend.rename(columns={'Other': 'Other_spend'})

    tactic_cols = [col for col in spend.columns if col not in ['Date']]
    spend['spend_Total'] = spend[tactic_cols].sum(axis=1)

    master = master.merge(spend, on="Date", how="left")

    # --- Final Cleanup ---
    master = master.fillna(0)

    # Create shift-share instruments: Population share × national spend = Market Spend 
    tactic_cols = [col for col in spend.columns if col not in ['Date']]
    for tactic in tactic_cols:
        instrument_name = f"Instrument_{tactic}"
        master[instrument_name] = master['Population_Percent'] * master[tactic]

    # --- Validation: check instrument sums equal spend totals ---
    for tactic in tactic_cols:
        instrument_name = f"Instrument_{tactic}"
        instrument_daily_sum = master.groupby('Date')[instrument_name].sum()
        spend_daily_total = master.groupby('Date')[tactic].first()
        try:
            pd.testing.assert_series_equal(
                instrument_daily_sum, spend_daily_total,
                check_names=False, atol=0.01, check_dtype=False
            )
        except AssertionError as e:
            print(f"❌ Assertion FAILED for: {instrument_name}\n{e}")

            # NEW GA data markets are misaligned so the population % isn't totaling to 100 --> Spending is less than the total
            # Could also be the Imputation on the OS Data causing misalignment

    # Replace spend totals with market-specific instrument values
    master = master.drop(columns=tactic_cols)
    rename_mapping = {f"Instrument_{tactic}": tactic for tactic in tactic_cols}
    master = master.rename(columns=rename_mapping)

    # --- Final Output ---
    OUTPUT_PATH = Path("./data/")
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    master['Sales_Channel'] = master['Sales_Channel'].astype(str)
    master.to_parquet(OUTPUT_PATH / "master.parquet", index=False)


if __name__ == '__main__':
    create_master_panel()
