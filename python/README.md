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


## foopm3

First attempt at a GUI...

To install it as a startup service:

```
mkdir -p ~/.config/systemd/user/
ln -s ~/rpizerogui/python/foopm3.service ~/.config/systemd/user/
# Make sure user service scripts are started without waiting for user login:
sudo loginctl enable-linger pi
systemctl --user enable foopm3
```
