# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import timeit
from math import sqrt
import threading
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
data_Churn_new = data_Churn.ix[:,1:-1]
#%%
class myThread (threading.Thread):
    def __init__(self, my_range, data, r,index):
        threading.Thread.__init__(self)
        self.my_range = my_range
        self.data = data
        self.index = index
        self.r = r
    def run(self):
        result = np.empty(shape = [len(self.my_range), len(self.data)])
        for i in self.my_range:
             s1= self.data.ix[i,:]
             temp = np.empty(shape = [len(self.my_range), len(self.data)])
             for j in range(len(self.data)):
                 s2 = self.data.ix[j,:]
                 LB_sum=0
                 for ind,k in enumerate(s1):
        
                    lower_bound=min(s2[(ind-self.r if ind-self.r >=0 else 0):(ind+self.r)])
                    upper_bound=max(s2[(ind-self.r if ind-self.r>=0 else 0):(ind+self.r)])
        
                    if k>upper_bound:
                        LB_sum=LB_sum+(k-upper_bound)**2
                    elif k<lower_bound:
                        LB_sum=LB_sum+(k-lower_bound)**2
             temp[0,j] = sqrt(LB_sum)
             result = np.append(result, np.array(temp), axis=0)
        score = pd.DataFrame(data = result)
        score.to_csv(out_path +str(self.index).zfill(3) + "thread.txt", mode = "a", header = None, index = False)
#%%
start = timeit.default_timer()


length_data = range(10)
#length_data = range(len(data_t5))
data_split = np.array_split(length_data,10)

threads = []
for index, item in enumerate(data_split, start=0):
    threads.append(myThread(item, data_Churn_new,20,index))

for t in threads:
    t.start()
for t in threads:
    t.join()
stop = timeit.default_timer()
        
print stop - start
print "Exiting Main Thread"
#%%
df = pd.read_csv("/data/tv/out_put_Lanh/000thread.txt", header = None)