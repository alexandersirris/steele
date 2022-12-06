The contents that you'll find in this folder include:

## Files Included
- product_churn_dummy_script.py
- dummy data
  - historical data set
  - day 2 
  - day 3

## DataTables 
- Historical Data table: This is local
- New Data Table: This is a pulled report, similar to historical data table and should refresh the local historical data table.
  The thought process here is that the iteration and refresh is always comparing the new data, to the last time it was pulled.
- Wins Data Table: 
    - t1 is_product_enabled == False 
    - t2 is_product_enabled == True 
- Churn Data table:
    - t1 is_product_enabled == True 
    - t2 is_product_enabled == False 

## Brief Overview
1. The historical data set is an initial snapshot of product adoption
2. Each day a report is pulled with changing adoption. 
3. Depending on how a UIDs 'is_product_enabled' column changes will determine whether it gets added to the wins or churns dataset. 
  4. A UID can only exist in one of the two sub-data tables, but will always exist in the parent data table
