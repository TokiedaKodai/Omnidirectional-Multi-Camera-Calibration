# Omnidirectional-Multi-Camera-Calibration
Calibration method of Omnidirectional Multi-camera whose scene has no overlap.

## Getting started
Environment : Ubuntu

Requirements
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

| Directory | Describe |
|:----------|:---------|
| capture   | Capture codes for RealSense and Kinect. |
| calib     | Caliblation codes. </br>Calcurate each extrinsic parameters between RealSense and Kinect. </br>Calcurate extrinsic parameters of omnidirectional multi-cameras. |
| reconst   | Reconstruct 3D point cloud and accumulate them. |
| utils     | Utility codes. |
| Captures  | Saving folder. |


### capture/
Capture codes for RealSense and Kinect.
- capture_realsense
- capture_kinect

### calib/


### utils/

- depth_tools
- parser
- file_tools

## Capture
### Folder
Example of saving name is '210715'.
```
Captures/
  └ 210715/
      ├ realsense/
      ├ kinect/
      └ calib/
```

## Tutorial
### Capture

### Extrinsic Parameters

