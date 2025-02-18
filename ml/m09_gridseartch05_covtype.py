parameters=  [
     {'n_estimators':[100,200],'max_depth':[1,3,2,5,10]},
     {'max_depth':[6,8,10,12],'min_samples_leaf':[1234,23,41,22]},
     {'min_samples_leaf':[3,5,7,10],'min_samples_split':[1,23,24,2,3,5]},
     {'min_samples_split':[2,3,5,10],'n_estimators':[400,20]},
     {'n_jobs':[-1,2,4],'n_estimators':[159,1278,2345,1234],'min_samples_leaf':[6,1,80],'min_samples_split':[1795,13947,149875,19387]}
]
from random import random
import tensorflow as tf
tf.random.set_seed(137)
import numpy as np
from sklearn.datasets import fetch_covtype
#1.데이터
datasets = fetch_covtype()
x = datasets.data
y = datasets.target
# print(y)
# print(x.shape, y.shape)
# print(np.unique(y, return_counts=True))
# (581012, 54) (581012,)
# (array([1, 2, 3, 4, 5, 6, 7]), array([211840, 283301,  35754,   2747,   9493,  17367,  20510],
#       dtype=int64))
# from sklearn.preprocessing import OneHotEncoder
# encoder = OneHotEncoder()
# encoder.fit(y)
# y = encoder.transform(y).toarray()

# print(y)
# print(x.shape, y.shape)
from sklearn.utils import all_estimators
from sklearn.model_selection import train_test_split,cross_val_score,KFold,GridSearchCV
from sklearn.ensemble import RandomForestClassifier
allAlgorithms = all_estimators(type_filter='classifier')
kfold = KFold(shuffle=True, random_state=23876, n_splits=5)
x_train, x_test, y_train, y_test = train_test_split(x,y, train_size=0.7, shuffle=True, random_state=137)
import time
start =time.time()
model = GridSearchCV(RandomForestClassifier(),parameters,cv=kfold,n_jobs=-1,refit=True)
model.fit(x_train,y_train)
print(model.best_estimator_)
print(model.best_index_)
print(model.best_params_)
print(model.best_score_)
print(model.best_estimator_.predict(x_test))
print(time.time()-start,'cho')
