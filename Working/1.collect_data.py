import numpy as np
import cv2
import time
from Working.getkeys import key_check
from Working.getFrame import GetFrameThread
import os
from Working.getcontrols import get_controls
import pygame


starting_value = 24
window_title_substring = 'PyCharm'

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(1)
joystick.init()


# creating the threading grabscreen object and starting the thread
grabscreen_thread = GetFrameThread(0, 40, 1920, 1120, window_title_substring=window_title_substring).start()

while True:
    file_name = 'sedan-hoodview-generalizled_noncourse-training_data-{}.npy'.format(starting_value)

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

    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    last_time = time.time()
    paused = False
    print('STARTING!!!')
    while True:

        if not paused:
            if time.time() - last_time >= .0125:  # Lets not record faster than 80 FPS

                screen = grabscreen_thread.return_frame()
                screen = cv2.resize(screen, (480, 270))

                steering_angle, throttle = get_controls(joystick)
                if abs(steering_angle) < .05:
                    steering_angle = 0
                output = [steering_angle, throttle]
                training_data.append([screen, output])

                print('loop took {} seconds'.format(time.time() - last_time))
                last_time = time.time()
                #ttgrabscreen_thread.get_fps()
                # last_time = time.time()
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
                        file_name = 'training_data-{}.npy'.format(starting_value)

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
