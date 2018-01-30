from PIL import Image
from math import sqrt
import cv2
import numpy as np
import os

BRIGHT_SPOT_SIZE_THRESHOLD_PARAMETER  = 1/2500.0
NEIGHBORHOOD_PARAMETER = 5


# === Getting the image from path ===
def get_image(path):

    """
    Gets the image from path and returns it in
    grayscale mode.
    If the pixel colors are encoded on 16 bits
    (values from 0 to 65535), it converts the
    image to 8-bit encoded pixels.
    If there's an input error, the function
    returns None.

    Input:
    - path: relative or absolute path at which
    the image is located.

    Output:
    - image: 8-bit encoded image in grayscale
    mode.
    Or None, if there's an IOError.
    """
    try:
        
        image = Image.open(path) #grayscale encoding
        if(image.mode!="I;16"):
            image = image.convert('L')
            
        else:
            image = cv2.imread(path).astype(np.uint8)
            cv2.imwrite('temp.jpg', image) #save as a temporary file
            image = Image.open('temp.jpg').convert('L') #load temporary file and convert to grayscale mode
            os.remove('temp.jpg') #remove temporary file
        return image
    except IOError:
        return None
            
# === Getting the brightness threshold ===
def get_brightness_threshold(image):
    """
    Getting the brightness threshold, defined as
    the smallest color code such that the number
    of pixels that have that color or a brighter
    one (i.e. larger color code), does not exceed
    the proportion of pixels in the image defined
    by the constant BRIGHT_SPOT_SIZE_THRESHOLD_PARAMETER
    which was fixed at 1/2500 of the image. The
    value of the parameter was chosen to fit with
    the provided examples, where the number of pixels
    representing the bright spot was observed to be
    lower than the total number of pixels in the
    image divided by 2500, mostly by a significant
    degree.

    Input:
    - image: the image in grayscale.

    Intermediary Variables:
    - bright_portion: maximum number of pixels
    that should be part of the bright spot.
    - color_proportions: a list of tuples each
    containing the color code and the number
    of pixels that have that color code.
    - pixel_total: a counter for the number of
    pixels starting from the last value in
    color_proportions, and going downwards until
    bright_portion is exceeded.
    

    Output:
    - brightness_threshold: an integer representing
    the brightness threshold, as defined above.
    """
    if(not image == None):
        bright_portion = (BRIGHT_SPOT_SIZE_THRESHOLD_PARAMETER *
                          image.size[0] * image.size[1])
        color_proportions = image.getcolors()
        if(len(color_proportions)>1): #image should not be monochrome or without color
            pixel_total = color_proportions[-1][0]
            brightness_threshold = color_proportions[-1][1]
            for i in range(1,len(color_proportions)):
                pixel_total+=color_proportions[-1-i][0]
                if(pixel_total<bright_portion):
                    brightness_threshold = color_proportions[-1-i][1]
                else:
                    break
            return brightness_threshold
    

def get_bright_pixel_list(image):
    if(image!=None):
        brightness_threshold = get_brightness_threshold(image)
        if(brightness_threshold!=None):
            bright_pixel_list = []
            for i in range(image.size[0]):
                for j in range(image.size[1]):
                    if(image.getpixel((i,j))>=brightness_threshold):
                        bright_pixel_list.append((i,j))
            return bright_pixel_list

def check_neighboring_pixel(pixel_list,pixel):
    for pixel_point in pixel_list:
        if (abs(pixel_point[0]-pixel[0])<NEIGHBORHOOD_PARAMETER
            and abs(pixel_point[1]-pixel[1])<NEIGHBORHOOD_PARAMETER):
                return True
    return False

def get_neighborhood_list(bright_pixel_list):
    if(bright_pixel_list!=None and len(bright_pixel_list)>0):
        neighborhood_list = [[bright_pixel_list[0]]]
        for i in range(1,len(bright_pixel_list)):
            added = False
            index = -1
            j = 0
            while(j<len(neighborhood_list)):
                if(check_neighboring_pixel(neighborhood_list[j],bright_pixel_list[i])):
                    if(added):
                        neighborhood_list[index]+=neighborhood_list[j]
                        del neighborhood_list[j]
                        j-=1
                    else:
                        neighborhood_list[j].append(bright_pixel_list[i])
                        added = True
                        index = j
                j+=1
            if(not added):
                neighborhood_list.append([bright_pixel_list[i]])
        return neighborhood_list
    return []

def get_bright_spot(neighborhood_list):
    try:
        max = len(neighborhood_list[0])
        index_max = 0
        for i in range(1,len(neighborhood_list)):
            if(len(neighborhood_list[i])>max):
                max = len(neighborhood_list[i])
                index_max = i
        return neighborhood_list[index_max]
    except:
        return []
        
def get_bright_spot_center(bright_spot):
    if(len(bright_spot)>0):
        x_center = 0
        y_center = 0
        for i in range(len(bright_spot)):
            x_center += bright_spot[i][0]
            y_center += bright_spot[i][1]

        return x_center/float(len(bright_spot)),y_center/float(len(bright_spot))
    

def get_image_center(image):
    if(image!=None):
        return (image.size[0]-1)/2.0,(image.size[1]-1)/2.0

def get_distance_to_center(image_center, spot_center):
    if(image_center!=None and spot_center!=None):
        return sqrt((image_center[0]-spot_center[0])**2+(image_center[1]-spot_center[1])**2)

if __name__=='__main__':

    files = ["spot1.tif","spot2.tif","spot3.tif","spot5.tif","black.tif","white.tif","test1.tif","test2.png","spot3 - Copy.jpg"]
    
    for i in range(len(files)):
        image = get_image("images/"+files[i])
        bright_spot = get_bright_spot(get_neighborhood_list(get_bright_pixel_list(image)))
        distance_to_center = get_distance_to_center(get_image_center(image), get_bright_spot_center(bright_spot))
        if(distance_to_center!=None):
            print("The distance between the bright spot and the center of the image "+files[i]+" is: {0:.2f}".format(distance_to_center))
        else:
            print(files[i]+": Invalid image or file!")
    
