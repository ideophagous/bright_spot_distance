from Tkinter import Tk
from tkFileDialog import askopenfilename
import bright_spot_distance as bsd

#to avoid opening the main window -->
Tk().withdraw()
path = askopenfilename()

image = bsd.get_image(path)

bright_spot = bsd.get_bright_spot(bsd.get_neighborhood_list(bsd.get_bright_pixel_list(image)))


distance_to_center = bsd.get_distance_to_center(bsd.get_image_center(image), bsd.get_bright_spot_center(bright_spot))

if(distance_to_center!=None):
    print("The distance between the bright spot and the center of the image is: {0:.2f}".format(distance_to_center))
else:
    print("Invalid image or file!")
