## LCD shield

### Refs

* https://www.waveshare.com/1.3inch-lcd-hat.htm
* http://www.rhydolabz.com/documents/33/manual.pdf
* https://www.aliexpress.com/item/1-3inch-IPS-LCD-Display-HAT-for-Raspberry-Pi-240x240-pixels-SPI-interface-Supports-Raspberry-Pi/32908225177.html
* https://www.waveshare.com/wiki/1.3inch_LCD_HAT
* https://wavesharejfs.blogspot.com/2018/03/raspberry-pi-driv-144inch-lcd-hat-with.html
* https://github.com/juj/fbcp-ili9341
* https://www.instructables.com/id/Orange-Pi-Zero-Connect-TFT-SPI-ST7735/

### Characteristics

* 1.3inch diagonal
* Driver: ST7789
* Interface: SPI
* Display color: RGB, 65K color
* Resolution: 240x240
* Backlight: LED
* Operating voltage: 3.3V

|SYMBOL        |Raspberry Pi PIN (BCM)|DESCRIPTION                      |
|--------------|----------------------|---------------------------------|
|KEY1          |P21                   |Button 1/GPIO                    |
|KEY2          |P20                   |Button 2/GPIO                    |
|KEY3          |P16                   |Button 3/GPIO                    |
|Joystick Up   |P6                    |Joystick Up                      |
|Joystick Down |P19                   |Joystick Down                    |
|Joystick Left |P5                    |Joystick Left                    |
|Joystick Right|P26                   |Joystick Right                   |
|Joystick Press|P13                   |Joystick Press                   |
|SCLK          |P11/SCLK              |SPI clock input                  |
|MOSI          |P10/MOSI              |SPI data input                   |
|DC            |P25                   |Data/Command selection (H=D, L=C)|
|CS            |P8/CE0                |Chip selection, low active       |
|RST           |P27                   |Reset, low active                |
|BL            |P24                   |Backlight                        |


## UPS-Lite shield

### Refs

* https://www.aliexpress.com/item/Raspberry-Pi-Zero-UPS-Power-Expansion-Board-With-integrated-serial-port-and-power-detection-Support-RPI/32961105269.html
* https://github.com/linshuqin329/UPS-Lite
* https://www.thingiverse.com/thing:3479388

### Characteristics

* serial port CP2104
* fuel gauge chip MAX17040G
* 1000mAh LiPo battery
* Charging current: 400mA
* Output voltage: 5V ±0.1V
* Output current
  * 1.3A@5V (without external adapter, only battery powered)
  *   2A@5V (in case of external adapter)

Mini DIP switch: to isolate RX/TX lines between USB and RPi

Solder bridge: to bring external voltage detection to GPIO BCM 4

## RPi Setup

Raspbian Lite:

https://www.raspberrypi.org/downloads/raspbian/ => Raspbian Buster Lite (better than NOOB to maximize available filesystem space)
```
unzip -p Downloads/2019-06-20-raspbian-buster-lite.zip | sudo dd of=/dev/mmcblk0 bs=4M conv=fsync status=progress
```

Resize FS:

```
sudo raspi-config
Advanced / resizefs
```

Activate SSH: add file ssh to the SDCard
```
touch boot/ssh
```

Activate Wi-Fi: add file wpa_supplicant.conf to the SDCard
```
vi boot/wpa_supplicant.conf
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=FR

network={
  ssid="mySSID"
  psk="todo"
  key_mgmt=WPA-PSK
}
network={
  ssid="mySSID2"
  psk="todo"
  key_mgmt=WPA-PSK
}
```

```
ssh pi@IP
# current pwd: raspberry
passwd
# change pwd
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install mc screen dos2unix hexedit
```

## RPi UPS Setup

Activate I2C:

```
sudo apt-get install python-smbus
sudo raspi-config
# Interfacing / P5 I2C
sudo shutdown -r now
sudo i2cdetect -l
# i2c-1	i2c       	bcm2835 I2C adapter             	I2C adapter
```

UPS external power: solder bridge to put it on GPIO BCM4 to detect when external power is supplied

UPS measures:
* charging: 500mA
* standby:  120mA
* working:  220mA

## RPi LCD Setup

```
sudo raspi-config
# Interfaces / SPI
```

## Python requirements

```
sudo apt-get install python-spidev python-numpy python-pil fonts-freefont-ttf
```
