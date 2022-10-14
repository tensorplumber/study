import numpy as np
import pandas as pd
from sklearn.datasets import load_boston, load_breast_cancer,fetch_covtype,load_wine,load_iris,load_digits
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split
#1. 데이터
datasets = fetch_covtype()
datasets = load_breast_cancer()
datasets = load_digits()
datasets = load_wine()
datasets = load_iris()
import xgboost as xg
print(xg.__version__)
x = datasets.data
y = datasets.target
print(x.shape) #(581012, 54)
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y = le.fit_transform(y)
print(np.unique(y))

# pca = PCA(n_components=3)
# x = pca.fit_transform(x)
# lda = LinearDiscriminantAnalysis(n_components = 2)
# lda.fit(x,y)
# x = lda.transform(x)
# pca_EVR = pca.explained_variance_ratio_
# cumsum = np.cumsum(pca_EVR)
# y = pd.get_dummies(y)
x_train, x_test, y_train, y_test = train_test_split(x,y, train_size=0.8,random_state=234,stratify=y)
print(np.unique(y_train,return_counts=True)) #(array([1, 2, 3, 4, 5, 6, 7]), array([169472, 226640,  28603,   2198,   7594,  13894,  16408],

#2.모델
from xgboost import XGBClassifier
model = XGBClassifier(verbose=2,tree_method='gpu_hist',predictor='gpu_predictor',gpu_id=0)

#3.훈련
import time
start = time.time()
model.fit(x_train, y_train)
print('시간',time.time()-start)
#4.평가 예측
result = model.score(x_test, y_test)
print('결과',result)

# x(150, 4)
# y[0 1 2]

# lda 2
# 시간 0.48270416259765625
# 결과 1.0

# pca 3
# 시간 0.5320522785186768
# 결과 0.9

# no pca lda
# 시간 0.5159707069396973
# 결과 0.9333333333333333