import numpy as np
import matplotlib.pyplot as plt
import time
import random
import cv2
import sys

cap = cv2.VideoCapture(int(sys.argv[1]))
w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

#print(w)
#print(h)


cap.set(3,3264) #WIDTH
cap.set(4,2448) #HEIGHT

w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(w)
print(h)

zoom_factor = 0.4
if 1:
    #time.sleep(0.5)
    ret, frame = cap.read()
    height, width, channels = frame.shape
    #print( height, width )
    mid_height = int(height/2)
    mid_width = int(width/2)
    prospective_min_dim = min(mid_height, mid_width)

    if 1:



        #no translation, just a trim (which effectively zooms)
        #random zoom
        min_dim = int(prospective_min_dim * zoom_factor)
        trimmed = frame[mid_height-min_dim:mid_height+min_dim,mid_width-min_dim:mid_width+min_dim]

        small = cv2.resize(trimmed, (200,200))





plt.imshow(small)
plt.show()
