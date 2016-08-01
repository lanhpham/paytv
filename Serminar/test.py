# -*- coding: utf-8 -*-
from sklearn.preprocessing import Imputer
import pandas as pd
from io import StringIO
import numpy as np
csv_data = ''' A, B, C, D 
1.0,2.0,3.0,4.0
5.0,6.0,,8.0
10.0,11.0,12.0,'''
#%%
csv_data = unicode(csv_data)
df = pd.read_csv(StringIO(csv_data))
df.isnull().sum()
df.values
imr = Imputer(missing_values = "NaN", strategy = 'most_frequent', axis =0)
print imr
imr = imr.fit(df)
print imr
imputed_data = imr.transform(df.values)
#%%
df = pd.DataFrame([
['green', 'M', 10.1, 'class1'],
['red', 'L', 13.5, 'class2'],
['blue', 'XL', 15.3, 'class1']])
df.columns = ['color', 'size', 'price', 'classlabel']
size_mapping = {'XL':3, 'L' :2, 'M' :1}
df['size'] = df['size'].map(size_mapping) 
### reverse-mapping
inv_size_mapping = {v: k for k, v in size_mapping.items()}
#%%
from sklearn.ensemble import RandomForestClassifier
data_train_days.to_csv("/data/tv/bf_only_vectordays/train_days.csv", index = False)
feat_labels = data_train_days.columns[1:]
forest = RandomForestClassifier(n_estimators=10000,random_state=0,n_jobs=-1)
#%%
from sklearn.cross_validation import train_test_split
X, y = data_train_days.iloc[:,1:29].values,data_train_days.iloc[:,-1].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
#%%
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(penalty='l1', C=0.1)
lr.fit(X_train, y_train)
print('Training accuracy:', lr.score(X_train, y_train))
print('Test accuracy:', lr.score(X_test, y_test))
lr.intercept_
lr.coef_
#%%
text1 = pd.read_table("/data/out_put/result_thread_0.txt", header= 0)
