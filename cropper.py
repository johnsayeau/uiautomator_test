from PIL import Image

img = Image.open("sheep2.png")
width, height = img.size
new_width = width/2
new_height = height/2

left = (width - new_width)/2
top = (height - new_height)/2
right = (width + new_width)/2
bottom = (height + new_height)/2

img.crop((left,top,right,bottom)).save("pic4.png")



#img.save("pic1.png")