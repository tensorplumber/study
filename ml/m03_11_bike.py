#1.트레인 데이터 불러와서 결측치 확인 및 제거, 트레인과 테스트셋 나누기
from sklearn.svm import LinearSVR
import pandas as pd
from sklearn.metrics import mean_squared_error

#path 정의
path = 'c:/study/_data/kaggle_bike/'
train_set = pd.read_csv(path + 'train.csv', index_col=0)
print(train_set)
test_set = pd.read_csv(path + 'test.csv', index_col=0)
print(test_set)
#열이 3개차이 이므로 y값도 3개?
#결측치 확인




# train_set['datetime'] = pd.to_datetime(train_set['datetime'])
# train_set['datetime'].head()

print(train_set.dtypes)
'''
train_set['Year']=train_set['datetime'].dt.year
train_set['Month']=train_set['datetime'].dt.month
train_set['Day']=train_set['datetime'].dt.day
train_set['Hour']=train_set['datetime'].dt.hour
train_set['Minute']=train_set['datetime'].dt.minute
train_set['Second']=train_set['datetime'].dt.second
train_set[['datetime', 'Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']].head()
train_set['Dayofweek'] = train_set['datetime'].dt.dayofweek
train_set['Dayname'] = train_set['datetime'].dt.day_name()
train_set[['datetime', 'Dayofweek', 'Dayname']]
print(train_set)
import seaborn as sns
sns.barplot(data = train_set, x = 'Year', y = 'count')
import matplotlib.pyplot as plt
figure, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows = 2, ncols=2)
sns.barplot(data = train_set, x = 'Year', y = 'count', ax = ax1)
train_set.loc[train_set['Month'] == 2, ['Month', 'season']]

def new_season(month):
    if month in [3,4,5]:
        return 1
    elif month in [6,7,8,]:
        return 2
    elif month in [9,10,11]:
        return 3
    elif month in [12,1,2]:
        return 4
    
train_set['season'] = train_set['Month'].apply(new_season)
print(train_set[['Month', 'season']])

test_set['season'] = test_set['Month'].apply(new_season)
train_set.loc[train_set['weather'] == 4, 'weather'] =3
train_set[train_set['weather']==4]
test_set.loc[test_set['weather'] == 4, 'weather'] =3
test_set[test_set['weather']==4]

train_set = train_set.drop(['atemp'], axis=1)
features = ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second', 'workingday', 'weatger', 
            'temp', 'humidity', 'windspeed', 'Dayofweek']
from sklearn.ensemble import RandomForestRegressor()
model = RandomForestRegressor()

https://blog.naver.com/fkdldjs60/221969628347
'''
print(train_set.info())
#nonnull값
print(train_set.describe())
#평균 등 수치
print(train_set.isnull().sum())
#null값

print(test_set.info())

#null값은 없음

#dims값 date 제외 8

#x,y 나누기
train_set=train_set.dropna()
x = train_set.drop(['casual', 'registered', 'count'], axis=1)
y = train_set['count']

# print(x)
# print(y)


from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.9, shuffle=False)
from sklearn.svm import LinearSVR
from sklearn.preprocessing import MinMaxScaler, StandardScaler, MaxAbsScaler, RobustScaler
import numpy as np
# scaler = MinMaxScaler()
# scaler = StandardScaler()
scaler = MaxAbsScaler()
# scaler = RobustScaler()
scaler.fit(x_train)
# x_train = scaler.transform(x_train)
# x_test = scaler.transform(x_test)
print(np.min(x_train))
print(np.max(x_train))
print(np.min(x_test))
print(np.max(x_test))
# robust
# -2.0
# 4.4014745308310985
# -1.4838709677419355
# 3.001340482573726
# def tanh(q):
#     p_exp_q = np.exp(q)
#     m_exp_q = np.exp(-q)
    
#     u = (p_exp_q - m_exp_q)/(p_exp_q + m_exp_q)
#     return u

#트레인 테스트셋 나눴으므로 모델구성

from tensorflow.python.keras.models import Sequential, Model
from tensorflow.python.keras.layers import Dense, Input,Conv1D,MaxPool1D,Flatten
from tensorflow.python.keras.callbacks import ModelCheckpoint
import datetime as dt
date = dt.datetime.now()
date=date.strftime('%m%d %H%M')
filename = '{epoch:04d} {val_loss:.4f}.hdf5'
filepath = './_ModelCheckPoint/k25/10/'
mcp = ModelCheckpoint(filepath=([filepath,date,' ',filename]),monitor='val_loss', mode='auto', save_best_only=True)
# x_train=x_train.reshape(-1,4,2)
# x_test=x_test.reshape(-1,4,2)
# model = Sequential()
# model.add(Conv1D(100,1, input_shape=(4,2)))
# model.add(MaxPool1D())
# model.add(Flatten())
# model.add(Dense(200))
# model.add(Dense(200))
# model.add(Dense(200))
# model.add(Dense(200))
# model.add(Dense(200))
# model.add(Dense(1))
# model.summary()
# x컬럼 8개 필요 y값은 3개이므로
# Model: "sequential"
# _________________________________________________________________
#  Layer (type)                Output Shape              Param #
# =================================================================
#  dense (Dense)               (None, 100)               900

#  dense_1 (Dense)             (None, 200)               20200

#  dense_2 (Dense)             (None, 200)               40200

#  dense_4 (Dense)             (None, 200)               40200

#  dense_5 (Dense)             (None, 200)               40200

#  dense_6 (Dense)             (None, 1)                 201

# =================================================================
# Total params: 182,101
# Trainable params: 182,101
# Non-trainable params: 0

# input1 = Input(shape=(8,))
# dense1 = Dense(100)(input1)
# dense2 = Dense(200)(dense1)
# dense3 = Dense(200)(dense2)
# dense4 = Dense(200)(dense3)
# dense5 = Dense(200)(dense4)
# dense6 = Dense(200)(dense5)
# output1 = Dense(1)(dense6)
# model = Model(inputs=input1, outputs=output1)
# model.summary()
# Model: "model"
# _________________________________________________________________
#  Layer (type)                Output Shape              Param #
# =================================================================
#  input_1 (InputLayer)        [(None, 8)]               0

#  dense (Dense)               (None, 100)               900

#  dense_1 (Dense)             (None, 200)               20200

#  dense_2 (Dense)             (None, 200)               40200

#  dense_3 (Dense)             (None, 200)               40200

#  dense_4 (Dense)             (None, 200)               40200

#  dense_5 (Dense)             (None, 200)               40200

#  dense_6 (Dense)             (None, 1)                 201

# =================================================================
# Total params: 182,101
# Trainable params: 182,101
# Non-trainable params: 0

#3.컴파일 훈련

# model.compile(loss = 'mse', optimizer = 'adam')
# model.fit(x_train, y_train, epochs=2500, batch_size=200, verbose=1, validation_split=0.2)

#4.평가 예측

# loss = model.evaluate(x_test, y_test)
#트레인셋에서 빼온 x.y 테스트셋으로 평가해 로스율을 구한다
# print('loss', loss)
# model = LinearSVR()
from sklearn.svm import LinearSVR, SVR
from sklearn.linear_model import Perceptron,LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

model = SVR()
model = LinearRegression()
model = KNeighborsRegressor()
model = DecisionTreeRegressor()
model = RandomForestRegressor()

# SVR
# r2 -0.2483059692432681
# -0.2483059692432681

# LINEAR
# r2 0.009822945650214021
# 0.009822945650214021

# KNEIGHBOR
# r2 -0.14230499795951523
# -0.14230499795951523

# DECSIONTREE
# r2 -0.3399505406073444
# -0.3399505406073444

# RANDOM
# r2 0.00947296586672508
# 0.00947296586672508





model.fit(x_train, y_train)
y_predict = model.predict(x_test)

from sklearn.metrics import r2_score
r2= r2_score(y_test, y_predict)
print('r2', r2)
print(model.score(x_test,y_test))
# linearsvr
# r2 -0.20357153353358393
# -0.20357153353358393
# rmse 212.96147089577215
#rmse
#로스율을 mse로 구했기때문에 루트를 씌워 rmse를 구한다
import numpy as np
def RMSE(a,b):
    return np.sqrt(mean_squared_error(a,b))

#쓸 함수를 정의하고 사용한다
rmse = RMSE(y_test, y_predict)
print('rmse', rmse)

#답안지를 제출하기 위해 일단 답안지에 적을 답을 뽑는다
def relu(q):
    return np.maximum(0, q)
y_summit = model.predict(test_set)
#주최측이 제공한 테스트셋을 넣음으로써 해당하는 y값을 뽑느다
y_summit2 = relu(y_summit)
print(y_summit.shape)

#답안지 불러오가
submission = pd.read_csv(path + 'sampleSubmission.csv', index_col=0)

#답안지의 해당부분은 y_summit값이다
submission['count']=y_summit2

#입력됐으므로 다시 저장한다
submission.to_csv(path + 'sampleSubmission.csv')

# loss 36359.20703125
# 35/35 [==============================] - 0s 909us/step
# r2 0.03509574142181349
# rmse 190.68090111089342
# 203/203 [==============================] - 0s 854us/step
# (6493, 1)


# loss 37196.76953125
# 35/35 [==============================] - 0s 632us/step
# r2 0.012868447217350809
# rmse 192.86463559770135
# 203/203 [==============================] - 0s 751us/step
# (6493, 1)


# submission['SalePrice'] = y_predict
# submission.to_csv(path + 'submission.csv')

#민맥스

# 로버스트
# loss 37050.65625
# r2 0.016745909987116447
# rmse 192.4854757712525
