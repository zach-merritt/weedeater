import numpy as np
import matplotlib.pyplot as plt
import time
import cv2
import sys


frame = cv2.imread(sys.argv[1])
height, width, channels = frame.shape
#print( height, width )
mid_height = int(height/2)
mid_width = int(width/2)
min_dim = min(mid_height, mid_width)
#print ( mid_height, mid_width, min_dim)
trimmed = frame[mid_height-min_dim:mid_height+min_dim,mid_width-min_dim:mid_width+min_dim]
#print( trimmed.shape )
small = cv2.resize(trimmed, (200,200))
cv2.imwrite("SQ_" + sys.argv[1], small)
