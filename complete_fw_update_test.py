from uiautomator import Device
from subprocess import Popen
import subprocess
import commands
import os
from new_connect_usb import UsbConnection
from time import sleep

def connect_device():
    os.system("adb kill-server > /dev/null 2>&1")
    os.system("adb start-server > /dev/null 2>&1")
    os.system("adb root > /dev/null 2>&1")
    os.system("adb connect 10.1.108.81 > /dev/null 2>&1")
    sleep(5)
    cmd_output = commands.getoutput("adb devices")
    if "10.1.108.81" in commands.getoutput(cmd):
        os.system("adb logcat -c")
        return Device()
    else:
        raise Exception("oops no device")


def connect_usb_stick(usb_con):
    usb = UsbConnection()
    usb.connect_usb(usb_con)

def disconnect_usb_stick(usb_con):
    usb = UsbConnection()
    usb.disconnect_usb(usb_con)

def save_logcat_to_file(file_name):
    p = Popen('adb logcat >> fail_file.txt', stdout=subprocess.PIPE, shell=True)
    sleep(8)
    p.kill()

def wait_for_button_and_click(bsq, button_text):
    for i in range(1,11):
        if bsq(text=button_text).exists:
            bsq(text=button_text).click()
            return
        sleep(1)
    if not bsq(text=button_text).exists:
        bsq.screenshot("ooops_no_dialog.png")
        save_logcat_to_file("logcat.txt")
        raise Exception("canna find the button")

def check_for_spinner(bsq):
    ## fix this
    for i in range (1,11):
        if bsq(className="android.WidgetProgressBar").exists:
            print "spinner present"
            return
        sleep(5)
    if not bsq(className="android.WidgetProgressBar").exists:
        print "aaaaw krrrap I canna find no spinner"

def get_MCU_version():
    #launch scaler settings
    os.system("adb shell am broadcast -a com.android.systemui.channels.RUN_CHANNEL --es package_name 'com.android.settings' > /dev/null 2>&1")
    bsq = connect_device()
    bsq(scrollable=True).scroll.to(text="About board")
    bsq(text="About board").click()
    list_view = bsq(className="android.widget.ListView")
    return list_view.child(className="android.widget.LinearLayout",instance=5).child(resourceId="android:id/summary").info['text']

def get_scaler_build_number():
    # launch scaler settings
    os.system("adb shell am broadcast -a com.android.systemui.channels.RUN_CHANNEL --es package_name 'com.android.settings' > /dev/null 2>&1")
    bsq = connect_device()
    bsq(scrollable=True).scroll.to(text="About board")
    bsq(text='About board').click()
    bsq(scrollable=True).scroll.to(text="Build number")
    return bsq(text="Build number").sibling(resourceId="android:id/summary").info['text']
    return bsq(className="android.widget.RelativeLayout",instance=9).child(resourceId="android:id/summary").info['text']

def update_fw(usb_stick_connection):
    connect_usb_stick(usb_stick_connection)
    bsq = connect_device()
    wait_for_button_and_click(bsq, "Restart")
    #check_for_spinner(bsq)
    sleep(600)  # wait for 600 seconds for fw update to complete
    disconnect_usb_stick(usb_stick_connection)
    sleep(3)

def check_fw_installed(target_scaler_version, target_mcu_version):
    result_str= ""
    installed_scaler_version = get_scaler_build_number()
    if target_scaler_version == installed_scaler_version:
        result_str = "scaler update successful"
    else:
        result_str = "scaler not changed"
    actual_mcu_version = get_MCU_version()
    if target_mcu_version == actual_mcu_version:
        result_str = result_str + " and mcu update successful"
    else:
        result_str = result_str + " and mcu update unsuccessful"
    return result_str


run = 1

while True:
    print get_MCU_version()
    print get_scaler_build_number()
    update_fw("usb4")
    print check_fw_installed("1.1.23(DEBUG)", "1.1.16.0")
    update_fw("usb3")
    print check_fw_installed("1.1.19(DEBUG)", "1.1.14.0")
    print "run # " + str(run)
    run +=1





