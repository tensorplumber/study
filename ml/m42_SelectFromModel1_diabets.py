from inspect import Parameter
from sklearn.datasets import load_breast_cancer, load_diabetes
from sklearn.model_selection import GridSearchCV,KFold,StratifiedKFold,train_test_split
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from xgboost import XGBClassifier,XGBRegressor
import time
import numpy as np
from sklearn.feature_selection import SelectFromModel
import warnings
warnings.filterwarnings('ignore')
#1.data
datasets = load_diabetes()
x = datasets.data
y = datasets.target
print(x.shape, y.shape)

x_train, x_test, y_train, y_test = train_test_split(x,y,train_size=0.8,random_state=234,)

scaler = MinMaxScaler()
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=234)


# }
Parameters = {
    'n_estimators':[100],
    'learning_rate':[0.1],
    'max_depth':[None],
    'gamma': [0],  
    'min_child_weight':[5], 
    'subsample':[1], #디폴트1 0~1
    'colsample_bytree':[0.1], 
    'colsample_bylevel':[1], 
    'colsample_bynode':[1], 
    'reg_alpha':[0], # l1 정규화 절대값으로 exploding 방지 0~inf/ alpha라고해도됨 디폴트0
    # 'reg_lambda':[0,0.1,0.001,0.00000001,100,10000,100000] # l2 정규화 제곱으로 exploding 방지 0~inf 디폴트1 lambda
}

#2.모델
model = XGBRegressor(random_state=238,n_estimators=1000,
                      learning_rate=0.1,
                      max_depth=3,
                      gemma=1,tree_method='gpu_hist',predictor='gpu_predictor',gpu_id=0)

# model = GridSearchCV(xgb,Parameters,cv=kfold,n_jobs=-1)

start = time.time()
model.fit(x_train,y_train, early_stopping_rounds=10,eval_set=[(x_test,y_test)],
          eval_metric='error',#다중분류나 회귀모델에 따라 다르다rmse error merror\
        #   eval_set = )
)
end = time.time()

# print('params',model.best_params_)
# print('score',model.best_score_)
print('time',end-start)
print('score',model.score(x_test,y_test))
from sklearn.metrics import r2_score
print(r2_score(y_test,(model.predict(x_test))))
print(model.feature_importances_)
# [0.0252094  0.         0.20542233 0.0806317  0.08252231 0.04732746
#  0.03902517 0.         0.46862164 0.05123999]

thresholds = model.feature_importances_
print(f'====================')
for thresh in thresholds:
    selection = SelectFromModel(model, threshold=thresh,prefit=True)
    
    selec_x_train = selection.transform(x_train)
    selec_x_test = selection.transform(x_test)
    print(selec_x_train.shape, selec_x_test.shape)

    model2 = XGBRegressor(n_jobs=-1,random_state=238,n_estimators=1000,
                      learning_rate=0.1,
                      max_depth=3,
                      gemma=1,tree_method='gpu_hist',predictor='gpu_predictor',gpu_id=0)
    
    model2.fit(selec_x_train,y_train)
    y_pred = model2.predict(selec_x_test)
    score = r2_score(y_test,y_pred)
    print("thresh=%.3f, n=%d, r2: %.2f%%"
          % (thresh, selec_x_train.shape[1],score*100))
