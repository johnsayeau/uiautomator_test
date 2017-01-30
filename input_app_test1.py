from uiautomator import Device
import os
from time import sleep
from PIL import ImageChops
from PIL import Image
import math, operator
from uiautomator_test import *

def start_input_app():
    # launch input app and go to the 4 tiles
    os.system('adb shell am startservice -n "com.smart.videoinput/com.smarttech.videoinput.StartOPSService"')
    sleep(5)
    os.system('adb shell am start -n "com.smart.videoinput/com.smarttech.videoinput.VideoSelectActivity"')









#start_input_app()
#sleep(4)
#bsq = Device()
#hdmi1_textView = bsq(text="HDMI 1")
#hdmi1_textView.click()
#sleep(9)
#bsq.screenshot("sheep2.png")


bsq = Device()
setup_reference_pics()
print tile_has_thumbnail(top_left_tile_bounds, bsq)
