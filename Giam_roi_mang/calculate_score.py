# -*- coding: utf-8 -*-
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
        df = pd.read_csv(file,index_col=None, header = None)
        df["maxscore"] = df.ix[:,:].max(axis = 1)
        df["meanscore"] = df.ix[:,:-1].mean(axis = 1)
        df["sumscore"] = df.ix[:,:-2].sum(axis =1)
        df = df[["maxscore", "meanscore", "sumscore"]]
        if (len(result) ==0):
            result = df
        else:
            result = pd.concat([df, result], ignore_index = None)
    result.to_csv("/data/output_Lanh/Final_score/" +"max_mean_sum00"+ ".csv", index = False)
#%% 
start = timeit.default_timer()        
fc_maxscore(allFiles)
stop = timeit.default_timer()
print stop- start
print "Finish"
