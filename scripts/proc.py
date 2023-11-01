from pathlib import Path
from shutil import copyfile

import pandas as pd
from helper.utils import knots_to_cat

IN_FILE = Path("output/JTWC_raw.parquet")
OUT_FILE = Path("output/JTWC.csv")


def main():
    df = pd.read_parquet(
        IN_FILE, columns=["CY", "YYYY", "MM", "DD", "HH", "LAT", "LON", "VMAX", "MSLP"]
    )

    out_df = df.rename(
        columns={
            "YYYY": "Year",
            "MM": "Month",
            "DD": "Day",
            "HH": "Hour",
            "LAT": "Lat",
            "LON": "Lon",
            "VMAX": "VMax",
        }
    )

    # Serial Number column
    out_df["SN"] = out_df["Year"].map(str) + out_df["CY"].map(str).str.pad(
        width=2, side="left", fillchar="0"
    )
    # Create category column
    out_df["Cat"] = out_df["VMax"].apply(knots_to_cat)
    # Get unique rows
    out_df = out_df.drop_duplicates(subset=["CY", "Year", "Month", "Day", "Hour"])
    out_df = out_df.sort_values(["SN", "Year", "Month", "Day", "Hour", "CY"])

    copyfile(OUT_FILE, OUT_FILE.with_suffix(".csv.bak"))  # Backup the file
    out_df.to_csv(OUT_FILE, index=False)


if __name__ == "__main__":
    main()
