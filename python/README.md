# Libraries

## UPS_Lite

```
from UPS_Lite import UPS

ups = UPS()
ups.get_voltage()
ups.get_capacity()
```

## ST7789

```
from ST7789 import ST7789

disp = ST7789()
disp.clear()
image1 = Image.open('pic.jpg')
disp.ShowImage(image1,0,0)
```

## hatkeys

```
from hatkeys import KEYS

keys = KEYS()
if keys.is_pressed('up'):
    print "UP pressed"
if keys.is_ext_power_available():
    print "Power applied"
```

`is_ext_power_available` relates to the UPS shield, not the LCD shield.
It requires the solder jumper to be bridged.

|hatkeys  |LCD shield|dummy emulation|
|---------|----------|---------------|
|up       |up        | up arrow      |
|down     |down      | down arrow    |
|left     |left      | left arrow    |
|right    |right     | right arrow   |
|enter    |press     | enter         |
|key1     |key1      | F1            |
|key2     |key2      | F2            |
|key3     |key3      | F3            |
|ext_power|UPS usb   | Caps lock     |


# foopm3

First attempt at a GUI...

## install it as a startup service

```
mkdir -p ~/.config/systemd/user/
ln -s ~/rpizerogui/python/foopm3.service ~/.config/systemd/user/
# Make sure user service scripts are started without waiting for user login:
sudo loginctl enable-linger pi
systemctl --user enable foopm3
```

## usage

* pull to left for 2s from main screen to quit. As it's a service it'll be restarted automatically.
* create "maintenance" file in `~/rpizerogui/python` to stall foopm3 service and be able to use the LCD
* it expects proxmark repo to be in `/home/pi/proxmark3/`, else define it in envvar `PM3PATH`.

## TODO list

* enable fb on boot to get dmesgs? Then disable fb when starting foopm3...
* detect when pm3 is not connected and handle it properly
* GUI menus, see below
* GUI: avoid 100% CPU and still stay reactive...

### TODO menu Level 1: Shell commands

* reactivate fb and get shell with BT/USB keyboard??
* wifi config
* display output progressively, not just after full exec

### TODO menu Level 2: Proxmark commands

* interactive expect-style
* handle interactive cmds...
