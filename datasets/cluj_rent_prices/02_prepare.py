# %%
from pathlib import Path
import pandas as pd

from src.preparation import *


if __name__ == "__main__":
    useless_cols = [
        'ad_id', 'item_condition', 'partner_code', 
        'if_jobseeker', 'poster_type', 'seller_id', 
        'cat_l1_id', 'cat_l1_name', 'cat_l2_id', 
        'cat_l2_name', 'cat_l3_id', 'cat_l3_name', 
        'category_id', 'region_id', 'city_id', 
        'seller_banner_visible']

    '''TODOs:
        * separate main into functions
        * itterate once over dataframe
    '''

    file_path = Path(r'data\raw\offers_cluj-napoca_2022-03-25.csv')
    out_path = Path(r'data\processed')
    out_path.mkdir(exist_ok=True)

    df = pd.read_csv(file_path)
    print('Loaded raw data')

    # process raw data
    for i, row in df.iterrows():
        df.loc[i, 'bathrooms'] = bathrooms_filler(row['bathrooms'])
        df.loc[i, 'floor'] = floor_level_filler(row['floor'])
        df.loc[i, 'rooms'] = rooms_filler(row['rooms'])
        df.loc[i, 'state'] = state_filler(row['state'])
        df.loc[i, 'surface'] = surface_filler(row['surface'])
        df.loc[i, 'zone'] = zone_aria_filler(row['zone_aria'], row['zone_aria'])
    print('Processed raw data')

    # extract relevant data
    value_cols = [
        'bathrooms', 'floor', 'rooms',
        'surface',
    ]
    categ_cols = [
        'state', 'zone'
    ]
    target_cols = [
        'ad_price'
    ]
    df = df.loc[:, value_cols+categ_cols+target_cols]
    print('Extracted relevant columns')

    # drop null rows
    df = df.dropna()
    df.to_csv(out_path / file_path.name, index=False)
    print('Done')
# %%
