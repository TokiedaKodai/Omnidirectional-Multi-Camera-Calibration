import cv2
import numpy as np
import os
import sys
from cv2 import aruco

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_100)
grid_board = aruco.GridBoard_create(9, 7, 0.05, 0.01, aruco_dict)
img_board = grid_board.draw((1024, 768))
cv2.imwrite('ARMarkerBoard.png', img_board)