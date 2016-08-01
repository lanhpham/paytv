import pandas as pd
import numpy as np

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
import seaborn as sns
time = []
for i in range(0,28):
    time.append(i)
test = pd.melt(days_Act, Id_vars = , value_vars = days_Act.mean())
#%%   
scale = df_t6days.ix[:,1:29]
from sklearn.preprocessing import MinMaxScaler
mms = MinMaxScaler()
X_scale = mms.fit_transform(scale)
#%%
day_id = [str(i) for i in range(28)]
day_meantime_Act = []

for i in day_id:
    mean = days_Act[i].mean()
    day_meantime_Act.append(mean)
day_meantime_Chur = []
for i in day_id:
    mean = days_Chur[i].mean()
    day_meantime_Chur.append(mean)
    
df_t6days_mean1 = pd.DataFrame({'Days': day_id, 'TimeMean_Act': day_meantime_Act,
                                'TimeMean_Churn' : day_meantime_Chur})
#%%
import matplotlib.pyplot as plt
plt.figure()
df_t6days_mean.plot.line(list('TimeMean_Act','TimeMean_Churn'))
#%%