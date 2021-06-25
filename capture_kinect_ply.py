import cv2
import numpy as np
import os
import argparse
import glob

from freenect2 import Device, FrameType

import config as cf
import depth_tools as tool

# Parser
parser = argparse.ArgumentParser()
parser.add_argument('--name', help='name of save dir (optional)')
parser.add_argument('--rgb', action='store_true', help='add to save rgb image')
parser.add_argument('--depth', action='store_true', help='add to save depth image')
args = parser.parse_args()

dir_name = args.name
is_rgb = args.rgb
is_depth = args.depth

# Save dir
dir_save = cf.dir_save
dir_name = args.name
if dir_name is None:
    dir_save += dir_name + '/'
else:
    dir_save += 'sample/'

save_rgb = 'rgb_{}.png'
save_depth = 'depth_{}.bmp'
save_ply = 'ply_{}.ply'
save_image = dir_save + save_rgb
save_depth = dir_save + save_depth
save_ply = dir_save + save_ply

os.makedirs(dir_save, exist_ok=True)

# Capture index
saved_files = glob.glob(dir_save + '*.ply')
idx = len(saved_files)

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

        cv2.namedWindow('Kinect', cv2.WINDOW_NORMAL)
        cv2.imshow('Kinect', rgb)
        cv2.waitKey(1)

	    # Save images and depth maps from selected camera by pressing camera number
        ch = cv2.waitKey(25)
        if ch == ord('s'):
            break

        color = device.color_camera_params
        ir = device.ir_camera_params

finally:
    device.stop()
    print(f'color\nfx:{color.fx}\nfy:{color.fy}\ncx:{color.cx}\ncy:{color.cy}')
    print(f'ir\nfx:{ir.fx}\nfy:{ir.fy}\ncx:{ir.cx}\ncy:{ir.cy}\nk1:{ir.k1}\nk2:{ir.k2}\nk3:{ir.k3}\np1:{ir.p1}\np2:{ir.p2}')

    cam_params = {
        'focal_length': float(ir.fx), # [pixel]
        'center_x': float(ir.cx),
        'center_y': float(ir.cy)
    }

    depth /= 1000 # mm -> m

    xyz = tool.convert_depth_to_coords_no_pix_size(depth, cam_params)
    tool.dump_ply(save_ply.format(idx), xyz.reshape(-1, 3).tolist())

    if is_rgb:
        cv2.imwrite(save_image.format(idx), rgb)
    if is_depth:
        depth_image = tool.pack_float_to_bmp_bgra(depth)
        cv2.imwrite(save_depth.format(idx), depth_image)