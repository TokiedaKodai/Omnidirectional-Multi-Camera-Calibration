import pyrealsense2 as rs

import numpy as np
import cv2
import os
import argparse

import config as cf
import tool_realsense as tr

# Parser
parser = argparse.ArgumentParser()
parser.add_argument('--name', help='name of save dir (optiional)')
args = parser.parse_args()

# Save dir
dir_save = cf.dir_save
dir_name = args.name
if not dir_name is None:
    dir_save += dir_name + '/'
save_image = dir_save + cf.save_image
save_depth = dir_save + cf.save_depth
os.makedirs(dir_save, exist_ok=True)

# Reset USB Connection
tr.reset_usb()

is_camera_1 = True
is_camera_2 = True
is_camera_3 = True

# Configure depth and color streams of 3 cameras
# Camera 1
pipeline_1 = rs.pipeline()
config_1 = rs.config()
config_1.enable_device(cf.CAMERA_1)
# config_1.enable_stream(rs.stream.depth, cf.CAPTURE_WIDTH, cf.CAPTURE_HEIGHT, rs.format.z16, cf.CAPTURE_FPS)
config_1.enable_stream(rs.stream.color, cf.CAPTURE_WIDTH, cf.CAPTURE_HEIGHT, rs.format.bgr8, cf.CAPTURE_FPS)
# Camera 2
pipeline_2 = rs.pipeline()
config_2 = rs.config()
config_2.enable_device(cf.CAMERA_2)
# config_2.enable_stream(rs.stream.depth, cf.CAPTURE_WIDTH, cf.CAPTURE_HEIGHT, rs.format.z16, cf.CAPTURE_FPS)
config_2.enable_stream(rs.stream.color, cf.CAPTURE_WIDTH, cf.CAPTURE_HEIGHT, rs.format.bgr8, cf.CAPTURE_FPS)
# Camera 3
pipeline_3 = rs.pipeline()
config_3 = rs.config()
config_3.enable_device(cf.CAMERA_3)
# config_3.enable_stream(rs.stream.depth, cf.CAPTURE_WIDTH, cf.CAPTURE_HEIGHT, rs.format.z16, cf.CAPTURE_FPS)
config_3.enable_stream(rs.stream.color, cf.CAPTURE_WIDTH, cf.CAPTURE_HEIGHT, rs.format.bgr8, cf.CAPTURE_FPS)


# Start streaming from multi-cameras
if is_camera_1:
    pipeline_1.start(config_1)
if is_camera_2:
    pipeline_2.start(config_2)
if is_camera_3:
    pipeline_3.start(config_3)

# Capture index
idx1 = 0
idx2 = 0
idx3 = 0

try:
    while True:
        #### Camera 1
        if is_camera_1:
            # Wait for a coherent pair of frames: depth and color
            frames_1 = pipeline_1.wait_for_frames()
            # depth_frame_1 = frames_1.get_depth_frame()
            color_frame_1 = frames_1.get_color_frame()
            # if not depth_frame_1 or not color_frame_1:
            if not color_frame_1:
                continue
            # Convert images to numpy arrays
            # depth_image_1 = np.asanyarray(depth_frame_1.get_data())
            color_image_1 = np.asanyarray(color_frame_1.get_data())
            # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            # depth_colormap_1 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image_1, alpha=0.5), cv2.COLORMAP_JET)

        #### Camera 2
        if is_camera_2:
            # Wait for a coherent pair of frames: depth and color
            frames_2 = pipeline_2.wait_for_frames()
            # depth_frame_2 = frames_2.get_depth_frame()
            color_frame_2 = frames_2.get_color_frame()
            # if not depth_frame_2 or not color_frame_2:
            if not color_frame_2:
                continue
            # Convert images to numpy arrays
            # depth_image_2 = np.asanyarray(depth_frame_2.get_data())
            color_image_2 = np.asanyarray(color_frame_2.get_data())
            # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            # depth_colormap_2 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image_2, alpha=0.5), cv2.COLORMAP_JET)

        #### Camera 3
        if is_camera_3:
            # Wait for a coherent pair of frames: depth and color
            frames_3 = pipeline_3.wait_for_frames()
            # depth_frame_3 = frames_3.get_depth_frame()
            color_frame_3 = frames_3.get_color_frame()
            # if not depth_frame_3 or not color_frame_3:
            if not color_frame_3:
                continue
            # Convert images to numpy arrays
            # depth_image_3 = np.asanyarray(depth_frame_3.get_data())
            color_image_3 = np.asanyarray(color_frame_3.get_data())
            # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            # depth_colormap_3 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image_3, alpha=0.5), cv2.COLORMAP_JET)


        # Stack all images horizontally
        list_stack = []
        if is_camera_1:
            # list_stack.append(color_image_1, depth_colormap_1)
            list_stack.append(color_image_1)
        if is_camera_2:
            # list_stack.append(color_image_2, depth_colormap_2)
            list_stack.append(color_image_2)
        if is_camera_3:
            # list_stack.append(color_image_3, depth_colormap_3)
            list_stack.append(color_image_3)
        images = np.hstack(list_stack)

        # Show images from both cameras
        cv2.namedWindow('RealSense', cv2.WINDOW_NORMAL)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)

        # Save images and depth maps from selected camera by pressing camera number
        ch = cv2.waitKey(25)
        if ch == ord('1') and is_camera_1:
            cv2.imwrite(save_image.format(1, idx1), color_image_1)
            # cv2.imwrite(save_depth.format(ch, idx1), depth_colormap_1)
            idx1 += 1
            print('Save camera-1 frame:{}'.format(idx1))
        elif ch == ord('2') and is_camera_2:
            cv2.imwrite(save_image.format(2, idx2), color_image_2)
            # cv2.imwrite(save_depth.format(ch, idx2), depth_colormap_2)
            idx2 += 1
            print('Save camera-2 frame:{}'.format(idx2))
        elif ch == ord('3') and is_camera_3:
            cv2.imwrite(save_image.format(3, idx3), color_image_3)
            # cv2.imwrite(save_depth.format(ch, idx3), depth_colormap_3)
            idx3 += 1
            print('Save camera-3 frame:{}'.format(idx3))
        elif ch == ord('s') and is_camera_1:
            cv2.imwrite(save_image.format(1, idx1), color_image_1)
            cv2.imwrite(save_image.format(2, idx2), color_image_2)
            cv2.imwrite(save_image.format(3, idx3), color_image_3)
            idx1 += 1
            idx2 += 1
            idx3 += 1
            print('Save all cameras frame:{},{},{}'.format(idx1, idx2, idx3))
        elif ch == 27:
            break

finally:
    # Stop streaming
    if is_camera_1:
        pipeline_1.stop()
    if is_camera_2:
        pipeline_2.stop()
    if is_camera_3:
        pipeline_3.stop()
