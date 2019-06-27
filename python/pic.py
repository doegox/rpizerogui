#!/usr/bin/env python

import sys
from PIL import Image
from PIL import ImageDraw

try:
    from ST7789 import get_disp
except ImportError:
    from dummy import get_disp

disp = get_disp()

image1 = Image.open(sys.argv[1])
draw = ImageDraw.Draw(image1)
disp.ShowImage(image1,0,0)
