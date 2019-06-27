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
        self._old_UP=0
        self._old_DOWN=0
        self._old_LEFT=0
        self._old_RIGHT=0
        self._old_PRESS=0
        self._old_KEY1=0
        self._old_KEY2=0
        self._old_KEY3=0

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

    def is_up_raise_event(self):
        return self._event_raise_up

    def is_down_raise_event(self):
        return self._event_raise_down

    def is_left_raise_event(self):
        return self._event_raise_left

    def is_right_raise_event(self):
        return self._event_raise_right

    def is_enter_raise_event(self):
        return self._event_raise_enter

    def is_key1_raise_event(self):
        return self._event_raise_key1

    def is_key2_raise_event(self):
        return self._event_raise_key2

    def is_key3_raise_event(self):
        return self._event_raise_key3

    def is_up_fall_event(self):
        return self._event_fall_up

    def is_down_fall_event(self):
        return self._event_fall_down

    def is_left_fall_event(self):
        return self._event_fall_left

    def is_right_fall_event(self):
        return self._event_fall_right

    def is_enter_fall_event(self):
        return self._event_fall_enter

    def is_key1_fall_event(self):
        return self._event_fall_key1

    def is_key2_fall_event(self):
        return self._event_fall_key2

    def is_key3_fall_event(self):
        return self._event_fall_key3

    def refresh_events(self):
        self._event_raise_up=False
        self._event_raise_down=False
        self._event_raise_left=False
        self._event_raise_right=False
        self._event_raise_enter=False
        self._event_raise_key1=False
        self._event_raise_key2=False
        self._event_raise_key3=False
        self._event_fall_up=False
        self._event_fall_down=False
        self._event_fall_left=False
        self._event_fall_right=False
        self._event_fall_enter=False
        self._event_fall_key1=False
        self._event_fall_key2=False
        self._event_fall_key3=False
        if self.is_up_pressed():
            if self._old_UP == 0:
                self._event_raise_up=True
            self._old_UP+=1
        elif self._old_UP > 0:
            self._event_fall_up=True
            self._old_UP=0

        if self.is_down_pressed():
            if self._old_DOWN == 0:
                self._event_raise_down=True
            self._old_DOWN+=1
        elif self._old_DOWN > 0:
            self._event_fall_down=True
            self._old_DOWN=0

        if self.is_left_pressed():
            if self._old_LEFT == 0:
                self._event_raise_left=True
            self._old_LEFT+=1
        elif self._old_LEFT > 0:
            self._event_fall_left=True
            self._old_LEFT=0

        if self.is_right_pressed():
            if self._old_RIGHT == 0:
                self._event_raise_right=True
            self._old_RIGHT+=1
        elif self._old_RIGHT > 0:
            self._event_fall_right=True
            self._old_RIGHT=0

        if self.is_enter_pressed():
            if self._old_PRESS == 0:
                self._event_raise_enter=True
            self._old_PRESS+=1
        elif self._old_PRESS > 0:
            self._event_fall_enter=True
            self._old_PRESS=0

        if self.is_key1_pressed():
            if self._old_KEY1 == 0:
                self._event_raise_key1=True
            self._old_KEY1+=1
        elif self._old_KEY1 > 0:
            self._event_fall_key1=True
            self._old_KEY1=0

        if self.is_key2_pressed():
            if self._old_KEY2 == 0:
                self._event_raise_key2=True
            self._old_KEY2+=1
        elif self._old_KEY2 > 0:
            self._event_fall_key2=True
            self._old_KEY2=0

        if self.is_key3_pressed():
            if self._old_KEY3 == 0:
                self._event_raise_key3=True
            self._old_KEY3+=1
        elif self._old_KEY3 > 0:
            self._event_fall_key3=True
            self._old_KEY3=0

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
