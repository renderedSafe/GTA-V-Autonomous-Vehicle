# created by Werseter

from threading import Thread
from Working.grabscreen import GrabScreen
import time


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
        self.printscreen = GrabScreen(window_title=self.window_title_substring,
                                      region=(self.x, self.y, self.w, self.h))
        self.image = None
        self.render_frame_times = []
        self.render_last_time = time.time()

    def start(self):
        """
        Starts the threading screenshot loop
        :return: self
        """
        Thread(target=self._get_frame, args=()).start()
        return self

    def _get_frame(self):
        """
        The threading loop that takes quick screenshots, this runs and constantly updates the self.image attribute
        by calling a function from grabscreen.py. This function updates self.image as the RGB image of the full sized
        screen shot at every iteration.
        :return: none
        """
        self.image = self.printscreen.get_frame()
        self.render_frame_times.append(time.time() - self.render_last_time)
        self.render_frame_times = self.render_frame_times[-20:]
        self.render_last_time = time.time()
        last_time = time.time()
        while True:
            try:
                print('Thread running at {} FPS'.format(1/(time.time() - last_time)))
            except ZeroDivisionError as e:
                print('Tried to divide by 0')
            last_time = time.time()
            if self.stop == True:
                self.printscreen.clear()
                break
            #if time.time() - self.render_last_time > 0.000:    # making sure we're not iterating too fast
            self.image = self.printscreen.get_frame()
            self.render_frame_times.append(time.time() - self.render_last_time)
            self.render_frame_times = self.render_frame_times[-20:]
            self.render_last_time = time.time()

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
        Prints the FPS based on last 20 frames
        :return: none
        """
        print('FPS: {}'.format(len(self.render_frame_times) / sum(self.render_frame_times)))