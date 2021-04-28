import cv2
import numpy as np
import os
import sys
from cv2 import aruco
import glob

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
board = aruco.CharucoBoard_create(10, 8, 1, .8, aruco_dict)

def read_chessboards(images):
	"""
	Charuco base pose estimation.
	"""
	print("POSE ESTIMATION STARTS:")
	allCorners = []
	allIds = []
	decimator = 0
	# SUB PIXEL CORNER DETECTION CRITERION
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)

	for im in images:
		print("=> Processing image {0}".format(im))
		frame = cv2.imread(im)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict)

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
	
		decimator+=1

	imsize = gray.shape
	return allCorners,allIds,imsize

def calibrate_camera(allCorners,allIds,imsize):
    """
    Calibrates the camera using the dected corners.
    """
    print("CAMERA CALIBRATION")

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


def draw_corner(images,allCorners,allIds):

	dst_images = []
	
	for ind0 in range(len(images)):
		src = cv2.imread(images[ind0],1)
		
		corners = allCorners[ind0]
		Ids = allIds[ind0]
		
		dst = src.copy()
		for ind1 in range(len(corners)):
			corner = corners[ind1]
			Id = Ids[ind1][0]
			px = corner[0][0]
			py = corner[0][1]

			ix = int(px + 0.5)
			iy = int(py + 0.5)

		
			dst = cv2.circle(dst,(ix,iy),3,(255,0,0),1)
			dst = cv2.putText(dst, str(Id), (ix - 10,iy -10), cv2.FONT_HERSHEY_PLAIN, 0.8, (0,0,255), 1, cv2.LINE_AA)

		dst_images.append(dst)

	return dst_images

base_folder = "test002/"
image_folder = base_folder+"/cam/"
iso_folder = base_folder+"/iso"
if (os.path.exists(iso_folder)==False):
	os.makedirs(iso_folder)
detect_folder = base_folder+"/detect"
if (os.path.exists(detect_folder)==False):
	os.makedirs(detect_folder)

point_folder = base_folder+"/point"
if (os.path.exists(point_folder)==False):
	os.makedirs(point_folder)

# read image folder
images = sorted(glob.glob(image_folder+"/*.png"))
print(images)
allCorners,allIds,imsize = read_chessboards(images)
print("allCorners num",len(allCorners[0]))
print("allIds num",len(allIds[0]))

# draw id
detect_images = draw_corner(images,allCorners,allIds)

for ind0 in range(len(detect_images)):
	dst_image = detect_images[ind0]
	cv2.imwrite(detect_folder+"/image%03d.png"%ind0,dst_image)

# output cam2D and cam3D
# display dotpitch 0.270mm [ Mitubishi diamondcrysta RDT24IWH]
# pattern 22 -> col 21 ids
# pattern 16 -> raw 15 ids



cam2d_format = point_folder+"/cam2D%03d.txt"
cam3d_format = point_folder+"/cam3D%03d.txt"

dot_pitch = 0.27 * 0.001#[mm]
marker_pixel_size = 100#[px]

marker_real_size = marker_pixel_size * dot_pitch

marker_x_num = 10
marker_y_num = 8

print("dot pithc ",dot_pitch," m")
print("marker pixel ",marker_pixel_size," px")
print("marker real ",marker_real_size," m")

cam_true_list = []

for ind0 in range(len(allCorners)):
	corners = allCorners[ind0]
	Ids = allIds[ind0]

	cam2d_file = cam2d_format%ind0
	cam3d_file = cam3d_format%ind0

	cam2d = np.zeros([len(corners),3])# id, px ,py
	cam3d = np.zeros([len(corners),4])# id, px,py,pz

	cam_true_list.append(ind0)

	for ind1 in range(len(corners)):
		corner = corners[ind1]
		Id = Ids[ind1]

		cam2d[ind1,0] = Id
		cam2d[ind1,1:] = corner.copy()
		
		cam3d[ind1,0] = Id
		cam3d[ind1,1] = float(int(Id%(marker_x_num - 1))) * marker_real_size
		cam3d[ind1,2] = float(int(Id/(marker_x_num - 1))) * marker_real_size

	fmt='%d %lf %lf'
	np.savetxt(cam2d_file,cam2d,delimiter=" ",fmt = fmt)
	fmt='%d %lf %lf %lf'
	np.savetxt(cam3d_file,cam3d,delimiter=" ",fmt = fmt)

cam_true_list = np.asarray(cam_true_list).astype('int32')
print(cam_true_list)
np.savetxt(point_folder+"/cam_true_num.txt",cam_true_list,delimiter=" ",  fmt='%d')

# calibration

		
		
		


