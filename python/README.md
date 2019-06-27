## UPS_Lite

```
try:
    from UPS_Lite import get_ups
except ImportError:
    from dummy_UPS_Lite import get_ups

ups = get_ups()
ups.get_voltage()
ups.get_capacity()
```

## ST7789

```
try:
    from ST7789 import get_disp
except ImportError:
    from dummy_ST7789 import get_disp

disp = get_disp()
disp.clear()
image1 = Image.open('pic.jpg')
disp.ShowImage(image1,0,0)
```

## hatkeys

```
try:
    from hatkeys import get_keys
except ImportError:
    from dummy_hatkeys import get_keys

keys = get_keys()
if keys.is_up_pressed():
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
