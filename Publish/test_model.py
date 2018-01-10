# forked from Sentdex's pygta-V collect_data.py
import numpy as np
from grabscreen import grab_screen
import cv2
import time
from getkeys import key_check
import os
from getcontrols import get_controls
import pygame
import keras


modelName = 'model.h5'


def main(model_name):
    model = keras.models.load_model(model_name)

    paused = False
    print('STARTING!!!')
    while True:
        if not paused:
            screen = grab_screen(region=(320,40,1920,1024)) # this takes a screenshot of the region defined
            # resize to something a bit more acceptable for a CNN
            resized_screen = cv2.resize(screen, (480, 270))

            # the model defined earlier spits out a 42 element array given the screenshot as input
            prediction = model.predict(resized_screen, batch_size=1, verbose=1)[0]

            """
            This splits the output from the predict funtion into the steering part (the first 21 elements)
            and the throttle part (the last 21 elements)
            """
            steering_prediction = np.split(prediction, 2)[0]
            throttle_prediction = np.split(prediction, 2)[1]

            """
            I'm pretty proud of this part. I found that even though the network was always trained 
            on a 42 element 2-hot array (one hot element representing the steering and the other the throttle)
            the total value of the prediction in either array after the previous split was very often not 1
            as one should expect, so these next couple actions find out what value you could multiply the 
            total prediction by to have it equal 1. This makes it so that we can have consistent final predictions
            for the simulated controller inputs we will feed into the game, which max out at an absolute value of one."""
            steering_correction_factor = sum(steering_prediction) ** -1
            throttle_correction_factor = sum(throttle_prediction) ** -1

            # steering prediction manipulation
            # this next set of operations splits the steering values into the left and right values and
            left_values = steering_prediction[10:]
            # this reverses the direction of this array, meaning that higher indexes represent higher left turn values
            left_values = left_values[::-1]
            right_values = steering_prediction[:11]

            # Here we are, parsing through the prediction at each index in the left values array. The goal is to add up
            # the total prediction for the left turn predictions the network spit out. We go through each element.
            # For example, when we are at element 2, we will see the predicted value for the left steering value of
            # .2 let's say it's 0.5. Using the prediction value as a weight and multiplying the two, we get the actual
            # predicted, no shit value to add to the sum of left values. We do the same process for the right steering
            # values, and the same for throttle, forward and backward. The index_equivalent_steering variable gives us
            # a value that turns the index of the array we're examining into the equivalent steering value
            # (the 1st element representing 0.1 steering, the 7th 0.7, etc.). Also worth noting is the multiplication
            # of the prediction at a given index by the steering_correction_factor. Doing this ensures that the total
            # 'probability' of all the steering predictions will sum to 1, so in essence we are mapping whatever total
            # value of the initial prediction was to 0.0 to 1.0. Important to know is that any real number raised to the
            # -1 (which is how we get the correction value) will produce a number that, multiplied by the original
            # number, will always equal 1. It's just some simple math to help us solve the non-1 prediction value
            # problem. A quick way to check intuitively if this is working is to think about a full 100% prediction for
            # the .5 steering value (which would be the 5th element this for loop checked, so i = 5). In this case, our
            # our array would look like this: [0 0 0 0 1 0 0 0 0 0]. Once the for loop parses through this value, in a
            # trace we would see that the number it adds to the total_weighted_left_value would be 0.5, accurately
            # reflecting the prediction of the network. You will find that this intuition holds for any number of
            # combinations of predicted values at each index.
            total_weighted_left_value = 0
            for i in left_values:
                index_equivalent_steering = i / 10
                index_prediction = (left_values[i] * steering_correction_factor) * index_equivalent_steering
                total_weighted_left_value += index_prediction

            total_weighted_right_value = 0
            for i in right_values:
                index_equivalent_steering = i / 10
                index_prediction = (right_values[i] * steering_correction_factor) * index_equivalent_steering
                total_weighted_right_value += index_prediction

            steering_value = total_weighted_right_value - total_weighted_left_value

            # throttle prediction manipulation
            backward_values = throttle_prediction[10:]
            backward_values = backward_values[::-1]
            forward_values = throttle_prediction[:11]

            total_weighted_backward_value = 0
            for i in backward_values:
                index_equivalent_throttle = i / 10
                index_prediction = (backward_values[i] * throttle_correction_factor) * index_equivalent_throttle
                total_weighted_backward_value += index_prediction

            total_weighted_forward_value = 0
            for i in forward_values:
                index_equivalent_throttle = i / 10
                index_prediction = (forward_values[i] * throttle_correction_factor) * index_equivalent_throttle
                total_weighted_forward_value += index_prediction

            throttle_value = total_weighted_forward_value - total_weighted_backward_value

            # here is where you would feed steering_value and throttle_value to the simulated xbox controller for
            # input into the game. I ended up using the values of steering_value and throttle_value alone.

        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)


main(modelName)
