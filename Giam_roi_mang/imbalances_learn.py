import numpy as np
import pandas as pd
import timeit
from fastdtw import dtw,fastdtw
from scipy.spatial.distance import *
import multiprocessing

#%%
class myThread (multiprocessing.Process):
    def __init__(self, my_range, data_Act,data_Churn, index):
        super(myThread, self).__init__()
        self.my_range = my_range
        self.data_Act = data_Act
        self.data_Churn = data_Churn
        self.index = index
    def run(self):
        result = np.empty(shape = [len(self.my_range), len(self.data_Churn)])
        row = 0
        for i in self.my_range:
            x =  self.data_Act.ix[i,:]
            x = np.array(x).reshape(1,-1)
            for j in range(len(self.data_Churn)):
                y =  self.data_Churn.ix[j,:]
                y = np.array(y).reshape(1,-1)
                distance = dtw(x, y,dist= cosine)[0]
                result[row,j] = distance
            row = row + 1
        score = pd.DataFrame(data = result)
        score.to_csv(out_path +str(self.index).zfill(3) + "thread.txt", header = None, index = False)
if __name__ == '__main__':   
    start = timeit.default_timer()
    out_path = "/data/user/lanhpth/output_Lanh/dtw_test_T6/"
    path_read = "/data/user/lanhpth/bf_only_vectordays/"
    data_t6 = pd.read_csv(path_read+"t6_fillter.csv")
#    data_Act = data_t5[data_t5["Churn"] == False]
    data_Act = data_t6.ix[:,1:-2]
    data_t5 = pd.read_csv(path_read+"t5_fillter.csv")
    data_ChurnT5 = data_t5[data_t5["Churn"] == True]
    data_t4 = pd.read_csv(path_read+"t4_fillter.csv")
    data_ChurnT4 = data_t4[data_t4["Churn"] == True]
    
    data_t3 = pd.read_csv(path_read +"t3_fillter.csv")
    data_ChurnT3 = data_t3[data_t3["Churn"] == True]
    
    data_Churn  = pd.concat([data_ChurnT5, data_ChurnT3, data_ChurnT4],ignore_index = True)
#    data_Churn = pd.read_csv(path_read+"trainChurn_0.csv")
    data_Churn = data_Churn.ix[:,1:-1]
    length_data = range(100)
    length_data = range(len(data_Act))
#    data_split = np.array_split(length_data,100)
    
    threads = []
    for index, item in enumerate(data_split, start=0):
        threads.append(myThread(item, data_Act,data_Churn, index))
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    stop = timeit.default_timer()
            
    print stop - start
    print "Exiting Main Thread"
#%%
