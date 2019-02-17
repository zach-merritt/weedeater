import numpy as np
import matplotlib.pyplot as plt
import time
import random
import cv2
import sys

cameras = [0,2]

#cameras[1] = cv2.VideoCapture(1)


#cameras[1].set(3,1920) #WIDTH
#cameras[1].set(4,1080) #HEIGHT

print ("Done getting cameras")


zoom_factor = 0.5
for index in range(50):   #How many pictures to take

    camera_index = -1
    for camera_number in cameras:
        print ("camera number %d" %( camera_number))
        camera_index = camera_index + 1


        time.sleep(random.uniform(0.4,0.6))
        camera = cv2.VideoCapture(camera_number)
        camera.set(3,1024) #WIDTH
        camera.set(4,768) #HEIGHT
        ret, frame = camera.read()


        camera.release()
        print(ret)
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
            cv2.imwrite(('image_%s_%04d_%1d_%02d.jpg' % (sys.argv[1], index, camera_index, loop) ), small)


#for camera in cameras:
#    camera.release()

#plt.imshow(small)
#plt.show()
