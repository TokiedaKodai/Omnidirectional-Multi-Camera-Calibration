import cv2
from cv2 import aruco
import numpy as np

class Arco:
    def __init__(self):
        self.num_marker_x = 9
        self.num_marker_y = 7
        self.res_board_x = 1024
        self.res_board_y = 768

    def aruco_dict(self):
        return aruco.getPredefinedDictionary(aruco.DICT_4X4_100)

    def aruco_board(self):
        dictionary = self.aruco_dict()
        grid_board = aruco.GridBoard_create(
            self.num_marker_x, self.num_marker_y, 0.05, 0.01, dictionary)
        return grid_board

    def img_aruco(self):
        grid_board = self.aruco_board()
        img_board = grid_board.draw((self.res_board_x, self.res_board_y))
        return img_board

if __name__ == '__main__':
    ar = Arco()
    img_board = ar.img_aruco()
    cv2.imwrite('ARMarkerBoard_test.png', img_board)