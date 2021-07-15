import cv2
import numpy as np
import os
import sys
from cv2 import aruco

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
board = aruco.CharucoBoard_create(10, 8, 1, .8, aruco_dict)
imboard = board.draw((1000, 800))
cv2.imwrite("chessboard.png", imboard)
