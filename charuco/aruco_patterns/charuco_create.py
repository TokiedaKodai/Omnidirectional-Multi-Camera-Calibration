import cv2
import numpy as np
import os
import sys
from cv2 import aruco

pattern_w = 20
pattern_h = 14
image_w = pattern_w*100
image_h = pattern_h*100

aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
board = aruco.CharucoBoard_create(pattern_w,pattern_h, 1, .85, aruco_dict)
imboard = board.draw((image_w,image_h))
cv2.imwrite("chessboard_%d_%d_%d_%d.png"%(pattern_w,pattern_h,image_w,image_h), imboard)
