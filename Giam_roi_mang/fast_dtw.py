import numpy as np
import pandas as pd
import timeit
from fastdtw import fastdtw
from scipy.spatial.distance import *
#%%
path_read = "/data/tv/bf_only_vectordays/"
out_path = "/data/tv/out_put_Lanh/fastdtw/"
data_t5 = pd.read_csv(path_read+"t5_fillter.csv")
data_ChurnT5 = data_t5[data_t5["Churn"] == True]

data_t4 = pd.read_csv(path_read+"t4_fillter.csv")
data_ChurnT4 = data_t4[data_t4["Churn"] == True]

data_t3 = pd.read_csv(path_read +"t3_fillter.csv")
data_ChurnT3 = data_t3[data_t3["Churn"] == True]

data_Churn  = pd.concat([data_ChurnT5, data_ChurnT3, data_ChurnT4],ignore_index = True)
#%%
data_Churn_new = data_Churn.ix[:,1:-1]
data_Churn_new = data_Churn_new.T
data_Churn_new["time"] = range(1,29)
start = timeit.default_timer()
result = np.empty((0, len(data_Churn)), float)
for i in range(len(data_Churn)):
    x = pd.concat([data_Churn_new["time"],data_Churn_new.ix[:,i]], axis =1)
    x = np.array(x)
    temp = np.empty(shape = [1, len(data_Churn)])
    for j in range(len(data_Churn)):
        y = pd.concat([data_Churn_new["time"],data_Churn_new.ix[:,j]], axis =1)
        y = np.array(y)
        distance, path = fastdtw(x, y, dist= cosine)
        temp[0,j] = distance
    result = np.append(result, np.array(temp), axis=0)
score = pd.DataFrame(data = result)
score.to_csv(path_read + "cosine_r1.txt",header = None, index = False)
        
print stop - start
print "FINISH"
