# -*- coding: utf-8 -*-
## Loai UserActive max_score >=0.8
## Visualine tập data vector days mới
import pandas as pd
import glob
import timeit 
path =r'/data/output_Lanh/Group'
allFiles = glob.glob(path + "/*.txt")
import matplotlib.pyplot as plt
import seaborn as sns
#%%
#df2 = pd.read_csv("/data/output_Lanh/Group/result9.txt",header = None )
#df = pd.concat([df1, df2], ignore_index = None)
#df1["maxscore"] = df1.ix[:,:].max(axis =1)
#df1 = df1["maxscore"]
#%%
def fc_maxscore (allfiles):
    result = []
    for file in allfiles:
        start = timeit.default_timer() 
        tmp = start
        df = pd.read_csv(file,index_col=None, header = None)
        print "load file " + str(timeit.default_timer()- start)
        start = timeit.default_timer() 
        df["maxscore"] = df.ix[:,:].max(axis = 1)
        df["meanscore"] = df.ix[:,:-1].mean(axis = 1)
        df["sumscore"] = df.ix[:,:-2].sum(axis =1)
        df = df[["maxscore", "meanscore", "sumscore"]]
        print "tinh toan" + str(timeit.default_timer()- start)
        start = timeit.default_timer()
        if (len(result) ==0):
            result = df
        else:
            result = pd.concat([df, result], ignore_index = None)
        print "noi table" + str(timeit.default_timer()- start)
        df = 0
        print "total" + str(timeit.default_timer()- tmp)
    result.to_csv("/data/output_Lanh/Final_score/" +"max_mean_sum00"+ ".csv", index = False)
#%% 
#start = timeit.default_timer()        
fc_maxscore(allFiles)
#stop = timeit.default_timer()
#print stop- start
print "Finish"
#%%
df_score = pd.read_csv("/data/output_Lanh/Final_score/max_mean_sum.csv")
data_t5 = pd.read_csv("/data/tv/bf_only_vectordays/t5.csv")
data_ActT5 = data_t5[data_t5["Churn"] == False]
#%% Merge score
data_mergeAct = pd.merge(data_ActT5, df_score,right_index= True, left_index = True)
data_mergeAct.to_csv("/data/output_Lanh/Final_score/data_Actt5_score" + ".csv", index = False)
#%% Data_Churn
data_ChurnT5 = data_t5[data_t5["Churn"] == True]

data_t4 = pd.read_csv("/data/tv/bf_only_vectordays/t4.csv")
data_ChurnT4 = data_t4[data_t4["Churn"] == True]

data_t3 = pd.read_csv("/data/tv/bf_only_vectordays/t3.csv")
data_ChurnT3 = data_t3[data_t3["Churn"] == True]

data_Churn  = pd.concat([data_ChurnT5, data_ChurnT3, data_ChurnT4],ignore_index = True)
#%%DATA_BEFORE SCORE
data_train_days = pd.concat([data_mergeActe, data_Churn], ignore_index = True)
#%%DATA_MAXSCORE
Active_maxscore = data_mergeAct[data_mergeAct["maxscore"] < 0.9]
Churn_maxscore = data_mergeAct[data_mergeAct["maxscore"]>= 0.9]
Churn_maxscore = Churn_maxscore.replace(False, True)
data_Churn = pd.concat([Churn_maxscore.ix[:,0:-2],data_Churn],ignore_index = True)
data_days_maxscore = pd.concat([Active_maxscore.ix[:,0:-2], data_Churn], ignore_index = True)
test_Churn = data_days_maxscore[data_days_maxscore["Churn"]== True]
#%% DATA_MEANSCORE
Active_meanscore = data_mergeAct[data_mergeAct["meanscore"] < 0.3]
Churn_meanscore = data_mergeAct[data_mergeAct["meanscore"] >= 0.3]
Churn_meanscore = Churn_meanscore.replace(False,True)
data_Churn = pd.concat([Churn_meanscore.ix[:,0:-2],data_Churn],ignore_index = True)
data_days_meanscore = pd.concat([Active_meanscore.ix[:,0:-2], data_Churn], ignore_index = True)
test_Churnmean = data_days_meanscore[data_days_meanscore["Churn"]== True]
test_Activemean = data_days_meanscore[data_days_meanscore["Churn"]== False]
#%% DATA_SUMSCORE


#%% VISUALIZE
# BEFORE SCORE
col_fist = data_train_days.columns.values.tolist()[1:29]
beta = data_train_days.groupby("Churn").boxplot(column = col_fist)
#%%%-----------
data_before = pd.melt(data_train_days, id_vars = ["CustomerId","Churn"],
                      value_vars=[str(i) for i in range(28)], var_name ="Days", value_name = 'Time')
plt.figure(figsize=(20,10))
sns.factorplot(data=data_before, x='Days', y='Time', hue='Churn', order=[str(i) for i in range(28)])
#%%
# ------VISULINZE ---MAXSCORE
col = data_days_maxscore.columns.values.tolist()[1:29]
alpha = data_days_maxscore.groupby("Churn").boxplot(column = col)
#%%
data_max = pd.melt(data_days_maxscore,id_vars = ["CustomerId","Churn"], value_vars = [str(i) for i in range(28)],
                   var_name = "Days", value_name = 'Time')
plt.figure(figsize = (15,10))
sns.factorplot(data = data_max, x = "Days", y = "Time", hue = "Churn", order = [str(i) for i in range(28)])
#%%
#___ VISUALINE ---- MEANSCORE
col2 = data_days_meanscore.columns.values.tolist()[1:29]
alpha2 = data_days_meanscore.boxplot(column = col)
#%%
data_mean = pd.melt(data_days_meanscore, id_vars = ["CustomerId", "Churn"], value_vars = [str(i) for i in range(28)],
                    var_name = "Days", value_name = "Time")
plt.figure(figsize = (30,20))
sns.factorplot(data = data_mean, x = "Days", y = "Time", hue = "Churn", order = [str(i) for i in range(28)])

#%%
sns.set(style='white')
ax = sns.boxplot(data = data, x='Daily', y='Time', hue = "Churn", order=[str(i) for i in range(28)], orient = "v", palette = "Set2", fliersize=0)
plt.legend(loc='upper center')
plt.ylim(0, 70000)
#%%

