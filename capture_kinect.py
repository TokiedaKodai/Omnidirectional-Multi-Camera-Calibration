import cv2
import numpy as np
import os
import argparse

from freenect2 import Device, FrameType

import config as cf

# Parser
parser = argparse.ArgumentParser()
parser.add_argument('--name', help='name of save dir (optiional)')
parser.add_argument('--depth', action='store_true', help='add to save depth image')
args = parser.parse_args()

dir_name = args.name
is_depth = args.depth

# Save dir
dir_save = cf.dir_save
dir_name = args.name
if not dir_name is None:
    dir_save += dir_name + '/'
save_image = dir_save + cf.save_kinect_img
save_depth = dir_save + cf.save_kinect_depth
os.makedirs(dir_save, exist_ok=True)

# Capture index
idx1 = 0
idx2 = 0
idx3 = 0

# Get Kinect
device = Device()

try:
    while True:
        frames = {}
        with device.running():
            for type_, frame in device:
                frames[type_] = frame
                if FrameType.Color in frames and FrameType.Depth in frames:
                    break

        rgb, depth = frames[FrameType.Color], frames[FrameType.Depth]

	# Stack all images horizontally
        list_stack = [rgb.to_array()]
        if is_depth:
            list_stack.append([depth.to_array(), depth.to_array(), depth.to_array()])
        images = np.hstack(list_stack)
	# Show images from both cameras
        cv2.namedWindow('Kinect', cv2.WINDOW_NORMAL)
        cv2.imshow('Kinect', images)
        cv2.waitKey(1)

	# Save images and depth maps from selected camera by pressing camera number
        ch = cv2.waitKey(25)
        if ch == ord('1'):
            cv2.imwrite(save_image.format(1, idx1), rgb.to_array())
            if is_depth:
                cv2.imwrite(save_depth.format(1, idx1), depth.to_array())
            idx1 += 1
            print('Save camera-1 frame:{}'.format(idx1))
        elif ch == ord('2'):
            cv2.imwrite(save_image.format(2, idx2), rgb.to_array())
            if is_depth:
                cv2.imwrite(save_depth.format(2, idx2), depth.to_array())
            idx2 += 1
            print('Save camera-2 frame:{}'.format(idx2))
        elif ch == ord('3'):
            cv2.imwrite(save_image.format(3, idx3), rgb.to_array())
            if is_depth:
                cv2.imwrite(save_depth.format(3, idx3), depth.to_array())
            idx3 += 1
            print('Save camera-3 frame:{}'.format(idx3))
        elif ch == 27:
            break

finally:
    device.stop()
