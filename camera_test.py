import pyrealsense2 as rs
import numpy as np
import cv2
import sys

import config as cf
import tool_realsense as tr

argv = sys.argv
_, camera_no = argv

if camera_no is '1':
    test_camera = "816612061596"
elif camera_no is '2':
    test_camera = "821212060533"
elif camera_no is '3':
    test_camera = "816612061727"

# Reset USB Connection
tr.reset_usb()

# Configure depth and color streams...
# from select Camera
pipeline_1 = rs.pipeline()
config_1 = rs.config()
config_1.enable_device(test_camera)
# config_1.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config_1.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)


# Start streaming from both cameras
pipeline_1.start(config_1)

idx1 = 0

try:
    while True:

        #### Camera 1
        # Wait for a coherent pair of frames: depth and color
        frames_1 = pipeline_1.wait_for_frames()
        # depth_frame_1 = frames_1.get_depth_frame()
        color_frame_1 = frames_1.get_color_frame()
        # if not depth_frame_1 or not color_frame_1:
        #     continue
        if not color_frame_1:
            continue
        # Convert images to numpy arrays
        # depth_image_1 = np.asanyarray(depth_frame_1.get_data())
        color_image_1 = np.asanyarray(color_frame_1.get_data())
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        # depth_colormap_1 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image_1, alpha=0.5), cv2.COLORMAP_JET)


        # Stack all images horizontally
        # images = np.hstack((color_image_1, depth_colormap_1))
        images = color_image_1

        # Show images from both cameras
        cv2.namedWindow('RealSense', cv2.WINDOW_NORMAL)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)

        # Save images and depth maps from both cameras by pressing 's'
        ch = cv2.waitKey(25)
        if ch == ord('s'):
            cv2.imwrite("test_camera-{}_rgb-{}.jpg".format(camera_no, idx1), color_image_1)
            # cv2.imwrite("test_camera-{}_depth-{}.jpg".format(camera_no, idx1), depth_colormap_1)
            idx1 += 1
            print("Save camera-{}".format(camera_no))
        elif ch == 27:
            break


finally:
    # Stop streaming
    pipeline_1.stop()