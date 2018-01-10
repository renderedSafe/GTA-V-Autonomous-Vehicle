# forked from Sentdex's pygta-V collect_data.py
import numpy as np
from grabscreen import grab_screen
import cv2
import time
from getkeys import key_check
import os
from getcontrols import get_controls
import pygame

# starting value of the files we will be saving, so we can regularly increment their names to save with
startingValue = 1
fileName = 'training-data'

# this the the joystick object we initialize to be able to get the values from the xbox controller as we play
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(1)
joystick.init()


def main(file_name, starting_value):
    # an empty list to store the training data in
    training_data = []

    # this variable allows us to pause the loop by pressing the 'T' key, see below
    paused = False
    print('STARTING!!!')
    while True:
        if not paused:
            # grabbing a screenshot of what we're seeing in the game
            screen = grab_screen(region=(320,40,1920,1024))
            # resize to something a bit more acceptable for a CNN
            resized_screen = cv2.resize(screen, (480, 270))

            # this gets our steering and throttle values from the position of the left stick and right trigger
            steering, throttle = get_controls(joystick)
            if abs(steering) < .05:   # this makes small changes of the stick around center a dead zone
                steering = 0
            # putting our controls into a list to store
            output = [steering, throttle]
            # storing our training data sample
            training_data.append([resized_screen, output])

            # this saves and subsequently starts recording for a new training-data file at regular intervals
            if len(training_data) == 1000:
                np.save(file_name, training_data)
                print('SAVED')
                training_data = []
                starting_value += 1
                file_name = '{}-{}.npy'.format(FILE_NAME, starting_value)

        # this bit of code checks to see if you've pressed 'T' and pauses the loop
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


main(fileName, startingValue)
