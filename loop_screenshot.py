from uiautomator import Device
import os
from time import sleep


bsq = Device()
#bsq.screenshot("g.png")
sleep(5)
for i in range(1,100):
    os.system("adb logcat -c")
    #bsq.screenshot("temp_images/bsq_" + str(i))
    #cmd = "adb shell screencap -p | perl -pe 's/\x0D\x0A/\/g' > \\temp_images\\bsq_"
    os.system("adb shell screencap -p | perl -pe 's/\\x0D\\x0A/\\x0A/g' > temp_images/screen_" + str(i) + ".png")
    print "run# " + str(i)
    if bsq(resourceId="android:id/button1").exists:
        print "crash"
        exit()
    sleep(5)
