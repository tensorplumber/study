import warnings
from sklearn.utils import all_estimators
from sklearn.svm import LinearSVR
import numpy as np
import datetime as dt 
import pandas as pd
from collections import Counter
import datetime as dt
from sqlalchemy import asc
# from keras.models import Sequential, Model
# from keras.layers import Activation, Dense, Conv2D, Flatten, MaxPooling2D, Input, Dropout, Conv1D, MaxPool1D
from sklearn.model_selection import train_test_split,KFold,cross_val_score,GridSearchCV,RandomizedSearchCV
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.preprocessing import MaxAbsScaler, RobustScaler

###########################폴더 생성시 현재 파일명으로 자동생성###########################################
import inspect, os
a = inspect.getfile(inspect.currentframe()) #현재 파일이 위치한 경로 + 현재 파일 명
print(a)
print(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))) #현재 파일이 위치한 경로
print(a.split("\\")[-1]) #현재 파일 명
current_name = a.split("\\")[-1]
##########################밑에 filepath경로에 추가로  + current_name + '/' 삽입해야 돌아감#######################


#1. 데이터
path = 'C:/Users/aiapalm/OneDrive - KNOU/beat/study/_data/kaggle_house/'
train_set = pd.read_csv(path + 'train.csv') # + 명령어는 문자를 앞문자와 더해줌  index_col=n n번째 컬럼을 인덱스로 인식
            
test_set = pd.read_csv(path + 'test.csv') # 예측에서 쓸거임  3

###################### IQR 이용해서 train_set에서 이상치나온 행 삭제########################
def detect_outliers(df, n, features):
    outlier_indices = []
    for col in features:
        Q1 = np.percentile(df[col], 25)
        Q3 = np.percentile(df[col], 75)
        IQR = Q3 - Q1
        
        outlier_step = 1.5 * IQR
        
        outlier_list_col = df[(df[col] < Q1 - outlier_step) | (df[col] > Q3 + outlier_step)].index
        outlier_indices.extend(outlier_list_col)
    outlier_indices = Counter(outlier_indices)
    multiple_outliers = list(k for k, v in outlier_indices.items() if v > n)
        
    return multiple_outliers
        
Outliers_to_drop = detect_outliers(train_set, 2, ['MSSubClass', 'LotFrontage', 'LotArea', 'OverallQual',
       'OverallCond', 'YearBuilt', 'YearRemodAdd', 'MasVnrArea', 'BsmtFinSF1',
       'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', '1stFlrSF', '2ndFlrSF',
       'LowQualFinSF', 'GrLivArea', 'BsmtFullBath', 'BsmtHalfBath', 'FullBath',
       'HalfBath', 'BedroomAbvGr', 'KitchenAbvGr', 'TotRmsAbvGrd',
       'Fireplaces', 'GarageYrBlt', 'GarageCars', 'GarageArea', 'WoodDeckSF',
       'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea',
       'MiscVal', 'MoSold', 'YrSold'])


train_set.loc[Outliers_to_drop]


train_set = train_set.drop(Outliers_to_drop, axis = 0).reset_index(drop=True)
train_set.shape

print(train_set)
#############################################################################



# 수치형 변수와 범주형 변수 찾기
numerical_feats = train_set.dtypes[train_set.dtypes != "object"].index
categorical_feats = train_set.dtypes[train_set.dtypes == "object"].index
numerical_feats_ = test_set.dtypes[test_set.dtypes != "object"].index
categorical_feats_ = test_set.dtypes[test_set.dtypes == "object"].index
# print("Number of Numberical features: ", len(numerical_feats)) # 37
# print("Number of Categorical features: ", len(categorical_feats)) # 43


# # ##############변수명 출력
# print(train_set[numerical_feats].columns)      
# print("*"*79)
# print(train_set[categorical_feats].columns)      
# print(test_set[numerical_feats_].columns)      
# print("*"*79)
# print(test_set[categorical_feats_].columns)   

# ###################범주형변수값 수치형으로 변환###############
# train_set_encoded = train_set.drop(numerical_feats,axis=1)
# print(train_set_encoded)

# test_set_encoded = test_set.drop(numerical_feats_,axis=1)
# print(test_set_encoded)

# le = LabelEncoder()

# train_set_encoded.loc[:,:] = \
# train_set_encoded.loc[:,:].apply(LabelEncoder().fit_transform)    

# print(train_set_encoded)

# train_set = pd.concat([train_set_encoded, train_set.loc[:,numerical_feats]], axis=1)

# print(train_set)

# test_set_encoded.loc[:,:] = \
# test_set_encoded.loc[:,:].apply(LabelEncoder().fit_transform)    

# print(test_set_encoded)

# test_set = pd.concat([test_set_encoded, test_set.loc[:,numerical_feats_]], axis=1)

# print(test_set)

#################긁어온거####################################

num_strong_corr = ['SalePrice','OverallQual','TotalBsmtSF','GrLivArea','GarageCars',
                   'FullBath','YearBuilt','YearRemodAdd']

num_weak_corr = ['MSSubClass', 'LotFrontage', 'LotArea', 'OverallCond', 'MasVnrArea', 'BsmtFinSF1',
                 'BsmtFinSF2', 'BsmtUnfSF', '1stFlrSF', '2ndFlrSF','LowQualFinSF', 'BsmtFullBath',
                 'BsmtHalfBath', 'HalfBath', 'BedroomAbvGr', 'KitchenAbvGr', 'TotRmsAbvGrd',
                 'Fireplaces', 'GarageYrBlt', 'GarageArea', 'WoodDeckSF','OpenPorchSF',
                 'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MiscVal', 'MoSold', 'YrSold']

catg_strong_corr = ['MSZoning', 'Neighborhood', 'Condition2', 'MasVnrType', 'ExterQual',
                    'BsmtQual','CentralAir', 'Electrical', 'KitchenQual', 'SaleType']

catg_weak_corr = ['Street', 'Alley', 'LotShape', 'LandContour', 'Utilities', 'LotConfig', 
                  'LandSlope', 'Condition1',  'BldgType', 'HouseStyle', 'RoofStyle', 
                  'RoofMatl', 'Exterior1st', 'Exterior2nd', 'ExterCond', 'Foundation', 
                  'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2', 'Heating', 
                  'HeatingQC', 'Functional', 'FireplaceQu', 'GarageType', 'GarageFinish', 
                  'GarageQual', 'GarageCond', 'PavedDrive', 'PoolQC', 'Fence', 'MiscFeature', 
                  'SaleCondition' ]

cols_fillna = ['PoolQC','MiscFeature','Alley','Fence','MasVnrType','FireplaceQu',
               'GarageQual','GarageCond','GarageFinish','GarageType', 'Electrical',
               'KitchenQual', 'SaleType', 'Functional', 'Exterior2nd', 'Exterior1st',
               'BsmtExposure','BsmtCond','BsmtQual','BsmtFinType1','BsmtFinType2',
               'MSZoning', 'Utilities']

for col in cols_fillna : 
    train_set[col].fillna('None', inplace=True)
    test_set[col].fillna('None', inplace=True)

total = train_set.isnull().sum().sort_values(ascending=False)
percent = (train_set.isnull().sum()/train_set.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total','Percent'])

train_set.fillna(train_set.mean(), inplace=True)
test_set.fillna(test_set.mean(), inplace=True)

total = train_set.isnull().sum().sort_values(ascending=False)
percent = (train_set.isnull().sum()/train_set.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])

print(train_set.isnull().sum().sum(), test_set.isnull().sum().sum()) # 0 0 출력시 결측치 확인 끝

id_test = test_set['Id']

to_drop_num = num_weak_corr
to_drop_catg = catg_weak_corr

cols_to_drop = ['Id'] + to_drop_num + to_drop_catg

for df in [train_set, test_set] :
    df.drop(cols_to_drop, inplace=True, axis = 1)
    
# 'MSZoning'
msz_catg2 = ['RM', 'RH']
msz_catg3 = ['RL', 'FV'] 

# Neighborhood
nbhd_catg2 = ['Blmngtn', 'ClearCr', 'CollgCr', 'Crawfor', 'Gilbert', 'NWAmes', 'Somerst', 'Timber', 'Veenker']
nbhd_catg3 = ['NoRidge', 'NridgHt', 'StoneBr']

# Condition2
cond2_catg2 = ['Norm', 'RRAe']
cond2_catg3 = ['PosA', 'PosN'] 

# SaleType
SlTy_catg1 = ['Oth']
SlTy_catg3 = ['CWD']
SlTy_catg4 = ['New', 'Con']

for df in [train_set, test_set]:
    
    df['MSZ_num'] = 1  
    df.loc[(df['MSZoning'].isin(msz_catg2) ), 'MSZ_num'] = 2    
    df.loc[(df['MSZoning'].isin(msz_catg3) ), 'MSZ_num'] = 3        
    
    df['NbHd_num'] = 1       
    df.loc[(df['Neighborhood'].isin(nbhd_catg2) ), 'NbHd_num'] = 2    
    df.loc[(df['Neighborhood'].isin(nbhd_catg3) ), 'NbHd_num'] = 3    

    df['Cond2_num'] = 1       
    df.loc[(df['Condition2'].isin(cond2_catg2) ), 'Cond2_num'] = 2    
    df.loc[(df['Condition2'].isin(cond2_catg3) ), 'Cond2_num'] = 3    
    
    df['Mas_num'] = 1       
    df.loc[(df['MasVnrType'] == 'Stone' ), 'Mas_num'] = 2 
    
    df['ExtQ_num'] = 1       
    df.loc[(df['ExterQual'] == 'TA' ), 'ExtQ_num'] = 2     
    df.loc[(df['ExterQual'] == 'Gd' ), 'ExtQ_num'] = 3     
    df.loc[(df['ExterQual'] == 'Ex' ), 'ExtQ_num'] = 4     
   
    df['BsQ_num'] = 1          
    df.loc[(df['BsmtQual'] == 'Gd' ), 'BsQ_num'] = 2     
    df.loc[(df['BsmtQual'] == 'Ex' ), 'BsQ_num'] = 3     
 
    df['CA_num'] = 0          
    df.loc[(df['CentralAir'] == 'Y' ), 'CA_num'] = 1    

    df['Elc_num'] = 1       
    df.loc[(df['Electrical'] == 'SBrkr' ), 'Elc_num'] = 2 


    df['KiQ_num'] = 1       
    df.loc[(df['KitchenQual'] == 'TA' ), 'KiQ_num'] = 2     
    df.loc[(df['KitchenQual'] == 'Gd' ), 'KiQ_num'] = 3     
    df.loc[(df['KitchenQual'] == 'Ex' ), 'KiQ_num'] = 4      
    
    df['SlTy_num'] = 2       
    df.loc[(df['SaleType'].isin(SlTy_catg1) ), 'SlTy_num'] = 1  
    df.loc[(df['SaleType'].isin(SlTy_catg3) ), 'SlTy_num'] = 3  
    df.loc[(df['SaleType'].isin(SlTy_catg4) ), 'SlTy_num'] = 4 

train_set.drop(['MSZoning','Neighborhood' , 'Condition2', 'MasVnrType', 'ExterQual', 'BsmtQual','CentralAir', 'Electrical', 'KitchenQual', 'SaleType', 'Cond2_num', 'Mas_num', 'CA_num', 'Elc_num', 'SlTy_num'], axis = 1, inplace = True)
test_set.drop(['MSZoning', 'Neighborhood' , 'Condition2', 'MasVnrType', 'ExterQual', 'BsmtQual','CentralAir', 'Electrical', 'KitchenQual', 'SaleType', 'Cond2_num', 'Mas_num', 'CA_num', 'Elc_num', 'SlTy_num'], axis = 1, inplace = True)


##############################긁어온거끝################################

x = train_set.drop(['SalePrice'], axis=1)
y = train_set['SalePrice']

x_train, x_test, y_train, y_test = train_test_split(x,y,
                                                    train_size=0.75,
                                                    random_state=984
                                                    )
warnings.filterwarnings('ignore')                                                    
allAlgorithms = all_estimators(type_filter='regressor')
n_splits = 5
kfold = KFold(n_splits=n_splits,random_state=278346,shuffle=True)
from sklearn.experimental import enable_halving_search_cv
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, cross_val_score,GridSearchCV, StratifiedKFold,RandomizedSearchCV,HalvingGridSearchCV,HalvingRandomSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import make_pipeline, Pipeline
pipe = Pipeline([('minmax',MinMaxScaler()),('RF',RandomForestRegressor())],verbose=2)
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import GridSearchCV,RandomizedSearchCV,HalvingGridSearchCV,HalvingRandomSearchCV,KFold,StratifiedKFold
parameters = [
     {'RF__n_estimators':[100,200],'RF__max_depth':[1,3,5,10]},
     {'RF__max_depth':[6,8,12],'RF__min_samples_leaf':[23,41,22]},
     {'RF__min_samples_leaf':[3,5,7,10],'RF__min_samples_split':[1,2,3,5]},
     {'RF__min_samples_split':[2,3,5,10],'RF__n_estimators':[400,20]},
     {'RF__n_jobs':[-1,2,4],'RF__n_estimators':[159,12,23],'RF__min_samples_leaf':[6,1,80],'RF__min_samples_split':[17,13,19]}
]
n_splits = 10
kfold = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=328947)
from xgboost import XGBClassifier,XGBRegressor
from sklearn.ensemble import VotingClassifier,VotingRegressor
from sklearn.linear_model import LogisticRegression,LinearRegression
from sklearn.neighbors import KNeighborsClassifier,KNeighborsRegressor
from lightgbm import LGBMClassifier,LGBMRegressor
from catboost import CatBoostClassifier,CatBoostRegressor
from sklearn.metrics import r2_score,accuracy_score
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)
lr = LinearRegression()
knn = KNeighborsRegressor(n_neighbors=8)
xg = XGBRegressor()
lg = LGBMRegressor()
cat = CatBoostRegressor(verbose=0)


model = VotingRegressor(estimators=[
    ('LR',lr),
    ('KNN',knn),
    ('XG',xg),
    ('LG',lg),
    ('CAT',cat)],
                         )
classifier = [lr,knn,xg,lg,cat]
for model2 in classifier:
    model2.fit(x_train,y_train)
    pred = model2.predict(x_test)
    score2 = r2_score(y_test,pred)
    class_name = model2.__class__.__name__
    print('{0} 정확도: {1:.4f}'.format(class_name,score2))
    

# model = GridSearchCV(pipe, parameters,cv=kfold,verbose=2)
import time
start = time.time()
model.fit(x_train,y_train)
print(time.time()-start)
print(model.score(x_test,y_test))


# RandomForestRegressor(n_estimators=400)
# 150
# {'n_estimators': 400, 'min_samples_split': 2}
# 0.8732144041661855

# xgb
# 0.1439981460571289
# 0.8191567880152726

# baggin100 xgb
# 8.921124458312988
# 0.8545199965612442

# voting
# LinearRegression 정확도: 0.8443
# KNeighborsRegressor 정확도: 0.8278
# XGBRegressor 정확도: 0.8186
# LGBMRegressor 정확도: 0.8466
# CatBoostRegressor 정확도: 0.8584

# voting 
# 2.0082178115844727
# 0.8637773161801086