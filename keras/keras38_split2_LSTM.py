# lstm -> dnn 좋음
# dnn -> lstm 별로 dnn은 불연속적인 데이터에 많이 사용하기 때문
# cnn -> lstm -> dnn도 가능
 
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM
 
trainset = np.array(range(1,101))
testset = np.array(range(96,106))
print(len(trainset))

size = 5
def split_x(seq, size):  
    aaa = []
    for i in range(len(seq) - size + 1):
        subset = seq[i:(i+size)]
        aaa.append(subset)
    print(type(aaa))
    return np.array(aaa)
train = split_x(trainset, size)

print('------------------')
print(train)
print(train.shape)
 
x = train[:, :-1]
y = train[:, -1] 
 
print(x.shape) 
print(y.shape) 








size = 4
test = split_x(testset, size)









print(test)
print(x.shape, y.shape, test.shape)

x = x.reshape(-1,4,1)
test = test.reshape(-1,4,1)

model = Sequential()
model.add(LSTM(34, return_sequences=True, input_shape=(4,1)))
model.add(LSTM(63, return_sequences=True, input_shape=(4,1)))
model.add(LSTM(22, return_sequences=False, input_shape=(4,1)))
model.add(Dense(5))
model.add(Dense(1))
model.summary()
# LSTM을 DNN으로 구현 가능
 
model.compile(optimizer='adam', loss='mse')
model.fit(x, y, epochs=100, batch_size=1, verbose=1)



y_pred = model.predict(test)
print(y_pred)

# dense
# [[ 99.99973 ]
#  [100.99947 ]
#  [101.999214]
#  [102.998985]
#  [103.998726]
#  [104.99848 ]
#  [105.99822 ]]

# lstm
# [[ 99.94272]
#  [100.94655]
#  [101.95059]
#  [102.95484]
#  [103.95929]
#  [104.96393]

lstm 
[[97.9384  ]
 [98.124756]
 [98.28192 ]
 [98.41568 ]
 [98.53052 ]
 [98.629906]
 [98.71659 ]]