from uiautomator import Device
from PIL import Image

bsq = Device()
hdmi1_textView = bsq(text="HDMI 1")
print hdmi1_textView.info['bounds']

#boundries of four tiles in input app
top_left_tile_bounds = (165, 60, 960, 510)
top_right_tile_bounds = (1020, 60, 1815, 510)
bottom_left_tile_bounds = (165, 570, 960, 1020)
bottom_right_tile_bounds = (1020, 570, 1815, 1020)

def screencap_tile(bounds):
    #returns image object - not file
    #arg is the left, top, right and bottom of the area
    whole_screen_img = Image.open(bsq.screenshot("bsq.png"))
    return whole_screen_img.crop(bounds)

def get_tile_reference_screenshots():
    screencap_tile(top_right_tile_bounds).save("top_right_tile_ref.png")
    screencap_tile(top_left_tile_bounds).save("top_left_tile_ref.png")
    screencap_tile(bottom_left_tile_bounds).save("bottom_left_tile_ref.png")
    screencap_tile(bottom_right_tile_bounds).save("bottom_right_tile_ref.png")

get_tile_reference_screenshots()