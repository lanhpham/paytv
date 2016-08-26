import numpy as np
import pandas as pd
import timeit
from fastdtw import dtw,fastdtw
from scipy.spatial.distance import *
#%%
out_path = "/data/tv/out_put_Lanh/"
data_Churn = pd.read_csv("/data/tv/Cluster_Cosine/T6_Clu6/trainChurn_0.csv")
data_Churn = data_Churn.ix[:,1:-2]
#%%
for j in range(2):
temp = np.empty(shape = [1, len(data_Churn)])
x = data_Churn.ix[0,:]
x = np.array(x).reshape(1,-1)
for i in range(len(data_Churn)):
    y = np.array(data_Churn.ix[i,:]).reshape(1,-1)
    distance = dtw(x, y,dist= cosine)[0]
    temp[0,i] = distance

#%%
class myThread (threading.Thread):
    def __init__(self, my_range, data, index):
        threading.Thread.__init__(self)
        self.my_range = my_range
        self.data = data
        self.index = index
    def run(self):
        result = np.empty((len(self.my_range), len(self.data)))
        for i in self.my_range:
            x =  self.data.ix[i,:]
            x = np.array(x).reshape(1,-1)
            temp = np.empty(shape = [1, len(self.data)])
            for j in range(len(self.data)+1):
                y =  self.data.ix[i,:]
                y = np.array(x).reshape(1,-1)
                distance = dtw(x, y,dist= cosine)[0]
                temp[i,j] = distance
            result = np.append(result, np.array(temp), axis=1)
        score = pd.DataFrame(data = result)
        score.to_csv(out_path +str(self.index).zfill(3) + "thread.txt", header = None, index = False)
    
start = timeit.default_timer()
length_data = range(100)
#length_data = range(len(data_Churn))
data_split = np.array_split(length_data,100)

threads = []
for index, item in enumerate(data_split, start=0):
    threads.append(myThread(item, data_Churn, index))

for t in threads:
    t.start()
for t in threads:
    t.join()
stop = timeit.default_timer()
        
print stop - start
print "Exiting Main Thread"