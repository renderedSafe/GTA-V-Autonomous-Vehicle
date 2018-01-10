# forked from Sentdex's train_model.py
import numpy as np
from keras import Sequential
from keras.utils import multi_gpu_model
from keras.optimizers import Adam
from keras.layers import Conv2D, MaxPooling2D, Dropout, Dense, Flatten
import tensorflow as tf

WIDTH = 480
HEIGHT = 270
LR = 5e-4
EPOCHS = 60
MODEL_NAME = 'model.h5'
TRAINING_DATA = 'training_data-1.npy'


def build_model():
    # This is based of of NVIDIA's model they used to train the Udacity self-driving car
    with tf.device('/cpu:0'):
        model = Sequential()
        model.add(Conv2D(24, (5, 5), activation='elu', strides=(2, 2)))
        model.add(Conv2D(36, (5, 5), activation='elu', strides=(2, 2)))
        model.add(MaxPooling2D(pool_size=(4, 4)))
        model.add(Conv2D(48, (5, 5), activation='elu', strides=(2, 2)))
        model.add(Conv2D(64, (3, 3), activation='elu'))
        model.add(Conv2D(64, (3, 3), activation='elu'))
        model.add(Dropout(.5))
        model.add(Flatten())
        model.add(Dense(1024, activation='elu'))
        model.add(Dense(42))
        model.summary()

        return model


def main():
    model = build_model()
    # I use multiple GPU's to train, that's what this next bit allows
    gpu_model = multi_gpu_model(model, 2)
    gpu_model.compile(loss='binary_crossentropy', optimizer=Adam(lr=LR), metrics=['acc'])

    # splitting our training data into training and testing data
    train_data = np.load(TRAINING_DATA)
    train = train_data[:-500]
    test = train_data[-500:]

    x = np.array([i[0] for i in train]).reshape(-1, HEIGHT, WIDTH, 3)   # the image data
    # this next part combines the 2 arrays we have as labels into one 2-hot array
    y = np.array([i[1].reshape(42) for i in train]).reshape(-1, 42)

    # same as above but for test data
    test_x = np.array([i[0] for i in test]).reshape(-1, HEIGHT, WIDTH, 3)
    test_y = np.array([i[1].reshape(42) for i in test]).reshape(-1, 42)

    gpu_model.fit(x, y, batch_size=16, epochs=20, verbose=1, validation_data=(test_x, test_y))
    model.save('{}'.format(MODEL_NAME))


if __name__ == '__main__':
    main()
