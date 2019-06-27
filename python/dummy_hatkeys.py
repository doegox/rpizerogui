#!/usr/bin/env python

from pynput import keyboard

class DummyHatkeys(object):
    """Emulate hat buttons
    arrows and press: arrows and enter
    key1: 1
    key2: 2
    key3: 3
    ext power: caps lock
    """
    def __init__(self):
        self._up=1
        self._down=1
        self._left=1
        self._right=1
        self._press=1
        self._key1=1
        self._key2=1
        self._key3=1
        self._ext_power=0
        def on_press(key):
            if key==keyboard.Key.up:
                self._up=0
            if key==keyboard.Key.down:
                self._down=0
            if key==keyboard.Key.left:
                self._left=0
            if key==keyboard.Key.right:
                self._right=0
            if key==keyboard.Key.enter:
                self._press=0
            if key==keyboard.Key.f1:
                self._key1=0
            if key==keyboard.Key.f2:
                self._key2=0
            if key==keyboard.Key.f3:
                self._key3=0
            if key==keyboard.Key.caps_lock:
                self._ext_power^=1

        def on_release(key):
            if key == keyboard.Key.esc:
                # Stop listener
                return False
            if key==keyboard.Key.up:
                self._up=1
            if key==keyboard.Key.down:
                self._down=1
            if key==keyboard.Key.left:
                self._left=1
            if key==keyboard.Key.right:
                self._right=1
            if key==keyboard.Key.enter:
                self._press=1
            if key==keyboard.Key.f1:
                self._key1=1
            if key==keyboard.Key.f2:
                self._key2=1
            if key==keyboard.Key.f3:
                self._key3=1

        listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release)
        listener.start()

    def is_ext_power_available(self):
        return self._ext_power

    def is_up_pressed(self):
        return not self._up

    def is_down_pressed(self):
        return not self._down

    def is_left_pressed(self):
        return not self._left

    def is_right_pressed(self):
        return not self._right

    def is_enter_pressed(self):
        return not self._press

    def is_key1_pressed(self):
        return not self._key1

    def is_key2_pressed(self):
        return not self._key2

    def is_key3_pressed(self):
        return not self._key3

def get_keys():
    keys = DummyHatkeys()
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
        sys.exit(0)
