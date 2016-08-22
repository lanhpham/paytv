import numpy as np
from scipy.spatial.distance import *
from fastdtw import fastdtw
import pandas as pd
import matplotlib.pyplot as plt
import timeit
import threading
#%%
#x = np.array([[1,1], [2,2], [3,3], [4,4], [5,5]])
#y = np.array([[2,2], [3,3], [4,4],[5,5]])
#distance, path = fastdtw(x, y, dist= cosine)
#print distance
#%%
path = "/data/tv/bf_only_vectordays/"
out_path = "/data/tv/out_put_Lanh/"
data_t5 = pd.read_csv(path+"t5_fillter.csv")
data_ChurnT5 = data_t5[data_t5["Churn"] == True]

data_t4 = pd.read_csv(path+"t4_fillter.csv")
data_ChurnT4 = data_t4[data_t4["Churn"] == True]

data_t3 = pd.read_csv(path +"t3_fillter.csv")
data_ChurnT3 = data_t3[data_t3["Churn"] == True]

data_Churn  = pd.concat([data_ChurnT5, data_ChurnT3, data_ChurnT4],ignore_index = True)
#%%
data_Churn_new = data_Churn.ix[:,1:-1]
data_Churn_new = data_Churn_new.T
data_Churn_new['time'] = [int(i) for i in range(1,29)]
#%%
#start = timeit.default_timer()
#for i in range(len(data_Churn)-1):
#    x = pd.concat([data_Churn_new["time"],data_Churn_new[i]], axis =1)
#    x = np.array(x)
#    for j in  range(i+1, len(data_Churn)) :
#        y = pd.concat([data_Churn_new["time"],data_Churn_new[j]], axis =1)
#        y = np.array(y)
#        distance, path = fastdtw(x, y, dist= euclidean)
#        result = distance
#        score = pd.DataFrame(data = result[0:,0:])
#        score.to_csv(out_path + "euclidean_distance_fastdtw.txt", mode = "a", header = None, index = False)
#        result[i,j] = distance
#stop = timeit.default_timer()
#print start - stop
#print "FINISH"
#%%
class myThread (threading.Thread):
    def __init__(self, my_range, data, index):
        threading.Thread.__init__(self)
        self.my_range = my_range
        self.data = data
#        self.cond = threading.Condition()
#        self.done = False
        self.index = index
#        self.arr = np.empty((0, len(y)), float)
    def run(self):
        for i in self.my_range:
            x =  pd.concat([self.data["time"],self.data[i]], axis =1)
            x = np.array(x)
            for j in self.my_range:
                y = pd.concat([self.data["time"],self.data[j]], axis =1)
                y = np.array(y)
                distance, path = fastdtw(x, y, dist= euclidean)
                result = distance
                score = pd.DataFrame(data = result[0:,0:])
                score.to_csv(out_path +str(self.index).zfill(3) + "thread.txt", mode = "a", header = None, index = False)
#%%
start = timeit.default_timer()
length_data = range(len(data_Churn_new))
data_split = np.array_split(length_data,10)

threads = []
for index, item in enumerate(data_split, start=0):
    threads.append(myThread(item, data_Churn_new, index))

for t in threads:
    t.start()
for t in threads:
    t.join()
stop = timeit.default_timer()
        
print stop - start
print "Exiting Main Thread"
                #%%
plt.plot(data_Churn_new.ix[:,8], 'b--')
plt.show()
#dayChurn_clus = Churn_clus_1.ix[:,1:-2]
#dayChurn_clus = dayChurn_clus.T
#dayChurn_clus['time'] = [int(i) for i in range(28)]
##%%
#dayAct_clus = Act_clus_1.ix[:,1:-2]
#dayAct_clus = dayAct_clus.T
#dayAct_clus['time'] = [int(i) for i in range(28)]
##%%
#result = np.empty(shape = [len(Act_clus_1), len(Churn_clus_1)])
#for i in range(len(dayAct_clus)):
#    x = pd.concat([dayAct_clus["time"],dayAct_clus[i]], axis =1)
#    x = np.array(x)
#    for j in range(len(dayChurn_clus)):
#        y = pd.concat([dayAct_clus["time"],dayAct_clus[j]], axis =1)
#        y = np.array(y)
#        distance, path = fastdtw(x, y, dist= cosine)
#        result= np.append(result,distance, axis = 0)
#%%  
