Code developed by Mounir AFIFI in Python 2.7 for a job interview

Intent: Given a grayscale image with a small bright spot in a darker background, 
the program has to find the distance of the bright spot to the center of the
image.

Content:

--- bright_spot_distance.py: main module, contains all the functions for image
treatment and for calculating the distance of the bright spot to the center.
Has a main section with some tests. The image files can be found here:
https://www.dropbox.com/s/9xx1bx79cifze4q/images.rar?dl=0
The images must be in a folder titled images located at the same folder as
bright_spot_distance.py
Requirements: PIL (pillow), cv2 (OpenCV), numpy, os, math

--- bright_spot_distance_test.py: contains unit testing functions for each functions
in bright_spot_distance.py. Uses the image files mentioned earlier.
Requirements: bright_spot_distance, unittest, math

--- execute.py: a small script for running bright_spot_distance.py with the option
of selecting any image file from your file system.
Requirements: bright_spot_distance, Tkinter, tkFileDialog