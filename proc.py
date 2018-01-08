import pandas as pd

from helper.utils import knots_to_cat

in_file = 'JTWC_raw.csv'
out_file = 'JTWC.csv'

df = pd.read_csv(in_file)

out_df = df.iloc[:, 0:9]  # get first 9 columns
out_df.columns = [
    'CY', 'Year', 'Month',
    'Day', 'Hour', 'Lat',
    'Lon', 'VMax', 'MSLP']  # rename columns
tc_id = out_df.apply(
    lambda r: "%d%02d" % (r['Year'], r['CY']), axis=1)  # Serial Number column
out_df = pd.concat([tc_id, out_df], axis=1)
out_df.rename(columns={0: 'SN'}, inplace=True)
out_df['Cat'] = out_df.VMax.apply(knots_to_cat)  # Create category column
out_df = out_df.drop_duplicates()  # Get unique rows
out_df = out_df.sort_values(['SN', 'Year', 'Month', 'Day', 'Hour', 'CY'])

out_df.to_csv(out_file, index=False)
