import numpy as np
import matplotlib.pyplot as plt
import time
import cv2
import sys

# Sample program to crop rectangular image (given as first artument) into square images
# 200 by 200 pixels

# Read the specified image
frame = cv2.imread(sys.argv[1])
height, width, channels = frame.shape
#print( height, width )

# Compute center point and length of shortest dimension
mid_height = int(height/2)
mid_width = int(width/2)
min_dim = min(mid_height, mid_width)
#print ( mid_height, mid_width, min_dim)

# Crop and scale to 200 by 200
trimmed = frame[mid_height-min_dim:mid_height+min_dim,mid_width-min_dim:mid_width+min_dim]
#print( trimmed.shape )
small = cv2.resize(trimmed, (200,200))

# Output the file, with SQ_  (for "Square") prepended to the original file name.
cv2.imwrite("SQ_" + sys.argv[1], small)
