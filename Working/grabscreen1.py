# Done by Frannecklp

import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api
from multiprocessing import Process, Pool
from os import getpid


def grab_screen(thread_number, region=None):
    x = 0
    y = 0
    w = 1919
    h = 1120
    slice_height = int(h / 3)
    slice_top = (x, y, w, slice_height)
    slice_middle = (x, slice_height, w, slice_height)
    slice_bottom = (x, (2 * slice_height), w, slice_height)

    if thread_number == 0:
        region = slice_top
    elif thread_number == 1:
        region = slice_middle
    elif thread_number == 2:
        region = slice_bottom

    hwin = win32gui.GetDesktopWindow()
    print(getpid())
    print('Region passed: {}'.format(region))
    if region:
            left,top,x2,y2 = region
            width = x2 - left #+ 1
            height = y2 - top #+ 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())
    print(np.shape(img))

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB), thread_number


if __name__ == '__main__':
    results = []
    final_results = [None, None, None]
    pool = Pool(processes=3)
    for i in range(3):
        results.append(pool.apply_async(grab_screen, (i,)))
    for i in results:
        tup = i.get()
        print('parsed tuple = {}'.format(tup))
        target_index = tup[1]
        final_results[target_index] = tup[0]
    print(final_results)
    stitched_image = np.vstack(final_results)
    print(np.shape(stitched_image))
    cv2.imshow('window', stitched_image)
