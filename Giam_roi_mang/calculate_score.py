# -*- coding: utf-8 -*-
import pandas as pd
import glob
import timeit 
import matplotlib.pyplot as plt
import os
import pandas as pd
import glob
import timeit 
import matplotlib.pyplot as plt
import os
#import seaborn as sns
#%%
#define variable
CHUNKSIZE = 1000
path =r'/Users/sondinh/Downloads/result'
output_path = '/Users/sondinh/Downloads/result/sum/result1.csv'
allFiles = glob.glob(path + "/*.txt")
#%%
#df2 = pd.read_csv("/data/output_Lanh/Group/result9.txt",header = None )
#df = pd.concat([df1, df2], ignore_index = None)
#df1["maxscore"] = df1.ix[:,:].max(axis =1)
#df1 = df1["maxscore"]
#%%
def fc_maxscore (allfiles):
    count = 0
    start = timeit.default_timer()
    for myfile in allfiles:
        
        for df in pd.read_csv(myfile, index_col=None, header = None, iterator = True, chunksize=CHUNKSIZE):
            
            count = count + 1
      
            df["maxscore"] = df.ix[:,:].max(axis = 1).round(3)
            df["meanscore"] = df.ix[:,:-1].mean(axis = 1)
            df["sumscore"] = df.ix[:,:-2].sum(axis =1)
            result = df[["maxscore", "meanscore", "sumscore"]]
            # if file does not exist write header 
            result.to_csv(output_path, mode = 'a',index = False)
    stop = timeit.default_timer()
    print count
    print stop - start

#%% 
fc_maxscore(allFiles)
print "Finish"
