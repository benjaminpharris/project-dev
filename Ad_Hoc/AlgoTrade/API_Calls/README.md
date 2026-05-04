# API Calls

Notebooks for retrieving rental data and exploring revenue scenarios. Example notebooks:

- `InflationControlAPICall.ipynb` – queries FRED for regional rent CPI data and merges it with base rents.
- `RentDistributionPlot.ipynb` – visualizes the distribution of units owned per landlord.
- `RevenueModeling.ipynb` – experiments with revenue curves using `rhfs.csv` sample data.

The folder also includes `rents.csv`, `rents.txt` and other small data sets used by the notebooks.

## Environment
Create a virtual environment with the standard scientific stack. Required packages include:
`pandas`, `numpy`, `matplotlib`, `seaborn`, `requests` and `scipy`.

```bash
python -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib seaborn requests scipy
```

## Running
Start Jupyter and open any of the notebooks:

```bash
jupyter notebook
```

The notebooks fetch data from external APIs (for example FRED). Ensure you have internet access and any required API keys before running.
