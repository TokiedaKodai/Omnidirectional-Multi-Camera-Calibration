import cv2
import numpy as np
import os
import argparse

from freenect2 import Device, FrameType

import config as cf
import depth_tools as dt

# Parser
parser = argparse.ArgumentParser()
parser.add_argument('--name', help='name of save dir (optional)')
parser.add_argument('--depth', action='store_true', help='add to save depth image')
args = parser.parse_args()

dir_name = args.name
is_depth = args.depth

# Save dir
dir_save = cf.dir_save
dir_name = args.name
if not dir_name is None:
    dir_save += dir_name + '/'
save_image = dir_save + cf.save_image
save_depth = dir_save + cf.save_depth
os.makedirs(dir_save, exist_ok=True)

def save_images(cam, idx, rgb, depth=None):
    cv2.imwrite(save_image.format(cam, idx), rgb)
    if depth is not None:
        depth_image = dt.pack_float_to_bmp_bgra(depth)
        cv2.imwrite(save_depth.format(cam, idx), depth_image)

# Capture index
idx1 = 0
idx2 = 0
idx3 = 0

# Get Kinect
device = Device()

depth = None

try:
    while True:
        frames = {}
        with device.running():
            for type_, frame in device:
                frames[type_] = frame
                if FrameType.Color in frames and FrameType.Depth in frames:
                    break

        rgb, depth = frames[FrameType.Color], frames[FrameType.Depth]

        rgb = cv2.flip(rgb.to_array(), 1)
        depth = cv2.flip(depth.to_array(), 1)

	    # Stack all images horizontally
        list_stack = [rgb]
        # if is_depth:
        #     list_stack.append([depth, depth, depth])
        images = np.hstack(list_stack)
	    # Show images from both cameras
        cv2.namedWindow('Kinect', cv2.WINDOW_NORMAL)
        cv2.imshow('Kinect', images)
        cv2.waitKey(1)

	    # Save images and depth maps from selected camera by pressing camera number
        ch = cv2.waitKey(25)
        if ch == ord('1'):
            save_images(1, idx1, rgb, depth)
            idx1 += 1
            print('Save camera-1 frame:{}'.format(idx1))
        elif ch == ord('2'):
            save_images(2, idx2, rgb, depth)
            idx2 += 1
            print('Save camera-2 frame:{}'.format(idx2))
        elif ch == ord('3'):
            save_images(3, idx3, rgb, depth)
            idx3 += 1
            print('Save camera-3 frame:{}'.format(idx3))
        elif ch == 27:
            break

finally:
    device.stop()
