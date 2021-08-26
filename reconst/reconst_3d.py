import os
import sys
import argparse

import cv2
import numpy as np
from scipy.spatial.transform import Rotation as R

dir_current = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir_current)
sys.path.append('../')

import config as cf
from utils import depth_tools as tool

os.chdir(dir_current)
###########################################################################################
cam_params = {
    'focal_length': 628.271728515625, # [pixel]
    'center_x': 317.635650634766,
    'center_y': 231.91423034668
}

# Parser
parser = argparse.ArgumentParser()
parser.add_argument('name', help='name of save dir')
args = parser.parse_args()

dir_save = cf.dir_save + args.name + '/'

rts = []
for dic in cf.dic_cams:
    directory = dir_save + dic['dir']

    rt = []
    file_param = directory + cf.save_param.format('r' + str(dic['cams'][0]), 'r' + str(dic['cams'][1]))
    print(file_param)
    for line in open(file_param, 'r'):
        rt.append(line.split())
    rts.append(np.array(rt, dtype=float))

rt12 = rts[0]
rt23 = rts[1]
rt31 = rts[2]
r12 = rt12[:3, :3]
r23 = rt23[:3, :3]
r31 = rt31[:3, :3]
t12 = rt12[:3, 3]
t23 = rt23[:3, 3]
t31 = rt31[:3, 3]

r21 = np.linalg.inv(r12)
t21 = t12 * -1

dir_name = '../Captures/210722/realsense/'
file_1 = dir_name + 'depth_1-0.bmp'
file_2 = dir_name + 'depth_2-0.bmp'
file_3 = dir_name + 'depth_3-0.bmp'

depth_1 = tool.unpack_bmp_bgra_to_float(cv2.imread(file_1, -1))
depth_2 = tool.unpack_bmp_bgra_to_float(cv2.imread(file_2, -1))
depth_3 = tool.unpack_bmp_bgra_to_float(cv2.imread(file_3, -1))
depth_1 = depth_1 / 1000
depth_2 = depth_2 / 1000
depth_3 = depth_3 / 1000

xyz_1 = tool.convert_depth_to_coords_no_pix_size(depth_1, cam_params).reshape(-1, 3).tolist()
xyz_2 = tool.convert_depth_to_coords_no_pix_size(depth_2, cam_params).reshape(-1, 3).tolist()
xyz_3 = tool.convert_depth_to_coords_no_pix_size(depth_3, cam_params).reshape(-1, 3).tolist()

new_xyz_2 = []
for i in range(len(xyz_2)):
    xyz = np.array(xyz_2[i])
    xyz = np.dot(xyz, r21)
    xyz += t21
    new_xyz_2.append(xyz)
new_xyz_3 = []
for i in range(len(xyz_3)):
    xyz = np.array(xyz_3[i])
    xyz = np.dot(xyz, r31)
    xyz += t31
    new_xyz_3.append(xyz)

list_xyz = xyz_1 + new_xyz_2 + new_xyz_3
tool.dump_ply(dir_name + '3d.ply', list_xyz)