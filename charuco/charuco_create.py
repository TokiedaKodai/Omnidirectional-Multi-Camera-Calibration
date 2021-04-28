import cv2
import numpy as np
import os
import sys
from cv2 import aruco

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
board = aruco.CharucoBoard_create(20, 14, 1, .8, aruco_dict)
imboard = board.draw((2000, 1400))
cv2.imwrite("chessboard.png", imboard)
