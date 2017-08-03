# -*- coding: utf-8 -*-
#%%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
DIR = "/home/kieukhanh/workspace/data/"
#%% Churn
train = pd.read_csv(DIR + "trainT345.csv")
trainChurn = train[train["Churn"] == True]
trainChurn["Sum"] = trainChurn.ix[:, 1:29].sum(axis = 1)
trainChurn = trainChurn[trainChurn["Sum"] > 0].reset_index()
trainChurn = trainChurn.drop(trainChurn.columns[-3], axis = 1)
trainChurn = trainChurn.drop(trainChurn.columns[-1], axis = 1)
trainChurn = trainChurn.drop(trainChurn.columns[0], axis = 1)
#%%
trainChurn.ix[0:0, 1:29]
#%% Active
train = pd.read_csv(DIR + "trainT345.csv")
trainActive = train[train["Churn"] == False]
trainActive["Sum"] = trainActive.ix[:, 1:29].sum(axis = 1)
trainActive = trainActive[trainActive["Sum"] > 0].reset_index()
trainActive = trainActive.drop(trainActive.columns[-3], axis = 1)
trainActive = trainActive.drop(trainActive.columns[-1], axis = 1)
trainActive = trainActive.drop(trainActive.columns[0], axis = 1)
#%% AGNES
from sklearn.cluster import AgglomerativeClustering
cluster_model = AgglomerativeClustering(n_clusters = 6, affinity = "cosine", linkage = "average", 
                                        memory = "/home/kieukhanh/workspace/data/cluster_cache")
cluster_model.fit(trainChurn.ix[:,1:29])
cluster = pd.DataFrame(data=cluster_model.labels_, columns = ["cluster"], index = trainChurn["CustomerId"]).reset_index()
test = trainChurn[trainChurn["CustomerId"].isin(cluster["CustomerId"])]
test = test.merge(cluster, on = "CustomerId")
print test["cluster"].value_counts()
#%%
from sklearn.cluster import AgglomerativeClustering
#cluster_model = AgglomerativeClustering(n_clusters = 6, affinity = "cosine", linkage = "average", 
#                                        memory = "/home/kieukhanh/workspace/data/cluster_cache")
temp= cluster_model.fit_predict(trainActive.ix[390000:, 1:29])
cluster_Active = pd.DataFrame(data=cluster_model.labels_, columns = ["cluster"], index = trainActive.ix[390000:,:]["CustomerId"]).reset_index()
test = trainActive[trainActive["CustomerId"].isin(cluster_Active["CustomerId"])]
test = test.merge(cluster_Active, on = "CustomerId")
print test["cluster"].value_counts()
#%%
#DIR_Active = DIR + "clusterCosin/Active/39/"
#for i in range(6):
#    test[test['cluster'] == i].to_csv(DIR_Active + 'trainAcive_' + str(i) + '.csv', index = False)
#    
#visualize = pd.read_csv(DIR_Active + "trainAcive_0.csv")
#data = pd.melt(visualize, id_vars=['CustomerId', 'Churn'], value_vars=[str(i) for i in range(28)], var_name='Daily', value_name='Time')
#sns_plot = sns.factorplot(data=data, x='Daily', y='Time', hue='Churn', order=[str(i) for i in range(28)])
#plt.ylim(0, 16000)
#sns_plot.savefig(DIR_Active + "0.png", dpi=200)    
#
#visualize = pd.read_csv(DIR_Active + "trainAcive_1.csv")
#data = pd.melt(visualize, id_vars=['CustomerId', 'Churn'], value_vars=[str(i) for i in range(28)], var_name='Daily', value_name='Time')
#sns_plot = sns.factorplot(data=data, x='Daily', y='Time', hue='Churn', order=[str(i) for i in range(28)])
#plt.ylim(0, 16000) 
#sns_plot.savefig(DIR_Active + "1.png", dpi=200)
#
#visualize = pd.read_csv(DIR_Active + "trainAcive_2.csv")
#data = pd.melt(visualize, id_vars=['CustomerId', 'Churn'], value_vars=[str(i) for i in range(28)], var_name='Daily', value_name='Time')
#sns_plot = sns.factorplot(data=data, x='Daily', y='Time', hue='Churn', order=[str(i) for i in range(28)])
#plt.ylim(0, 16000) 
#sns_plot.savefig(DIR_Active + "2.png", dpi=200)
#
#visualize = pd.read_csv(DIR_Active + "trainAcive_3.csv")
#data = pd.melt(visualize, id_vars=['CustomerId', 'Churn'], value_vars=[str(i) for i in range(28)], var_name='Daily', value_name='Time')
#sns_plot = sns.factorplot(data=data, x='Daily', y='Time', hue='Churn', order=[str(i) for i in range(28)])
#plt.ylim(0, 16000) 
#sns_plot.savefig(DIR_Active + "3.png", dpi=200)
#
#visualize = pd.read_csv(DIR_Active + "trainAcive_4.csv")
#data = pd.melt(visualize, id_vars=['CustomerId', 'Churn'], value_vars=[str(i) for i in range(28)], var_name='Daily', value_name='Time')
#sns_plot = sns.factorplot(data=data, x='Daily', y='Time', hue='Churn', order=[str(i) for i in range(28)])
#plt.ylim(0, 16000) 
#sns_plot.savefig(DIR_Active + "4.png", dpi=200)
#
#visualize = pd.read_csv(DIR_Active + "trainAcive_5.csv")
#data = pd.melt(visualize, id_vars=['CustomerId', 'Churn'], value_vars=[str(i) for i in range(28)], var_name='Daily', value_name='Time')
#sns_plot = sns.factorplot(data=data, x='Daily', y='Time', hue='Churn', order=[str(i) for i in range(28)])
#plt.ylim(0, 16000) 
#sns_plot.savefig(DIR_Active + "5.png", dpi=200)                    

#%%
score_clu = {
    1: pd.read_csv("/data/Score_Clu1/score_clu1.txt", header = None),
    2: pd.read_csv("/data/Score_Clu2/score_clu2.txt", header = None),
    3: pd.read_csv("/data/Score_Clu3/score_clu3.txt", header = None),
    4: pd.read_csv("/data/Score_Clu4/score_clu4.txt", header = None),
    5: pd.read_csv("/data/Score_Clu5/score_clu5.txt", header = None),
}
score_clu_mean = {}
score_clu_min = {}
score_clu_max = {}
#%%
for i in score_clu:
    score_clu_mean.update({i: score_clu[i].mean(axis=1)})
    score_clu_min.update({i: score_clu[i].min(axis=1)})
    score_clu_max.update({i: score_clu[i].max(axis=1)})

#%%
import pandas as pd
DIR_Act = "/home/kieukhanh/workspace/data/clusterCosin/Active/"
#%%
trainActive = {
    1: pd.read_csv(DIR_Act + "trainActive_1.csv"),
    2: pd.read_csv(DIR_Act + "trainActive_2.csv"),
    3: pd.read_csv(DIR_Act + "trainActive_3.csv"),
    4: pd.read_csv(DIR_Act + "trainActive_4.csv"),
    5: pd.read_csv(DIR_Act + "trainActive_5.csv"),
}

for i in trainActive:
    df = trainActive[i]
    df['Min'] = score_clu_min[i]
    df['Max'] = score_clu_max[i]
    df['Mean'] = score_clu_mean[i]
#%%
trainActive_0 = pd.read_csv(DIR_Act + "trainActive_0.csv")
#%%

#%%

#for i in range(6):
#    test[test['cluster'] == i].to_csv(DIR + "clusterCosin/T6_Clu6/" + 'trainChurn_' + str(i) + '.csv', index = False)
#%%
#import matplotlib.pyplot as plt
#train = pd.read_csv(DIR + "clusterCosin/T6_Clu6/" + "trainChurn_5.csv")
#data = pd.melt(train, id_vars=['CustomerId', 'Churn'], value_vars=[str(i) for i in range(28)], var_name='Daily', value_name='Time')
#sns_plot = sns.factorplot(data=data, x='Daily', y='Time', hue='Churn', order=[str(i) for i in range(28)])
#plt.ylim(0, 70000) 
#sns_plot.savefig("/home/kieukhanh/workspace/data/clusterCosin/T6_Clu6/abc555.png", dpi=200)
#%%
#trainChurn_2 = pd.read_csv(DIR + "clusterCosin/T4_Clu10/" + "trainChurn_2.csv")
#trainChurn_3 = pd.read_csv(DIR + "clusterCosin/T4_Clu10/" + "trainChurn_3.csv")
#trainChurn_3 = pd.concat([trainChurn_3, trainChurn_2], ignore_index = True)
#trainChurn_3.to_csv(DIR + "clusterCosin/T1/" + "trainChurn_3m2.csv", index = False)

