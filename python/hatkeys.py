#!/usr/bin/env python

dummy=False
try:
    import RPi.GPIO as GPIO
except ImportError:
    from pynput import keyboard
    dummy=True

class KEYS(object):
    """class for Keys of 240*240 1.3inch OLED displays."""

    def __init__(self,ext_power=4, up=6, down=19, left=5, right=26, enter=13, key1=21, key2=20, key3=16):
        # For ext_power to be detected, solder bridge the solder jumper
        self._prev = {'up':0, 'down':0, 'left':0, 'right':0, 'enter':0, 'key1':0, 'key2':0, 'key3':0}

        if dummy: # Emulate hat buttons
            # arrows: arrows
            # enter:  Enter
            # key1:   F1
            # key2:   F2
            # key3:   F3
            # power:  Caps lock
            self._kbddict={
                keyboard.Key.up: 'up',
                keyboard.Key.down: 'down',
                keyboard.Key.left: 'left',
                keyboard.Key.right: 'right',
                keyboard.Key.enter: 'enter',
                keyboard.Key.f1: 'key1',
                keyboard.Key.f2: 'key2',
                keyboard.Key.f3: 'key3'
            }
            self._leveldict = {'up':1, 'down':1, 'left':1, 'right':1, 'enter':1, 'key1':1, 'key2':1, 'key3':1}
            self._level_ext_power=0
            def on_press(key):
                if key in self._kbddict:
                    self._leveldict[self._kbddict[key]] = 0
                if key==keyboard.Key.caps_lock:
                    self._level_ext_power^=1

            def on_release(key):
                if key in self._kbddict:
                    self._leveldict[self._kbddict[key]] = 1

            listener = keyboard.Listener(
                on_press=on_press,
                on_release=on_release)
            listener.start()
            self.refresh_events()
            return
        # else: non dummy:
        self._gpio_ext_power=ext_power
        self._gpiodict = {'up':up, 'down':down, 'left':left, 'right':right, 'enter':enter, 'key1':key1, 'key2':key2, 'key3':key3}
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self._gpio_ext_power, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
        for key in self._gpiodict.keys():
            GPIO.setup(self._gpiodict[key], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.refresh_events()

    def is_ext_power_available(self):
        if dummy:
            return self._level_ext_power
        return GPIO.input(self._gpio_ext_power)==1

    def is_pressed(self, key):
        if key not in self._event_fall:
            raise ValueError
        if dummy:
            return self._leveldict[key] == 0
        return GPIO.input(self._gpiodict[key])==0

    def is_raise_event(self, key):
        if key not in self._event_fall:
            raise ValueError
        return self._event_raise[key]

    def is_fall_event(self, key):
        if key not in self._event_fall:
            raise ValueError
        return self._event_fall[key]

    def refresh_events(self):
        self._event_raise = {'up':False, 'down':False, 'left':False, 'right':False, 'enter':False, 'key1':False, 'key2':False, 'key3':False}
        self._event_fall  = {'up':False, 'down':False, 'left':False, 'right':False, 'enter':False, 'key1':False, 'key2':False, 'key3':False}
        for key in self._event_raise.keys():
            if self.is_pressed(key):
                if self._prev[key] == 0:
                    self._event_raise[key]=True
                self._prev[key]+=1
            elif self._prev[key] > 0:
                self._event_fall[key]=True
                self._prev[key]=0

    def cleanup(self):
        if dummy:
            return
        GPIO.cleanup()

if __name__=='__main__':
    import time
    import sys
    keys = KEYS()
    old = {'up':False, 'down':False, 'left':False, 'right':False, 'enter':False, 'key1':False, 'key2':False, 'key3':False}
    old_POWER=False
    try:
        while True:
            for key in old.keys():
                if keys.is_pressed(key) and not old[key]:
                    print "%s pressed" % key
                    old[key]=True
                elif not keys.is_pressed(key) and old[key]:
                    print "%s released" % key
                    old[key]=False

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
