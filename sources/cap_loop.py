import numpy as np
import matplotlib.pyplot as plt
import time
import cv2

#
# Set up video capture device, with default settings
#

cap = cv2.VideoCapture(0)

#
# This just takes 10 pictures, three seconds apart.  Assumption is that the object
# is slowly moving (in our case, rotating on a slow turntable) so that a 3 second
# interval will give a different view, but motion is not fast enough to blur the image
#
for index in range(10):
    time.sleep(3.0)
    
    # Capture an image
    ret, frame = cap.read()
    height, width, channels = frame.shape
    #print( height, width )
    
    #
    #   Here is where we could flip or rotate or futher zoom/scale the image.
    #  Could loop on applying different combinations of transforms
    #
    
    # Find the middle of the frame
    mid_height = int(height/2)
    mid_width = int(width/2)
    
    # Find the "half length" of the shortest dimension (or just put in a fixed value, or parameter
    min_dim = 100 #min(mid_height, mid_width)
    #print ( mid_height, mid_width, min_dim)
    
    # Crop the image by just using python slices.  Image is now square
    trimmed = frame[mid_height-min_dim:mid_height+min_dim,mid_width-min_dim:mid_width+min_dim]
    #print( trimmed.shape )
    
    #
    # Scale the square to our desired final output size and write it
    #
    small = cv2.resize(trimmed, (200,200))
    cv2.imwrite(('the%04d.png' % index), small)

#plt.imshow(small)   #Could put these statements inside loop to view progress, 
#plt.show()
