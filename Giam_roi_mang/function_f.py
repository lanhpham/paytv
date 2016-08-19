import numpy as np
from scipy.spatial.distance import *
from fastdtw import fastdtw
import pandas as pd
import matplotlib.pyplot as plt
#%%
x = np.array(arr[[1,1], [2,2], [3,3], [4,4], [5,5]])
y = np.array([[-1,-1], [-2,-2], [-3,-3], [-4,-4], [-5,-5]])
distance, path = fastdtw(x, y, dist= euclidean)
print distance
print path/home/honglanh/workspace/data/tv/t3.csv
#%%
Churn_clus_1 = pd.read_csv("/data/tv/Cluster_Cosine/T6_Clu6/trainChurn_1.csv")
Act_clus_1 = pd.read_csv("/data/tv/Cluster_Cosine/Train_Active/trainActive_1.csv")
#%%
dayChurn_clus = Churn_clus_1.ix[:,1:-2]
dayChurn_clus = dayChurn_clus.T
dayChurn_clus['time'] = [int(i) for i in range(28)]
#%%
dayAct_clus = Act_clus_1.ix[:,1:-2]
dayAct_clus = dayAct_clus.T
dayAct_clus['time'] = [int(i) for i in range(28)]
#%%
result = np.empty(shape = [len(Act_clus_1), len(Churn_clus_1)])
for i in range(len(dayAct_clus)):
    x = pd.concat([dayAct_clus["time"],dayAct_clus[i]], axis =1)
    x = np.array(x)
    for j in range(len(dayChurn_clus)):
        y = pd.concat([dayAct_clus["time"],dayAct_clus[j]], axis =1)
        y = np.array(y)
        distance, path = fastdtw(x, y, dist= cosine)
        result.append(distance)
#%%  
