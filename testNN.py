
from sklearn.neural_network import BernoulliRBM
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score,classification_report, confusion_matrix
from sklearn.naive_bayes import GaussianNB
from sklearn import datasets, metrics
#%%
dfTrain = pd.read_csv('/data/tv/bm_vectordays/t5.csv', sep= ',')
#%%
X_train = dfTrain.ix[:, 1:29]
Y_train = dfTrain.ix[:, -1]
#%%
dfTest = pd.read_csv('/data/tv/bm_vectordays/t6.csv', sep = ',')
#%%
X_test = dfTest.ix[:,1:29]
Y_test = dfTest.ix[:, -1]
#%%Scale feature : (x_i -X_min)/(x_max-X_min)
from sklearn.preprocessing import MinMaxScaler
mms = MinMaxScaler()
X_train_norm = mms.fit_transform(X_train)
X_test_norm = mms.transform(X_test)
#%cale feature: Standard
from sklearn.preprocessing import StandardScaler
stdsc = StandardScaler()
X_train_std = stdsc.fit_transform(X_train)
X_test_std = stdsc.transform(X_test)
#%%
import matplotlib.pyplot as plt
plt.scatter(X_train,Y_train,marker='s',s=50)
#%%
import theano 
theano.config.floatX = 'float32'
#%%
X_train = X_train.as_matrix().astype(theano.config.floatX) 
#%%
X_test = X_test.as_matrix().astype(theano.config.floatX)

#%%
from keras.utils import np_utils

#%%
y_train = np_utils.to_categorical(Y_train)
#%%
y_test = np_utils.to_categorical(Y_test)
#print(y_test[368532])
#%%
print(y_train.shape[1])
print (X_train_std.shape[1])
#%%
from keras.models import Sequential
from keras.layers.core import Dense
from keras.optimizers import SGD
#%%
np.random.seed(1) 
model = Sequential()
#first layer
model.add(Dense(input_dim=X_train.shape[1], output_dim=50, init = 'uniform',activation='tanh',bias = True))
#%%
model.add(Dense(input_dim=50,output_dim=50,init = 'uniform', activation='tanh', bias = True))
#%%
#model.add(Dense(input_dim=50, output_dim = 25,init = 'uniform',activation = 'tanh', bias = True))
#%%
model.add(Dense(input_dim=50, output_dim=y_train.shape[1], init = 'uniform', activation='softmax'))
sgd = SGD(lr=0.001, decay=1e-5, momentum=.9)
model.compile(loss='categorical_crossentropy', optimizer=sgd)

#%%
layer = model.layers

print layer
#%%
weight = model.get_weights()
print weight
#%%
model.fit(X_train, y_train, nb_epoch=50,  batch_size=300, verbose=0, validation_split=0.1, 
          show_accuracy=True)
          
#%%
print (theano.config.floatX)
print (theano.config.device)
#%%
from sklearn.metrics import accuracy_score, confusion_matrix

y_train_pred = model.predict_classes(X_train, verbose=0)
accS = accuracy_score(Y_train, y_train_pred)
conf = confusion_matrix(Y_train, y_train_pred)
#%%
y_test_pred = model.predict_classes(X_test, verbose=0)
y_train_pred = model.predict_classes(X_test, verbose=0)
accSTest = accuracy_score(Y_test, y_test_pred)
confTest = confusion_matrix(Y_test, y_test_pred)
#%%
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
fig = plt.figure()
ax = plt.subplot(111)
colors = ['blue', 'green', 'red', 'cyan',
            'magenta', 'yellow', 'black',
            'pink', 'lightgreen', 'lightblue',
            'gray', 'indigo', 'orange']
weights, params = [], []
for c in np.arange(-4, 6):
    lr = LogisticRegression(penalty='l1',
                            C=10**c,
                            random_state=0)
    lr.fit(X_train, y_train)
    weights.append(lr.coef_[1])
    params.append(10**c)
    weights = np.array(weights)
for column, color in zip(range(weights.shape[1]), colors):
    plt.plot(params, weights[:, column],
    label=df_wine.columns[column+1],
    color=color)
plt.axhline(0, color='black', linestyle='--', linewidth=3)
plt.xlim([10**(-5), 10**5])
plt.ylabel('weight coefficient')
plt.xlabel('C')
plt.xscale('log')
plt.legend(loc='upper left')
ax.legend(loc='upper center',
          bbox_to_anchor=(1.38, 1.03),
          ncol=1, fancybox=True)
plt.show()