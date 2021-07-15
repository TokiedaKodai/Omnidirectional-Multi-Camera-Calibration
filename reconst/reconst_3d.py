import numpy as np
import cv2
import glob

import config as cf
import depth_tools as tool

cam_params = {
    'focal_length': 628.271728515625, # [pixel]
    'center_x': 317.635650634766,
    'center_y': 231.91423034668
}

file_ext_param = '../captures/210623/calib/extrinsic_params.txt'

rt12 = []
rt23 = []
rt31 = []
cnt = 0
for line in open(file_ext_param, 'r'):
    line = line.rstrip('\n')
    if 1 < cnt < 5:
        rt12.append(line.split())
    if 8 < cnt < 12:
        rt23.append(line.split())
    if 15 < cnt < 19:
        rt31.append(line.split())
    cnt += 1
    
rt12 = np.array(rt12, dtype=float)
rt23 = np.array(rt23, dtype=float)
rt31 = np.array(rt31, dtype=float)
r12 = rt12[:3, :3]
r23 = rt23[:3, :3]
r31 = rt31[:3, :3]
t12 = rt12[:3, 3]
t23 = rt23[:3, 3]
t31 = rt31[:3, 3]

r13 = np.linalg.inv(r31)
t13 = t31 * -1


dir_0 = '../experiments/20210702T140403.448/image_00/depth/'
dir_1 = '../experiments/20210702T140403.448/image_01/depth/'
dir_2 = '../experiments/20210702T140403.448/image_02/depth/'
filename = '000000.png'

depth_2 = cv2.imread(dir_0 + filename, -1)
depth_1 = cv2.imread(dir_1 + filename, -1)
depth_3 = cv2.imread(dir_2 + filename, -1)
depth_1 = depth_1 / 1000
depth_2 = depth_2 / 1000
depth_3 = depth_3 / 1000

xyz_1 = tool.convert_depth_to_coords_no_pix_size(depth_1, cam_params).reshape(-1, 3).tolist()
xyz_2 = tool.convert_depth_to_coords_no_pix_size(depth_2, cam_params).reshape(-1, 3).tolist()
xyz_3 = tool.convert_depth_to_coords_no_pix_size(depth_3, cam_params).reshape(-1, 3).tolist()


new_xyz_1 = []
for i in range(len(xyz_1)):
    xyz = np.array(xyz_1[i])
    xyz = np.dot(xyz, r13)
    xyz += t13
    new_xyz_1.append(xyz)
new_xyz_2 = []
for i in range(len(xyz_2)):
    xyz = np.array(xyz_2[i])
    xyz = np.dot(xyz, r23)
    xyz += t23
    new_xyz_2.append(xyz)

list_xyz = new_xyz_1 + new_xyz_2 + xyz_3
tool.dump_ply(dir_0 + '3d.ply', list_xyz)