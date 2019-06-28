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

# Press
draw.ellipse((90-25, 120-25, 90+25, 120+25), outline="BLUE", fill="WHITE")
draw.text((82, 112), "P", fill = "BLUE", font=font)

# Left
draw.rectangle([(15, 95), (65, 145)], outline="BLUE", fill="WHITE")
draw.text((32, 112), "L", fill = "BLUE", font=font)

# Down
draw.rectangle([(65, 145), (115, 195)], outline = "BLUE", fill="WHITE")
draw.text((82, 162), "D", fill = "BLUE", font=font)

# Right
draw.rectangle([(115, 95), (165, 145)], outline = "BLUE", fill="WHITE")
draw.text((132, 112), "R", fill = "BLUE", font=font)

# Up
draw.rectangle([(65, 45), (115, 95)], outline = "BLUE", fill="WHITE")
draw.text((82, 62), "U", fill = "BLUE", font=font)

# Key1
draw.rectangle([(185, 35), (235, 85)], outline = "BLUE", fill="WHITE")
draw.text((195, 52), "K1", fill = "BLUE", font=font)

# Key2
draw.rectangle([(185, 95), (235, 145)], outline = "BLUE", fill="WHITE")
draw.text((195, 112), "K2", fill = "BLUE", font=font)

# Key3
draw.rectangle([(185, 155), (235, 205)], outline = "BLUE", fill="WHITE")
draw.text((195, 172), "K3", fill = "BLUE", font=font)


MAXCOUNTER=20
counter=MAXCOUNTER
XYVAL=(130, 6)
XYBAT=(208, 5)
XYPOW=(190, 2)
COUNT_DOWN=0

while True:
    keys.refresh_events()

    if keys.is_down_pressed():
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

    if keys.is_up_raise_event():
        draw.rectangle([(65, 45), (115, 95)], outline = "BLUE", fill="RED")
        draw.text((82, 62), "U", fill = "BLUE", font=font)
        print "UP pressed"
    if keys.is_up_fall_event():
        draw.rectangle([(65, 45), (115, 95)], outline = "BLUE", fill="WHITE")
        draw.text((82, 62), "U", fill = "BLUE", font=font)
        print "UP released"
    if keys.is_down_raise_event():
        draw.rectangle([(65, 145), (115, 195)], outline = "BLUE", fill="RED")
        draw.text((82, 162), "D", fill = "BLUE", font=font)
        print "DOWN pressed"
    if keys.is_down_fall_event():
        draw.rectangle([(65, 145), (115, 195)], outline = "BLUE", fill="WHITE")
        draw.text((82, 162), "D", fill = "BLUE", font=font)
        print "DOWN released"
    if keys.is_left_raise_event():
        draw.rectangle([(15, 95), (65, 145)], outline="BLUE", fill="RED")
        draw.text((32, 112), "L", fill = "BLUE", font=font)
        print "LEFT pressed"
    if keys.is_left_fall_event():
        draw.rectangle([(15, 95), (65, 145)], outline="BLUE", fill="WHITE")
        draw.text((32, 112), "L", fill = "BLUE", font=font)
        print "LEFT released"
    if keys.is_right_raise_event():
        draw.rectangle([(115, 95), (165, 145)], outline = "BLUE", fill="RED")
        draw.text((132, 112), "R", fill = "BLUE", font=font)
        print "RIGHT pressed"
    if keys.is_right_fall_event():
        draw.rectangle([(115, 95), (165, 145)], outline = "BLUE", fill="WHITE")
        draw.text((132, 112), "R", fill = "BLUE", font=font)
        print "RIGHT released"
    if keys.is_enter_raise_event():
        draw.ellipse((90-25, 120-25, 90+25, 120+25), outline="BLUE", fill="RED")
        draw.text((82, 112), "P", fill = "BLUE", font=font)
        print "PRESS pressed"
    if keys.is_enter_fall_event():
        draw.ellipse((90-25, 120-25, 90+25, 120+25), outline="BLUE", fill="WHITE")
        draw.text((82, 112), "P", fill = "BLUE", font=font)
        print "PRESS released"
    if keys.is_key1_raise_event():
        draw.rectangle([(185, 35), (235, 85)], outline = "BLUE", fill="RED")
        draw.text((195, 52), "K1", fill = "BLUE", font=font)
        print "KEY1 pressed"
    if keys.is_key1_fall_event():
        draw.rectangle([(185, 35), (235, 85)], outline = "BLUE", fill="WHITE")
        draw.text((195, 52), "K1", fill = "BLUE", font=font)
        print "KEY1 released"
    if keys.is_key2_raise_event():
        draw.rectangle([(185, 95), (235, 145)], outline = "BLUE", fill="RED")
        draw.text((195, 112), "K2", fill = "BLUE", font=font)
        print "KEY2 pressed"
    if keys.is_key2_fall_event():
        draw.rectangle([(185, 95), (235, 145)], outline = "BLUE", fill="WHITE")
        draw.text((195, 112), "K2", fill = "BLUE", font=font)
        print "KEY2 released"
    if keys.is_key3_raise_event():
        draw.rectangle([(185, 155), (235, 205)], outline = "BLUE", fill="RED")
        draw.text((195, 172), "K3", fill = "BLUE", font=font)
        print "KEY3 pressed"
    if keys.is_key3_fall_event():
        draw.rectangle([(185, 155), (235, 205)], outline = "BLUE", fill="WHITE")
        draw.text((195, 172), "K3", fill = "BLUE", font=font)
        print "KEY3 released"

    disp.ShowImage(image1,0,0)
