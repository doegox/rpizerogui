#!/usr/bin/env python

import sys
from PIL import Image
from PIL import ImageDraw

from ST7789 import ST7789

disp = ST7789()

image1 = Image.open(sys.argv[1])
draw = ImageDraw.Draw(image1)
disp.ShowImage(image1,0,0)
raw_input("Press key to quit")
