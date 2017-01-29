import uiautomator

tablet = uiautomator.Device()
tablet_info_dict = tablet.info
for k,v in tablet_info_dict.iteritems():
    print(str(k) + " : " + str(v))

tablet.screen.on()
tablet.press.home()
#apps_button = tablet(description="Apps")
#apps_button.click()
tablet.dump()

