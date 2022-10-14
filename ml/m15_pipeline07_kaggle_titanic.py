import tensorflow as tf
from sklearn.model_selection import train_test_split,cross_val_score,KFold,RandomizedSearchCV
from sklearn.utils import all_estimators
from sklearn.metrics import accuracy_score
import numpy as np
import warnings
import pandas as pd
warnings.filterwarnings('ignore')
path = 'c:/study/_data/kaggle_titanic/'
train_set = pd.read_csv(path + 'train.csv', index_col=0)
train_set = train_set.dropna()
test_set = pd.read_csv(path + 'test.csv', index_col=0)
test_set = test_set.dropna()
x = train_set.drop(['Survived','Name', 'Ticket', 'Cabin','Sex','Embarked'], axis=1)
y = train_set['Survived']

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.7, random_state=137)

n_splits = 5
kfold = KFold(random_state=234,shuffle=True,n_splits=n_splits)
from sklearn.experimental import enable_halving_search_cv
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold, cross_val_score,GridSearchCV, StratifiedKFold,RandomizedSearchCV,HalvingGridSearchCV,HalvingRandomSearchCV
parameters = [
     {'n_estimators':[100,200],'max_depth':[1,3,2,5,10]},
     {'max_depth':[6,8,10,12],'min_samples_leaf':[1234,23,41,22]},
     {'min_samples_leaf':[3,5,7,10],'min_samples_split':[1,23,24,2,3,5]},
     {'min_samples_split':[2,3,5,10],'n_estimators':[400,20]},
     {'n_jobs':[-1,2,4],'n_estimators':[159,1278,2345,1234],'min_samples_leaf':[6,1,80],'min_samples_split':[1795,13947,149875,19387]}
]
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler
model = make_pipeline(MinMaxScaler(),RandomForestClassifier)
# model =  HalvingGridSearchCV(RandomForestClassifier(),parameters,cv=kfold,refit=True,n_jobs=-1,verbose=1)
# model =  HalvingRandomSearchCV(RandomForestClassifier(),parameters,cv=kfold,refit=True,n_jobs=-1,verbose=1)
import time
start = time.time()
model.fit(x_train,y_train)
print(time.time()-start)
# predict = model.best_estimator_.predict(x_test)
# print(predict)
# print(model.best_estimator_)
# print(model.best_index_)
# print(model.best_params_)
# print(model.best_score_)
print(model.score(x_test))