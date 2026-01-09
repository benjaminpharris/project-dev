# AlgoTrade

A small prototype notebook (`SPY_MA_Arb.ipynb`) explores a simple moving-average strategy for trading SPY using the Alpha Vantage API.

## Environment
Install the dependencies with pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the notebook
Launch Jupyter and open `SPY_MA_Arb.ipynb`:

```bash
jupyter notebook
```

The notebook fetches price data from Alpha Vantage, so you will need an API key set in your environment as `ALPHAVANTAGE_API_KEY`.
