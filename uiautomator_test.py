from uiautomator import Device
from PIL import Image


#boundries of four tiles in input app
top_left_tile_bounds = (165, 60, 960, 510)
top_right_tile_bounds = (1020, 60, 1815, 510)
bottom_left_tile_bounds = (165, 570, 960, 1020)
bottom_right_tile_bounds = (1020, 570, 1815, 1020)

def screencap_tile(tile_bounds, bsq):
    #returns image object - not file
    #arg is the left, top, right and bottom of the area
    whole_screen_img = Image.open(bsq.screenshot("reference_pics/video_input_tiles.png"))
    return whole_screen_img.crop(tile_bounds)

def get_tile_reference_screenshots():
    #has to be run while in the video input app with 4 tiles showing.
    screencap_tile(top_right_tile_bounds).save("reference_pics/top_right_tile_ref.png")
    screencap_tile(top_left_tile_bounds).save("reference_pics/top_left_tile_ref.png")
    screencap_tile(bottom_left_tile_bounds).save("reference_pics/bottom_left_tile_ref.png")
    screencap_tile(bottom_right_tile_bounds).save("reference_pics/bottom_right_tile_ref.png")

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
    result = math.sqrt(reduce(operator.add,
    map(lambda a,b: (a-b)**2, h1, h2))/len(h1))
    if result is None:
        return 0
    else:
        return result

def tiles_show_usb_connection(bsq_device):
    #setup - all tiles should have usb connected
    if len(bsq_device(text="Touch enabled")) == 4:
        return True
    else:
        return False

def tile_has_thumbnail(tile_bounds, ref_tile_img_file,bsq):
    whole_screen_img = Image.open(bsq.screenshot("temp_images/video_input_tiles.png"))
    thumbnail_image = whole_screen_img.crop(tile_bounds)
    thumbnail_image_cropped = crop_out_center(thumbnail_image)
    cropped_ref_img = crop_out_center(ref_tile_img_file)
    return images_equal(thumbnail_image_cropped, cropped_ref_img)




def setup_reference_pics():
    get_tile_reference_screenshots()

