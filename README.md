# Analiza dużych zbiorów danych

Semestr zimowy 2026/2027

Materiały z laboratoriów: notebooki, skrypty i małe pliki przykładowe.

## Zawartość

- `lab_01` — wczytywanie i dzielenie dużych plików (pandas, multiprocessing, filesplit)
- `lab_02` — wprowadzenie do Daska
- `lab_03` — Dask bags, delayed i futures oraz lokalny klaster
- `lab_04` — Dask w Machine Learning (`dask-ml`, `joblib`, `xgboost.dask`)

## Środowisko

Python 3.14. Zależności z aktualnego środowiska wirtualnego:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Notebook z laboratorium 2 importuje też `dask` i `psutil`. Tych pakietów nie ma jeszcze w `requirements.txt`, bo nie są zainstalowane w `.venv`.

Duże pliki CSV i Parquet (Instagram, rozszerzone zamówienia, części podziału) są w `.gitignore`. Zostają lokalnie i nie wchodzą do repozytorium.
