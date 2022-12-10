This outline explains the overall project files, direction, and goal. The contents that you'll find in this folder include:

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

## Process 
1. (d0) Pull a data table of product adoption associated with a unique ID or person
2. (d1) Pull the same data table of product adoption, compare it to d0. 
3. Compare deltas of new to old data 
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

## How to track impact
1. CSM Slack Submission Form or CSMs submit opportunity into CRM
2. Create a new table of all CRM activity for a CSM. Compare the difference in time when a person churns to when a CSM engages with said person. 


## Notification System
- A slack bot that reads the product adoption wins/churn tables, finds the associated CSM, and pings them with a message. 
- Bot:
    - Asks CSM to reach out to merchant with multiple follow up notifications. 
    - Was this notification useful? Gauge program usefulness. 
    - CSM Win/Lost Form
        - Win/Lost Table with CSM, UID, Merchant Name, Time Stamp
        - Compare CSM win submission table with re-adopted table to determine if TRUE win. 

## Topline KPIs
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