#### RealSense Config
ID_VENDOR_REALSENSE = 0x8086 # Intel
MANUFACTURER_REALSENSE = 'Intel(R) RealSense(TM)'
PRODUCT_REALSENSE = 'Intel(R) RealSense(TM)'

CAPTURE_WIDTH = 640
CAPTURE_HEIGHT = 480
CAPTURE_FPS = 30

CAMERA_1 = '816612061596'
CAMERA_2 = '821212060533'
CAMERA_3 = '816612061727'

#### Capture Setting

# Capture order and camera number for stereo capture
cap_1 = {
    'dir': 'cap1/',
    'cams': [1, 2]
}
cap_2 = {
    'dir': 'cap2/',
    'cams': [2, 3]
}
cap_3 = {
    'dir': 'cap3/',
    'cams': [3, 1]
}
capture_stereo = { 
    1: cap_1,
    2: cap_2,
    3: cap_3
}
num_capture = 10

#### Data
dir_save = '../captures/'
dir_realsense = 'realsense/'
dir_kinect = 'kinect/'
dir_calib = 'calib/'
dir_cap_1 = 'cap1/'
dir_cap_2 = 'cap2/'

save_image = 'image_{}-{}.png'
save_depth = 'depth_{}-{}.png'
