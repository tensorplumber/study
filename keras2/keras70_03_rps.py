from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Conv2D, Flatten
from tensorflow.python.keras.callbacks import EarlyStopping
from keras.applications import vgg16
import numpy as np



x = np.load('d:/study_data/_save/_npy/kears_47_03_01_x.npy')
y = np.load('d:/study_data/_save/_npy/kears_47_03_02_y.npy')

print(x.shape)   # (2520, 150, 150, 3) 3개의 데이터 확인
print(y.shape)   # (2520, 3)       

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.75, shuffle=True, random_state=66)


#2. 모델구성
model = Sequential()
model.add(vgg16.VGG16(include_top=False,weights='imagenet', input_shape=(150, 150, 3)))
model.trainable = True
# model.add(Conv2D(6, (2, 2), input_shape=(150, 150, 3), activation='relu'))
# model.add(Conv2D(4, (2, 2), activation='relu'))
model.add(Flatten())
model.add(Dense(100, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(3, activation='softmax'))


#3. 컴파일,훈련
model.compile(loss='categorical_crossentropy', optimizer='adam')
earlyStopping= EarlyStopping(monitor='val_loss', patience=20, mode='auto', restore_best_weights=True)
hist = model.fit(x_train, y_train,epochs=3, validation_split=0.2, verbose=1, batch_size=32, callbacks=[earlyStopping])

 

#4. 평가, 예측
loss = model.evaluate(x_test, y_test)
y_predict = model.predict(x_test)


print(loss)
print(y_predict)

from sklearn.metrics import accuracy_score
y_predict = y_predict.round()
acc = accuracy_score(y_test, y_predict)

print('loss : ', loss)
print('acc : ', acc)

# loss :  0.2772544026374817
# acc :  0.9222222222222223

# vgg 16 epoch3 tranable
# false 
# loss :  1.1439794301986694
# acc :  0.2492063492063492
# True
# loss :  0.018748529255390167
# acc :  0.9968253968253968
