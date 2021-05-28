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
parser.add_argument('--name', help='name of save dir (optional)')
args = parser.parse_args()

camera_no = args.cam
idx = args.idx
dir_name = args.name
is_depth = args.depth

# Save dir
dir_save = cf.dir_save
if not dir_name is None:
    dir_save += dir_name + '/'
os.makedirs(dir_save, exist_ok=True)

save_ply_file = dir_save + cf.save_ply

if camera_no == 1:
    CAMERA = cf.CAMERA_1
elif camera_no == 2:
    CAMERA = cf.CAMERA_2
elif camera_no == 3:
    CAMERA = cf.CAMERA_3


pipeline = rs.pipeline()
config = rs.config()
config.enable_device(CAMERA)
config.enable_stream(rs.stream.color, cf.CAPTURE_WIDTH, cf.CAPTURE_HEIGHT, rs.format.bgr8, cf.CAPTURE_FPS)
config.enable_stream(rs.stream.depth, cf.CAPTURE_WIDTH, cf.CAPTURE_HEIGHT, rs.format.z16, cf.CAPTURE_FPS)


pipeline.start(config)

colorizer = rs.colorizer()

try:
    # Wait for the next set of frames from the camera
    frames = pipe.wait_for_frames()
    colorized = colorizer.process(frames)

    # Create save_to_ply object
    ply = rs.save_to_ply(save_ply_file.format(camera_no, idx))

    # Set options to the desired values
    # In this example we'll generate a textual PLY with normals (mesh is already created by default)
    ply.set_option(rs.save_to_ply.option_ply_binary, False)
    ply.set_option(rs.save_to_ply.option_ply_normals, True)

    print("Saving to 1.ply...")
    # Apply the processing block to the frameset which contains the depth frame and the texture
    ply.process(colorized)
    print("Done")
finally:
    pipe.stop()