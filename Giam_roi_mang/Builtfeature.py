# -*- coding: utf-8 -*-
import pandas as pd
DIR = "/data/tv/"
#%%
feature = ['CustomerId', "mean_Hourly", 'mean_Daily', 
           'IPTV', 'IPTV', 'SPORT', 'PAY_TOTAL', 'SERVICE', 
           'LOGID_TIMESHIFT', 'LOGID_PAY', 'LOGID_SERVICE', 'LOGID_UTIL_IPTV', 
           'LOGID_UTIL_VOD', 'LOGID_UTIL_SPORT', 
           'ReuseCount', 'ReuseAvg', 'ReuseMax', 'DayActive', 'Churn']
#%%
uAct = pd.read_csv(DIR + "support_data/userActive_t3.csv" ,parse_dates = ["Date"], 
                  infer_datetime_format = True, dayfirst=True)
uAct["Churn"] = False 
#%%
uChu = pd.read_csv(DIR + "support_data/userChurn_t3.csv" ,parse_dates = ["Date", "StopDate"], 
                  infer_datetime_format = True, dayfirst=True)
uChu["Churn"] = True
#%%
uChu_addT2 = pd.read_csv(DIR + "support_data/userChurn_t2.csv" ,parse_dates = ["Date", "StopDate"], 
                  infer_datetime_format = True, dayfirst=True)
uChu_addT2["Churn"] = True     
##uChu_addT3 = pd.read_csv(DIR + "support_data/userChurn_t3.csv" ,parse_dates = ["Date", "StopDate"], 
##                  infer_datetime_format = True, dayfirst=True)
##uChu_addT3["Churn"] = True 
##uChu_addT4 = pd.read_csv(DIR + "support_data/userChurn_t4.csv" ,parse_dates = ["Date", "StopDate"], 
##                  infer_datetime_format = True, dayfirst=True)
##uChu_addT4["Churn"] = True  
##        
uChu = pd.concat([uChu,uChu_addT2], ignore_index=True)
#%%----------BUILD FEATURE DAYS
raw = pd.read_csv(DIR + "t3/vectorDays.csv")
raw = raw.replace("null", "0", regex = True)
raw_uAct = raw[raw["CustomerId"].isin(uAct["CustomerId"])]
raw_uChu = raw[raw["CustomerId"].isin(uChu["CustomerId"])]

vector_days = pd.concat([raw_uAct,raw_uChu], ignore_index = True)
#%% ------- BUILD FEATURE Tiem
raw = pd.read_csv(DIR + "t3/vectorHourly.csv")
raw = raw.replace("null", "0", regex=True)
raw = raw[raw.columns.values].astype(int)
raw["mean_Hourly"] = raw.ix[:,1:].mean(axis=1).astype(int)

raw_uAct = raw[raw["CustomerId"].isin(uAct["CustomerId"])]
raw_uChu = raw[raw["CustomerId"].isin(uChu["CustomerId"])]

raw = pd.concat([raw_uAct,raw_uChu], ignore_index = True)

vector_hourly = raw[["CustomerId", "mean_Hourly"]]
#%%---------BUILD VECTOR APP
raw = pd.read_csv(DIR + "t3/vectorApp.csv")
raw = raw.replace("null", "0", regex=True)
raw = raw[raw.columns.values].astype(int)

raw["VOD_TOTAL"] = raw[["VOD","CHILD","RELAX"]].sum(axis = 1)
raw["PAY_TOTAL"] = raw[["BHD","FIMs"]].sum(axis = 1)

vector_app = raw[["CustomerId", "IPTV", "VOD_TOTAL", "SPORT", "PAY_TOTAL", "SERVICE"]]
#%% BUILD FEATURE LOGID 
raw = pd.read_csv(DIR + "t3/logIdCount.csv")
raw = raw.replace("null", "0", regex=True)
raw = raw[raw.columns.values].astype(int)

raw["LOGID_TIMESHIFT"] = raw[["43", "46"]].sum(axis = 1)
raw["LOGID_PAY"] = raw[["411", "132", "151"]].sum(axis = 1)
raw["LOGID_SERVICE"] = raw[["81", "110"]].sum(axis = 1)
raw["LOGID_UTIL_IPTV"] = raw[["413", "414"]].sum(axis = 1)
raw["LOGID_UTIL_VOD"] = raw[["58"]].sum(axis = 1)
raw["LOGID_UTIL_SPORT"] = raw[["69"]].sum(axis = 1)

raw_uAct = raw[raw["CustomerId"].isin(uAct["CustomerId"])]
raw_uChu = raw[raw["CustomerId"].isin(uChu["CustomerId"])]
raw_logID = pd.concat([raw_uAct, raw_uChu])

vector_logID = raw_logID[["CustomerId","LOGID_TIMESHIFT", "LOGID_PAY", "LOGID_SERVICE", "LOGID_UTIL_IPTV",
                          "LOGID_UTIL_SPORT", "LOGID_UTIL_VOD"]]
#%%--,BUILD Feature daily
raw_Daily = pd.read_csv(DIR +"t3/vectorDaily.csv")
raw_uAct = raw_Daily[raw_Daily["CustomerId"].isin(uAct["CustomerId"])]
raw_uAct['mean_Daily'] = raw_uAct.ix[:,1:].mean(axis=1).astype(int)
raw_uChu = raw_Daily[raw_Daily["CustomerId"].isin(uChu["CustomerId"])]
raw_uChu["mean_Daily"] = raw_uChu.ix[:,1:].mean(axis =1).astype(int)

raw_daily = pd.concat([raw_uChu, raw_uAct])
vector_Daily = raw_daily[["CustomerId", "mean_Daily"]]
#%%
import seaborn as sns
sns.set(style="white")
time = ["Mon", "Tue", "Wed", "Thu", "Fri","Sat", "Sun"]
#g = sns.factorplot( data = raw_Daily,
#                   palette="BuPu", size=6, aspect=1.5, order=time)
#g.set_xticklabels(step=2)

uAct_Daily2 = pd.melt(raw_uAct, id_vars=['CustomerId'], value_vars=time, var_name='DailyTime')

#g = sns.factorplot(x='DailyTime', y='value', kind='bar', data = raw_Daily3, palette="BuPu")
g = sns.barplot(x='DailyTime', y='value', data = uAct_Daily2, palette="BuPu")
uChu_Daily2 = pd.melt(raw_uChu, id_vars = "CustomerId",value_vars = time, var_name = 'DailyTime')
g = sns.barplot(x='DailyTime', y='value', data = uChu_Daily2, palette="BuPu")
#%%------- BUILD FEATURE REUSETIME
raw = pd.read_csv(DIR + "t3/returnUse.csv")
raw = raw.replace("null", "0", regex=True)


raw_uAct = raw[raw["CustomerId"].isin(uAct["CustomerId"])]
raw_uChu = raw[raw["CustomerId"].isin(uChu["CustomerId"])]
raw_returnUse = pd.concat([raw_uAct,raw_uChu])
vector_Resuetime = raw_returnUse[["CustomerId", "ReuseCount", "ReuseAvg", "ReuseMax"]]
#%%---BUIL DATA
data = pd.merge(vector_days, vector_app, on="CustomerId", how = "inner")
#data = pd.merge(vector_hourly, vector_app, on = "CustomerId", how = "inner")
data = pd.merge(data, vector_logID, on = "CustomerId", how = "inner")
data = pd.merge(data, vector_Resuetime, on = "CustomerId", how = "inner")
#data = pd.merge(data, vector_Daily, on = "CustomerId", how = "inner")

active = pd.merge(data, uAct[["CustomerId", "DayActive", "Churn"]], on = "CustomerId", how = "inner")
churn = pd.merge(data, uChu[["CustomerId", "DayActive", "Churn"]], on = "CustomerId", how = "inner")             
data = pd.concat([active, churn], ignore_index = True)
#%%
data.to_csv("/data/tv/bm_vectordays/t3.csv", index = False)