import pyrealsense2 as rs

import numpy as np
import cv2
import os
import argparse

import config as cf
import tool_realsense as tr

# Parser
parser = argparse.ArgumentParser()
parser.add_argument('cam', type=int, help='camera number')
parser.add_argument('idx', type=int, help='capture index')
parser.add_argument('--name', help='name of save dir (optiional)')
parser.add_argument('--depth', action='store_true', help='add to save depth image')
args = parser.parse_args()

camera_no = args.cam
idx = args.idx
dir_name = args.name
is_depth = args.depth

# Save dir
dir_save = cf.dir_save
if not dir_name is None:
    dir_save += dir_name + '/'
save_image = dir_save + cf.save_image
save_depth = dir_save + cf.save_depth
os.makedirs(dir_save, exist_ok=True)


if camera_no == 1:
    CAMERA = CAMERA_1
elif camera_no == 2:
    CAMERA = CAMERA_2
elif camera_no == 3:
    CAMERA = CAMERA_2


# Reset USB Connection
tr.reset_usb()

# Configure depth and color streams...
# from select Camera
pipeline = rs.pipeline()
config = rs.config()
config.enable_device(CAMERA)
config.enable_stream(rs.stream.color, cf.CAPTURE_WIDTH, cf.CAPTURE_HEIGHT, rs.format.bgr8, cf.CAPTURE_FPS)
if is_depth:
    config.enable_stream(rs.stream.depth, cf.CAPTURE_WIDTH, cf.CAPTURE_HEIGHT, rs.format.z16, cf.CAPTURE_FPS)

# Start streaming from both cameras
pipeline.start(config)

try:
    while True:
        # Wait for frames
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if is_depth:
            depth_frame = frames.get_depth_frame()
        
        if not color_frame or (is_depth and not depth_frame):
            continue

        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())
        if is_depth:
            depth_image = np.asanyarray(depth_frame.get_data())
            # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.5), cv2.COLORMAP_JET)

        # Save
        cv2.imwrite(save_image.format(camera_no, idx), color_image)
        if is_depth:
            cv2.imwrite(save_depth.format(camera_no, idx), depth_colormap)
	
        break

finally:
    # Stop streaming
    pipeline.stop()
