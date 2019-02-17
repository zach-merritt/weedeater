import numpy as np
import matplotlib.pyplot as plt
import time
import random
import cv2
import sys
import glob
import os





zoom_factor = 0.80

for file_name in glob.glob("DSC*.JPG"):

    frame = cv2.imread(file_name)

    height, width, channels = frame.shape
    print( frame.shape )
    mid_height = int(height/2)
    mid_width = int(width/2)
    prospective_min_dim = min(mid_height, mid_width)

    for loop in range(0,10):   #how much to augment

        small = None

        if loop != 0:  #We want the first one undistorted
            #random rotate
            M = cv2.getRotationMatrix2D((width/2,height/2),random.randint(-20,20),1)
            rotated = cv2.warpAffine(frame,M,(width,height))

            #no translation, just a trim (which effectively zooms)
            #random zoom
            min_dim = int(prospective_min_dim * zoom_factor * random.uniform(0.85,1.15))

            #random left/right shift
            #random up/down shift
            rleft = int(prospective_min_dim * zoom_factor * random.uniform(-0.1,0.1))
            rdown = int(prospective_min_dim * zoom_factor * random.uniform(-0.1,0.1))

            trimmed = rotated[mid_height-min_dim+rdown:mid_height+min_dim+rdown,mid_width-min_dim+rleft:mid_width+min_dim+rleft]

            small = cv2.resize(trimmed, (200,200))

            #And finally, a random flip side to side
            if random.randint(0,1):
                small = cv2.flip(small, 1)
        else:
            min_dim = int(prospective_min_dim * zoom_factor)
            trimmed = frame[mid_height-min_dim:mid_height+min_dim,mid_width-min_dim:mid_width+min_dim]
            small = cv2.resize(trimmed, (200,200))

        #And write it out
        cv2.imwrite(('image_%s_%02d_%s' % (sys.argv[1], loop, file_name) ), small)


#for camera in cameras:
#    camera.release()

#plt.imshow(small)
#plt.show()
