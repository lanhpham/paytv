# -*- coding: utf-8 -*-
## Loai UserActive max_score >=0.8
## Visualine tập data vector days mới
import pandas as pd
import glob
import timeit 
path =r'/data/output_Lanh/Group'
allFiles = glob.glob(path + "/*.csv")
#%%
#df1 = pd.read_csv("/data/output_Lanh/Group8/Group8.csv")
#df1["maxscore"] = df1.ix[:,:].max(axis =1)
#df1 = df1["maxscore"]
#%%
def fc_maxscore (allfiles):
    result = []
    for file in allfiles:
        df = pd.read_csv(file,index_col=None)
        df["maxscore"] = df.ix[:,:].max(axis =1)
        df["meanscore"] = df.ix[:,0:10812].mean(axis =1)
        df = df[["maxscore", "meanscore"]]
        if (len(result) ==0):
            result = df
        else:
            result = pd.concat([df, result], ignore_index = None)
    result.to_csv("/data/output_Lanh/Final_score/" +"max_meanscore"+ ".csv", index = False)
#%% 
start = timeit.default_timer()        
fc_maxscore(allFiles)
stop = timeit.default_timer()
print stop- start
print "Finish"
#%%