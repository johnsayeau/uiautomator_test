from uiautomator import Device
from PIL import Image
import math, operator
import os.path
from time import sleep

#boundries of four tiles in input app
top_left_tile_bounds = (165, 60, 960, 510)
top_right_tile_bounds = (1020, 60, 1815, 510)
bottom_left_tile_bounds = (165, 570, 960, 1020)
bottom_right_tile_bounds = (1020, 570, 1815, 1020)

def screencap_tile(tile_bounds, bsq):
    #returns image object - not file
    #arg is the left, top, right and bottom of the area
    #whole_screen_img = Image.open(bsq.screenshot("reference_pics/video_input_tiles.png"))
    if os.path.exists("reference_pics/video_input_tiles.png"):
        whole_screen_img = Image.open("reference_pics/video_input_tiles.png")
    else:
        whole_screen_img = Image.open(bsq.screenshot("reference_pics/video_input_tiles.png"))
    return whole_screen_img.crop(tile_bounds)

def get_tile_reference_screenshots(bsq_device):
    #has to be run while in the video input app with 4 tiles showing.
    print "2"
    screencap_tile(top_right_tile_bounds, bsq_device).save("reference_pics/top_right_tile_ref.png")
    screencap_tile(top_left_tile_bounds, bsq_device).save("reference_pics/top_left_tile_ref.png")
    screencap_tile(bottom_left_tile_bounds, bsq_device).save("reference_pics/bottom_left_tile_ref.png")
    screencap_tile(bottom_right_tile_bounds, bsq_device).save("reference_pics/bottom_right_tile_ref.png")

def crop_out_center(img):
    #img = Image.open(img_to_crop)
    width, height = img.size
    new_width = width / 2
    new_height = height / 2
    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2
    return img.crop((left, top, right, bottom))

def images_equal(img_file1, img_file2):
    h1 = img_file1.histogram()
    h2 = img_file2.histogram()
    result = math.sqrt(reduce(operator.add,
    map(lambda a,b: (a-b)**2, h1, h2))/len(h1))
    #if result > 10.0:
     #   print("images did not match")
      #  #get an exception handling method here
       # raise Exception("no matchy matchy")
    #else:
     #   return True
    return result


def tiles_show_usb_connection(bsq_device):
    #setup - all tiles should have usb connected
    if len(bsq_device(text="Touch enabled")) == 4:
        return True
    else:
        return False

def tile_has_thumbnail(tile_bounds, ref_tile_img_file,bsq):
    if os.path.exists("temp_images/video_input_tiles.png"):
        whole_screen_img = Image.open("temp_images/video_input_tiles.png")
    else:
        whole_screen_img = Image.open(bsq.screenshot("temp_images/video_input_tiles.png"))
    thumbnail_image = whole_screen_img.crop(tile_bounds)
    thumbnail_image_cropped = crop_out_center(thumbnail_image)
    cropped_ref_img = crop_out_center(Image.open(ref_tile_img_file))
    return images_equal(thumbnail_image_cropped, cropped_ref_img)


def click_tile(bsq, video_input):
    # this must be run when the video input app is open and the 4 tiles are showing
    # possible video_input are hdmi1, hdmi2, display_port, vga
    hdmi1_tile = bsq(className="android.widget.ImageButton")[0]
    hdmi2_tile = bsq(className="android.widget.ImageButton")[2]
    display_port_tile = bsq(className="android.widget.ImageButton")[1]
    vga_tile = bsq

    if video_input == "hdmi1":
        hdmi1_tile.click()
    elif video_input == "hdmi2":
        hdmi2_tile.click()
    elif video_input == "display_port":
        display_port_tile.click()
    elif video_input == "vga":
        vga_tile.click()
    else:
        print "possible video inputs are hdmi1, hdmi2, display_port, vga"
        exit()

def get_reference_pics_for_desktops(bsq, video_input):
    # possible video_input are hdmi1, hdmi2, display_port, vga
    click_tile(bsq, video_input)




def setup_reference_pics(bsq_device):
    get_tile_reference_screenshots(bsq_device)

