import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras import Sequential
from keras.utils import multi_gpu_model
from keras.optimizers import Adam
from keras.applications import Xception
from keras.callbacks import ModelCheckpoint
from keras.layers import Lambda, Conv2D, MaxPooling2D, Dropout, Dense, Flatten
import argparse
import tensorflow as tf
from random import shuffle
import keras
import os
import matplotlib.pyplot as plt

FILE_I_END = 16

WIDTH = 480
HEIGHT = 270
LR = 5e-4
EPOCHS = 60
MODEL_NAME = '15Ks-controller-waypoint.h5'
PREV_MODEL = ''
TRAINING_DATA = 'concat-controller-waypoint_training_data-1.npy'

LOAD_MODEL = True

# def load_data():
#     data = np.load('training_data-{}.npy'.format(batch_number)).reshape(-1, )
#     print(data.shape)
#     X = np.array(data[0])
#     Y = np.array(data[1])
#
#     X_train, X_valid, Y_train, Y_valid = train_test_split(X, Y, test_size=100, random_state=0)
#
#     return X_train, X_valid, Y_train, Y_valid


def build_model():
    with tf.device('/cpu:0'):
        model = Sequential()
        model.add(Lambda(lambda x: x / 127.5 - 1.0, input_shape=(HEIGHT, WIDTH, 3)))
        model.add(Conv2D(24, (5, 5), activation='elu', strides=(2, 2)))
        model.add(Conv2D(36, (5, 5), activation='elu', strides=(2, 2)))
        #model.add(MaxPooling2D(pool_size=(4, 4)))
        model.add(Conv2D(48, (5, 5), activation='elu', strides=(2, 2)))
        model.add(Conv2D(64, (3, 3), activation='elu'))
        model.add(Conv2D(64, (3, 3), activation='elu'))
        model.add(Dropout(.5))
        model.add(Flatten())
        model.add(Dense(1024, activation='elu'))
        model.add(Dense(50, activation='elu'))
        model.add(Dense(10, activation='elu'))
        # remember to change this based on whether we're trying to predict one or 2 values
        model.add(Dense(9))
        model.summary()

        return model


def main():
    if os.path.exists(MODEL_NAME):
        model = keras.models.load_model(MODEL_NAME)
        print('Loaded previous model!')
    else:
        with tf.device('/cpu:0'):
            model = build_model()
    gpu_model = multi_gpu_model(model, 2)
    gpu_model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=LR), metrics=['acc'])

    train_data = np.load(TRAINING_DATA)


    print('{}'.format(TRAINING_DATA), len(train_data))

    ##            # [   [    [FRAMES], CHOICE   ]    ]
    ##            train_data = []
    ##            current_frames = deque(maxlen=HM_FRAMES)
    ##
    ##            for ds in data:
    ##                screen, choice = ds
    ##                gray_screen = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
    ##
    ##
    ##                current_frames.append(gray_screen)
    ##                if len(current_frames) == HM_FRAMES:
    ##                    train_data.append([list(current_frames),choice])

    # #
    # always validating unique data:
    # shuffle(train_data)
    train = train_data[:-500]
    test = train_data[-500:]

    X = np.array([i[0] for i in train]).reshape(-1, HEIGHT, WIDTH, 3)
    # getting the 1st element in the second element of the array, which is the steering
    Y = [i[1] for i in train]

    test_x = np.array([i[0] for i in test]).reshape(-1, HEIGHT, WIDTH, 3)
    # getting the 1st element in the second element of the array, which is the steering
    test_y = [i[1] for i in test]

    history = gpu_model.fit(X, Y, batch_size=16, epochs=20, verbose=1, validation_data=(test_x, test_y))
    plt.plot(history.history['val_acc'])
    plt.plot(history.history['loss'])
    model.save('2-{}'.format(MODEL_NAME))
    print('Model saved!')
    plt.show()





if __name__ == '__main__':
    main()