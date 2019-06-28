#!/usr/bin/env python

dummy=False
try:
    import RPi.GPIO as GPIO
except ImportError:
    from pynput import keyboard
    dummy=True

class KEYS(object):
    """class for Keys of 240*240 1.3inch OLED displays."""

    def __init__(self,ext_power=4, up=6, down=19, left=5, right=26, press=13, key1=21, key2=20, key3=16):
        # For ext_power to be detected, solder bridge the solder jumper
        self._prev_UP=0
        self._prev_DOWN=0
        self._prev_LEFT=0
        self._prev_RIGHT=0
        self._prev_PRESS=0
        self._prev_KEY1=0
        self._prev_KEY2=0
        self._prev_KEY3=0

        if dummy: # Emulate hat buttons
            # arrows: arrows
            # press:  Enter
            # key1:   F1
            # key2:   F2
            # key3:   F3
            # power:  Caps lock
            self._keydict={
                keyboard.Key.up: 1,
                keyboard.Key.down: 1,
                keyboard.Key.left: 1,
                keyboard.Key.right: 1,
                keyboard.Key.enter: 1,
                keyboard.Key.f1: 1,
                keyboard.Key.f2: 1,
                keyboard.Key.f3: 1
            }
            self._level_ext_power=0
            def on_press(key):
                if key in self._keydict:
                    self._keydict[key] = 0
                if key==keyboard.Key.caps_lock:
                    self._level_ext_power^=1

            def on_release(key):
                if key in self._keydict:
                    self._keydict[key] = 1

            listener = keyboard.Listener(
                on_press=on_press,
                on_release=on_release)
            listener.start()
            self.refresh_events()
            return
        # else: non dummy:
        self._gpio_ext_power=ext_power
        self._gpio_up=up
        self._gpio_down=down
        self._gpio_left=left
        self._gpio_right=right
        self._gpio_press=press
        self._gpio_key1=key1
        self._gpio_key2=key2
        self._gpio_key3=key3
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self._gpio_ext_power, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
        GPIO.setup(self._gpio_up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._gpio_down, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._gpio_left, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._gpio_right, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._gpio_press, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._gpio_key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._gpio_key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._gpio_key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.refresh_events()

    def is_ext_power_available(self):
        if dummy:
            return self._level_ext_power
        return GPIO.input(self._gpio_ext_power)==1

    def is_up_pressed(self):
        if dummy:
            return self._keydict[keyboard.Key.up] == 0
        return GPIO.input(self._gpio_up)==0

    def is_down_pressed(self):
        if dummy:
            return self._keydict[keyboard.Key.down] == 0
        return GPIO.input(self._gpio_down)==0

    def is_left_pressed(self):
        if dummy:
            return self._keydict[keyboard.Key.left] == 0
        return GPIO.input(self._gpio_left)==0

    def is_right_pressed(self):
        if dummy:
            return self._keydict[keyboard.Key.right] == 0
        return GPIO.input(self._gpio_right)==0

    def is_enter_pressed(self):
        if dummy:
            return self._keydict[keyboard.Key.enter] == 0
        return GPIO.input(self._gpio_press)==0

    def is_key1_pressed(self):
        if dummy:
            return self._keydict[keyboard.Key.f1] == 0
        return GPIO.input(self._gpio_key1)==0

    def is_key2_pressed(self):
        if dummy:
            return self._keydict[keyboard.Key.f2] == 0
        return GPIO.input(self._gpio_key2)==0

    def is_key3_pressed(self):
        if dummy:
            return self._keydict[keyboard.Key.f3] == 0
        return GPIO.input(self._gpio_key3)==0

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
            if self._prev_UP == 0:
                self._event_raise_up=True
            self._prev_UP+=1
        elif self._prev_UP > 0:
            self._event_fall_up=True
            self._prev_UP=0

        if self.is_down_pressed():
            if self._prev_DOWN == 0:
                self._event_raise_down=True
            self._prev_DOWN+=1
        elif self._prev_DOWN > 0:
            self._event_fall_down=True
            self._prev_DOWN=0

        if self.is_left_pressed():
            if self._prev_LEFT == 0:
                self._event_raise_left=True
            self._prev_LEFT+=1
        elif self._prev_LEFT > 0:
            self._event_fall_left=True
            self._prev_LEFT=0

        if self.is_right_pressed():
            if self._prev_RIGHT == 0:
                self._event_raise_right=True
            self._prev_RIGHT+=1
        elif self._prev_RIGHT > 0:
            self._event_fall_right=True
            self._prev_RIGHT=0

        if self.is_enter_pressed():
            if self._prev_PRESS == 0:
                self._event_raise_enter=True
            self._prev_PRESS+=1
        elif self._prev_PRESS > 0:
            self._event_fall_enter=True
            self._prev_PRESS=0

        if self.is_key1_pressed():
            if self._prev_KEY1 == 0:
                self._event_raise_key1=True
            self._prev_KEY1+=1
        elif self._prev_KEY1 > 0:
            self._event_fall_key1=True
            self._prev_KEY1=0

        if self.is_key2_pressed():
            if self._prev_KEY2 == 0:
                self._event_raise_key2=True
            self._prev_KEY2+=1
        elif self._prev_KEY2 > 0:
            self._event_fall_key2=True
            self._prev_KEY2=0

        if self.is_key3_pressed():
            if self._prev_KEY3 == 0:
                self._event_raise_key3=True
            self._prev_KEY3+=1
        elif self._prev_KEY3 > 0:
            self._event_fall_key3=True
            self._prev_KEY3=0

    def cleanup(self):
        if dummy:
            return
        GPIO.cleanup()

if __name__=='__main__':
    import time
    import sys
    keys = KEYS()
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
        keys.cleanup()
        sys.exit(0)
