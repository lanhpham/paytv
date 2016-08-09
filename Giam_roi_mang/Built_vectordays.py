import pandas as pd
import numpy as np
#%%--THAY THE THANG 3,4,5.
vectorDays = pd.read_csv("/data/tv/t6/vectorDays.csv")
uAct_t6 = pd.read_csv("/data/tv/support_data/userActive_t6.csv")
uChur_t6 = pd.read_csv("/data/tv/support_data/userChurn_t6.csv")
df_t6= pd.concat([uAct_t6, uChur_t6], ignore_index = True)

df_t6days = pd.merge(vectorDays, df_t6[["CustomerId","Churn"]], on = "CustomerId", how = "inner")
#%%---Write data_t6_vectordays
df_t6days.to_csv("data/tv/bf_only_vectordays/t6.csv)
#%%
days_Act = df_t6days[df_t6days["Churn"] == False]
days_Chur = df_t6days[df_t6days["Churn"] == True]
#%%
