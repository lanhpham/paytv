import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn import neighbors, datasets
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn import linear_model, datasets
#%%
def ft_map(df):
    df["DistFromCenter"] = np.sqrt(df["XCoord"]**2 + df["YCoord"]**2)
    class_mappling ={label:idx for idx,label in enumerate(np.unique(df["Competitor"]))}
    df["Competitor"] = df["Competitor"].map(class_mappling)
    return df
#%%
train_dataset = pd.read_csv("/home/lanhpth/Downloads/MLPB-master/Problems/Classify Dart Throwers/_Data/train.csv")
train_dataset = ft_map(train_dataset)
#%%
test_dataset = pd.read_csv("/home/lanhpth/Downloads/MLPB-master/Problems/Classify Dart Throwers/_Data/test.csv")
test_dataset = ft_map(test_dataset)
#%%
"""Split data_train into five folder"""
data_train_split = np.array_split(train_dataset,5)
testFold = []
trainFold = []
for i in range(0,5):
    testFold.append(data_train_split[i])
    train = pd.concat(data_train_split)
    train = train[~train["ID"].isin(data_train_split[i]["ID"])]
    trainFold.append(train)
#%%
"""Model KNN & SVM with  five folder"""
y_pred_KNN = []
y_pred_SVM = []
for i in range(0,5):
    X_train = trainFold[i][["XCoord","YCoord","DistFromCenter"]]
    y_train = trainFold[i][["Competitor"]]
    X_test = testFold[i][["XCoord","YCoord","DistFromCenter"]]
    y_test = testFold[i][["Competitor"]]
    clf_KNN = neighbors.KNeighborsClassifier(n_neighbors = 1, p = 2)
    clf_KNN.fit(X_train, y_train)
    y_pred_KNN.append(clf_KNN.predict(X_test))
####"""SVM_model""""
    clf_SVM = SVC(kernel = 'linear', C = 1e5) # just a big number 
    clf_SVM.fit(X_train,y_train)
    y_pred_SVM.append(clf_SVM.predict(X_test))
#%%
"""Model KNN & SVM full dataset"""
X = train_dataset[["XCoord","YCoord","DistFromCenter"]]
y = train_dataset[["Competitor"]]
X_test = test_dataset[["XCoord","YCoord","DistFromCenter"]]
y_test = test_dataset[["Competitor"]]
#%%%
clf_KNN = neighbors.KNeighborsClassifier(n_neighbors = 1, p = 2)
clf_KNN.fit(X, y)
y_pred_full_KNN = clf_KNN.predict(X_test)
acc_KNN = accuracy_score(y_test, y_pred_full_KNN)
#%%%
clf_SVM = SVC(kernel = 'linear', C = 1e5) # just a big number 
clf_SVM.fit(X_train,y_train)
y_pred_full_SVM = clf_SVM.predict(X_test)
acc_SVM = accuracy_score(y_test, y_pred_full_SVM)
#%%
"""BUILD DATATRAIN- DATATEST META"""
dataset_train_meta = train_dataset.copy()
dataset_train_meta["M1"] = np.concatenate(y_pred_KNN)
dataset_train_meta["M2"] = np.concatenate(y_pred_SVM)
dataset_test_meta = test_dataset.copy()
dataset_test_meta["M1"] = y_pred_full_KNN
dataset_test_meta["M2"] = y_pred_full_SVM
#%%
"""Model logistice-regression"""
X_train_meta = dataset_train_meta[["XCoord","YCoord","DistFromCenter","M1","M2"]]
y_train_meta = dataset_train_meta[["Competitor"]]
X_test_meta = dataset_test_meta[["XCoord","YCoord","DistFromCenter","M1","M2"]]
y_test_meta = dataset_test_meta[["Competitor"]]
logreg = linear_model.LogisticRegression(C=1e5)
logreg.fit(X_train_meta, y_train_meta)
Z = logreg.predict(X_test_meta)
acc_logreg = accuracy_score(y_test_meta,Z)
#%%