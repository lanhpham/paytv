import numpy as np
import pandas as pd
import timeit
from fastdtw import dtw,fastdtw
from scipy.spatial.distance import *
#%%
out_path = "/data/tv/output_Lanh/"
data_Churn = pd.read_csv("/data/tv/Cluster_Cosine/T6_Clu6/trainChurn_0.csv")
data_Churn = data_Churn.ix[:,1:-2]
#%%
#temp = np.empty(shape = [1, len(data_Churn)])
#x = data_Churn.ix[0,1:-2]
#x = np.array(x).reshape(1,-1)
#y = np.array(data_Churn.ix[:,])
#y =np.array(y).reshape(1,-1)
#t = dtw(x, y,dist= cosine)[0]
#%%
class myThread (threading.Thread):
    def __init__(self, my_range, data,y, index):
        threading.Thread.__init__(self)
        self.my_range = my_range
        self.data = data
        self.y = y
        self.index = index
    def run(self):
        temp = np.empty(shape = [self.len(my_shape), self.len(my_shape)])
        y = self.y
        for i in self.my_range:
            x =  self.data.ix[i,:]
            x = np.array(x).reshape(1,-1)
            distance = dtw(x, y,dist= cosine)[0]
            score = pd.DataFrame(data = distance[0:,0:])
            score.to_csv(out_path +str(self.index).zfill(3) + "thread.txt", mode = "a", header = None, index = False)
    
start = timeit.default_timer()
y = np.array(data_Churn.ix[:,:])


length_data = range(100)
#length_data = range(len(data_Churn))
data_split = np.array_split(length_data,100)

threads = []
for index, item in enumerate(data_split, start=0):
    threads.append(myThread(item, data_Churn, y, index))

for t in threads:
    t.start()
for t in threads:
    t.join()
stop = timeit.default_timer()
        
print stop - start
print "Exiting Main Thread"