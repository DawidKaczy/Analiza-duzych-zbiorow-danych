import os
from datetime import datetime
from functools import partial
from multiprocessing import Pool

import pandas as pd
from filesplit.split import Split


def count_time(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        print(f"Czas wykonania {func.__name__}: {datetime.now() - start} sekund")
        return result

    return wrapper


@count_time
def read_file_1():
    return pd.read_csv("instagram.csv", header=0)


@count_time
def read_file_2(chunksize):
    chunks = pd.read_csv("instagram.csv", header=0, chunksize=chunksize)
    return pd.concat(chunks, ignore_index=True)


def split_file(filepath, chunksize, destination):
    os.makedirs(destination, exist_ok=True)
    split = Split(filepath, destination)
    split.bylinecount(linecount=chunksize, includeheader=True)


def load_files(directory, processes):
    files = sorted(
        os.path.join(directory, name)
        for name in os.listdir(directory)
        if name.endswith(".csv")
    )
    print(f"plików: {len(files)}, procesów: {processes}")
    start = datetime.now()
    with Pool(processes=processes) as pool:
        read_csv_custom = partial(pd.read_csv, on_bad_lines="skip")
        results = pool.map(read_csv_custom, files)
        frame = pd.concat(results, ignore_index=True)
    print(f"Czas wczytania multiprocessing: {datetime.now() - start} sekund, wierszy: {len(frame)}")
    return frame


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    df = read_file_1()
    print("wierszy:", len(df))
    del df

    for chunksize in (100_000, 500_000):
        print(f"chunksize={chunksize}")
        df = read_file_2(chunksize)
        print("wierszy:", len(df))
        del df

    parts_dir = "csv_parts"
    juz_podzielone = os.path.isdir(parts_dir) and any(
        name.endswith(".csv") for name in os.listdir(parts_dir)
    )
    if not juz_podzielone:
        split_file("instagram.csv", 80_000, parts_dir)

    cores = os.cpu_count() or 1
    for processes in (max(1, cores - 2), max(1, (cores - 2) * 2)):
        df = load_files(parts_dir, processes)
        del df
