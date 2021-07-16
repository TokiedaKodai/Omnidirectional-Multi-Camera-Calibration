import os
import sys
import argparse

from freenect2 import Device, FrameType
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
parser.add_argument('--idx', type=int, default=0, help='capture index')
args = parser.parse_args()

cam = args.cam
idx = args.idx
dir_save = cf.dir_save + args.name + '/' + cf.dir_kinect
os.makedirs(dir_save, exist_ok=True)

file_ply = dir_save + cf.save_ply
file_img = dir_save + cf.save_image
file_depth = dir_save + cf.save_depth

def save_images(cam, idx, rgb, depth=None):
    cv2.imwrite(file_img.format(cam, idx), rgb)
    depth_image = tool.pack_float_to_bmp_bgra(depth)
    cv2.imwrite(file_depth.format(cam, idx), depth_image)


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
        depth = cv2.flip(depth.to_array(), 1)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth, alpha=0.5), cv2.COLORMAP_JET)

        window = np.zeros((cf.RGB_HEIGHT, cf.RGB_WIDTH + cf.DEPTH_WIDTH, 3), dtype='uint8')
        window[:, :cf.RGB_WIDTH, :] = np.array(rgb[:, :, :3], dtype='uint8')
        h_start = (cf.RGB_HEIGHT - cf.DEPTH_HEIGHT)//2
        window[h_start:h_start + cf.DEPTH_HEIGHT, cf.RGB_WIDTH:, :3] = np.array(depth_colormap, dtype='uint8')

        cv2.namedWindow('Kinect', cv2.WINDOW_NORMAL)
        cv2.imshow('Kinect', window)
        cv2.waitKey(1)

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

    # depth /= 1000 # mm -> m

    xyz = tool.convert_depth_to_coords_no_pix_size(depth, cam_params)
    tool.dump_ply(file_ply.format(cam, idx), xyz.reshape(-1, 3).tolist())

    save_images(cam, idx, rgb, depth)
