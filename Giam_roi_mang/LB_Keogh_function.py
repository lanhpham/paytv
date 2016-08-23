# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import timeit
from math import *
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
#def LB_Keogh(s1,s2,r):
#    LB_sum=0
#    for ind,i in enumerate(s1):
#        
#        lower_bound=min(s2[(ind-r if ind-r>=0 else 0):(ind+r)])
#        upper_bound=max(s2[(ind-r if ind-r>=0 else 0):(ind+r)])
#        
#        if i>upper_bound:
#            LB_sum=LB_sum+(i-upper_bound)**2
#        elif i<lower_bound:
#            LB_sum=LB_sum+(i-lower_bound)**2
#    
#    return sqrt(LB_sum)
##%%
#start = timeit.default_timer()
#result = np.empty(shape = [len(data_Churn), len(data_Churn)])
#for i in range(len(data_Churn)-1):
#    x = data_Churn_new.ix[i,:]
#    for j in  range(i+1, len(data_Churn)) :
#        y = data_Churn_new.ix[j,:]
#        result[i,j] = LB_Keogh(x,y,20)
#stop = timeit.default_timer()
#print start - stop
#print "FINISH"
#result.to_csv(out_path + "cosine_distance_fasdtw.txt", header = None, index = False)
#%%
class myThread (threading.Thread):
    def __init__(self, my_range, data, r,index):
        threading.Thread.__init__(self)
        self.my_range = my_range
        self.data = data
        self.index = index
        self.r = r
    def run(self):
        result = np.empty(shape = [len(self.my_range), len(self.my_range)])        
        for i in self.my_range:
             s1= self.data.ix[i,:]
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
                 result[i,j] = sqrt(LB_sum)
        score = pd.DataFrame(data = result)
        score.to_csv(out_path +str(self.index).zfill(3) + "thread.txt", mode = "a", header = None, index = False)
#%%        
start = timeit.default_timer()


length_data = range(100)
#length_data = range(len(data_t5))
data_split = np.array_split(length_data,100)

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