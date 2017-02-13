from uiautomator import Device
import os
from time import sleep
from PIL import ImageChops
from PIL import Image
import math, operator
from uiautomator_test import *
import pyaudio
import audioop

hdmi1_sound_level = range(10,30)
hdmi2_sound_level = range(180, 200)
display_port_level = range(750, 850)



tile_tuples = [(top_left_tile_bounds, "reference_pics/top_left_tile_ref.png", hdmi1_sound_level),
                       (top_right_tile_bounds, "reference_pics/top_right_tile_ref.png", display_port_level),
                       (bottom_left_tile_bounds, "reference_pics/bottom_left_tile_ref.png", hdmi2_sound_level)]


def start_input_app():
    # launch input app and go to the 4 tiles
    os.system('adb shell am startservice -n "com.smart.videoinput/com.smarttech.videoinput.StartOPSService"')
    sleep(5)
    os.system('adb shell am start -n "com.smart.videoinput/com.smarttech.videoinput.VideoSelectActivity"')

def check_sound(level_range):
    times_level_was_zero = 0
    times_level_in_range = 0
    for i in range(1,50):
        chunk = 1024
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        frames_per_buffer=chunk)
        data = stream.read(chunk)
        rms = audioop.rms(data, 2)
        if rms in level_range:
            times_level_in_range +=1
        if rms == 0:
            times_level_was_zero +=1
        sleep(0.01)
    if times_level_was_zero > 10:
        print "no audio detectd"
        exit()
    elif times_level_in_range > 5:
        return "audio in range detected"
    else:
        print "audio out of range"
        exit()



def test_all_tiles_4_thumbnails(bsq):
    start_input_app()
    sleep(30)
    bsq.screenshot("temp_images/video_input_tiles.png")
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
print "1"
setup_reference_pics(bsq)
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

