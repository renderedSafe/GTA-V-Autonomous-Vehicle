# made by renderedSafe

import numpy as np
from random import shuffle
import math


starting_num = 1
ending_num = 10


""" Understanding this little diagram is important to understanding how the discretization works:
            turn value = -1 -.9 -.8 -.7 -.6 -.5 -.4 -.3 -.2 -.1   0  .1  .2  .3  .4  .5  .6  .7  .8  .9   1
steering angle one-hot = [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
                indexes:  0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20
        throttle value = -1 -.9 -.8 -.7 -.6 -.5 -.4 -.3 -.2 -.1   0  .1  .2  .3  .4  .5  .6  .7  .8  .9   1
      throttle one-hot = [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
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

        # steering discretization
        # so this basically turns our steering value into a one-hot array. It does this by multiplying the steering
        # value by 10, and then adding 10 to the product which gives us our hot index (we add 10 because a steering
        # value of 0 is actually represented at index 10 in the 1-hot array, ending up giving us negative(left) steering
        #  values to the left, and positive(right) steering values to the right of index 10). Remember that the steering value
        # we feed into this is a continuous value between -1.0 and 1.0. This process in essence, since we cast the
        # product as an integer (causing a round) turns all of our continuous values into their corresponding one-hot
        # index, which we then take, and set as 1.
        steering_equivalent_index = int((steering_angle * 10) + 10)
        steering_one_hot[steering_equivalent_index] = 1

        # throttle discretization
        throttle_equivalent_index = int((throttle * 10) + 10)
        throttle_one_hot[throttle_equivalent_index] = 1

        # putting the new values back where we got them...
        choice = [steering_one_hot, throttle_one_hot]
        holding_list.append([img, choice])

    final_data = holding_list
    print('Final number of elements: {}'.format(len(final_data)))
    shuffle(final_data)

    np.save('discretized-training_data-{}.npy'.format(i), final_data)
