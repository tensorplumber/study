import tensorflow as tf

node1 = tf.constant(3.0,tf.float32)
node2 = tf.constant(4.0)
node3 = node1 + node2

# print(node3)
# Tensor("add:0", shape=(), dtype=float32)
sess = tf.Session()
print(sess.run(node3))

sess = tf.compat.v1.Session()


#########################

node4 = tf.add(node1,node2)
print(sess.run(node4))

