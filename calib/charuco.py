import cv2
from cv2 import aruco
import numpy as np

import config as cf

class Aruco:
    def __init__(self):
        self.num_marker_x = cf.num_marker_x
        self.num_marker_y = cf.num_marker_y
        self.num_corners = (cf.num_marker_x - 1) * (cf.num_marker_y -1)
        self.res_board_x = cf.res_board_x
        self.res_board_y = cf.res_board_y
        self.marker_real_size = cf.marker_real_size

    def aruco_dict(self):
        # return aruco.getPredefinedDictionary(aruco.DICT_6X6_100)
        return aruco.Dictionary_get(aruco.DICT_6X6_250)

    def aruco_board(self):
        dictionary = self.aruco_dict()
        # grid_board = aruco.GridBoard_create(
        #     self.num_marker_x, self.num_marker_y, 0.05, 0.01, dictionary)
        grid_board = aruco.CharucoBoard_create(
            self.num_marker_x, self.num_marker_y, 1, 0.8, dictionary)
        return grid_board

    def img_aruco(self):
        grid_board = self.aruco_board()
        img_board = grid_board.draw((self.res_board_x, self.res_board_y))
        return img_board

    def get_object_points(self):
        size_x = self.num_marker_x - 1
        size_y = self.num_marker_y - 1
        toReal = self.marker_real_size / 1000 # [m]
        objp = []
        for y in range(size_y):
            for x in range(size_x):
                px = x * toReal
                py = (size_y - y - 1) * toReal
                objp.append([py, px, 0])
        return np.float32(objp)

    # Find Chessboard Corners
    def read_chessboards(self, images, files=None):
        """
        Charuco base pose estimation.
        """
        print("POSE ESTIMATION STARTS:")
        allCorners = []
        allIds = []
        index = []
        decimator = 0
        # SUB PIXEL CORNER DETECTION CRITERION
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)

        aruco_dict = self.aruco_dict()
        board = self.aruco_board()

        for i, img in enumerate(images):
            if files is not None:
                print("=> image : {}".format(files[i]))
            else:
                print("=> image : {}".format(i))

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict)

            if len(corners)>0:
                # SUB PIXEL DETECTION
                for corner in corners:
                    cv2.cornerSubPix(gray, corner,
                        winSize = (3,3),
                        zeroZone = (-1,-1),
                        criteria = criteria)
                res2 = cv2.aruco.interpolateCornersCharuco(corners,ids,gray,board)
                if res2[1] is not None and res2[2] is not None and len(res2[1])>3 and decimator%1==0:
                    allCorners.append(res2[1])
                    allIds.append(res2[2])
                    index.append(1)
                    print("success")
                else:
                    index.append(0)
            else:	
                index.append(0)
            decimator+=1

        imsize = gray.shape
        return allCorners,allIds,imsize,index

    # Find Chessboard Corners for STEREO
    def read_chessboards_stereo(self, images_1, images_2, files_1=None, files_2=None):
        """
        Charuco base pose estimation.
        """
        print("POSE ESTIMATION (STEREO) STARTS:")
        allCorners_1 = []
        allCorners_2 = []
        allIds_1 = []
        allIds_2 = []
        objPoints = []
        index = []
        decimator = 0
        # SUB PIXEL CORNER DETECTION CRITERION
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)

        aruco_dict = self.aruco_dict()
        board = self.aruco_board()
        object_points = self.get_object_points()

        for i, (img_1, img_2) in enumerate(zip(images_1, images_2)):
            if files_1 is not None and files_2 is not None:
                print("=> image : {} , {}".format(files_1[i], files_2[i]))
            else:
                print("=> image : {} / {}".format(i, len(images_1)))

            gray_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
            gray_2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)
            corners_1, ids_1, _ = cv2.aruco.detectMarkers(gray_1, aruco_dict)
            corners_2, ids_2, _ = cv2.aruco.detectMarkers(gray_2, aruco_dict)

            # ids = []
            # new_corners_1 = []
            # new_corners_2 = []
            # for idx_1, Id in enumerate(ids_1):
            #     if Id in np.array(ids_2).flatten():
            #         idx_2 = list(ids_2).index([Id])
            #         new_corners_1.append(corners_1[idx_1])
            #         new_corners_2.append(corners_2[idx_2])
            #         ids.append([Id])

            # corners_1 = new_corners_1
            # corners_2 = new_corners_2
            # ids_1 = np.array(ids)
            # ids_2 = np.array(ids)

            both_exist = len(corners_1)>0 and len(corners_2)>0

            if both_exist:
                # print(len(corners_1),len(ids_1))
                # SUB PIXEL DETECTION
                for corner_1, corner_2 in zip(corners_1, corners_2):
                    cv2.cornerSubPix(gray_1, corner_1,
                        winSize = (3,3),
                        zeroZone = (-1,-1),
                        criteria = criteria)
                    cv2.cornerSubPix(gray_2, corner_2,
                        winSize = (3,3),
                        zeroZone = (-1,-1),
                        criteria = criteria)
                res_1 = cv2.aruco.interpolateCornersCharuco(corners_1,ids_1,gray_1,board)
                res_2 = cv2.aruco.interpolateCornersCharuco(corners_2,ids_2,gray_2,board)
                corners_1,ids_1 = res_1[1], res_1[2]
                corners_2,ids_2 = res_2[1], res_2[2]

                ids = []
                new_corners_1 = []
                new_corners_2 = []
                for idx_1, Id in enumerate(ids_1):
                    if Id in np.array(ids_2).flatten():
                        idx_2 = list(ids_2).index([Id])
                        new_corners_1.append(corners_1[idx_1])
                        new_corners_2.append(corners_2[idx_2])
                        ids.append([Id][0])

                corners_1 = np.array(new_corners_1)
                corners_2 = np.array(new_corners_2)
                ids_1 = np.array(ids)
                ids_2 = np.array(ids)

                # valid_1 = res_1[1] is not None and res_1[2] is not None and len(res_1[1])>3
                # valid_2 = res_2[1] is not None and res_2[2] is not None and len(res_2[1])>3
                valid_1 = corners_1 is not None and ids_1 is not None #and len(corners_1)>3
                valid_2 = corners_2 is not None and ids_2 is not None #and len(corners_2)>3
                if len(corners_1) > 0 and decimator%1==0:
                # if valid_1 and valid_2 and decimator%1==0:
                    allCorners_1.append(corners_2)
                    allCorners_2.append(corners_2)
                    allIds_1.append(ids_1)
                    allIds_2.append(ids_2)
                    # Object Points
                    objp = []
                    for i in ids:
                        objp.append(object_points[i][0])
                    objPoints.append(np.array(objp))
                    index.append(1)
                    print("success")
                else:
                    index.append(0)
            else:	
                index.append(0)
            decimator+=1

        imsize_1 = gray_1.shape
        imsize_2 = gray_2.shape
        return allCorners_1,allCorners_2,allIds_1,allIds_2,imsize_1,imsize_2,objPoints,index

    def draw_corner(self, images, allCorners, allIds):
        draw_images = []
        for img, corners, Ids in zip(images, allCorners, allIds):
            for corner, Id in zip(corners, Ids):
                Id = Id[0]
                px = corner[0][0]
                py = corner[0][1]

                ix = int(px + 0.5)
                iy = int(py + 0.5)

                img = cv2.circle(img, (ix,iy), 3, (255,0,0), 1)
                img = cv2.putText(img, str(Id), (ix - 10,iy -10), cv2.FONT_HERSHEY_PLAIN, 
                                    0.8, (0,0,255), 1, cv2.LINE_AA)
            draw_images.append(img)
        return draw_images

    # Calibration
    def calibrate_camera(self, allCorners, allIds, imsize):
        """
        Calibrates the camera using the dected corners.
        """
        print("CAMERA CALIBRATION")

        board = self.aruco_board()

        cameraMatrixInit = np.array([[ 1000.,    0., imsize[0]/2.],
                                    [    0., 1000., imsize[1]/2.],
                                    [    0.,    0.,           1.]])

        distCoeffsInit = np.zeros((5,1))
        flags = (cv2.CALIB_USE_INTRINSIC_GUESS + cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_FIX_ASPECT_RATIO)
        #flags = (cv2.CALIB_RATIONAL_MODEL)
        (ret, camera_matrix, distortion_coefficients0,
        rotation_vectors, translation_vectors,
        stdDeviationsIntrinsics, stdDeviationsExtrinsics,
        perViewErrors) = cv2.aruco.calibrateCameraCharucoExtended(
                        charucoCorners=allCorners,
                        charucoIds=allIds,
                        board=board,
                        imageSize=imsize,
                        cameraMatrix=cameraMatrixInit,
                        distCoeffs=distCoeffsInit,
                        flags=flags,
                        criteria=(cv2.TERM_CRITERIA_EPS & cv2.TERM_CRITERIA_COUNT, 10000, 1e-9))

        return ret, camera_matrix, distortion_coefficients0, rotation_vectors, translation_vectors

    # Calibration STEREO
    def calibrate_camera_stereo(self, allCorners_1, allCorners_2, allIds_1, allIds_2, objPoints, imsize_1, imsize_2):
        """ 
        Calibrates the camera using the dected corners.
        """
        print("CAMERA CALIBRATION STEREO")

        # Calibrate cameras separately to estimate intrinsic camera matrices
        ret_1, mtx_1, dist_1, rvecs_1, tvecs_1 = self.calibrate_camera(allCorners_1,allIds_1,imsize_1)
        ret_2, mtx_2, dist_2, rvecs_2, tvecs_2 = self.calibrate_camera(allCorners_2,allIds_2,imsize_2)

        # Stereo Calibration
        for i, (o, c1, c2) in enumerate(zip(objPoints, allCorners_1, allCorners_2)):
            print(i, len(o), len(c1), len(c2))
        # print(c1)

        res = cv2.stereoCalibrate(objPoints, allCorners_1, allCorners_2, mtx_1, dist_1, mtx_2, dist_2, None, 
                                flags=cv2.CALIB_FIX_INTRINSIC, 
                                criteria=(cv2.TERM_CRITERIA_EPS & cv2.TERM_CRITERIA_COUNT, 10000, 1e-9))
        err, KK_1, distCoeffs_1, KK_2, distCoeffs_2, R, T, E, F = res
        print('Error = {}'.format(err))
        return R, T, E, F

    def undist_images(self, images, mtx, dist):
        undist_images = []
        for img in images:
            img_undist = cv2.undistort(img,mtx,dist,None)
            undist_images.append(img_undist)
        return undist_images


if __name__ == '__main__':
    ar = Aruco()
    img_board = ar.img_aruco()
    cv2.imwrite('ARMarkerBoard_1500.png', img_board)