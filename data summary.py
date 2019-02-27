# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 16:00:04 2018

@author: MortensenS19
"""

import os
import pandas as pd
import numpy as np

pd.set_option('display.max_columns',20)

path = "C:\\Users\\MortensenS19\\Documents\\DSI\\Capstone\\Data\\2019.02.25"

files = os.listdir(path)

files_csv = [f for f in files if '.csv' in f]
# print(files_csv[0][:-4])

data_dict = {}

for f in files_csv:
    print("reading in "+f+", which is "+str(len(f))+" characters.")
    data = pd.read_csv(path+"\\"+f,encoding='iso-8859-1')
    data_dict[f] = data
    print("added all "+str(data.shape[0])+" rows and "+str(data.shape[1])+" columns of "+f)
    
# for x in data_dict:
#     print(x)

writer = pd.ExcelWriter(path+"\\"+'WestrockDataSummaryFeb2019.xlsx')

for x in data_dict:
    df = data_dict[x]
    x = x[:-4].replace('_Feb2019','').replace('eSFDC_','')

    first_values = pd.DataFrame({'Column Name':'del','First Value':'del'},index=[0])

    for column in df.columns:
        fv_i = df.loc[:,[column]].first_valid_index()
        if fv_i is not None:
            fv1 = df.loc[:,column].loc[df.loc[:,[column]].first_valid_index()]
            fv2 = pd.DataFrame({'Column Name':[column],'First Value':fv1})
            first_values = first_values.append(fv2)
        else:
            fv2 = pd.DataFrame({'Column Name': [column], 'First Value': [None]})
            first_values = first_values.append(fv2)
    
    first_values = first_values[1:]
    first_values = first_values.reset_index(drop=True)
    
    summary_df = pd.concat([pd.DataFrame(df.columns), pd.DataFrame(df.dtypes.values.reshape(-1,1)),
                            pd.DataFrame(df.isnull().sum().values), pd.DataFrame(np.round(df.isnull().sum().values/df.shape[0] * 100,1)), 
                            pd.DataFrame([df[name].nunique() for name in df.columns]),first_values.iloc[:,1]], axis=1)
    summary_df.columns = ['Variable Name', 'Data Type', 'Nulls','Nulls % of Total', 'Unique Values','First Value']
    
    if len(x) <= 31:
        summary_df.to_excel(writer,sheet_name=x)
        print("output "+x+" to file")
    else:
        summary_df.to_excel(writer,sheet_name=x[:30])
        print("output "+x[:30]+" to file")

writer.save()
