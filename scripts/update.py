from pathlib import Path
from re import findall
from shutil import copyfile
from zipfile import ZipFile
from io import StringIO
import pandas as pd

OUT_FILE = Path("output/JTWC_raw.csv")
BAK_FILE = Path("output/JTWC_raw.csv.bak")
IN_DIR = Path("input/update")

COL_NAMES = [
    "BASIN",
    "CY",
    "YYYYMMDDHH",
    "TECHNUM",
    "TECH",
    "TAU",
    "LAT",
    "LON",
    "VMAX",
    "MSLP",
    "TY",
    "RAD",
    "WINDCODE",
    "RAD1",
    "RAD2",
    "RAD3",
    "RAD4",
    "RADP",
    "RRP",
    "MRD",
    "GUSTS",
    "EYE",
    "SUBREGION",
    "MAXSEAS",
    "INITIALS",
    "DIR",
    "SPEED",
    "STORMNAME",
    "DEPTH",
    "SEAS",
    "SEASCODE",
    "SEAS1",
    "SEAS2",
    "SEAS3",
    "SEAS4",
]


def coord_str_to_num(coord_str):
    """ Convert a string coordinate to float

    Params:
    -------
    coord_str: str
    The value to be converted

    Returns:
    --------
    coord: float
    The converted value
    """
    coord_dir = coord_str[-1]
    coord = float(coord_str[:-1]) / 10
    if (coord_dir == "S") | (coord_dir == "W"):
        coord = -coord
    return coord


def parse_input(filepath_or_buffer):
    """ Parse the input into a DataFrame

    Params:
    -------
    filepath_or_buffer: str, StringIO
    The input

    Returns:
    --------
    out_df: pd.DataFrame
    The output dataframe
    """
    _df = pd.read_csv(filepath_or_buffer, header=None, names=COL_NAMES)
    _df = _df.loc[_df["BASIN"] == "WP"]
    _df.drop(_df.columns[[0, 3, 4, 5]], axis=1, inplace=True)
    _df["YYYYMMDDHH"] = pd.to_datetime(_df["YYYYMMDDHH"], format="%Y%m%d%H")

    _df2 = pd.DataFrame(_df["CY"])

    _df2["YYYY"] = _df["YYYYMMDDHH"].dt.year
    _df2["MM"] = _df["YYYYMMDDHH"].dt.month
    _df2["DD"] = _df["YYYYMMDDHH"].dt.day
    _df2["HH"] = _df["YYYYMMDDHH"].dt.hour
    _df2["LAT"] = _df["LAT"].apply(coord_str_to_num)
    _df2["LON"] = _df["LON"].apply(coord_str_to_num)

    _out_df = pd.concat([_df2, _df.iloc[:, 4:]], axis=1)

    return _out_df


zip_files = list(IN_DIR.glob("*.zip"))
zip_files = pd.DataFrame(
    zip_files,
    index=[int(findall("[0-9]{4}", z.as_posix())[0]) for z in zip_files],
    columns=["name"],
).sort_index()

if OUT_FILE.exists():
    in_df = pd.read_csv(OUT_FILE)
else:
    in_df = pd.DataFrame()

new_df = []
for zfile in zip_files["name"]:
    with ZipFile(zfile) as z:
        for f in z.namelist():
            ff = StringIO(z.read(f).decode("utf-8").replace(" ", ""))
            new_df.append(parse_input(ff))

new_df = pd.concat(new_df, sort=False, ignore_index=True)

new_df = new_df.sort_values(["YYYY", "MM", "DD", "HH", "CY"])

out_df = pd.concat([in_df, new_df], sort=False, ignore_index=True)

if OUT_FILE.exists():
    copyfile(OUT_FILE, BAK_FILE)  # Backup the file

out_df.to_csv(OUT_FILE, index=False)  # Save
