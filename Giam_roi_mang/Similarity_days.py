# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import threading
import timeit
#%%
data_t6 = pd.read_csv("/data/tv/bf_only_vectordays/t6.csv")
#data_t6.columns.values[1:29]
data_t6["Sum"] = data_t6.ix[:,1:29].sum(axis = 1)
data_t6 = data_t6[data_t6.ix[:,1:29].sum(axis = 1) > 0].reset_index()
data_t6= data_t6.ix[:,1:29]

#%%
data_t5 = pd.read_csv("/data/tv/bf_only_vectordays/t5.csv")
data_t5 = data_t5[data_t5.ix[:,1:29].sum(axis = 1) > 0]
data_ChurnT5 = data_t5[data_t5["Churn"] == True]

data_t4 = pd.read_csv("/data/tv/bf_only_vectordays/t4.csv")
data_t4 = data_t4[data_t4.ix[:,1:29].sum(axis = 1) > 0]
data_ChurnT4 = data_t4[data_t4["Churn"] == True]

data_t3 = pd.read_csv("/data/tv/bf_only_vectordays/t3.csv")
data_t3 = data_t3[data_t3.ix[:,1:29].sum(axis = 1) > 0]
data_ChurnT3 = data_t3[data_t3["Churn"] == True]

data_Churn  = pd.concat([data_ChurnT5, data_ChurnT3, data_ChurnT4],ignore_index = True)
#%% ---Write data_train
#data_train_days = pd.concat([data_ActT5, data_Churn], ignore_index = True)
#data_train_days.to_csv("/data/tv/bf_only_vectordays/train_days.csv", index = False)
#%%
y = data_Churn.ix[:,1:29]
data_t6.reset_index(inplace = True)   
data_t6.drop('index',axis=1,inplace=True) 
arr = np.empty((0, len(y)), float)
for i in range(10):
    x =  data_t6.ix[i:i,:]
    result = cosine_similarity(x,y)
    arr = np.append(arr, np.array(result), axis=0)
#%%
#y = data_Churn.ix[:,1:29]
#arr = np.array([], float)
#for i in range(100):
#    x =  data_t6.ix[i:i,:]
#    result = cosine_similarity(x,y)
#    arr = np.append(arr, np.array(result), axis=0)

#%%
class myThread (threading.Thread):
    def __init__(self, my_range, data, y, index):
        threading.Thread.__init__(self)
        self.my_range = my_range
        self.data = data
        self.y = y
#        self.cond = threading.Condition()
#        self.done = False
        self.index = index
        self.arr = np.empty((0, len(y)), float)
    def run(self):
        y = self.y
        for i in self.my_range:
            x =  self.data.ix[i:i,:]
            #print cosine_similarity(x,y)
            result = cosine_similarity(x,y)
            self.arr = np.append(self.arr, np.array(result), axis=0)
#        self.done = True
#        self.cond.notify()
#        self.cond.release()
        score = pd.DataFrame(data = self.arr[0:,0:])
        score.to_csv("/data/user/lanhpth/output_lanh/result_thread" + str(self.index) +  ".txt" ,index = False)
start = timeit.default_timer()
y = data_Churn.ix[:,1:29]
arr = np.empty((0, len(y)), float)

#length_data = range(1000)
length_data = range(len(data_t6))
data_split = np.array_split(length_data,100)

threads = []
for index, item in enumerate(data_split, start=0):
    threads.append(myThread(item, data_t6, y, index))

for t in threads:
    t.start()
for t in threads:
    t.join()
stop = timeit.default_timer()
        
print stop - start
print "Exiting Main Thread"
# ------------Max Score
#score = pd.DataFrame(data = result[0:,0:])
#score.to_csv("/data/tv/bf_only_vectordays/score.csv",index = False)
#max_score =pd.DataFrame(score.ix[:,0:].max())
#max_score.columns = ['max_score']
#max_score['ID'] = pd.Series(list(range(len(max_score))))
#max_score.to_csv("/data/tv/bf_only_vectordays/max_score.csv")
##
#max_score.hist('max_score')
#max_score.plot(x='ID', y= 'max_score')
