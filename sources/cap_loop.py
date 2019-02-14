import numpy as np
import matplotlib.pyplot as plt
import time
import cv2

cap = cv2.VideoCapture(0)

for index in range(10):
    time.sleep(3.0)
    ret, frame = cap.read()
    height, width, channels = frame.shape
    print( height, width )
    mid_height = int(height/2)
    mid_width = int(width/2)
    min_dim = 100 #min(mid_height, mid_width)
    print ( mid_height, mid_width, min_dim)
    trimmed = frame[mid_height-min_dim:mid_height+min_dim,mid_width-min_dim:mid_width+min_dim]
    print( trimmed.shape )
    small = cv2.resize(trimmed, (200,200))
    cv2.imwrite(('the%04d.png' % index), small)

#plt.imshow(small)
#plt.show()
