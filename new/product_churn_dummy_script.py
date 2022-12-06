# -*- coding: utf-8 -*-
"""product churn dummy script.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sJI-819jMX6oFOXsNIESAkXyL3jZTrzL
"""

'''
1. Take new file with product churn UID
2. Compare deltas of new to old data 
    1. If UID from new file doesn’t exist in old file, add UID + new data to row
        * AT RISK TABLE + First Notif
        1. Add Churn Time Stamp to New Rows. 
        2. Add column to compare current date - churn time stamp 
            * KPI: Time Since Churn 
            * Slack Bot Reads CSM name, search to find slack UID, send Slack notification to CSM
    2. If UID still exists, leave row in old file. 
        1. Compare difference of Current Date - Churn Date Column for UID 
            1. If Total is >= 2 days and <= 3 days send “2nd follow up notification” 
            2. If Total is > 3 AND <  send “Final follow up notification”
    3. If UID from old file no longer exists in new file, remove row and add to re-adopted table 
        1. Add time stamps for date closed
        2. Compare current date - Churn time stamp 
            * KPI: Turn over time 

CSM Slack Submission Form 

- Bot:
    - Asks CSM to reach out to merchant with multiple follow up notifications. 
    - Was this notification useful? Gauge program usefulness. 
    - CSM Win/Lost Form
        - Win/Lost Table with CSM, UID, Merchant Name, Time Stamp
        - Compare CSM win submission table with re-adopted table to determine if TRUE win. 

- Topline KPIs - 
Total Revenue Recovered 

Number Accounts At Risk
Total GMV at Risk
Risk Bucketed by Time L24HRS, L48HRS, L72HRS, L30, L60, L90, L>90

Number of Accounts Churned
Total Revenue lost
Accounts lost by time L24HRS, L48HRS, L72HRS, L30, L60, L90, L>90

Number Accounts Won
Total Revenue Won
Accounts Won by time L24HRS, L48HRS, L72HRS, L30, L60, L90, L>90

Revenue Recovered by Region
CSM True Wins / Losses
Total Self-Service Wins / Losses 
CSM Revenue Recovered
Wins bucketed by time L24HRS, L48HRS, L72HRS, L30, L60, L90, L>90 
'''

# Import numpy and pandas package
import os
import time
from datetime import datetime
from pytz import timezone
import numpy as np
import pandas as pd

# Move 'UID' to first column in the two dataframes
# col_to_first(day_1, 'UID')
# col_to_first(day_2, 'UID')
# Running the codeblock here to check. Let's see how these DFs look. It worked.

# pd.set_option('max_columns', None)
# double_df.head()

# Sets timezone to EST
def timestamp():
  # define date format
  fmt = '%Y-%m-%d %H:%M:%S'
  # define eastern timezone
  eastern = timezone('US/Eastern')
  # localized datetime
  loc_dt = datetime.now(eastern)
  # 2015-12-31 19:21:00 
  return(loc_dt.strftime(fmt))

# Moves specific column to the beginning of the dataframe
def col_to_first(df, column):
    # define column 'column' to be moved to first position
    first_column = df.pop(column)

    # insert column using insert(position,column_name, first_column) function
    df.insert(0, column, first_column)
    print("Column", column, "was shifted to first position")

# Strips suffix from column where there is a join 
def strip_right(df, suffix="_x"):
    df.columns = df.columns.str.rstrip(suffix)
    return df

# Removes the time column, and updates the column with a new timestamp
def update_time(df):
    df = df.drop(labels='date', axis='columns')
    df = df.assign(date = pd.to_datetime(timestamp()))
    return df

# Read Historical CSV file 
# Convert Historical CSV to dataframe with select columns 
h_csv_3 = "historical_dataset.csv" #this works because they're in the working folder
h_df3_spi = pd.read_csv(h_csv_3, index_col=None, usecols = ['UID', 'current_csm', 'shop_name', 'region', 'internal_url', 'revenue_365', 'is_product_enabled'])
h_df3_spi.sort_values('UID',ascending = True, ignore_index= True)
h_df3_spi.head(30)

# Read New CSV File
# Convert New CSV File to dataframe with select columns
n_csv_3 = "day_2.csv" # day 2 pull of the report
n_df3_spi = pd.read_csv(n_csv_3, index_col=None, usecols = ['UID', 'current_csm', 'shop_name', 'region', 'internal_url', 'revenue_365', 'is_product_enabled'])
n_df3_spi.sort_values('UID',ascending = True, ignore_index= True)

# Compare new CSV with updated historical CSV
# Inner join new table with historical data table will remove new records. 
double_df1 = h_df3_spi.merge(n_df3_spi, on='UID', how='inner', suffixes=("_d1","_d2"), sort=True)
double_df1 = double_df1.loc[(double_df1['is_product_enabled_d1'] == True) & (double_df1['is_product_enabled_d2'] == False), ['UID', 'current_csm_d2', 'shop_name_d2', 'region_d2', 'internal_url_d2', 'revenue_365_d2', 'is_product_enabled_d2']]
double_df1.rename(columns={'current_csm_d2': 'current_csm', 'shop_name_d2': 'shop_name', 'region_d2':'region', 'internal_url_d2':'internal_url', 'revenue_365_d2': 'revenue_365', 'is_product_enabled_d2':'is_product_enabled'}, inplace=True)
double_df1.sort_values('UID',ascending = True, ignore_index= True)

# New Churned Accounts
spi_churned_new = double_df1
spi_churned_new = spi_churned_new.assign(date = pd.to_datetime(timestamp()))

# Update historical csv file with new records and snopshot
# This will concatinate the historical dataframe with the new dataframe, then remove the last duplicate
# Keep = 'first' will refresh the data table with the newest data, while adding new records
df_all = pd.concat([h_df3_spi,n_df3_spi],ignore_index=True).drop_duplicates(subset='UID', keep='last')
df_all = df_all.sort_values('UID',ascending = True, ignore_index= True)

# spi_churned_new = update_time(spi_churned_new)
spi_churned_new.head()

# ------------------------------------------------------------------------
# Overwrite historical data table with refreshed data. i.e 
# df_all = pd.concat([h_df3_spi,n_df3_spi],ignore_index=True).drop_duplicates(subset='UID', keep='first')
# df_all.to_csv("historical_dataset.csv", index = False)

# Update Churn Dataset and move wins to win dataset
# Refresh Wins Data Set 
# Import Historical Churn Table
h_churn_csv = "Churn_Table.CSV"
h_churn_df = pd.read_csv(h_churn_csv, index_col=None)
h_churn_df = h_churn_df.sort_values('UID',ascending = True, ignore_index=True,)
h_churn_df.head()

# Add new churn to churn table. Drop duplicates. This data frame includes all previous churns + new 
df_churn_all = pd.concat([h_churn_df,spi_churned_new], ignore_index=True,).drop_duplicates(subset='UID', keep='first')
df_churn_all = df_churn_all.sort_values('UID',ascending = True, ignore_index= True)

# ------------------------------------------------------------------------
# Overwrite historical churn table with refreshed data. 
# df_all = pd.concat([h_df3_spi,n_df3_spi],ignore_index=True).drop_duplicates(subset='UID', keep='first')
# df_all.to_csv("Churn_Table.CSV", index = False)

# Check if ID is no longer a churn by comparing the updated churn dataframe, to the historical dataframe. Add only left dataset to new dataframe
churn_win_n = df_churn_all.merge(spi_churned_new, how='outer', on='UID', indicator='i',).query('i=="left_only"').drop('i', axis=1) # Left Outer Join 
churn_win_n = churn_win_n.dropna(axis=1, how='all') # Drop columns with NaN
churn_win_n = strip_right(churn_win_n) # Strip suffix 
churn_win_n = update_time(churn_win_n) # Update date column with new timestamps
churn_win_n.head()

# ------------------------------------------------------------------------
# Overwrite historical wins table with refreshed data.
# df_all = pd.concat([h_df3_spi,n_df3_spi],ignore_index=True).drop_duplicates(subset='UID', keep='first')
# df_all.to_csv("Wins_Table.CSV", index = False)