import os
import sys
import argparse

import pyrealsense2 as rs
import numpy as np
import cv2

dir_current = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir_current)
sys.path.append('../')

import config as cf
from utils import depth_tools as tool

os.chdir(dir_current)
###########################################################################################

# Parser
parser = argparse.ArgumentParser()
parser.add_argument('name', help='name of save dir')
parser.add_argument('cam', type=int, help='camera number')
parser.add_argument('idx', type=int, help='capture index')
args = parser.parse_args()

cam = args.cam
idx = args.idx
dir_save = cf.dir_save + args.name + '/' + cf.dir_realsense
os.makedirs(dir_save, exist_ok=True)

file_ply = dir_save + cf.save_ply
file_img = dir_save + cf.save_image
file_depth = dir_save + cf.save_depth

def save_images(cam, idx, rgb, depth):
    cv2.imwrite(file_img.format(cam, idx), rgb)
    depth_image = tool.pack_float_to_bmp_bgra(depth)
    cv2.imwrite(file_depth.format(cam, idx), depth_image)


if cam == 1:
    CAMERA = cf.CAMERA_1
elif cam == 2:
    CAMERA = cf.CAMERA_2
elif cam == 3:
    CAMERA = cf.CAMERA_3

pipeline = rs.pipeline()
config = rs.config()
config.enable_device(CAMERA)
config.enable_stream(rs.stream.color, cf.CAPTURE_WIDTH, cf.CAPTURE_HEIGHT, rs.format.bgr8, cf.CAPTURE_FPS)
config.enable_stream(rs.stream.depth, cf.CAPTURE_WIDTH, cf.CAPTURE_HEIGHT, rs.format.z16, cf.CAPTURE_FPS)
pipeline.start(config)

colorizer = rs.colorizer()

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        colorized = colorizer.process(frames)
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue
        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.5), cv2.COLORMAP_JET)

        # Stack RGB and depth horizontally
        list_stack = []
        list_stack.append(color_image)
        list_stack.append(depth_colormap)
        images = np.hstack(list_stack)

        # Show RGB and depth
        cv2.namedWindow('RealSense', cv2.WINDOW_NORMAL)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)

        # Save to press 's'
        ch = cv2.waitKey(25)
        if ch == ord('s'):
            print('Save')
            save_images(ch, idx, color_image, depth_image)
            ply = rs.save_to_ply(file_ply.format(cam, idx))
            ply.set_option(rs.save_to_ply.option_ply_binary, False)
            ply.set_option(rs.save_to_ply.option_ply_normals, False)
            print('Saving to ply...')
            ply.process(colorized)
            print('Done')
        elif ch == 27:
            break

finally:
    # Stop streaming
    pipeline.stop()