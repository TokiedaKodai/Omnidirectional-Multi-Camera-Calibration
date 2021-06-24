import argparse
import cv2
import numpy as np
import glob

import config as cf
import depth_tools as tool

def getNewFile(file_path):
    file_hierarchy = file_path.split('.')
    new_file_path = '.'.join(file_hierarchy[:-1] + ['ply'])
    print(new_file_path)
    return new_file_path

cam_params = {
    'focal_length': 0.03648738098144531,
    # 'pix_x': 1.25e-05,
    # 'pix_y': ,
    'center_x': 259.96539306640625,
    'center_y': 212.30979919433594
}

cam_params = {
    'focal_length': 0.037009,
    'pix_x': 1.25e-05,
    'pix_y': 1.2381443057539635e-05,
    'center_x': 790.902,
    'center_y': 600.635
}

parser = argparse.ArgumentParser()
parser.add_argument('dir', help='directory')
args = parser.parse_args()

dire = args.dir

if not dire[0] == 'C':
    dire = cf.dir_save + dire

read_files = sorted(glob.glob(dire + '/*.bmp'))

for file in read_files:
    img = cv2.imread(file, -1)
    depth = tool.unpack_bmp_bgra_to_float(img) / 1000
    xyz = tool.convert_depth_to_coords_no_pix_size(depth, cam_params)
    # xyz = tool.convert_depth_to_coords(depth, cam_params)
    tool.dump_ply(getNewFile(file), xyz.reshape(-1, 3).tolist())
