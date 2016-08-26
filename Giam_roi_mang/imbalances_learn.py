import numpy as np
import pandas as pd
import timeit
from fastdtw import dtw,fastdtw
from scipy.spatial.distance import *
import multiprocessing
#%%
out_path = "/data/tv/out_put_Lanh/"
data_Churn = pd.read_csv("/data/tv/Cluster_Cosine/T6_Clu6/trainChurn_0.csv")
data_Churn = data_Churn.ix[:,1:-2]
#%%
result = np.empty((2, len(data_Churn)))
for j in range(2):
    temp = np.empty(shape = [1, len(data_Churn)])
    x = data_Churn.ix[j,:]
    x = np.array(x).reshape(1,-1)
    for i in range(len(data_Churn)):
        y = np.array(data_Churn.ix[i,:]).reshape(1,-1)
        distance = dtw(x, y,dist= cosine)[0]
        temp[0,i] = distance
result = np.append(result, np.array(temp), axis=1)
#%%
class myThread (multiprocessing.Process):
    def __init__(self, my_range, data, index):
        super(myThread, self).__init__()
        self.my_range = my_range
        self.data = data
        self.index = index
    def run(self):
        result = np.empty(shape = [len(self.my_range), len(self.data)])
        for i in self.my_range:
            x =  self.data.ix[i,:]
            x = np.array(x).reshape(1,-1)
            for j in range(len(self.data)+1):
                y =  self.data.ix[i,:]
                y = np.array(x).reshape(1,-1)
                distance = dtw(x, y,dist= cosine)[0]
                result[i,j] = distance
        score = pd.DataFrame(data = result)
        score.to_csv(out_path +str(self.index).zfill(3) + "thread.txt", header = None, index = False)
if __name__ == '__main__':   
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
