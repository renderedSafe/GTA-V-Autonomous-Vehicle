from multiprocessing import Process
import numpy as np
import time
import cv2
import win32gui, win32ui, win32con, win32api
from Working.grabscreen1 import grab_screen
from PIL import ImageGrab


class GrabSections:
    def __init__(self):
        self.top = None
        self.middle = None
        self.bottom = None

    def get_top(self):
        print('grabbing top')
        self.top = grab_screen(region=(0, 0, 840, 470))

    def get_middle(self):
        self.middle = grab_screen()

    def get_bottom(self):
        self.bottom = grab_screen()


def stitch():
    while True:
        if grabber.top is not None: #and grabber.middle and grabber.bottom:
            #image = np.vstack((grabber.top, grabber.middle, grabber.bottom))
            image = grabber.top
            # p1.terminate()
            # p2.terminate()
            # p3.terminate()
            return image



def grab():
    grabber = ImageGrab
    grabber.grab((0, 0, 840, 470))
    print('grabbed')


if __name__ == '__main__':
    grabber = GrabSections()
    Process(target=grab).start()
    #grabber.get_top()
    # p2 = Process(target=grabber.get_middle, args=())
    # p2.start()
    # p3 = Process(target=grabber.get_bottom, args=())
    # p3.start()
    print(np.shape(stitch()))

        

