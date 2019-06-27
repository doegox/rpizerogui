#!/usr/bin/env python

import RPi.GPIO as GPIO

class hatkeys(object):
    """class for Keys of 240*240 1.3inch OLED displays."""

    def __init__(self,ext_power=4, up=6, down=19, left=5, right=26, press=13, key1=21, key2=20, key3=16):
        # For ext_power to be detected, solder bridge the solder jumper
        self._ext_power=ext_power
        self._up=up
        self._down=down
        self._left=left
        self._right=right
        self._press=press
        self._key1=key1
        self._key2=key2
        self._key3=key3
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self._ext_power, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
        GPIO.setup(self._up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._down, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._left, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._right, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._press, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def is_ext_power_available(self):
        return GPIO.input(self._ext_power)==1

    def is_up_pressed(self):
        return GPIO.input(self._up)==0

    def is_down_pressed(self):
        return GPIO.input(self._down)==0

    def is_left_pressed(self):
        return GPIO.input(self._left)==0

    def is_right_pressed(self):
        return GPIO.input(self._right)==0

    def is_enter_pressed(self):
        return GPIO.input(self._press)==0

    def is_key1_pressed(self):
        return GPIO.input(self._key1)==0

    def is_key2_pressed(self):
        return GPIO.input(self._key2)==0

    def is_key3_pressed(self):
        return GPIO.input(self._key3)==0

def get_keys():
    keys = hatkeys()
    return keys

if __name__=='__main__':
    import time
    import sys
    keys = get_keys()
    old_UP=False
    old_DOWN=False
    old_LEFT=False
    old_RIGHT=False
    old_PRESS=False
    old_KEY1=False
    old_KEY2=False
    old_KEY3=False
    old_POWER=False
    try:
        while True:
            if keys.is_up_pressed() and not old_UP:
                print "UP pressed"
                old_UP=True
            elif not keys.is_up_pressed() and old_UP:
                print "UP released"
                old_UP=False

            if keys.is_down_pressed() and not old_DOWN:
                print "DOWN pressed"
                old_DOWN=True
            elif not keys.is_down_pressed() and old_DOWN:
                print "DOWN released"
                old_DOWN=False

            if keys.is_left_pressed() and not old_LEFT:
                print "LEFT pressed"
                old_LEFT=True
            elif not keys.is_left_pressed() and old_LEFT:
                print "LEFT released"
                old_LEFT=False

            if keys.is_right_pressed() and not old_RIGHT:
                print "RIGHT pressed"
                old_RIGHT=True
            elif not keys.is_right_pressed() and old_RIGHT:
                print "RIGHT released"
                old_RIGHT=False

            if keys.is_enter_pressed() and not old_PRESS:
                print "PRESS pressed"
                old_PRESS=True
            elif not keys.is_enter_pressed() and old_PRESS:
                print "PRESS released"
                old_PRESS=False

            if keys.is_key1_pressed() and not old_KEY1:
                print "KEY1 pressed"
                old_KEY1=True
            elif not keys.is_key1_pressed() and old_KEY1:
                print "KEY1 released"
                old_KEY1=False

            if keys.is_key2_pressed() and not old_KEY2:
                print "KEY2 pressed"
                old_KEY2=True
            elif not keys.is_key2_pressed() and old_KEY2:
                print "KEY2 released"
                old_KEY2=False

            if keys.is_key3_pressed() and not old_KEY3:
                print "KEY3 pressed"
                old_KEY3=True
            elif not keys.is_key3_pressed() and old_KEY3:
                print "KEY3 released"
                old_KEY3=False

            if keys.is_ext_power_available() and not old_POWER:
                print "Power applied"
                old_POWER=True
            elif not keys.is_ext_power_available() and old_POWER:
                print "Power removed"
                old_POWER=False

            time.sleep(0.1)
    finally:
        print("Bye!")
        GPIO.cleanup()
        sys.exit(0)
