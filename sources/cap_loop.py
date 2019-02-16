import numpy as np
import matplotlib.pyplot as plt
import time
import random
import cv2

cap = cv2.VideoCapture(0)
zoom_factor = 0.4
for index in range(10):
    time.sleep(0.5)
    ret, frame = cap.read()
    height, width, channels = frame.shape
    #print( height, width )
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
        trimmed = rotated[mid_height-min_dim:mid_height+min_dim,mid_width-min_dim:mid_width+min_dim]
        #print( trimmed.shape )
        small = cv2.resize(trimmed, (200,200))

        #And finally, a random flip side to side
        if random.randint(0,1):
            small = cv2.flip(small, 1)

        #And write it out
        cv2.imwrite(('image_%04d_%02d.jpg' % (index, loop) ), small)


#plt.imshow(small)
#plt.show()
