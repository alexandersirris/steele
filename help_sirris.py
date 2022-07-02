# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 23:50:46 2022

@author: steelandquill
@source: alexandersirris
"""

#I'll be documenting my thought process in comments as I go

#Goals of the code, taken from the conversation
#- Pull a CSV file
#- Push it to a data frame
#- Move the unique identifier to the first column
#- Do that again for the next day with similar data types and structure 
#   (except new rows would be added or potentially removed)
#- Use the UID to scan the row and column, check if product adoption has 
#   changed. Then list any rows where product adoption has changed 
#   to a new CSV file.
#I’ve looked at a few different ways of potentially doing this. 
#   One was concat() the data frames on a left join so that only UIDs from 
#   the previous day would be added. Then from there I’m not entirely sure 
#   how to actually perform the checks 


# just looking at the goals, I know I need to import the following packages
    
import numpy as np
import pandas as pd

# Before I go defining any functions, lemme check out these CSVs

csv_1 = "day_1.csv" #this works because they're in the working folder
csv_2 = "day_2.csv" #this works because they're in the working folder

#turns the CSVs into DataFrames
day_1 = pd.read_csv(csv_1)
day_2 = pd.read_csv(csv_2)

# I run the code for the first time here and note 1 10x7 and 1 16x7

#%% Now that I've run that block of code, I split a new one to continue thinking

# Now I want to ensure that 'UID' is always the first column. 
#    Let's do a function that generically moves a column to front.

def col_to_first(df, column):
    # define column 'column' to be moved to first position
    first_column = df.pop(column)
  
    # insert column using insert(position,column_name, first_column) function
    df.insert(0, column, first_column)
    print("Column ", column, "was shifted to first position")
    
# Move 'UID' to first column in the two dataframes
col_to_first(day_1, 'UID')
col_to_first(day_2, 'UID')

# Running the codeblock here to check. Let's see how these DFs look. It worked.

#%% Now let's merge the two to figure out how it all looks together.

double_df = day_1.merge(day_2, on='UID', how='outer', suffixes=("_d1","_d2"), sort=True)

# Running the code here and looking at it.
# Welp. That's a lot of NaNs. Jesus, that's a lot of NaNs. Don't outer join.

#%% Let's redefine things.

#Let's use an inner join to find UIDs active on both days
active_users = day_1.merge(day_2, on='UID', how='inner', suffixes=("_d1","_d2"))

#Let's find the people who only interacted on one day with some negated truth statements
one_timers = day_1[~day_1.UID.isin(day_2.UID)].append(day_2[~day_2.UID.isin(day_1.UID)], ignore_index=True)

# Note: append is deprecated, but easier for me to use in the moment.

# now I'll look at the two new DataFrames
# Result: one_timers is clean. 12x7. active_users though, is 7x13. Hm. 

#%% Trying out that truth logic again, let's just look at repeat customers. 

day_2_rpt = day_2[day_2.UID.isin(day_1.UID)]
day_1_rpt = day_1[day_1.UID.isin(day_2.UID)]

#Note when you look at these, the indexes are messed up. 
#    If you leave the indexes messed up, it gaps the math below. Fix them like this.
day_1_rpt.reset_index(drop=True, inplace=True)
day_2_rpt.reset_index(drop=True, inplace=True)
#drop=True makes sure this method doesn't tack the index on as a column
#inplace=True modifies the DF in place without creating another object. USE THIS METHOD CAREFULLY
#Now the other DFs inherit the corrected indicies of these selections
#I'm going to do elementwise addition in this section

#split the engagements per day into dataframes of their own for elementwise.
engg_d1 = day_1_rpt[['Product 1', 'Product 2','Product 3','Product 4','Product 5']]
engg_d2 = day_2_rpt[['Product 1', 'Product 2','Product 3','Product 4','Product 5']]

#Convert the booleans to ints by simple math trick
engg_d1 = engg_d1*1
engg_d2 = engg_d2*1

#Total them up
engg_total = engg_d1.add(engg_d2)

#Tack 'UID' back on
engg_total['UID'] = day_1_rpt['UID']

#Hey remember this?
col_to_first(engg_total, 'UID')

#Let's make sure the totals are better described
engg_total.insert(1, 'Day 2', day_2_rpt['Date']) #note the "backwards" way of doing this.
engg_total.insert(1, 'Day 1', day_1_rpt['Date'])

#%% Now that that's all figured out, here's a csv out for engg_total

engg_total.to_csv('RepeatCustInfo.csv')

#from here, it's a matter of working some math method of calculating engagement over longer periods
#and batching steps of this process into callable functions.