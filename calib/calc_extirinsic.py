import numpy as np
from scipy.spatial.transform import Rotation as R
import sys

def getNewFile(file_path):
    file_hierarchy = file_path.rsplit('\\', 1)
    file_name = file_hierarchy[-1]
    new_name = 'new_extrinsic_param.txt'
    save_file = '\\'.join([file_hierarchy[0], new_name])
    return save_file

file_name = sys.argv[1]

devices = []
rt = []
cnt = 0
is_param = False

for line in open(file_name, 'r'):
    line = line.rstrip('\n')
    device = line.split('->')
    if len(device) == 2:
        devices.append(device)
    if cnt == 4:
        is_param = False
        cnt = 0
    elif line == 'RT:':
        is_param = True
    elif is_param:
        rt.append(line.split())
        cnt += 1
print(devices)
if devices[0][1] != devices[1][0]:
    raise Exception('ERROR: order of extrinsic params is NOT correct!')


rt1 = np.array(rt[:4], dtype=float)
rt2 = np.array(rt[4:], dtype=float)

device1 = devices[0][0]
device2 = devices[1][1]
rt12 = np.dot(rt2, rt1)
print(f'New extrinsic param: {device1} -> {device2}\n{rt12}')

# f = open(getNewFile(file_name), 'w')
f = open(file_name, 'a')

f.write(f'\n\n{device1}->{device2}\nRT:\n')
for line in rt12:
    f.write('{} {} {} {}\n'.format(*line))
f.close()

r = R.from_matrix(rt12[:3, :3])
print('Rotate [xyz]:', r.as_euler('xyz', degrees=True))