import numpy as np
import matplotlib.pyplot as plt
import time
import random
import cv2

cap = [1,2,3,4]

for i in [0,2]:
    print ( i )
    cap[i] = cv2.VideoCapture(i)
    cap[i].set(3,3264) #WIDTH
    cap[i].set(4,2448) #HEIGHT


zoom_factor = 0.4
for index in range(10):

    for camera in [0,2]:
        time.sleep(random.uniform(0.25,0.75))
        ret, frame = cap[camera].read()
        height, width, channels = frame.shape
        print( index )
        mid_height = int(height/2)
        mid_width = int(width/2)
        prospective_min_dim = min(mid_height, mid_width)

        for loop in range(0,10):

            #random rotate
            M = cv2.getRotationMatrix2D((width/2,height/2),random.randint(-20,20),1)
            rotated = cv2.warpAffine(frame,M,(width,height))

            #no translation, just a trim (which effectively zooms)
            #random zoom
            min_dim = int(prospective_min_dim * zoom_factor * random.uniform(0.85,1.15))

            #random left/right shift
            #random up/down shift
            rleft = int(prospective_min_dim * zoom_factor * random.uniform(-0.25,0.25))
            rdown = int(prospective_min_dim * zoom_factor * random.uniform(-0.25,0.25))

            trimmed = rotated[mid_height-min_dim+rdown:mid_height+min_dim+rdown,mid_width-min_dim+rleft:mid_width+min_dim+rleft]

            small = cv2.resize(trimmed, (200,200))

            #And finally, a random flip side to side
            if random.randint(0,1):
                small = cv2.flip(small, 1)

            #And write it out
            cv2.imwrite(('image_%04d_%1d_%02d.jpg' % (index, camera, loop) ), small)


#plt.imshow(small)
#plt.show()
