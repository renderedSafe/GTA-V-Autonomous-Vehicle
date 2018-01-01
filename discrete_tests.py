"""
A script to quickly test and verify the codification of our one-hot generation algorithm. This paradigm is
easily scalable and breaks down continuous value variables into discrete one-hot arrays representing variable states
at a resolution defined by the size of the array.

                         -1 -.9 -.8 -.7 -.6 -.5 -.4 -.3 -.2 -.1   0  .1  .2  .3  .4  .5  .6  .7  .8  .9   1
steering angle one-hot = [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
                indexes:  0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20
"""


steering_value = -0    # steering values range from -1 at full left to 1 at full right
steering_one_hot = [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
zero_value_index = 10   # the index of 0 steering. lower indexes represent left turns, higher, right turns

rounded_steering = round(steering_value, 1)
one_hot_index = int(rounded_steering * 10) + zero_value_index    # adding the zero value index effectively sets it as the zero point
print('Raw value: {} ----Rounded to----> {} ----To one-hot index----> {}'.format(steering_value, rounded_steering, one_hot_index))

steering_one_hot[one_hot_index] = 1
print('Final one-hot array value: \n {}'.format(steering_one_hot))