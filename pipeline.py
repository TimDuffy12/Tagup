"""Tim Duffy 1/18/2022"""
import xarray as xr
import sqlalchemy
import numpy as np
import pandas as pd


# Establishing connection
engine = sqlalchemy.create_engine('sqlite:///exampleco_db.db')
inspector = sqlalchemy.inspect(engine)
tables = inspector.get_table_names()


def main():
    dataframes = create_data_frames()
    dataframes = convert_time_to_unix_epoch(dataframes)

    # Identifying outliers.
    outliers = []
    for df in dataframes:
        outliers.append(find_outliers(df, 'value'))

    # Replacing outliers with NaN.
    for df, is_ol in zip(dataframes, outliers):
        df.loc[is_ol, 'value'] = np.NaN

    # Creating 3D array
    # Moving data from flat dataframe to 3000 x 20 x 4 numpy array.
    data = np.zeros((3000, 20, 0))
    for df in dataframes:
        temp = np.transpose(np.resize(df['value'], (20, 3000)))
        data = np.dstack((data, temp))

    # Preparing Dimensions/Coords
    coords = create_coords(dataframes)

    # Creating xarray with labeled dimentions and coords
    dims = ['time', 'machine_id', 'feature']
    data_xr = xr.DataArray(data, dims=dims, coords=coords)
    print(data_xr[:20, 0, 0])


def convert_time_to_unix_epoch(dfs: pd.DataFrame) -> list:
    """
    Converts timestamps to UNIX epoch ints.
    This is necessary because numpy arrays require homogeneous data types.
    """
    for idx, df in enumerate(dfs):
        df = df['timestamp'].view('int64')
        dfs[idx]['timestamp'] = df
    return dfs


def create_coords(dfs: pd.DataFrame) ->list:
    """
    Creates a list of coordinates from the dataframes and SQLite table names.
    This assumes that the timestamps are the same across all tables/features and machines,
    and that all machine IDs are the same across all tables/features.
    """
    times = dfs[0]['timestamp'].unique()
    machine_ids = dfs[0]['machine'].unique()
    features = np.array(tables[:4])
    coords = [times, machine_ids, features]
    return coords


def create_data_frames() -> list:
    """
    Creates a list of dataframes from SQLite tables.
    """
    dfs = []
    # The last table is the static table, which is not used, hence the slice
    for table in tables[:-1]:
        dfs.append(pd.read_sql(table, engine))
    return dfs


def find_outliers(df: pd.DataFrame, col: str) -> pd.Series:
    """
    Returns a Pandas Series of boolean values where true indicates the presence of an outlier.
    """
    sigma = df[col].std()
    mean = df[col].mean()
    cutoff = 3*sigma
    is_outlier = ((df[col] > mean + cutoff) | (df[col] < mean - cutoff))
    return is_outlier


if __name__ == "__main__":
    main()
