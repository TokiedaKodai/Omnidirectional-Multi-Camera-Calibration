import cv2
import numpy as np
import os
import sys
from cv2 import aruco

import charuco

ar = charuco.Arco()
img_board = ar.img_aruco()
cv2.imwrite('ARMarkerBoard.png', img_board)