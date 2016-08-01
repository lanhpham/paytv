# -*- coding: utf-8 -*-
import glob
import pandas as pd
import threading
import timeit
import numpy as np
path =r"/Users/sondinh/Downloads/bf_only_vectordays/group/" # use your path
allFiles = glob.glob(path + "/*.csv")
#%%
#for file_ in allFiles:
#    df = pd.read_csv(file_)
#    if len(result) == 0:
#        result = df
#    else:
#        result = pd.concat([df,result] )
class myThread(threading.Thread):
    def __init__(self, my_range, allFiles, index):
        threading.Thread.__init__(self)
        self.my_range = my_range
        self.allFiles = allFiles
        self.index = index
    def run(self):
        result = []
        for i in self.my_range:
            df = pd.read_csv(self.allFiles[i],index_col=None)
            if (len(result) == 0):
                result = df
            else:
                result = pd.concat([df,result],ignore_index = True)
        result.to_csv("/Users/sondinh/Downloads/bf_only_vectordays/sum/" + str(self.index) +  ".csv" ,index = False)    
start = timeit.default_timer()        
length_data = range(len(allFiles))
data_split = np.array_split(length_data,1)

threads = []
for index, item in enumerate(data_split, start=0):
    threads.append(myThread(item, allFiles, index))
arr_result = []
# Start new Threads
for t in threads:
    t.start()
for t in threads:
    t.join()
stop = timeit.default_timer()
print stop - start
print "Exiting Main Thread"
#%%
sum = pd.read_csv("/Users/sondinh/Downloads/bf_only_vectordays/sum/0.csv")
