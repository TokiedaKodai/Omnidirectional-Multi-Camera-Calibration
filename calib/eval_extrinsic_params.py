import numpy as np
from scipy.spatial.transform import Rotation as R
import sys

dire = sys.argv[1]

device_name = 'realsense'

out_file = dire + '/extrinsic_params.txt'
f = open(out_file, 'w')

rts = []

for i in range(3):
    i += 1
    d1 = i
    d2 = i%3 + 1

    d1_name = device_name + str(d1)
    d2_name = device_name + str(d2)

    file_name = dire + '/cam{}{}.txt'.format(d1, d2)
    f.write(f'{device_name}{d1}->{device_name}{d2}\nRT:\n')

    cnt = 0

    for line in open(file_name, 'r'):
        cnt += 1
        if cnt < 17:
            continue
        f.write(line)
        
        line = line.rstrip('\n')
        rts.append(line.split())
    f.write('\n')
    print(f'{device_name}{d1}->{device_name}{d2}')

rt12 = np.array(rts[:4], dtype=float)
rt23 = np.array(rts[4:8], dtype=float)
rt31 = np.array(rts[8:12], dtype=float)

rt123 = np.dot(rt23, rt12)
rt1231 = np.dot(rt31, rt123)

print(rt1231)

f.write(f'{device_name}1->{device_name}2->{device_name}3-{device_name}1\nRT:\n')
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