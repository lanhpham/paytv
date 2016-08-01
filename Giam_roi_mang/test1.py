# -*- coding: utf-8 -*-
import pandas as pd
import timeit
import glob
import threading
import numpy as np
path =r'/data/out_put'
allFiles = glob.glob(path + "/*.txt")
#%%
data = pd.DataFrame()
#mylist = []
#%%
#for file_ in allFiles:
#    df = pd.read_csv(file_,index_col=None, header= None)
    #maxscore = pd.DataFrame(df.ix[:,0:].max())
    #mylist.append(df)
    #data = pd.concat(df, ignore_index = True)
#%%
#maxscore  = pd.DataFrame(data.ix[:,0:].max())
#%%
#print len(allFiles)
#%%
class myThread(threading.Thread):
    def __init__(self, my_range, allFiles):
        threading.Thread.__init__(self)
        self.my_range = my_range
        self.allFiles = allFiles
        self.mylist = []
    def run(self):
        self.cond.acquire()
        for i in self.my_range:
            for j in self.allFiles:
                df = pd.read_csv(file_,index_col=None, header= None)
                self.list.append(df)
    def getResult(self):
        self.cond.acquire() # <--
        while not self.done: #  <--
            self.cond.wait()#  <--  We're waiting that self.done becomes True
        self.cond.release() #  <--
        return self.mylist
start = timeit.default_timer()        
length_data = range(len(allFiles))
data_split = np.array_split(length_data,10)

threads = []
for index, item in enumerate(data_split, start=0):
    threads.append(myThread(item, allFiles))
arr_result = []
# Start new Threads
for t in threads:
    t.start()
for t in threads:
    t.join()
for t in threads:
    arr_result.append(t.getResult())