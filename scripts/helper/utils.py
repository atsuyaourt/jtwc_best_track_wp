import numpy as np
import pandas as pd
from const import CAT_COLS, FLOAT_COLS, INT_COLS, STR_COLS


def knots_to_cat(wind_speed):
    """Converts wind speed in knots to equivalent tropical cyclone category
    based on Saffir-Simpson scale

    Input:
    wind_speed (int) -- wind speed in knots

    Output:
    cat (str) -- TC category
    """
    cat = ""
    if wind_speed < 15:
        cat = ""
    elif wind_speed <= 33:
        cat = "TD"
    elif wind_speed <= 63:
        cat = "TS"
    elif wind_speed <= 82:
        cat = "Cat1"
    elif wind_speed <= 95:
        cat = "Cat2"
    elif wind_speed <= 112:
        cat = "Cat3"
    elif wind_speed <= 136:
        cat = "Cat4"
    else:
        cat = "Cat5"
    return cat


def format_types(df: pd.DataFrame):
    for col_name in CAT_COLS:
        try:
            df[col_name] = df[col_name].str.strip().str.upper()
        except Exception:
            pass
        df[col_name] = df[col_name].replace(np.nan, "")
        df[col_name] = df[col_name].astype("category")

    for col_name in INT_COLS:
        try:
            df[col_name] = df[col_name].str.strip()
        except Exception:
            pass
        df[col_name] = df[col_name].replace(np.nan, "")
        df[col_name] = df[col_name].replace("", 0)
        df[col_name] = df[col_name].astype("int32")

    for col_name in FLOAT_COLS:
        try:
            df[col_name] = df[col_name].str.strip()
        except Exception:
            pass
        df[col_name] = df[col_name].replace("", np.nan)
        df[col_name] = df[col_name].astype("float32")

    for col_name in STR_COLS:
        try:
            df[col_name] = df[col_name].str.strip()
        except Exception:
            pass
        df[col_name] = df[col_name].replace(np.nan, "")

    for col_name in df.select_dtypes(include=["float64"]).columns:
        df[col_name] = df[col_name].astype("float32")

    for col_name in df.select_dtypes(include=["int64"]).columns:
        df[col_name] = df[col_name].astype("int32")

    return df
