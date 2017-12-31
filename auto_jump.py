#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy
import os
import time
from PIL import Image

filename = 'shot1.png'
swipe_x1, swipe_y1, swipe_x2, swipe_y2 = 320, 410, 320, 410
press_coefficient = 1.392
adbAlias = '~/workspace/android-sdk-macosx/platform-tools/adb ' #也可添加alias到bashrc里直接用adb

def takeShot():
    """docstring for takeShot"""
    os.system(adbAlias + 'shell screencap -p /sdcard/' + filename)
    os.system(adbAlias + 'pull /sdcard/' + filename + ' .')

def getDistance():
    """docstring for getDistance"""
    im = Image.open(filename)
    plt.imshow(im)
    [(pos1x, pos1y), (pos2x, pos2y)] = plt.ginput(2)
    plt.close()
    im.close()
    return numpy.sqrt(pow(pos1x-pos2x, 2) + pow(pos1y - pos2y, 2))

def press(distance):
    """docstring for press"""
    if distance <= 10: #如果截图错误可双击跳过
        return
    press_time = distance * press_coefficient
    press_time = max(press_time, 200)   # 设置 200 ms 是最小的按压时间
    press_time = int(press_time)
    cmd = adbAlias + 'shell input swipe {} {} {} {} {}'.format(swipe_x1, swipe_y1, swipe_x2, swipe_y2, press_time)
    print(cmd)
    os.system(cmd)

def main():
    while True:
        try:
            takeShot()
            distance = getDistance()
            print distance
            press(distance)
            time.sleep(1)
        except Exception, e:
            print e
            break

if __name__ == '__main__':
    main()
