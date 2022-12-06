# -*- coding: utf-8 -*-
"""filter and remove.ipynb

Automatically generated by Colaboratory.


### ***Refactor***
"""

import numpy as np
import pandas as pd
import csv
import io

def diff_pd(df1, df2):
    """Identify differences between two pandas DataFrames"""
    assert (df1.columns == df2.columns).all(), \
        "DataFrame column names are different"
    if any(df1.dtypes != df2.dtypes):
        "Data Types are different, trying to convert"
        df2 = df2.astype(df1.dtypes)
    if df1.equals(df2):
        return None
    else:
        # need to account for np.nan != np.nan returning True
        diff_mask = (df1 != df2) & ~(df1.isnull() & df2.isnull())
        ne_stacked = diff_mask.stack()
        changed = ne_stacked[ne_stacked]
        changed.index.names = ['Shop_ID', 'col']
        difference_locations = np.where(diff_mask)
        changed_from = df1.values[difference_locations]
        changed_to = df2.values[difference_locations]
        return pd.DataFrame({'from': changed_from, 'to': changed_to},
                            index=changed.index)

#Read CSV and create data frame
csv = '/content/drive/MyDrive/Product Adoption/Analysis/Raw Data/June/pa_6_29.csv'
df1 = pd.read_csv(csv)

# replacing blank spaces with '_' 
df1.columns =[column.replace(" ", "_") for column in df1.columns]

first_column = df1.pop('Shop_ID')
df1.insert(0, 'Shop_ID', first_column)
df1.set_index('Shop_ID', inplace=True)
df1.sort_index(axis=0,ascending=True)

#Read CSV and create data frame
csv = '/content/drive/MyDrive/Product Adoption/Analysis/Raw Data/June/pa_6_30.csv'
df2 = pd.read_csv(csv)

# replacing blank spaces with '_' 
df2.columns =[column.replace(" ", "_") for column in df2.columns]

first_column = df2.pop('Shop_ID')
df2.insert(0, 'Shop_ID', first_column)
df2.set_index('Shop_ID', inplace=True)
df2.sort_index(axis=0,ascending=True)

diff_pd(df1, df2)

# df1 = pd.read_csv('/datalab/Product Adoption/2022/June/Raw Data/pa_29.csv', index_col='Shop ID')
# df2 = pd.read_csv('/datalab/Product Adoption/2022/June/Raw Data/pa_30.csv', index_col='Shop ID')
# data_top = df2.head()
   
# display
# data_top