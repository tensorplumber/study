# 1에서 넘파이를 불러와서 모델링

import numpy as np 
from keras.preprocessing.image import ImageDataGenerator

 
x_train = np.load('d:/study_data/_save/_npy/keras47_01_train_x.npy')
y_train = np.load('d:/study_data/_save/_npy/keras47_01_train_y.npy')
x_test = np.load('d:/study_data/_save/_npy/keras47_01_test_x.npy')
y_test = np.load('d:/study_data/_save/_npy/keras47_01_test_y.npy')
 

#2.모델
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense,Conv2D,Flatten
from keras.applications import vgg16
print(y_train.shape,y_test.shape,x_train.shape)
model = Sequential()
model.add(vgg16.VGG16(include_top=False,input_shape = (150,150,3),weights='imagenet'))

# model.add(Conv2D(6, (2,2), input_shape = (150,150,3),activation='relu'))
# model.add(Conv2D(2, (3,3), activation='relu'))
model.add(Flatten())
model.add(Dense(50, activation='relu'))
model.add(Dense(50, activation='relu'))
model.add(Dense(50, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.build(input_shape=(None,150,150,3))
model.summary()

#3.컴파일,훈련
model.compile(loss= 'binary_crossentropy',optimizer='adam')
# batch를 최대로 잡으면 이렇게도 가능.
from tensorflow.python.keras.callbacks import EarlyStopping
es= EarlyStopping(monitor= 'val_loss', patience=30, mode='auto', restore_best_weights=True)
hist = model.fit(x_train, y_train, epochs=30, 
                 validation_split=0.2, 
                 verbose=1, 
                 batch_size=32,
                 callbacks=es)
# hist = model.fit_generator(x_train,y_train, epochs= 40, steps_per_epoch=32,
#                                         #전체데이터/batch = 160/5 = 32
#                     validation_data=x_train,
#                     validation_steps=4) #val_steps: 한 epoch 종료 시 마다 검증할 때 사용되는 검증 스텝 수를 지정합니다. 

# accuracy = hist.history['accuracy']
# val_accuracy =  hist.history['val_accuracy']
# loss = hist.history['loss']
# val_loss = hist.history['val_loss']

# print('loss : ', loss[-1])
# print('val_loss : ', val_loss[-1])
# print('accuracy : ', accuracy[-1])
# print('val_accuracy : ', val_accuracy[-1])

#4.평가,예측 
loss = model.evaluate(x_test,y_test)
y_predict = model.predict(x_test)   

from sklearn.metrics import accuracy_score
y_predict = y_predict.round()
acc = accuracy_score(y_test,y_predict)

print('loss : ', loss)
print('acc : ', acc)


# loss :  0.6558058857917786
# acc :  0.6104794859120118