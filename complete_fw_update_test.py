from uiautomator import Device
from subprocess import Popen
import commands
import os
from new_connect_usb import UsbConnection
from time import sleep

def connect_device(ip_address):
    os.system("adb kill-server")
    os.system("adb start-server")
    os.system("adb root")
    os.system("adb connect 10.1.108.81")
    sleep(5)
    cmd_output = commands.getoutput("adb devices")
    print cmd_output
    if "10.1.108.81" in commands.getoutput("adb devices"):
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
    cmd = 'adb logcat >> ' + file_name
    p = Popen(['adb logcat >> '])
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
    for i in range (1,11):
        if bsq(className="android.WidgetProgressBar").exists:
            print "spinner present"
            sleep(1)
    if not bsq(className="android.WidgetProgressBar").exists:
        print "aaaaw krrrap I canna find no spinner"


def update_fw(usb_stick_connection):
    connect_usb_stick(usb_stick_connection)
    bsq = connect_device("10.1.108.81")
    wait_for_button_and_click(bsq, "Restart")
    check_for_spinner(bsq)
    sleep(600)  # wait for 600 seconds for fw update to complete
    disconnect_usb_stick(usb_stick_connection)
    sleep(3)



run = 1

while True:
    update_fw("usb5")
    update_fw("usb6")
    print "run # " + str(1)
    run +=1





