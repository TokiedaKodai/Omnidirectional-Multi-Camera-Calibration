# Omnidirectional-Multi-Camera-Calibration
Calibration method of Omnidirectional Multi-camera whose scene has no overlap.


<img width=50% src="images/overview.png" title="Overview">


## Camera setting

<img width=50% src="images/camera_setting.png" title="Setting">


## Getting started
Environment : Ubuntu

Requirements
- pyrealsense2
- pyfreenect2
- numpy
- scipy

## Directory
```
root/
  ├ capture/
  ├ calib/
  ├ utils/
  ├ reconst/
  ├ config.py
  |
  └ Captures/
```

| Directory | Description |
|:----------|:------------|
| capture   | Capture codes for RealSense and Kinect. |
| calib     | Caliblation codes. </br>Calcurate each extrinsic parameters between RealSense and Kinect. </br>Calcurate extrinsic parameters of omnidirectional multi-cameras. |
| reconst   | Reconstruct 3D point cloud and accumulate them. |
| utils     | Utility codes. |
| Captures  | Root save folder. |


### capture/
#### Options
capture_realsense.py
- save folder name
- camera number
- capture index (optional)

capture_kinect.py
- save folder name
- camera number
- capture index (optional)

### calib/
Calibration using PLY file by MeshLab.
> - calc_extrinsic.py
> - eval_extrinsic.py
> - edit_ply_realsense.py
> - edit_ply_kinect.py

### utils/
- depth_tools.py
- file_tools.py
- realsense_tools.py

## Tutorial
### Folder
In all capturing and calibration sessions, you shold use same folder name to save.
If you have 3 cameras to calibrate, sub-folder name shold be 'cam12', 'cam13', and 'cam23'.
Example of folder name is '210715'.
```
Captures/
  └ 210715/
      ├ cam12/
      |   ├ realsense/
      |   └ kinect/
      ├ cam13/
      |   ├ realsense/
      |   └ kinect/
      └ cam23/
          ├ realsense/
          └ kinect/
```

### Capture
Change directory to root/capture/.
```
cd capture
```

To calibrate RealSense 1 and 2, capture by RealSense 1 and Kinect, and then, capture by RealSense 2 and Kinect.

Capture the same object by RealSense 1 and Kinect.

Capture by RealSense 1 
```
python capture_realsense.py 210715/cam12 1
```

Capture by Kinect 
```
python capture_kinect.py 210715/cam12 1
```

Then, move the oject in scene of RealSense 2, capture in the same way.
```
python capture_realsense.py 210715/cam12 2
python capture_kinect.py 210715/cam12 2
```

Capture by RealSense 1 and 3, and Kinect.
```
python capture_realsense.py 210715/cam13 1
python capture_kinect.py 210715/cam13 1
python capture_realsense.py 210715/cam13 3
python capture_kinect.py 210715/cam13 3
```

Capture by RealSense 2 and 3, and Kinect.


### Extrinsic Parameters between RealSense and Kinect
Since the PLY file of RealSense is saved in metric units and the PLY file of Kinect is saved in millimeters, convert the file of RealSense to millimeters.
```
python edit_ply_realsense.py 210715
```



### Extrinsic Parameters between RealSense and RealSense

```
python calc_extrinsic.py 210715
```