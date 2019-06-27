#!/usr/bin/env python
import struct
import smbus

class UPS(object):
    def __init__(self, port=1):
        self.bus = smbus.SMBus(port)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

    def get_voltage(self):
        "returns as float the voltage from the Raspi UPS Hat"
        address = 0x36
        read = self.bus.read_word_data(address, 2)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        voltage = swapped * 1.25 /1000/16
        return voltage

    def get_capacity(self):
        "returns as a int the remaining capacity in %% of the battery connected to the Raspi UPS Hat"
        address = 0x36
        capacity = self.bus.read_byte_data(address, 4)
        # apparently MAX17040 may return 101%, let's max it to 100%...
        return min(capacity, 100)

def get_ups():
    ups = UPS()
    return ups

if __name__=='__main__':
    import sys
    import time
    ups = get_ups()
    if len(sys.argv) > 1 and sys.argv[1] == '-c':
        # continuous mode
        while True:
            print "++++++++++++++++++++"
            print "Voltage:%5.2fV" % ups.get_voltage()
            c = ups.get_capacity()
            print "Battery:%5i%%" % c
            if c == 100:
                print "Battery FULL"
            if c < 20:
                print "Battery LOW"
            print "++++++++++++++++++++"
            time.sleep(2)
    else:
        print ("%.2f V|%i%%" %(ups.get_voltage(),ups.get_capacity()))
