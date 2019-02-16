import numpy as np
import matplotlib.pyplot as plt
import time
import random
import cv2

#
# Set up video capture device, with default settings
#

cap = cv2.VideoCapture(0)
<<<<<<< HEAD
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

=======

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
>>>>>>> f62f7b322628b36017c25ae12ab8158ce3f06a56

#plt.imshow(small)   #Could put these statements inside loop to view progress, 
#plt.show()
