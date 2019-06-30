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

from ST7789 import ST7789
from hatkeys import KEYS
from UPS_Lite import UPS

if 'PM3PATH' in os.environ:
    g_pm3path=os.environ['PM3PATH']
else:
    g_pm3path="/home/pi/proxmark3/"

g_scriptpath = os.path.dirname(os.path.realpath(__file__))

def tadd(a, b):
    if isinstance(b, list):
        return [(a[0]+i[0], a[1]+i[1]) for i in b]
    else:
        return (a[0]+b[0], a[1]+b[1])

def get_wifi_ssid():
    try:
        scanoutput = subprocess.check_output(["iw", "wlan0", "info"], stderr=devnull)
        for line in scanoutput.split('\n'):
            line = line.decode("utf-8").strip()
            if line[:4]  == "ssid":
                ssid = line.split()[1]
    except:
        ssid = "WiFi not found"
    return ssid

def get_ip():
    try:
        ipoutput = subprocess.check_output(["ip", "-f", "inet", "addr", "show", "wlan0"], stderr=devnull)
        for line in ipoutput.split('\n'):
            line = line.decode("utf-8").strip()
            if line[:4]  == "inet":
                ip = line.split()[1].split('/')[0]
    except:
        ip = "IP not found"
    return ip

g_disp = ST7789()
g_keys = KEYS()
g_ups = UPS()

# Clear display.
g_disp.clear()
g_font32 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 32)

# Welcome screen

g_image1 = Image.open(os.path.join(g_scriptpath, 'illuminated_rfid_240.png'))
g_draw1 = ImageDraw.Draw(g_image1)

if os.path.isfile(os.path.join(g_scriptpath, 'maintenance')):
#    print('maintenance')
    g_draw1.rectangle([(15,70),(230,100)],fill = "BLACK")
    g_draw1.text((20, 70), 'Maintenance', fill = "LIGHTBLUE", font=g_font32)
    g_disp.ShowImage(g_image1,0,0)
    while os.path.isfile(os.path.join(g_scriptpath, 'maintenance')):
        time.sleep(1)
    exit(0)

g_draw1.rectangle([(15,70),(195,100)],fill = "BLACK")
g_draw1.text((20, 70), 'Proxmark3', fill = "LIGHTBLUE", font=g_font32)
g_draw1.text((19, 139), 'Wardriving', fill = "WHITE", font=g_font32)
g_draw1.text((19, 142), 'Wardriving', fill = "WHITE", font=g_font32)
g_draw1.text((22, 139), 'Wardriving', fill = "WHITE", font=g_font32)
g_draw1.text((20, 140), 'Wardriving', fill = "BLACK", font=g_font32)
g_disp.ShowImage(g_image1,0,0)
del(g_image1)
del(g_draw1)
time.sleep(2)

# Create blank image for drawing.
g_image = Image.new("RGB", (g_disp.width, g_disp.height), "BLACK")
g_draw = ImageDraw.Draw(g_image)

def init_cmds(cmds, cur_bullet):
    g_draw.rectangle([(0, YCMD), (240, 240)], fill="BLACK")
    for i in range(len(cmds)):
        g_draw.ellipse((10-5, (YCMD+15*i), 10+5, (YCMD+15*i)+10), outline="BLACK", fill="WHITE")
        g_draw.text((20, (YCMD+15*i)), cmds[i][0], fill = "white")
    g_draw.ellipse((10-5, (YCMD+15*cur_bullet), 10+5, (YCMD+15*cur_bullet)+10), outline="BLACK", fill="RED")

def display_output(out):
    outlist = []
    for l in out.split('\n'):
        outlist += [ l[i:i+TXTWIDTH] for i in range(0, len(l.rstrip()), TXTWIDTH) ]
    off = 0
    max_off = max(0, len(outlist) - TXTHEIGHT//2)
    while True:
        g_draw.rectangle([(0, YCMD), (240, 240)], fill="BLACK")
        outlistscreen = '\n'.join(outlist[off:TXTHEIGHT+off])
        g_draw.text((0, YCMD), outlistscreen, fill = "WHITE")
        g_disp.ShowImage(g_image,0,0)
        g_keys.refresh_events()
        if g_keys.is_raise_event('left'):
            break
        if g_keys.is_pressed('up'):
            if off == 0:
                off = max_off
            else:
                off -= 1
        if g_keys.is_pressed('down'):
            if off == max_off:
                off = 0
            else:
                off += 1

def display_menu(cmds, level):
    MAXCOUNTER=8
    counter=MAXCOUNTER
    cur_bullet=0
    max_bullet=len(cmds) - 1
    init_cmds(cmds, cur_bullet)
    while True:
        g_keys.refresh_events()

        if g_keys.is_pressed('left'):
            if level > 0:
                break
            if COUNT_DOWN > 5:
                g_disp.clear()
                time.sleep(0.6)
                break
            COUNT_DOWN+=1
        else:
            COUNT_DOWN=0

        if g_keys.is_raise_event('up'):
            g_draw.ellipse((10-5, (YCMD+15*cur_bullet), 10+5, (YCMD+15*cur_bullet)+10), outline="BLACK", fill="WHITE")
            if cur_bullet == 0:
                cur_bullet = max_bullet
            else:
                cur_bullet-=1
            g_draw.ellipse((10-5, (YCMD+15*cur_bullet), 10+5, (YCMD+15*cur_bullet)+10), outline="BLACK", fill="RED")

        if g_keys.is_raise_event('down'):
            g_draw.ellipse((10-5, (YCMD+15*cur_bullet), 10+5, (YCMD+15*cur_bullet)+10), outline="BLACK", fill="WHITE")
            if cur_bullet == max_bullet:
                cur_bullet = 0
            else:
                cur_bullet+=1
            g_draw.ellipse((10-5, (YCMD+15*cur_bullet), 10+5, (YCMD+15*cur_bullet)+10), outline="BLACK", fill="RED")

        if g_keys.is_raise_event('enter'):
            g_draw.rectangle([(0, YCMD), (240, 240)], fill="BLACK")
            g_draw.text((0, YCMD), "Please wait...", fill = "WHITE")
            g_disp.ShowImage(g_image,0,0)
            if isinstance(cmds[cur_bullet][1], list):
                display_menu(cmds[cur_bullet][1], level+1)
            else:
                try:
                    out = subprocess.check_output(cmds[cur_bullet][1], shell=True)
                    display_output(out)
                except subprocess.CalledProcessError, e:
                    display_output(str(e))
            init_cmds(cmds, cur_bullet)

        if counter == MAXCOUNTER:
            counter = 0
            g_draw.rectangle([(0, 0), (240, 20)], fill="BLACK")
            # time
            now = datetime.datetime.now()
            g_draw.text(XYTIM, now.strftime("%H:%M:%S"), fill = "LIGHTGREEN")
            # battery stats
            v, c = g_ups.get_voltage(), g_ups.get_capacity()
            BATSTAT="%.2fV %i%%" %(v, c)
            #print (BATSTAT)
            g_draw.text(XYVAL, BATSTAT, fill = "LIGHTGREEN")
            # battery icon
            g_draw.rectangle(tadd(XYBAT, [(2,0), (2+25,10)]), outline = "LIGHTGREEN")
            g_draw.rectangle(tadd(XYBAT, [(0,3), (1,7)]), fill = "LIGHTGREEN")
            g_draw.rectangle(tadd(XYBAT, [(2+25-(c/4), 0), (2+25,10)]), fill="LIGHTGREEN")
            # power icon
            if g_keys.is_ext_power_available():
                g_draw.polygon(tadd(XYPOW, [(7,0), (0,10), (4,9), (1,16), (10,6), (5,7)]), fill="LIGHTGREEN")
            # network info
            SSID = get_wifi_ssid()
            IP = get_ip()
            g_draw.text(XYNET, IP + (" " * (TXTWIDTH - len(SSID) - len(IP))) + SSID, fill = "YELLOW")
        counter+=1

        g_disp.ShowImage(g_image,0,0)

YCMD=30
XYVAL=(130, 6)
XYBAT=(208, 5)
XYPOW=(192, 2)
XYTIM=(5, 5)
XYNET=(5, 16)
COUNT_DOWN=0
# nr of chars with the default font:
TXTWIDTH=39
TXTHEIGHT=14

pm3cmds=[
    ("hw status", "%s/client/proxmark3 -p /dev/ttyACM0 -c \"hw status\"" % g_pm3path),
    ("hf search", "%s/client/proxmark3 -p /dev/ttyACM0 -c \"hf search\"" % g_pm3path),
    ("lf search", "%s/client/proxmark3 -p /dev/ttyACM0 -c \"lf search\"" % g_pm3path)
]
maincmds=[
    ("Go to PROXMARK3 Menu", pm3cmds),
    ("PM3> git pull", "cd \"%s\" && git pull" % g_pm3path),
    ("PM3> make clean", "cd \"%s\" && make clean" % g_pm3path),
    ("PM3> make", "cd \"%s\" && make" % g_pm3path),
    ("PM3> flash-all.sh", "cd \"%s\" && ./flash-all.sh" % g_pm3path),
    ("GUI> git pull", "cd \"%s\" && git pull" % g_scriptpath),
    ("SYS> shutdown...", "sudo shutdown -h now"),
]
MENULEVEL=1
display_menu(maincmds, 0)
