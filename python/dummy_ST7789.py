#!/usr/bin/env python

import time
import numpy as np
import matplotlib.pyplot as plt

FACTOR=2

class DummyST7789(object):
    def __init__(self):
        self.width = 240
        self.height = 240
        plt.ion()
        plt.gcf().set_size_inches(self.width*FACTOR/72, self.height*FACTOR/72)
        plt.gca().set_axis_off()

    def ShowImage(self,Image,Xstart,Ystart):
        plt.clf()
        plt.gca().set_axis_off()
        plt.imshow(Image)
        plt.pause(0.01)

    def clear(self):
        plt.clf()
        plt.pause(0.01)

# 240x240 display with hardware SPI:
def get_disp():
    disp = DummyST7789()
    return disp

if __name__=='__main__':
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
    disp = get_disp()
    image1 = Image.open('pic.jpg')
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 32)
    draw.rectangle([(15,70),(210,100)],fill = "BLACK")
    draw.text((20, 70), 'ST7789 lib', fill = "LIGHTBLUE", font=font)
    disp.ShowImage(image1,0,0)
    time.sleep(1)
