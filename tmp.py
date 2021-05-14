import glob, os

for c in [2,3]:
    for i in range(10):
        os.rename('../captures/210430/kinect/cap2/kinect-rgb_%d-%d.png'%(c,i),
                    '../captures/210430/kinect/cap2/image_%d-%d.png'%(c,i))