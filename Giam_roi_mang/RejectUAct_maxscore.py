# -*- coding: utf-8 -*-
## Loai UserActive max_score >=0.8
## Visualine tập data vector days mới
import pandas as pd
import glob
import timeit 
path =r'/data/output_Lanh/Group'
allFiles = glob.glob(path + "/*.txt")
#%%
#df1 = pd.read_csv("/data/output_Lanh/Group/result10.txt",header = None )
#print df1.columns.values
#df2 = pd.read_csv("/data/output_Lanh/Group/result9.txt",header = None )
#df = pd.concat([df1, df2], ignore_index = None)
#df1["maxscore"] = df1.ix[:,:].max(axis =1)
#df1 = df1["maxscore"]
#%%
def fc_maxscore (allfiles):
    result = []
    for file in allfiles:
        df = pd.read_csv(file,index_col=None, header = None)
        df["maxscore"] = df.ix[:,:].max(axis =1)
        df["meanscore"] = df.ix[:,:-1].mean(axis =1)
        df = df[["maxscore", "meanscore"]]
        if (len(result) ==0):
            result = df
        else:
            result = pd.concat([df, result], ignore_index = None)
    result.to_csv("/data/output_Lanh/Final_score/" +"max_meanscore1"+ ".csv", index = False)
#%% 
start = timeit.default_timer()        
fc_maxscore(allFiles)
stop = timeit.default_timer()
print stop- start
print "Finish"
#%%
df_score = pd.read_csv("/data/output_Lanh/Final_score/max_meanscore.csv")
data_t5 = pd.read_csv("/data/tv/bf_only_vectordays/t5.csv")
data_ActT5 = data_t5[data_t5["Churn"] == False]
a = data_ActT5[["CustomerId"]]
data_merge = pd.merge(data_ActT5[["CustomerId"]], df_score,right_index= True, left_index = True)
    