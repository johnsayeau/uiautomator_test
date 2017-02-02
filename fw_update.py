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
        return Device()
    else:
        raise Exception("oops no device")



def connect_usb_stick():
    usb = UsbConnection()
    usb.connect_usb("usb5")

def disconnect_usb_stick():
    usb = UsbConnection()
    usb.disconnect_usb("usb5")

bsq = connect_device("10.1.108.81")


run = 1

while True:
    connect_usb_stick()
    for i in range(1,10):
        if bsq(text="Cancel").exists:
            bsq(text="Cancel").click()
            break
        sleep(1)
    if not bsq(text="Cancel").exists:
        bsq.screenshot("Fail.png")
    disconnect_usb_stick()
    print "run " + str(run)
    run = run + 1
    sleep(3)