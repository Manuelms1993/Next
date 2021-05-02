import numpy as np
from keras.datasets import mnist
from keras.layers import Input, Dense, Reshape, Flatten, Dropout
from keras.layers import BatchNormalization, Activation
from keras.layers.advanced_activations import LeakyReLU
from keras.models import Sequential, Model
from keras.optimizers import Adam
from pypianoroll import Multitrack, Track
from matplotlib import pyplot as plt
import keras
import tensorflow as tf
import Persistence as P

#https://towardsdatascience.com/writing-your-first-generative-adversarial-network-with-keras-2d16fd8d4889
#https://towardsdatascience.com/10-lessons-i-learned-training-generative-adversarial-networks-gans-for-a-year-c9071159628
#https://puentesdigitales.com/2019/04/05/todo-lo-que-necesitas-saber-sobre-las-gan-redes-generativas-antagonicas/
#https://machinelearningmastery.com/how-to-train-stable-generative-adversarial-networks/
#https://salu133445.github.io/musegan/model
#https://www.tensorflow.org/tutorials/generative/dcgan

class GAN():

    img_rows = 128
    img_cols = 768
    img_shape = (0, 0)
    latent_dim = 100

    def __init__(self, row = 768, cols = 128):
        self.img_rows = row
        self.img_cols = cols
        self.img_shape = (self.img_rows, self.img_cols)
        self.latent_dim = 10000
        optimizer = Adam(0.00001, 0.5)

        self.discriminator = self.build_discriminator()
        self.discriminator.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

        self.generator = self.build_generator()

        z = Input(shape=(self.latent_dim,))
        img = self.generator(z)

        self.discriminator.trainable = False
        validity = self.discriminator(img)

        self.combined = Model(z, validity)
        self.combined.compile(loss='binary_crossentropy', optimizer=optimizer)

    def build_generator(self):
        model = Sequential()
        model.add(Dense(256, input_dim=self.latent_dim))
        model.add(LeakyReLU(alpha=0.1))

        model.add(Dense(512))
        model.add(LeakyReLU(alpha=0.1))

        model.add(Dense(1024))
        model.add(LeakyReLU(alpha=0.1))


        model.add(Dense(np.prod(self.img_shape), activation='linear'))
        model.add(Reshape(self.img_shape))

        model.summary()
        noise = Input(shape=(self.latent_dim,))
        img = model(noise)

        return Model(noise, img)


    def build_discriminator(self):
        model = Sequential()

        model.add(Flatten(input_shape=self.img_shape))
        model.add(Dense(512))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(256))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(1, activation='sigmoid'))
        model.summary()

        img = Input(shape=self.img_shape)
        validity = model(img)

        return Model(img, validity)

    def trainGAN(self, epochs, X_train, batch_size=1, sample_interval=50):

        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))

        for epoch in range(epochs):

            idx = np.random.randint(0, X_train.shape[0], batch_size)
            imgs = X_train[idx]

            #training discrimator
            noise = np.random.normal(0, 1, (batch_size, self.latent_dim))

            gen_imgs = self.generator.predict(noise)

            d_loss_real = self.discriminator.train_on_batch(imgs, valid)
            d_loss_fake = self.discriminator.train_on_batch(gen_imgs, fake)

            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

            # training generator
            for _ in range(3):
                noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
                g_loss = self.combined.train_on_batch(noise, valid)

            print ("%d [D loss: %f] [G loss: %f]" % (epoch, d_loss[0], g_loss))

            p = self.generator.predict(np.random.normal(0, 1, (1, self.latent_dim)))
            p = np.reshape(p, self.img_shape)

            #p[p > 0.2] = 100
            #p[p <= 0.2] = 0
            #print(np.max(p))
            #P.saveMidiFile(p, "./model/song" + str(epoch) + ".mid")
            P.saveWavFile(p, "./model/song" + str(epoch) + ".wav")


