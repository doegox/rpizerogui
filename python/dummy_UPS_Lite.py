#!/usr/bin/env python

class UPS(object):
    def __init__(self):
        pass

    def get_voltage(self):
        "returns as float the voltage from the Raspi UPS Hat"
        return 3.1416

    def get_capacity(self):
        return 20

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
