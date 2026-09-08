# DNM_Data

## General Codebase for eda on the _dnmarchives_ dataset 

> There is currently no specific analytical objective here, other than probably doing a lot of duplicative work against *Wang et. al* who already wrote a custom parser. The end result will hopefully be something similar but built on more modern architecture and which is *hopefully* extensible beyond the _dnmarchives_ dataset.

---

### Setup

1. Everything runs out of the notebook, directory structure is assumed to follow the repository.
2. To build the environment you can either use the included environment.yml if that's your thing or run:
    >` conda create -n env-dnm python=3.12 jupyterlab ipykernel ipywidgets numpy scipy pandas pyarrow matplotlib seaborn altair scikit-learn beautifulsoup4 lxml pillow tqdm polars`
    
    >`conda activate env-dnm`

    >`pip install dotenv` 

---

### **Attribution:** 

- **Gwern Branwen:** `https://gwern.net/index`
- **Archives:** `https://archive.org/download/dnmarchives` & `https://archive.org/details/dnmarchives`
- **Link:** `https://archive.org/download/dnmarchives/dnmarchives_archive.torrent`
  - **magnet:**`xt=urn:btih:3e5be1f435a4e545a24e497e2d9a25e67720791e&dn=dnmarchives&xl=51946455040&tr=http%3A%2F%2Fbt1.archive.org%3A6969%2Fannounce&tr=http%3A%2F%2Fbt2.archive.org%3A6969%2Fannounce&ws=http%3A%2F%2Fia601504.us.archive.org%2F12%2Fitems%2F&ws=http%3A%2F%2Fia801504.us.archive.org%2F12%2Fitems%2F&ws=https%3A%2F%2Farchive.org%2Fdownload%2F`

### Literature:

- **Early NN Features:** *Thomas and Kovashka, “Seeing Behind the Camera: Identifying the Authorship of a Photograph” (CVPR 2016)*
