import os
import sys
import argparse

import numpy as np
from scipy.spatial.transform import Rotation as R

dir_current = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir_current)
sys.path.append('../')

import config as cf

os.chdir(dir_current)
###########################################################################################

# Parser
parser = argparse.ArgumentParser()
parser.add_argument('name', help='name of save dir')
args = parser.parse_args()

dir_save = cf.dir_save + args.name + '/'
file_extrinsic = dir_save + cf.save_extrinsic_param

f = open(file_extrinsic, 'w')

rts = []
for dic in cf.dic_cams:
    directory = dir_save + dic['dir']

    f.write('{}->{}'.format(*dic['cams']))
    rt = []
    for line in open(directory + cf.save_param.format('r' + dic['cams'][0], 'r' + dic['cams'][1]), 'r'):
        f.write(line)
        rt.append(line.split())
    rts.append(np.array(rt, dtype=float))
    f.write('\n')


rt12 = rts[0]
rt23 = rts[1]
rt31 = rts[2]

rt123 = np.dot(rt23, rt12)
rt1231 = np.dot(rt31, rt123)

print(rt1231)

f.write('Evaluation\n')
f.write('1->2->3->1\n')
for line in list(rt1231):
    f.write('{} {} {} {}\n'.format(*line))

r = R.from_matrix(rt1231[:3, :3])
angle_err = r.as_euler('xyz', degrees=True)
angle_err_total = np.sqrt(np.sum(np.square(angle_err)))
trans_err = rt1231[0:3,3]
trans_err_total = np.sqrt(np.sum(np.square(trans_err)))

print('Rotation(xyz)[degrees]: {} {} {}'.format(*angle_err))
print('Rotation(Total)[degrees]: {}'.format(angle_err))
print('Translation(xyz)[m]: {} {} {}'.format(*trans_err))
print('Translation(Total)[m]: {}'.format(trans_err_total))

f.write('Error\n')
f.write('Rotation(xyz)[degrees]: {} {} {}\n'.format(*angle_err))
f.write('Rotation(Total)[degrees]: {}\n'.format(angle_err_total))
f.write('Translation(xyz)[m]: {} {} {}\n'.format(*trans_err))
f.write('Translation(Total)[m]: {}\n'.format(trans_err_total))

f.close()