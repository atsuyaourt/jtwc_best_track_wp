import shutil
from zipfile import ZipFile
from glob import glob
from StringIO import StringIO
import pandas as pd

IN_FILE = 'output/JTWC_raw.csv'
BAK_FILE = 'output/JTWC_raw.csv.bak'
IN_DIR = 'input/raw/'

COL_NAMES = [
    'BASIN', 'CY', 'YYYYMMDDHH', 'TECHNUM', 'TECH', 'TAU', 'LAT', 'LON',
    'VMAX', 'MSLP', 'TY', 'RAD', 'WINDCODE', 'RAD1', 'RAD2', 'RAD3', 'RAD4',
    'RADP', 'RRP', 'MRD', 'GUSTS', 'EYE', 'SUBREGION', 'MAXSEAS', 'INITIALS',
    'DIR', 'SPEED', 'STORMNAME', 'DEPTH', 'SEAS', 'SEASCODE', 'SEAS1', 'SEAS2',
    'SEAS3', 'SEAS4']


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
    if (coord_dir == 'S') | (coord_dir == 'W'):
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
    _df = _df.loc[_df['BASIN'] == 'WP']
    _df.drop(_df.columns[[0, 3, 4, 5]], axis=1, inplace=True)
    _df['YYYYMMDDHH'] = pd.to_datetime(_df['YYYYMMDDHH'], format='%Y%m%d%H')

    _df2 = pd.DataFrame(_df['CY'])

    _df2['YYYY'] = _df['YYYYMMDDHH'].dt.year
    _df2['MM'] = _df['YYYYMMDDHH'].dt.month
    _df2['DD'] = _df['YYYYMMDDHH'].dt.day
    _df2['HH'] = _df['YYYYMMDDHH'].dt.hour
    _df2['LAT'] = _df['LAT'].apply(coord_str_to_num)
    _df2['LON'] = _df['LON'].apply(coord_str_to_num)

    _out_df = pd.concat([_df2, _df.iloc[:, 4:]], axis=1)

    return _out_df


zip_files = glob(IN_DIR + '*.zip')

df = None
for zfile in zip_files:
    with ZipFile(zfile) as z:
        for f in z.namelist():
            ff = StringIO(z.read(f).replace(' ', ''))
            if df is None:
                df = parse_input(ff)
            df = pd.concat([df, parse_input(ff)])

out_df = df.sort_values(['YY', 'MM', 'DD', 'HH', 'CY'])

shutil.copyfile(IN_FILE, BAK_FILE)  # Backup the file
out_df.to_csv(IN_FILE, mode='a', index=False, header=False)
