#!/usr/bin/env python

# Testing UPS-Lite + LCD hat:
#   Press DOWN for 3s to quit
# Host dummy test mode:
#   Use arrows, Enter and F1/F2/F3
#   Toggle Caps lock for toggling external power availability

import os
import datetime
import time
import subprocess
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

if 'PM3PATH' in os.environ:
    PM3PATH=os.environ['PM3PATH']
else:
    PM3PATH="/home/pi/proxmark3/"

def tadd(a, b):
    if isinstance(b, list):
        return [(a[0]+i[0], a[1]+i[1]) for i in b]
    else:
        return (a[0]+b[0], a[1]+b[1])

from ST7789 import ST7789
from hatkeys import KEYS
from UPS_Lite import UPS

scriptpath = os.path.dirname(os.path.realpath(__file__))

disp = ST7789()
keys = KEYS()
ups = UPS()

# Clear display.
disp.clear()

# Create blank image for drawing.
image1 = Image.new("RGB", (disp.width, disp.height), "BLACK")
#image1 = Image.open(os.path.join(scriptpath, 'illuminated_rfid_240.png'))
draw = ImageDraw.Draw(image1)

font32 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 32)

cmds=["hw status", "hf search", "lf search"]
def init_cmds():
    draw.rectangle([(0, 20), (240, 240)], fill="BLACK")
    for i in range(len(cmds)):
        draw.ellipse((10-5, (30+15*i)-5, 10+5, (30+15*i)+5), outline="BLACK", fill="WHITE")
        draw.text((20, (25+15*i)), cmds[i], fill = "white")
    draw.ellipse((10-5, (30+15*cur_bullet)-5, 10+5, (30+15*cur_bullet)+5), outline="BLACK", fill="RED")

MAXCOUNTER=8
counter=MAXCOUNTER
XYVAL=(130, 6)
XYBAT=(208, 5)
XYPOW=(192, 2)
XYTIM=(5, 5)
COUNT_DOWN=0
cur_bullet=0
max_bullet=2

init_cmds()
while True:
    keys.refresh_events()

    if keys.is_pressed('down'):
        if COUNT_DOWN > 5:
            disp.clear()
            time.sleep(0.6)
            break
        COUNT_DOWN+=1
    else:
        COUNT_DOWN=0

    if keys.is_raise_event('up'):
        draw.ellipse((10-5, (30+15*cur_bullet)-5, 10+5, (30+15*cur_bullet)+5), outline="BLACK", fill="WHITE")
        if cur_bullet == 0:
            cur_bullet = max_bullet
        else:
            cur_bullet-=1
        draw.ellipse((10-5, (30+15*cur_bullet)-5, 10+5, (30+15*cur_bullet)+5), outline="BLACK", fill="RED")

    if keys.is_raise_event('down'):
        draw.ellipse((10-5, (30+15*cur_bullet)-5, 10+5, (30+15*cur_bullet)+5), outline="BLACK", fill="WHITE")
        if cur_bullet == max_bullet:
            cur_bullet = 0
        else:
            cur_bullet+=1
        draw.ellipse((10-5, (30+15*cur_bullet)-5, 10+5, (30+15*cur_bullet)+5), outline="BLACK", fill="RED")

    if keys.is_raise_event('enter'):
        draw.rectangle([(0, 20), (240, 240)], fill="BLACK")
        out = subprocess.check_output([PM3PATH+"/client/proxmark3", "-p", "/dev/ttyACM0", "-c", cmds[cur_bullet]])
        draw.text((0, 30), out, fill = "WHITE")
        while True:
            disp.ShowImage(image1,0,0)
            keys.refresh_events()
            if keys.is_raise_event('left'):
                break
        init_cmds()

    if counter == MAXCOUNTER:
        counter = 0
        draw.rectangle([(0, 0), (240, 20)], fill="BLACK")
        # time
        now = datetime.datetime.now()
        draw.text(XYTIM, now.strftime("%H:%M:%S"), fill = "LIGHTGREEN")
        # battery stats
        v, c = ups.get_voltage(), ups.get_capacity()
        BATSTAT="%.2fV %i%%" %(v, c)
        print (BATSTAT)
        draw.text(XYVAL, BATSTAT, fill = "LIGHTGREEN")
        # battery icon
        draw.rectangle(tadd(XYBAT, [(2,0), (2+25,10)]), outline = "LIGHTGREEN")
        draw.rectangle(tadd(XYBAT, [(0,3), (1,7)]), fill = "LIGHTGREEN")
        draw.rectangle(tadd(XYBAT, [(2+25-(c/4), 0), (2+25,10)]), fill="LIGHTGREEN")
        # power icon
        if keys.is_ext_power_available():
            draw.polygon(tadd(XYPOW, [(7,0), (0,10), (4,9), (1,16), (10,6), (5,7)]), fill="LIGHTGREEN")
    counter+=1


    disp.ShowImage(image1,0,0)
