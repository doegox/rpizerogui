#!/usr/bin/env python

# Testing UPS-Lite + LCD hat:
#   Press DOWN for 3s to quit
# Host dummy test mode:
#   Use arrows, Enter and F1/F2/F3
#   Toggle Caps lock for toggling external power availability

import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

def tadd(a, b):
    if isinstance(b, list):
        return [(a[0]+i[0], a[1]+i[1]) for i in b]
    else:
        return (a[0]+b[0], a[1]+b[1])

from ST7789 import ST7789
from hatkeys import KEYS
from UPS_Lite import UPS

disp = ST7789()
keys = KEYS()
ups = UPS()

# Clear display.
disp.clear()

# Create blank image for drawing.
#image1 = Image.new("RGB", (disp.width, disp.height), "WHITE")
image1 = Image.open('pic.jpg')
draw = ImageDraw.Draw(image1)

font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 32)

MAXCOUNTER=20
counter=MAXCOUNTER
XYVAL=(130, 6)
XYBAT=(208, 5)
XYPOW=(190, 2)
COUNT_DOWN=0

keydict = {
    'up':    {'rect':[(65, 45), (115, 95)],          'txtpos': (82, 62),   'txt': 'U'},
    'down':  {'rect':[(65, 145), (115, 195)],        'txtpos': (82, 162),  'txt': 'D'},
    'left':  {'rect':[(15, 95), (65, 145)],          'txtpos': (32, 112),  'txt': 'L'},
    'right': {'rect':[(115, 95), (165, 145)],        'txtpos': (132, 112), 'txt': 'R'},
    'enter': {'circ':(90-25, 120-25, 90+25, 120+25), 'txtpos': (82, 112),  'txt': 'P'},
    'key1':  {'rect':[(185, 35), (235, 85)],         'txtpos': (195, 52),  'txt': 'K1'},
    'key2':  {'rect':[(185, 95), (235, 145)],        'txtpos': (195, 112), 'txt': 'K2'},
    'key3':  {'rect':[(185, 155), (235, 205)],       'txtpos': (195, 172), 'txt': 'K3'}
}
for key in keydict.keys():
    if 'rect' in keydict[key]:
        draw.rectangle(keydict[key]['rect'], outline = "BLUE", fill="WHITE")
    elif 'circ' in keydict[key]:
        draw.ellipse(keydict[key]['circ'], outline = "BLUE", fill="WHITE")
    draw.text(keydict[key]['txtpos'], keydict[key]['txt'], fill = "BLUE", font=font)

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

    if counter == MAXCOUNTER:
        counter = 0
        draw.rectangle([(0, 0), (240, 20)], fill="BLACK")
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

    for key in keydict.keys():
        if keys.is_raise_event(key):
            if 'rect' in keydict[key]:
                draw.rectangle(keydict[key]['rect'], outline = "BLUE", fill="RED")
            elif 'circ' in keydict[key]:
                draw.ellipse(keydict[key]['circ'], outline = "BLUE", fill="RED")
            draw.text(keydict[key]['txtpos'], keydict[key]['txt'], fill = "BLUE", font=font)
            print "%s pressed" % key
        if keys.is_fall_event(key):
            if 'rect' in keydict[key]:
                draw.rectangle(keydict[key]['rect'], outline = "BLUE", fill="WHITE")
            elif 'circ' in keydict[key]:
                draw.ellipse(keydict[key]['circ'], outline = "BLUE", fill="WHITE")
            draw.text(keydict[key]['txtpos'], keydict[key]['txt'], fill = "BLUE", font=font)
            print "%s released" % key

    disp.ShowImage(image1,0,0)
