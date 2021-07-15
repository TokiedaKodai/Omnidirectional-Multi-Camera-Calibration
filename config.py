#### Data
dir_save = '../Captures/'
dir_realsense = 'realsense/'
dir_kinect = 'kinect/'
dir_calib = 'calib/'

save_image = 'rgb_{}-{}.png'
save_depth = 'depth_{}-{}.bmp'
save_ply = 'ply_{}-{}.ply'
save_param = 'param_{}-{}.txt'
save_extrinsic_param = 'extrinsic_param.txt'

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

#### Kinect config
RGB_WIDTH = 1920
RGB_HEIGHT = 1080
DEPTH_WIDTH = 512
DEPTH_HEIGHT = 424

#### Calibration
dic_cams = [
    {
        'dir': 'cam12/',
        'cams': [1, 2]
        },
    {
        'dir': 'cam13/',
        'cams': [1, 3]
        },
    {
        'dir': 'cap3/',
        'cams': [2, 3]
        }
]
template_param = '''
0.00 0.00 0.00 0.00
0.00 0.00 0.00 0.00
0.00 0.00 0.00 0.00
0.00 0.00 0.00 1.00
'''




# #### Calibration
# dir_detect_marker = 'detect/'
# dir_undist = 'undist/'
# num_marker_x = 10
# num_marker_y = 7
# res_board_scale = 150
# res_board_x = num_marker_x * res_board_scale
# res_board_y = num_marker_y * res_board_scale
# marker_real_size = 20 # [mm]

# #### Capture Setting
# # Capture order and camera number for stereo capture
# capture_stereo = { 
#     1: {'dir': 'cap1/',
#         'cams': [1, 2]},
#     2: {'dir': 'cap2/',
#         'cams': [2, 3]},
#     3: {'dir': 'cap3/',
#         'cams': [3, 1]}
# }
# num_capture = 10
