from pathlib import Path

import pandas as pd
from helper.utils import format_types

if __name__ == "__main__":
    IN_FILE = Path("output/JTWC_raw.csv")
    OUT_FILE = Path("output/JTWC_raw.parquet")
    df = pd.read_csv(IN_FILE, low_memory=False)
    df = format_types(df)
    df.to_parquet(OUT_FILE)
