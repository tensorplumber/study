import tensorflow as tf
tf.compat.v1.set_random_seed(3242)

x_train = [1,2,3]
y_train = [1,2,3]
x_test = [4,5,6]
y_test = [4,5,6]
x = tf.compat.v1.placeholder(tf.float32)
y = tf.compat.v1.placeholder(tf.float32)
w = tf.Variable(1,dtype=tf.float32)
sess = tf.compat.v1.Session()
sess.run(tf.global_variables_initializer())
print(sess.run(w))
hypothesis = x*w
loss = tf.reduce_mean(tf.square(hypothesis-y))

lr = 0.2
gradient = tf.reduce_mean((w*x-y)*x)
decent = w- lr *gradient
update = w.assign(decent)
#계산하고 러닝레이트 바꿔서 계산
w_history = []
loss_history = []


for step in range(21):

    _,loss_v,w_v = sess.run([update,loss,w],feed_dict={x:x_train,y:y_train})
    
    print(step,'\t',_,'\t',loss_v,'\t',w_v)

    w_history.append(w_v)
    loss_history.append(loss_v)

#################r2

pred = x_test * w_v
# pred_data = sess.run(pred,feed_dict={x_test:x_test_data})
from sklearn.metrics import r2_score,mean_absolute_error
r2 = r2_score(y_test,pred)
print(r2)
mae = mean_absolute_error(y_test,pred)
print(mae)
sess.close()