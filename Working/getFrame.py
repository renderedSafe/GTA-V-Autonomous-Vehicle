# created by Werseter

from threading import Thread
from Working.grabscreen import GrabScreen
import time
import numpy as np


class GetFrameThread:
    def __init__(self, x, y, w, h, window_title_substring):
        """
        An object that will thread through a loop, constantly updating the self.image attribute as the last value of the
        screen. Call self.start() to start the thread, and self.return_frame() to return the latest screen shot.
        :param x: farthest left part of window
        :param y: how far down the window starts. normally 40 for the window header (tested on Windows 10)
        :param w: width of window
        :param h: height of window
        :param window_title_substring: a substring of the window title
        """

        self.stop = False
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.window_title_substring = window_title_substring

        # defining the top third, middle third, and bottom third GrabScreen objects to be threaded
        self.printscreen_top = GrabScreen(window_title=self.window_title_substring,
                                      region=(self.x, self.y, self.w, int(self.h/3)))
        self.printscreen_middle = GrabScreen(window_title=self.window_title_substring,
                                      region=(self.x, int(self.h/3), self.w, int(self.h/3)))
        self.printscreen_bottom = GrabScreen(window_title=self.window_title_substring,
                                             region=(self.x, 2*(int(self.h/3)), self.w, int(self.h/3)))
        self.top_captured = False
        self.middle_captured = False
        self.bottom_captured = False

        self.image_top = None
        self.image_middle = None
        self.image_bottom = None

        self.image = None

        self.render_frame_times = []
        self.render_last_time = time.time()

    def start(self):
        """
        Starts the threading screenshot loop, as well as starting a thread
        checking to see if all the threads have pending frames, and stitching them together
        :return: self
        """
        Thread(target=self._get_frame, args=(self.printscreen_top,)).start()
        Thread(target=self._get_frame, args=(self.printscreen_middle,)).start()
        Thread(target=self._get_frame, args=(self.printscreen_bottom,)).start()
        Thread(target=self._stitch_images, args=()).start()

        return self

    def _stitch_images(self):
        """Runs on a dedicated thread to check for all frames pending and then stitches them
        """
        while True:
            if self.top_captured and self.middle_captured and self.bottom_captured:
                self.image = np.vstack((self.image_top, self.image_middle, self.image_bottom))
                self.top_captured = False
                self.middle_captured = False
                self.bottom_captured = False

                self.render_frame_times.append(time.time() - self.render_last_time)
                self.render_frame_times = self.render_frame_times[-20:]
                self.render_last_time = time.time()

    def _get_frame(self, section):
        """
        The threading loop that takes quick screenshots, this runs and constantly updates the self.image attribute
        by calling a function from grabscreen.py. This function updates self.image as the RGB image of the full sized
        screen shot at every iteration.
        :section: GrabScreen object, the idea is to be able to split up the screen between threads. i.e. one thread
        grabs the top third, one the middle, and one the bottom
        :return: none
        """
        while True:
            if self.stop:
                section.clear()
                break

            image = section.get_frame()
            if section == self.printscreen_top and not self.top_captured:
                self.image_top = image
                self.top_captured = True
            elif section == self.printscreen_middle and not self.middle_captured:
                self.image_middle = image
                self.middle_captured = True
            elif section == self.printscreen_bottom and not self.bottom_captured:
                self.image_bottom = image
                self.bottom_captured = True

    def return_frame(self):
        """
        Call this function to get the last value of self.image
        :return: self.image, array of shape [H, W, 3] channels in the order RGB
        """
        return self.image

    def stop_now(self):
        """
        Stops the object's threading loop
        :return: none
        """
        self.stop = True

    def get_fps(self):
        """
        Returns the FPS based on last 20 frames
        :return: int Frames per second (FPS)
        """
        fps = (len(self.render_frame_times) / sum(self.render_frame_times))
        return fps
