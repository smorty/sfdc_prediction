# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 18:59:30 2019

@author: LiB19
"""

import numpy as np 
import pandas as pd 
from sklearn.preprocessing import Imputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import brier_score_loss
from sklearn.tree import DecisionTreeClassifier 
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import matplotlib.pyplot as plt  
import time

pd.set_option('display.max_columns',20)

# Read in data=================================================================
path = "/Users/stephenmortensen/Documents/DSI/Capstone/Data"
data_raw = pd.read_csv(path+'/'+'Oppty_Acct_df.csv')

# Preprocessing================================================================
# Filter to only closed deals
data_closed = data_raw[data_raw["CLOSED__C"] == 1]

# Select relevant variables
target = ["WON__C"]
features = ["AMOUNT",
            "Code_1",
            "CREDIT_LIMIT_ESTABLISHED__C",
            "TYPE",
            "CORE_RECORD_TYPE__C",
            "ENTERPRISE_ACCOUNT__C_x",
            "ANNUALREVENUE",
            "ACCOUNT_TIER__C",
            "ACCOUNT_TYPE__C",
            "CUSTOMER_CLASSIFICATION__C",
            "OPENTIME",
            "LASTACTTIME",
            "VALID_OPENTIME",
            "FIELDS_COMPLETED",
            "QUALIFICATION_APPROVAL_NA",
            "TASK_COUNT",
            "DIVISION__C",
            "Code_2",
            "Code_industry",
            "FLD_MARKET_SEGMENT__C"]

all_variables = target + features

df = data_closed.loc[:, all_variables]
df.shape

# Summarize data 
summary_df = pd.concat([pd.DataFrame(df.columns), pd.DataFrame(np.array(df.dtypes).reshape(-1,1)),
                        pd.DataFrame(df.isnull().sum().values), pd.DataFrame([df[name].nunique() for name in df.columns])],
                       axis=1)
summary_df.columns = ['Variable Name', 'Data Type', 'Nulls', 'Unique Values']
summary_df

# Create original X and y
X = df.loc[:, features]
y = df.loc[:, target]

# Create dummies
# CREDIT_LIMIT_ESTABLISHED__C dummies
X['CREDIT_LIMIT_ESTABLISHED__C'].value_counts(dropna=False)
dummies_CREDIT_LIMIT_ESTABLISHED__C = pd.get_dummies(X['CREDIT_LIMIT_ESTABLISHED__C'])
dummies_CREDIT_LIMIT_ESTABLISHED__C.columns = ['CREDIT_LIMIT'+str(col) for col in dummies_CREDIT_LIMIT_ESTABLISHED__C.columns]
dummies_CREDIT_LIMIT_ESTABLISHED__C.head()

# QUALIFICATION_APPROVAL_NA dummies
X['QUALIFICATION_APPROVAL_NA'].value_counts(dropna=False)
dummies_QUALIFICATION_APPROVAL_NA = pd.get_dummies(X['QUALIFICATION_APPROVAL_NA'])
dummies_QUALIFICATION_APPROVAL_NA.columns = ['QUALIFICATION'+str(col) for col in dummies_QUALIFICATION_APPROVAL_NA.columns]
dummies_QUALIFICATION_APPROVAL_NA.head()

# Code_1 dummies
X['Code_1'].value_counts(dropna=False)
dummies_Code_1 = pd.get_dummies(X['Code_1'])
dummies_Code_1.columns = ['Code_1'+str(col) for col in dummies_Code_1.columns]
dummies_Code_1.head()

# TYPE dummies
X['TYPE'].value_counts(dropna=False)
dummies_TYPE = pd.get_dummies(X['TYPE'])
dummies_TYPE.columns = ['TYPE'+str(col) for col in dummies_TYPE.columns]
dummies_TYPE.head()

# CORE_RECORD_TYPE__C dummies
X['CORE_RECORD_TYPE__C'].value_counts(dropna=False)
dummies_CORE_RECORD_TYPE__C = pd.get_dummies(X['CORE_RECORD_TYPE__C'])
dummies_CORE_RECORD_TYPE__C.columns = ['CORE_RECORD_TYPE'+str(col) for col in dummies_CORE_RECORD_TYPE__C.columns]
dummies_CORE_RECORD_TYPE__C.head()

# ENTERPRISE_ACCOUNT__C_x dummies
X['ENTERPRISE_ACCOUNT__C_x'].value_counts(dropna=False)
dummies_ENTERPRISE_ACCOUNT__C_x = pd.get_dummies(X['ENTERPRISE_ACCOUNT__C_x'])
dummies_ENTERPRISE_ACCOUNT__C_x.columns = ['ENTERPRISE'+str(col) for col in dummies_ENTERPRISE_ACCOUNT__C_x.columns]
dummies_ENTERPRISE_ACCOUNT__C_x.head()

# ACCOUNT_TIER__C dummies
X['ACCOUNT_TIER__C'].value_counts(dropna=False)
dummies_ACCOUNT_TIER__C = pd.get_dummies(X['ACCOUNT_TIER__C'])
dummies_ACCOUNT_TIER__C.columns = ['ACCOUNT_TIER'+str(col) for col in dummies_ACCOUNT_TIER__C.columns]
dummies_ACCOUNT_TIER__C.head()

# ACCOUNT_TYPE__C dummies
X['ACCOUNT_TYPE__C'].value_counts(dropna=False)
dummies_ACCOUNT_TYPE__C = pd.get_dummies(X['ACCOUNT_TYPE__C'])
dummies_ACCOUNT_TYPE__C.columns = ['ACCOUNT_TYPE'+str(col) for col in dummies_ACCOUNT_TYPE__C.columns]
dummies_ACCOUNT_TYPE__C.head()

# CUSTOMER_CLASSIFICATION__C dummies
X['CUSTOMER_CLASSIFICATION__C'].value_counts(dropna=False)
dummies_CUSTOMER_CLASSIFICATION__C = pd.get_dummies(X['CUSTOMER_CLASSIFICATION__C'])
dummies_CUSTOMER_CLASSIFICATION__C.columns = ['CUSTOMER_CLASSIFICATION'+str(col) for col in dummies_CUSTOMER_CLASSIFICATION__C.columns]
dummies_CUSTOMER_CLASSIFICATION__C.head()

# DIVISION__C dummies
X['DIVISION__C'].value_counts(dropna=False)
dummies_DIVISION__C = pd.get_dummies(X['DIVISION__C'])
dummies_DIVISION__C.columns = ['DIVISION'+str(col) for col in dummies_DIVISION__C.columns]
dummies_DIVISION__C.head()

# Code_2 dummies
X['Code_2'].value_counts(dropna=False)
dummies_Code_2 = pd.get_dummies(X['Code_2'])
dummies_Code_2.columns = ['Code_2'+str(col) for col in dummies_Code_2.columns]
dummies_Code_2.head()

# Code_industry dummies
X['Code_industry'].value_counts(dropna=False)
dummies_Code_industry = pd.get_dummies(X['Code_industry'])
dummies_Code_industry.columns = ['industry'+str(col) for col in dummies_Code_industry.columns]
dummies_Code_industry.head()

# FLD_MARKET_SEGMENT__C dummies
X['FLD_MARKET_SEGMENT__C'].value_counts(dropna=False)
dummies_FLD_MARKET_SEGMENT__C = pd.get_dummies(X['FLD_MARKET_SEGMENT__C'])
dummies_FLD_MARKET_SEGMENT__C.columns = ['FLD_MARKET_SEGMENT'+str(col) for col in dummies_FLD_MARKET_SEGMENT__C.columns]
dummies_FLD_MARKET_SEGMENT__C.head()

# New dataset with dummies
X_with_dummies = pd.concat([X, 
                            #  dummies_CREDIT_LIMIT_ESTABLISHED__C,
                            #  dummies_QUALIFICATION_APPROVAL_NA,
                             dummies_Code_1, 
                             dummies_TYPE, 
                             dummies_CORE_RECORD_TYPE__C,
                             dummies_ENTERPRISE_ACCOUNT__C_x,
                             dummies_ACCOUNT_TIER__C,
                             dummies_ACCOUNT_TYPE__C,
                             dummies_CUSTOMER_CLASSIFICATION__C,
                             dummies_DIVISION__C,
                             dummies_Code_2,
                             dummies_Code_industry,
                             dummies_FLD_MARKET_SEGMENT__C], axis=1)
X_with_dummies.head()

# Create final X
X_with_dummies = X_with_dummies.drop(['Code_1', 
                     'TYPE',
                     'CORE_RECORD_TYPE__C',
                     'ENTERPRISE_ACCOUNT__C_x',
                     'ACCOUNT_TIER__C',
                     'ACCOUNT_TYPE__C',
                     'CUSTOMER_CLASSIFICATION__C',
                     'DIVISION__C',
                     'Code_2',
                     'Code_industry',
                     'FLD_MARKET_SEGMENT__C',
                     'CREDIT_LIMIT_ESTABLISHED__C',
                     'QUALIFICATION_APPROVAL_NA'], axis=1)

X_with_dummies.shape

# create smaller train and validate
X_train, X_valid, y_train, y_valid = train_test_split(X_with_dummies, y, test_size=0.25, random_state=123)

# Modeling=====================================================================
# Classification tree (or decision tree classifier) ---------------------------
algorithm_starts = time.time()
dt = DecisionTreeClassifier(min_samples_split=5000, max_depth=50, random_state=201)
dt_train = dt.fit(X_train, y_train)
dt_valid_prob_all = pd.DataFrame(dt_train.predict_proba(X_valid))
dt_valid_prob = dt_valid_prob_all[1]
print(time.time() - algorithm_starts)

# Confusion matrix
y_pred = []
for p in dt_valid_prob:
    if p >= 0.5:
        y_pred.append(1)
    else:
        y_pred.append(0)

y_pred = pd.Series(y_pred, name='Predicted')    
y_valid = pd.Series(y_valid.iloc[:,0], name='Actual') 
dt_confusion = pd.crosstab(y_valid, y_pred)
print(dt_confusion)
#Predicted    0    1
#Actual             
#0.0        596  444
#1.0        665  499

# Feature importance
pd.DataFrame(dt_train.feature_importances_, index=X_train.columns)

# Boosted trees model ---------------------------------------------------------
X_train_xgb = xgb.DMatrix(X_train, label = y_train)
X_valid_xgb = xgb.DMatrix(X_valid)
X_only_train_xgb = xgb.DMatrix(X_train)

num_round_for_cv = 200
param = {'max_depth':3, 'eta':0.3, 'seed':201, 'objective':'binary:logistic', 'nthread':4}

algorithm_starts = time.time()
xgb.cv(param,
    X_train_xgb,
    num_round_for_cv,
    nfold = 5,
    show_stdv = False,
    verbose_eval = True,
    as_pandas = False)
print(time.time() - algorithm_starts)

algorithm_starts = time.time()
num_round = 60
xgb_train = xgb.train(param, X_train_xgb, num_round)
xgb_valid_prob = pd.Series(xgb_train.predict(X_only_train_xgb))
time.time() - algorithm_starts

fig, ax = plt.subplots(figsize=(12,18))
xgb.plot_importance(xgb_train, height=0.8, ax=ax)
plt.show()

# Confusion matrix
y_pred = []
for p in xgb_valid_prob:
    if p >= 0.5:
        y_pred.append(1)
    else:
        y_pred.append(0)

y_pred = pd.Series(y_pred, name='Predicted')    
dt_confusion = pd.crosstab(y_valid, y_pred)
print(dt_confusion)
#Predicted     0     1
#Actual               
#0.0        1357  1385
#1.0        1692  1547













