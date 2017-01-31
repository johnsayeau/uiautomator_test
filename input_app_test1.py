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

def test_all_tiles_4_thumbnails(bsq):
    start_input_app()
    sleep(30)
    tile_tuples = [(top_left_tile_bounds, "reference_pics/top_left_tile_ref.png"),
                       (top_right_tile_bounds, "reference_pics/top_right_tile_ref.png"),
                       (bottom_left_tile_bounds, "reference_pics/bottom_left_tile_ref.png")]
    for tile in tile_tuples:
        sleep(5)
        match = tile_has_thumbnail(tile[0], tile[1], bsq)
        if  match < 100:
            print "thumbnail loaded " + str(match)
        else:
            print "fail"
            print match
            bsq.screenshot("fail_pics/fail.png")
            exit()

bsq=Device()
bsq.screenshot("temp_images/video_input_tiles.png")
#setup_reference_pics(bsq)
for i in range(1,100):
    print "start of iteration " + str(i)
    test_all_tiles_4_thumbnails(bsq)
    os.system("adb shell am broadcast -a com.android.systemui.channels.RUN_CHANNEL --es package_name com.android.settings")
    sleep(5)





#start_input_app()
#sleep(4)
#bsq = Device()
#hdmi1_textView = bsq(text="HDMI 1")
#hdmi1_textView.click()
#sleep(9)
#bsq.screenshot("sheep2.png")

#start_input_app()
#sleep(30)
#bsq = Device()
#setup_reference_pics(bsq)
#tile_has_thumbnail(top_left_tile_bounds,"reference_pics/top_left_tile_ref.png", bsq)

