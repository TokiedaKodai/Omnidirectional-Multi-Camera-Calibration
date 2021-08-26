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

for dic in cf.dic_cams:
    directory = dir_save + dic['dir']

    rt = []
    for i in range(2):
        for line in open(directory + cf.save_param.format('r' + str(dic['cams'][i]), 'k'), 'r'):
            rt.append(line.split())

    rt1 = np.array(rt[:4], dtype=float)
    rt2 = np.array(rt[4:], dtype=float)

    r1 = rt1[:3, :3]
    t1 = rt1[:3, 3]
    r2 = rt2[:3, :3]
    t2 = rt2[:3, 3]

    r2 = np.linalg.inv(rt2[:3, :3])
    t2 = rt2[:3, 3] * -1
    rt2[:3, :3] = r2
    rt2[:3, 3] = t2

    rt12 = np.dot(rt2, rt1)

    print('extrinsic param: {} -> {}\n{}'.format(*dic['cams'], rt12))

    with open(directory + cf.save_param.format('r' + str(dic['cams'][0]), 'r' + str(dic['cams'][1])), 'w') as f:
        for line in rt12:
            f.write('{} {} {} {}\n'.format(*line))

        r = R.from_matrix(rt12[:3, :3])
        print('Rotate [xyz]:', r.as_euler('xyz', degrees=True))