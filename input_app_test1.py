from uiautomator import Device
import os
from time import sleep
from PIL import ImageChops
from PIL import Image
import math, operator


def start_input_app():
    # launch input app and go to the 4 tiles
    os.system('adb shell am startservice -n "com.smart.videoinput/com.smarttech.videoinput.StartOPSService"')
    sleep(5)
    os.system('adb shell am start -n "com.smart.videoinput/com.smarttech.videoinput.VideoSelectActivity"')

def crop_out_center(img_to_crop):
    img = Image.open(img_to_crop)
    width, height = img.size
    new_width = width / 2
    new_height = height / 2
    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2
    return img.crop((left, top, right, bottom))

def images_equal(img_file1, img_file2):
    h1 = Image.open(img_file1).histogram()
    h2 = Image.open(img_file2).histogram()
    return math.sqrt(reduce(operator.add,
    map(lambda a,b: (a-b)**2, h1, h2))/len(h1))




#start_input_app()
#sleep(4)
#bsq = Device()
#hdmi1_textView = bsq(text="HDMI 1")
#hdmi1_textView.click()
#sleep(9)
#bsq.screenshot("sheep2.png")



print images_equal("pic3.png", "pic4.png")
