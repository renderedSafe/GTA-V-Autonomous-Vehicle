import numpy as np
from grabscreen import grab_screen
import cv2
import time
from getkeys import key_check
import os
from getcontrols import get_controls
import pygame


starting_value = 1
FILE_NAME = '1.controller-waypoint'

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(1)
joystick.init()

while True:
    file_name = '{}-{}.npy'.format(FILE_NAME, starting_value)

    if os.path.isfile(file_name):
        print('File exists, moving along', starting_value)
        starting_value += 1
    else:
        print('File does not exist, starting fresh!', starting_value)

        break


def main(file_name, starting_value):
    file_name = file_name
    starting_value = starting_value
    training_data = []

    for i in list(range(5))[::-1]:
        print(i + 1)
        time.sleep(1)

    last_time = time.time()
    paused = False
    print('STARTING!!!')
    while True:

        if not paused:
            last_time = time.time()
            screen = grab_screen(region=(320,40,1920,1024))

            # resize to something a bit more acceptable for a CNN
            screen = cv2.resize(screen, (480, 270))
            # run a color convert:
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

            keys = key_check()

            steering_angle, throttle = get_controls(joystick)
            if abs(steering_angle) < .05:
                steering_angle = 0
            output = [steering_angle, throttle]
            training_data.append([screen, output])

            print('FPS: {}'.format(1/(time.time() - last_time)))
            #last_time = time.time()
            # cv2.imshow('window',cv2.resize(screen,(640,360)))
            # if cv2.waitKey(25) & 0xFF == ord('q'):
            #     cv2.destroyAllWindows()
            #     break

            if len(training_data) % 100 == 0:
                print(len(training_data))

                if len(training_data) == 1000:
                    np.save(file_name, training_data)
                    print('SAVED')
                    training_data = []
                    starting_value += 1
                    file_name = '{}-{}.npy'.format(FILE_NAME, starting_value)

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


main(file_name, starting_value)
