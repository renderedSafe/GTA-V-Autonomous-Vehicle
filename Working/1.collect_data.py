import numpy as np
import cv2
import time
from Working.getkeys import key_check
from Working.getFrame import GetFrameThread
import os
from Working.getcontrols import get_controls
import pygame
from Working.grabscreen1 import grab_screen
from threading import Thread
from multiprocessing import Pool


starting_value = 1
window_title_substring = 'PyCharm'

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()


while True:
    file_name = 'training_data-{}.npy'.format(starting_value)

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
    loops = 0
    while True:

        if not paused:
            if time.time() - last_time >= .0125:  # Lets not record faster than whatever

                screen = vars.latest_image
                try:
                    screen = cv2.resize(screen, (480, 270))
                except cv2.error as e:
                    print(e)
                    screen = None

                steering_angle, throttle = get_controls(joystick)
                if abs(steering_angle) < .05:
                    steering_angle = 0
                output = [steering_angle, throttle]
                if screen is not None:
                    training_data.append([screen, output])

                if loops >= 50:
                    print('collect_data FPS: {}'.format(1/(time.time() - last_time)))
                    loops = 0
                loops += 1
                last_time = time.time()

                # grabscreen_thread.get_fps()
                # last_time = time.time()
                # cv2.imshow('window',cv2.resize(screen,(640,360)))
                # if cv2.waitKey(25) & 0xFF == ord('q'):
                #     cv2.destroyAllWindows()
                #     break

                if len(training_data) % 100 == 0:
                    print(len(training_data))

                    if len(training_data) == 300:
                        np.save(file_name, training_data)
                        print('SAVED')
                        training_data = []
                        starting_value += 1
                        file_name = 'training_data-{}.npy'.format(starting_value)

        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                vars.stop = True
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                vars.stop = False
                time.sleep(1)

def update_image():
    while not vars.stop:
        last_time = time.time()
        img_list = pool.map_async(grab_screen, ((0, 0, 1920, 1120),))
        lst = img_list.get()
        vars.latest_image = lst[-1]
        print('Screenshot loop FPS: {}'.format(1/(time.time() - last_time)))

class Variables:
    def __init__(self):
        self.latest_image = None
        self.stop = False

if __name__ == '__main__':
    pool = Pool(processes=2)
    vars = Variables()
    Thread(target=update_image, args=()).start()
    time.sleep(3)
    main(file_name, starting_value)
