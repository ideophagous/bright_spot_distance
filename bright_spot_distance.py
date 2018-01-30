from PIL import Image
from math import sqrt

BRIGHT_SPOT_SIZE_THRESHOLD_PARAMETER  = 1/2500.0
NEIGHBORHOOD_PARAMETER = 5



def get_image(path):
    try:
        
        image = Image.open(path) #grayscale encoding
        if(image.mode!="I;16"):
            image = image.convert('L')
            #image = check_convert_int16(path,image)
            
        else:
            image = check_convert_int16(path).convert('L')
        return image
    except IOError:
        return None

def check_convert_int16(path):
    x = path.split('.')
    if(x[-1] in ['tif','tiff']):
        image = Image.open(path).convert("I;16")
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                image.putpixel((i,j),image.getpixel((i,j))//256)
                image.save(path+"-converted.tif")   
        return image
            

def get_brightness_threshold(image):
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
    #image1 = get_image("spot1.jpg")
    #print(check_int16("spot1.jpg",image1))
    image1 = get_image("spot1.tif")
    
    #print(check_int16("spot1.tif",image1))
    '''image2 = get_image("spot2.jpg")
    image3 = get_image("spot3.jpg")

    bright_spot1 = get_bright_spot(get_neighborhood_list(get_bright_pixel_list(image1)))
    bright_spot2 = get_bright_spot(get_neighborhood_list(get_bright_pixel_list(image2)))
    bright_spot3 = get_bright_spot(get_neighborhood_list(get_bright_pixel_list(image3)))

    distance_to_center1 = get_distance_to_center(get_image_center(image1), get_bright_spot_center(bright_spot1))
    distance_to_center2 = get_distance_to_center(get_image_center(image2), get_bright_spot_center(bright_spot2))
    distance_to_center3 = get_distance_to_center(get_image_center(image3), get_bright_spot_center(bright_spot3))

    print("The distance between the bright spot and the center of the image spot1.jpg is: {0:.2f}".format(distance_to_center1))
    print("The distance between the bright spot and the center of the image spot2.jpg is: {0:.2f}".format(distance_to_center2))
    print("The distance between the bright spot and the center of the image spot3.jpg is: {0:.2f}".format(distance_to_center3))'''
    
    
