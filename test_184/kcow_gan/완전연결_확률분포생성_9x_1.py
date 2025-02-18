#확률분포 생성을 위한 
import numpy as np
import matplotlib.pyplot as plt
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from keras import models
from keras.layers import Dense, Conv1D, Reshape, Flatten, Lambda

from keras.optimizer_v2 import adam
from keras import backend as K
from torch import _batch_norm_impl_index

def add_decorate(x):
    #axis = 01  last dim in an array
    m = K.mean(x, axis=1, keepdims=True)
    d = K.square(x-m) #평균값을 뺀 제곱값을 합쳐서
    return K.concatenate([x,d], axis=1)

def add_decorate_shape(input_shape):
    shape = list(input_shape)
    assert len(shape) == 2
    shape[1] *= 2
    return tuple(shape)

#model.add(lambda(antirectifier, output_shape=antirectifier_output_shape))

lr = 2e-4 #0.0002
opt = adam.Adam(lr=lr, beta_1=0.9, beta_2=0.999)

def model_compile(model):
    return model.compile(loss = 'binary_crossentropy', optimizer = opt, metrics=['accuracy'])


class GAN:
    def __init__(self, ni_D, nh_D, nh_G):
        self.ni_D = ni_D
        self.nh_D = nh_D
        self.nh_G = nh_G

        self.D = self.gen_D()
        self.G = self.gen_G()
        self.GD = self.make_GD() #업그레이드

    def gen_D(self):
        ni_D = self.ni_D
        nh_D = self.nh_D
        D = models.Sequential()
        D.__init__()
        D.add(Lambda(add_decorate, output_shape=add_decorate_shape, input_shape=(ni_D,))) #임의로 추가적 계ㅒ층 생성
        D.add(Dense(nh_D, activation='relu'))
        D.add(Dense(nh_D, activation='relu'))
        D.add(Dense(1, activation='sigmoid'))

        D.summary()

        model_compile(D)
        return D


    def gen_G(self):
        ni_D = self.ni_D
        nh_G = self.nh_G
        G = models.Sequential() #batch,ni_D
        G.add(Reshape((ni_D,1), input_shape=(ni_D, ))) #100개의 확률분포 데이터 batch, steps = ni_D, inputdim = 1
        G.add(Conv1D(nh_G, 1, activation='relu')) #batch, ni_d nh_G
        G.add(Conv1D(nh_G, 1, activation='sigmoid')) #batch ni_D, nh_G
        G.add(Conv1D(1, 1)) #batych, nh_D, 1
        G.add(Flatten()) #batych, ni_D

        G.summary()

        model_compile(G)
        return G

    def make_GD(self):
        G, D = self.G, self.D
        GD = models.Sequential()
        GD.add(G)
        GD.add(D)
        D.trainable = False
        model_compile(GD)
        D.trainable = True
        return GD

    def  D_train_on_batch(self, Real, Gen):
        D = self.D
        X = np.concatenate([Real, Gen], axis = 0)
        y = np.array([1] * Real.shape[0]+[0]*Gen.shape[0])
        D.train_on_batch(X,y)

    def GD_train_on_batch(self, Z):
        GD = self.GD
        y = np.array([1]*Z.shape[0])
        GD.train_on_batch(Z, y)

class Data:
    def __init__(self, mu, sigma, ni_D):
        self.real_sample = lambda n_batch: np.random.normal(mu,sigma, (n_batch, ni_D)) #평균, 확률
        self.in_sample = lambda n_batch: np.random.rand(n_batch, ni_D) #리얼과 같이 동일한 확률분포를 갖게끔

class Machine:
    def __init__(self, n_batch=10, ni_D=100):
        data_mean = 4
        data_stddev = 1.25
        #평균, 확률분포

        self.n_iter_D = 1
        self.n_iter_G = 5

        self.data = Data(data_mean, data_stddev, ni_D)
        self.gan = GAN(ni_D=ni_D, nh_D=50, nh_G=50)

        self.n_batch = n_batch
        #self.ni_D = ni_D

    def train_D(self):
        gan = self.gan
        n_batch = self.n_batch
        data = self.data

        #real data
        Real = data.real_sample(n_batch) #n_batch, ni_D
        #print(Real.shape)
        #gen data
        Z = data.in_sample(n_batch) #n_batch, ni_D
        Gen = gan.G.predict(Z) #n_batch, ni_D
        #print(Gen.shape)

        gan.D.trainable = True
        gan.D_train_on_batch(Real, Gen)

    def train_GD(self):
        gan = self.gan
        n_batch = self.n_batch
        data = self.data
        #seed data for data gen
        Z = data.in_sample(n_batch)

        gan.D.trainable = False
        gan.GD_train_on_batch(Z)

    def train_each(self):
        for it in range(self.n_iter_D):
            self.train_D()
        for it in range(self.n_iter_G):
            self.train_GD()

    def train(self, epochs):
        for epoch in range(epochs):
            self.train_each()

    def test(self, n_test):
        #gen new image

        gan = self.gan
        data = self.data
        Z = data.in_sample(n_test)
        Gen = gan.G.predict(Z)
        return Gen, Z

    def show_hist(self, Real, Gen, Z):
        plt.hist(Real.reshape(-1), histtype='step', label='Real')
        plt.hist(Gen.reshape(-1), histtype='step', label='Generated')
        plt.hist(Z.reshape(-1), histtype='step', label='Input')
        plt.legend(loc=0)

    def test_and_show(self, n_test):
        data = self.data
        Gen, Z = self.test(n_test)
        Real = data.real_sample(n_test)
        self.show_hist(Real, Gen, Z)
        Machine.print_stat(Real, Gen)

    def run_epochs(self, epochs, n_test):
        #train Gan and wshwo reault for showing the oringal and th artifical result willb e compared
        self.train(epochs)
        self.test_and_show(n_test)

    def run(self, n_repeat=200, n_show=200, n_test=100):
        for ii in range(n_repeat):
            print('==Stage', ii, '(epoch:{}'.format(ii*n_show))
            self.run_epochs(n_show, n_test)
            plt.show()

    @staticmethod
    def print_stat(Real, Gen):
        def stat(d):
            return (np.mean(d), np.std(d))
        print('Mena and Std of Real', stat(Real))
        print('Mena and Std of Real', stat(Gen))

def main():
    machine = Machine(n_batch=1, ni_D=100)
    machine.run(n_repeat=200, n_show=200, n_test=100)

if __name__=='__main__':
    main()


    



