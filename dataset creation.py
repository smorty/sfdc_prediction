# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 16:00:04 2018

@author: MortensenS19
"""
# Read data from files ----------------------------------------------------------

import os
import pandas as pd
import numpy as np
import xlwings as xw
import matplotlib.pyplot as plt

pd.set_option('display.max_columns',20)

path = "C:\\Users\\MortensenS19\\Documents\\DSI\\Capstone\\Data\\2019.02.25"
files = os.listdir(path)

files_csv = [f for f in files if '.csv' in f]
# print(files_csv[0][:-4])

d = {}

for f in files_csv:
    print("reading in "+f+", which is "+str(len(f))+" characters.")
    data = pd.read_csv(path+"\\"+f,encoding='iso-8859-1')
    d[f] = data
    print("added all "+str(data.shape[0])+" rows and "+str(data.shape[1])+" columns of "+f)

for x in d:
    d[x.replace("Reports","Report").replace("SurveyAction","Survey_Action").replace("ties","ty").replace("Tasks","Task").replace("Events","Event").replace("eSFDC_","").replace("_Feb2019","").replace(".csv","").replace("_Extract","")] = d.pop(x)
    
for key, value in d.items():
    print(key,"Row:" + str(value.shape[0]), "Variable:" + str(value.shape[1]))

# Create variable lists ---------------------------------------------------------
AccountPlan = ["OWNERID",
               "ISDELETED",
               "NAME",
               "LASTMODIFIEDDATE",
               "ACCOUNT_GOALS__C",
               "ACCOUNT__C",
               "ANNUAL_REVENUE__C",
               "AT_RISK_FOR__C",
               "AT_RISK_REASON__C",
               "BRANDS__C",
               "DATE_PLACED_AT_RISK__C",
               "DIVISION__C",
               "HQ_LOCATION__C",
               "KEY_BUSINESS_PROBLEMS__C",
               "OPPORTUNITIES__C",
               "OVERVIEW__C",
               "PLAN_STATUS__C",
               "SALES_STRATEGY__C",
               "STRENGTHS__C",
               "THREATS__C",
               "WEAKNESSES__C",
               "REGION__C",
               "COUNT_OF_CUSTOMER_ENGAGEMENT_ON_ACCOUNT__C"]
Account = ["NAME",
           "BILLINGCOUNTRY",
           "INDUSTRY",
           "ANNUALREVENUE",
           "NUMBEROFEMPLOYEES",
           "OWNERID",
           "ACCOUNT_ID__C",
           "ACCOUNT_TIER__C",
           "ACCOUNT_TYPE__C",
           "CUSTOMER_CLASSIFICATION__C",
           "ENTERPRISE_ACCOUNT__C",
           "FOLDING_CARTON_CUSTOMER__C",
           "SALES_OPS_LEAD__C",
           "CLUSTER__C",
           "TASK_COUNT"]
CallReport = ["ID",
              "OWNERID",
              "NAME",
              "ACCOUNT__C",
              "CLOSING__C",
              "NOTES_NEXT_STEPS__C",
              "OBJECTIVES_TOPICS_TO_COVER__C",
              "OPENING__C",
              "PRESENTING__C",
              "PROBING__C",
              "RESULTS__C",
              "REGION__C",
              "EMAIL_CALL_REPORT__C",
              "OWNER_S_EMAIL_ADDRESS__C",
              "FOLLOW_UP_DATE__C",
              "ACCOUNT_LOCATION__C",
              "ACCOUNT_ID__C"]
Contact = ["ACCOUNTID",
           "OWNERID",
           "ACCOUNT_NAME__C",
           "ALIGNMENT_STATUS__C",
           "CONTACT_STATUS__C",
           "LEVEL_OF_ENGAGEMENT__C",
           "OPT_OUT_OF_SURVEY__C"]
CrossSellingProgram = ["OPPORTUNITY__C",
                       "CROSS_SELL_TYPE__C",
                       "STAGE__C",
                       "ASSIGN_SALES_REP__C"]
CustomerSurvey_ActionItem = ["OWNERID",
                             "ISDELETED",
                             "NAME",
                             "ACCOUNT__C",
                             "SCORE__C",
                             "STATUS__C",
                             "ACTION_ALERT__C",
                             "ACTUAL_COMPLETION_DATE__C",
                             "RAW_RESPONSE__C",
                             "RATING__C",
                             "ACCOUNT_ID__C"]
Event = ["WHOCOUNT",
         "WHATCOUNT",
         "SUBJECT",
         "DURATIONINMINUTES",
         "STARTDATETIME",
         "ACCOUNTID",
         "OWNERID",
         "TYPE",
         "ISDELETED",
         "ISGROUPEVENT",
         "ISRECURRENCE",
         "ISREMINDERSET",
         "DB_ACTIVITY_TYPE__C"]
Opportunity = ["ID",
               "ACCOUNTID",
               "ISPRIVATE",
               "NAME",
               "DESCRIPTION",
               "STAGENAME",
               "AMOUNT",
               "PROBABILITY",
               "EXPECTEDREVENUE",
               "TOTALOPPORTUNITYQUANTITY",
               "CLOSEDATE",
               "TYPE",
               "NEXTSTEP",
               "LEADSOURCE",
               "ISCLOSED",
               "ISWON",
               "FORECASTCATEGORY",
               "FORECASTCATEGORYNAME",
               "CURRENCYISOCODE",
               "HASOPPORTUNITYLINEITEM",
               "OWNERID",
               "CREATEDDATE",
               "LASTMODIFIEDDATE",
               "LASTACTIVITYDATE",
               "FISCALQUARTER",
               "FISCALYEAR",   
               "FISCAL",
               "LASTVIEWEDDATE",
               "LASTREFERENCEDDATE",
               "HASOPENACTIVITY",
               "HASOVERDUETASK",
               "ANNUAL_RECYCLABLE__C",
               "ANNUAL_WASTE_SPEND__C",
               "BIG_DEAL_APPROVAL__C",
               "BILL_TO_STATE__C",
               "BRANDS__C",
               "CREDIT_LIMIT_ESTABLISHED__C",
               "CRITICAL_BUSINESS_ISSUES__C",
               "CUSTOMER_HOT_BUTTONS__C",
               "CUSTOMER_PRESSURES__C",
               "CUSTOMER_PRESSURES_DESCRIPTION__C",
               "DIVISION__C",
               "GAME_CHANGER__C",
               "INDUSTRY__C",
               "MPN__C",
               "MATERIAL_SAMPLES_APPROVAL_STATUS__C",
               "NAICS_CODE__C",
               "OPPORTUNITY_OWNER_MANAGER_EMAIL_FORMULA__C",
               "PAPERBOARD_SUBSTRATES_UTILIZED__C",
               "PIPELINE_STATUS__C",
               "PROPOSAL_SUBMISSION_APPROVAL_STATUS__C",
               "QUALIFICATION_APPROVAL_STATUS__C",
               "REGION__C",
               "SHIP_TO_STATE__C",
               "STAGE_AGE_FORMULA__C",
               "STAGE_CHANGE_DATE_STAMP__C",
               "WARM_TO_HOT_MANAGER_APPROVAL_STATUS__C",
               "TOTAL_MSF__C",
               "TOTAL_TONS__C",
               "LEGACY_DIVISION__C",
               "LEGACY_CREATEDDATE__C",
               "MSF__C",
               "OPPORTUNITY_HAS_BEEN_EDITED__C",
               "OWNER_BU__C",
               "AREA__C",
               "TOTAL_MSM__C",
               "MSM__C",
               "ENTERPRISE_ACCOUNT__C",
               "EMERGING_CUSTOMER__C",
               "PROACTIVE_BUSINESS_DEVELOPMENT__C",
               "TONS_OTHER__C",
               "TONS_CRB__C",
               "TONS_CUK__C",
               "TONS_OTHER_COUNT__C",
               "TONS_SBS__C",
               "TONS_URB__C",
               "TONS_UNCOATED_KRAFT__C",
               "BEV_PRODUCT_FAMILY_MACHINE_COUNT__C",
               "COR_REQUIRED_FIELD_PRODUCT_LEVEL_COUNT__C",
               "PRODUCT_COUNT__C",
               "FLD_PRODUCTS_WITH_TONS_COUNT__C",
               "ANNUAL_EXPECTED_CARTON_K__C",
               "OPPORTUNITY_PLAN_COMPLETED__C",
               "WEEKLY_DASHBOARD_STORY__C",
               "PROACTIVE_OTHER__C",
               "OPPORTUNITY_DIVISION__C",
               "TOTAL_EXTENDED_MARGIN__C",
               "PLANT_COUNT__C",
               "CLOSED__C",
               "LOST__C",
               "WON__C",
               "CORE_RECORD_TYPE__C",
               "MPS_PRODUCTS_WITH_TONS_COUNT__C",
               "FLD_MARKET_SEGMENT__C",
               "RECORDTYPEID",
               "FIELDS_COMPLETED",
               "OPENTIME",
               "LASTACTTIME",
               "VALID_OPENTIME",
               "QUALIFICATION_APPROVAL_NA"]
Task = ["SUBJECT",
        "ACTIVITYDATE",
        "STATUS",
        "PRIORITY",
        "ISHIGHPRIORITY",
        "OWNERID",
        "DESCRIPTION",
        "TYPE",
        "ISDELETED",
        "ACCOUNTID",
        "ISCLOSED",
        "CREATEDDATE",
        "LASTMODIFIEDDATE",
        "ISARCHIVED",
        "CALLDURATIONINSECONDS",
        "CALLTYPE",
        "CALLDISPOSITION",
        "CALLOBJECT",
        "REMINDERDATETIME",
        "ISREMINDERSET",
        "ISRECURRENCE",
        "TASKSUBTYPE",
        "ASSIGNED_TO_MANAGER__C",
        "DB_ACTIVITY_TYPE__C",
        "DIVISION__C",
        "REGION__C",
        "ACTIVITY_TYPE__C",
        "ISDC_INBOUND_CALL_ANSWERED__C"]

# Extract tables from imported data --------------------------------------------
AccountPlan_raw = d['AccountPlan']
Account_raw = d['Account']
CallReport_raw = d['CallReport']
Contact_raw = d['Contact']
CustomerSurvey_ActionItem_raw = d['CustomerSurvey_ActionItem']
Event_raw = d['Event']
Opportunity_raw = d['Opportunity']
Task_raw = d['Task']
CrossSell_raw = d['CrossSellingProgram']
Ind_raw = d['industry_index']
NAICS_raw = d['NAICS_code_index']

# Create new variables, tables --------------------------------------------------

# Create completed field count variable
flds_cmplt = len(Opportunity_raw.columns.values) - Opportunity_raw.isnull().sum(axis=1)
min_cmplt = min(flds_cmplt)
range_cmplt = max(flds_cmplt) - min_cmplt
Opportunity_raw['FIELDS_COMPLETED'] = flds_cmplt - min_cmplt

# Create account-level task count variable
Task_count = Task_raw.groupby(by='ACCOUNTID', as_index=False).agg({'ID': pd.Series.count})
Task_count.rename(columns={'ID': 'TASK_COUNT'}, inplace=True)
Account_raw = pd.merge(Account_raw, Task_count, left_on="ID", right_on="ACCOUNTID", how="left")

# Create age-related variables
Opportunity_raw["OPENTIME"] = (pd.to_numeric(pd.to_datetime(Opportunity_raw["CLOSEDATE"],yearfirst=True)) - pd.to_numeric(pd.to_datetime(Opportunity_raw["CREATEDDATE"],yearfirst=True)))/1000000000/60/60/24
Opportunity_raw["LASTACTTIME"] =  (pd.to_numeric(pd.to_datetime(Opportunity_raw["LASTACTIVITYDATE"],yearfirst=True)) - pd.to_numeric(pd.to_datetime(Opportunity_raw["CREATEDDATE"],yearfirst=True)))/1000000000/60/60/24
Opportunity_raw["VALID_OPENTIME"] = (Opportunity_raw.OPENTIME > 0).astype(int)

# Group infrequent levels of variables, filter some small anomalies
Opportunity_raw["QUALIFICATION_APPROVAL_NA"] = Opportunity_raw["QUALIFICATION_APPROVAL_STATUS__C"].isna()
Opportunity_raw = Opportunity_raw[Opportunity_raw['ENTERPRISE_ACCOUNT__C'] != "$1MM * 2 Segments"]
Account_raw = Account_raw[Account_raw["CUSTOMER_CLASSIFICATION__C"] != "Global"]
Opportunity_raw["DIVISION__C"][Opportunity_raw.DIVISION__C.isin(["Corporate","CBM","HHB","ENT","RCY"])] = "Other"

# Limit variables to just those specified above
AccountPlan_df = AccountPlan_raw.loc[:, AccountPlan]
Account_df = Account_raw.loc[:, Account]
CallReport_df = CallReport_raw.loc[:, CallReport]
Contact_df = Contact_raw.loc[:, Contact]
CustomerSurvey_ActionItem_df = CustomerSurvey_ActionItem_raw.loc[:, CustomerSurvey_ActionItem]
Event_df = Event_raw.loc[:, Event]
Opportunity_df = Opportunity_raw.loc[:, Opportunity]
Task_df = Task_raw.loc[:, Task]
CrossSell_df = CrossSell_raw.loc[:, CrossSellingProgram]

# Merge opportunities, accounts, cross-selling data, and industry lookups
Oppty_Acct1 = pd.merge(Opportunity_df, Account_df, left_on="ACCOUNTID", right_on="ACCOUNT_ID__C", how="left")
Oppty_Acct2 = pd.merge(Oppty_Acct1, Ind_raw, left_on="INDUSTRY__C", right_on="industry", how="left")
Oppty_Acct3 = pd.merge(Oppty_Acct2, NAICS_raw, on="NAICS_CODE__C", how="left")
Oppty_Acct4 = pd.merge(Oppty_Acct3, CrossSell_df, left_on="ID",right_on="OPPORTUNITY__C", how="left")

# Filter data to only relevant dates, after 2016-04-01
Oppty_Acct_df = Oppty_Acct4[(Oppty_Acct4['CREATEDDATE'] >= '2016-04-01')]

# Remove some more pesky NA's
Oppty_Acct_df = Oppty_Acct_df[Oppty_Acct_df['ACCOUNT_TIER__C'].notna()]

# Impute NA's
Oppty_Acct_df['TASK_COUNT'][Oppty_Acct_df['TASK_COUNT'].isna()] = 0
Oppty_Acct_df['ANNUALREVENUE'][Oppty_Acct_df['ANNUALREVENUE'].isna()] = 0

Oppty_Acct_df['TASK_COUNT'][Oppty_Acct_df['TASK_COUNT'] != 0].shape
# Write data to csv -----------------------------------------------------------

# Check dimensions of data
print(AccountPlan_df.shape)
print(Account_df.shape)
print(CallReport_df.shape)
print(Contact_df.shape)
print(CustomerSurvey_ActionItem_df.shape)
print(Event_df.shape)
print(Opportunity_df.shape)
print(Task_df.shape)
print(Oppty_Acct_df.shape)

# Write data to csvs
AccountPlan_df.to_csv(path+"\\AccountPlan_df.csv")
print("Wrote AccountPlan to file.")
Account_df.to_csv(path+"\\Account_df.csv")
print("Wrote Account to file.")
CallReport_df.to_csv(path+"\\CallReport_df.csv")
print("Wrote CallReport to file.")
Contact_df.to_csv(path+"\\Contact_df.csv")
print("Wrote Contact to file.")
CustomerSurvey_ActionItem_df.to_csv(path+"\\CustomerSurvey_ActionItem_df.csv")
print("Wrote Customer Survey Action Item to file.")
Event_df.to_csv(path+"\\Event_df.csv")
print("Wrote Event to file.")
Opportunity_df.to_csv(path+"\\Opportunity_df.csv")
print("Wrote Opportunity to file.")
Task_df.to_csv(path+"\\Task_df.csv")
print("Wrote Task to file.")
Oppty_Acct_df.to_csv(path+"\\Oppty_Acct_df.csv")
print("Wrote Oppty Acct to file.")

# Old stuff around creating new tables -----------------------------------------
# 1) Initial Info: Account, AccountPlan, Contact
# PK: ACCOUNT_ID__C, ANNUALREVENUE, NAME, OWNERID from Account
# left = Account_df
# right = AccountPlan_df
# right.columns = right.columns.str.replace('ACCOUNT__C','ACCOUNT_ID__C')
# right.columns = right.columns.str.replace('ANNUAL_REVENUE__C','ANNUALREVENUE')
# InitialInfo = pd.merge(left, right, on = ['ACCOUNT_ID__C','ANNUALREVENUE','NAME','OWNERID'], how = 'left')
# InitialInfo.shape

# left = InitialInfo
# right = Contact_df
# right.columns = right.columns.str.replace('ACCOUNTID','ACCOUNT_ID__C')
# InitialInfo = pd.merge(left, right, on = ['ACCOUNT_ID__C','OWNERID'], how = 'left')
# InitialInfo.shape

# InitialInfo.to_excel('InitialInfo.xlsx', sheet_name='InitialInfo', index=False)

# # 2) Deal Progression: Opportunity, Customer Survey
# # PK: ACCOUNT_ID__C from Opportunity_df
# # Join by: ACCOUNT2__C from CustomerSurvey_ActionItem_df
# left = Opportunity_df
# right = CustomerSurvey_ActionItem_df
# left.columns = left.columns.str.replace('ACCOUNTID','ACCOUNT_ID__C')
# right.columns = right.columns.str.replace('ACCOUNT2__C','ACCOUNT_ID__C')
# DealProgression = pd.merge(left, right, on = ['ACCOUNT_ID__C','NAME','OWNERID'], how = 'left')
# DealProgression.shape

# DealProgression.to_excel('DealProgression.xlsx', sheet_name='DealProgression', index=False)

# 3) Sales Activities: Task, Call Report, Event
# PK: ACCOUNT_ID__C, OWNERID ??





















 
 