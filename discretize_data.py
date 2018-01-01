import numpy as np
from random import shuffle
import math
starting_num = 1
ending_num = 47


"""
                         -1 -.9 -.8 -.7 -.6 -.5 -.4 -.3 -.2 -.1   0  .1  .2  .3  .4  .5  .6  .7  .8  .9   1
steering angle one-hot = [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
                indexes:  0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20


                         -1 -.9 -.8 -.7 -.6 -.5 -.4 -.3 -.2 -.1   0  .1  .2  .3  .4  .5  .6  .7  .8  .9   1
throttle       one-hot = [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
"""

for i in range(starting_num, ending_num + 1):
    train_data = np.load('training_data-{}.npy'.format(i))
    print('Loaded training_data-{}.npy'.format(i))

    holding_list = []

    for data in train_data:
        steering_one_hot = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        throttle_one_hot = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        img = data[0]
        choice = data[1]

        steering_angle = choice[0]
        throttle = choice[1]

        # steering descretization


        # putting the new values back where we got them...

        choice = [steering_angle, throttle]
        holding_list.append([img, choice])

    final_data = holding_list
    print('Final number of elements: {}'.format(len(final_data)))
    shuffle(final_data)

    np.save('1-onehot-discretized-training_data-{}.npy'.format(i), final_data)
