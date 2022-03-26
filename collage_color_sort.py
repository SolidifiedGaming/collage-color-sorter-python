import sys, os
import math
import colorsys
import numpy as np
from PIL import Image

def _get_image_count(path, fileTypes):
    return sum(filename.endswith(fileTypes) for filename in os.listdir(path))

def _get_image_size(path, fileTypes):
    size = [math.inf,math.inf] if len(os.listdir(path)) > 0 else [100, 100]
    for filename in os.listdir(path):
        if filename.endswith((".png", ".jpg")):
            s = Image.open(path + "/" + filename).size
            size = np.minimum(size, s)
    return tuple(size.astype(int))

def _get_rgb_average(rgb_list):
    # Calculate the sum of all squared rgb tuples
    rgb_squared_sum = np.sum([tuple(map(lambda x: x**2, rgb)) for rgb in rgb_list], axis=0)
    # Calculate the average tuple of rgb values
    rgb_avg = [math.sqrt(rgb / len(rgb_squared_sum)) for rgb in rgb_squared_sum.tolist()]
    return tuple(rgb_avg)

def _get_color_data(path, image_size, fileTypes):
    list = []
    for filename in os.listdir(path):
        if filename.endswith(fileTypes):
            image = Image.open(path + "/" + filename)
            if image.size != image_size:
                image.resize(image_size)
                
            # Currently gets an average pixel color from the image borders - subject to change
            pixel_values = []
            for i in range(image_size[0]):
                pixel_values.append(image.getpixel((i,0)))
                pixel_values.append(image.getpixel((i,image_size[1]-1)))
            for i in range(1, image_size[1]-1):
                pixel_values.append(image.getpixel((0,i)))
                pixel_values.append(image.getpixel((image_size[0]-1,i)))
            rgb_avg = _get_rgb_average(pixel_values)
            hsv = colorsys.rgb_to_hsv(rgb_avg[0], rgb_avg[1], rgb_avg[2])
            list.append((filename,) + hsv)
            
    list = sorted(list, key=lambda tup:(-tup[1]))
    return list

def generate_collage(col_amt, border_width, transparent, path):
    if os.path.exists(path + "\collage.png"):
      os.remove(path + "\collage.png")
    
    fileTypes = ("png", "jpg")
    image_count = _get_image_count(path, fileTypes)
    row_amt = math.ceil(image_count / col_amt)
    image_size = _get_image_size(path, fileTypes)
    color_data = _get_color_data(path, image_size, fileTypes)
    output_alpha = 255 * int(transparent == "n")

    full_image_size = (col_amt * image_size[0] + border_width * (col_amt + 1), \
        row_amt * image_size[1] + border_width * (row_amt + 1))
    collage = Image.new("RGBA",full_image_size, (0, 0, 0, output_alpha))

    col_num, row_num = 0, 0
    for tuple in color_data:
        image = Image.open(path + "/" + tuple[0])
        if image.size != image_size:
            image = image.resize(image_size)
        collage.paste(image, \
            (border_width * (col_num + 1) + image_size[0] * col_num, \
            border_width * (row_num + 1) + image_size[1] * row_num))

        col_num = (col_num + 1) % col_amt
        if col_num == 0:
            row_num += 1
            
    collage.save(path + "\collage.png")
    collage.show()
