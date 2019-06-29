#!/usr/bin/env python

import os
import sys
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

from ST7789 import ST7789

scriptpath = os.path.dirname(os.path.realpath(__file__))
disp = ST7789()

image1 = Image.open(os.path.join(scriptpath, 'pic.jpg'))
draw = ImageDraw.Draw(image1)

font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 32)
draw.rectangle([(15,70),(195,100)],fill = "BLACK")
draw.text((20, 70), 'Proxmark3', fill = "LIGHTBLUE", font=font)
draw.text((19, 139), 'Wardriving', fill = "WHITE", font=font)
draw.text((19, 142), 'Wardriving', fill = "WHITE", font=font)
draw.text((22, 139), 'Wardriving', fill = "WHITE", font=font)
draw.text((22, 142), 'Wardriving', fill = "WHITE", font=font)
draw.text((20, 140), 'Wardriving', fill = "BLACK", font=font)

disp.ShowImage(image1,0,0)
