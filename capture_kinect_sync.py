import cv2
import numpy as np
import os
import argparse

from freenect2 import Device, FrameType

import config as cf

# Parser
parser = argparse.ArgumentParser()
parser.add_argument('cam', type=int, help='camera number')
parser.add_argument('idx', type=int, help='capture index')
parser.add_argument('--name', help='name of save dir (optiional)')
parser.add_argument('--depth', action='store_true', help='add to save depth image')
args = parser.parse_args()

cam = args.cam
idx = args.idx
dir_name = args.name
is_depth = args.depth

# Save dir
dir_save = cf.dir_save
if not dir_name is None:
    dir_save += dir_name + '/'
save_image = dir_save + cf.save_kinect_img
save_depth = dir_save + cf.save_kinect_depth
os.makedirs(dir_save, exist_ok=True)


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

        rgb = cv2.flip(rgb.to_array(), 1)
        depth = depth.to_array()

	# Stack all images horizontally
        list_stack = [rgb]
        if is_depth:
            list_stack.append([depth, depth, depth])
        images = np.hstack(list_stack)
	# Show images from both cameras
        cv2.namedWindow('Kinect', cv2.WINDOW_NORMAL)
        cv2.imshow('Kinect', images)
        cv2.waitKey(1)

        cv2.imwrite(save_image.format(cam, idx), rgb)
        if is_depth:
            cv2.imwrite(save_depth.format(cam, idx), depth)

        break

finally:
    device.stop()