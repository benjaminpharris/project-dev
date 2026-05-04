# Functional Estimation

This folder contains experiments with marketing and door swing data using traditional econometrics and causal inference methods. The notebooks rely on `econml` and related libraries. Raw data lives in `data/` and preprocessed outputs in `outputs/`.

## Environment
Use the provided conda environment file to recreate a working environment:

```bash
conda env create -f environment.yml
conda activate econml_env
```

## Running the analysis
1. Run the preprocessing script to clean marketing, door swing and CPI data:

```bash
python PreProcessing.py
```

The cleaned data will be written to `data/clean/mkt_2h_2024.csv`.

2. Launch JupyterLab to explore the notebooks (`analysis.ipynb`, `econML_media.ipynb`, etc.):

```bash
jupyter lab
```

Each notebook expects the preprocessed data from step 1.
