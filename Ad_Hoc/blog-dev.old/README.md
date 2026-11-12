# Blog Development

Experiments and scripts used for blog posts. Code in this folder produces interactive and static visualizations showing model behavior and data examples.

Key files:

- `OutOfSampleViz.py` and `oos_static.py` generate Plotly visualizations of out-of-sample fits.
- `QBR_Plots.ipynb` and `MonstersSampleCode.ipynb` contain exploratory notebooks for articles.
- `regional_rent_cpi_fred.xlsx` and `rents.csv` provide sample data.

## Environment
Use Python 3 with Plotly, pandas, numpy and statsmodels:

```bash
python -m venv .venv
source .venv/bin/activate
pip install pandas numpy plotly statsmodels
```

## Running
To produce the interactive chart:

```bash
python OutOfSampleViz.py
```

This writes `out_of_sample_viz.html` which you can open in a browser. The static version is created with `python oos_static.py`.

For the notebooks, launch Jupyter:

```bash
jupyter notebook
```
