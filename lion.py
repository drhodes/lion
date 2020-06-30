# https://creativecommons.org/publicdomain/zero/1.0/
# CC0 1.0 Universal (CC0 1.0)
# Public Domain Dedication

from PIL import Image
import math

# make sure Python Imaging Library is installed
# to run:
#
# $ python lion.py
#
# note: the transform and image filename/location are hard coded, so
# the lion image has to be in the same directory where the script is

def from_screen_to_cage(p):
    # from screen space to the unit cage.    
    x = (p[0]-500) / 250.0
    y = (p[1]-500) / 250.0
    return (x, y)

def from_cage_to_screen(p):
    # from cage to screen space.
    x = int((p[0] * 250) + 500)
    y = int((p[1] * 250) + 500)
    return (x, y)

def find_z(p):
    # take a cage point and return r * exp(i*theta)
    a, b = p
    r = math.sqrt(a**2 + b**2)
    theta = 0
    if a > 0: theta = math.atan(b/a)
    elif a<0 and b>=0: theta = math.atan(b/a) + math.pi
    elif a<0 and b<0: theta = math.atan(b/a) - math.pi
    else : theta = math.atan(b)
    
    z = complex(r*math.cos(theta), r*math.sin(theta))

    if z == 0:
        return complex(1, 1)
    else:        
        return 1 / z

def transform_pixel(pixels, p): 
    # convert screen coordinates to cage coordinates
    x0, y0 = from_screen_to_cage(p)
    # get the pixel color
    color = pixels[p[0], p[1]]
    # apply the transform
    z = find_z((x0, y0))
    # convert new cage coordinate to screen coordinate
    point = from_cage_to_screen((z.real, z.imag))
    # add pixel at new location to dictionary (coord -> color)
    return (point, color)

def process_image(img):
    width, height = img.size
    pixels = img.load() # speed things up.
    
    output_pixels = {}    
    # for each pixel in the image
    for x in range(0, width):
        for y in range(0, height):
            # transform pixel
            point, color = transform_pixel(pixels, (x, y))
            # build dictionary with (coord -> color)
            output_pixels[point] = color

    # create new image
    output_image = Image.new(mode="RGBA",
                             size=img.size,
                             color=(255,255,255,255))
    # draw the dictionary
    for point in output_pixels:
        x, y = point
        if 0 < x < width and 0 < y < height:
            color = output_pixels[point]        
            output_image.putpixel(point, color)
        
    # save the file
    output_image.save("lion-caught.png")
    print("lion-caught.png has been written")
    
def main():
    lion_img = Image.open("lion.png")
    process_image(lion_img)

if __name__ == "__main__":
    main()    
