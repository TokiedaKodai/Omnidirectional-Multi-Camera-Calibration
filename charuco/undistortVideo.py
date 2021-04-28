# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 16:01:58 2020

@author: genki
"""

import cv2
import numpy as np
import os
import sys

print("argv[1] : input video file")
print("argv[2] : output video file")
print("argv[3] : intrinsic params")
print("argv[4] : distortion params")

input_video_file = sys.argv[1]
output_video_file = sys.argv[2]
cam_k_file = sys.argv[3]
cam_d_file = sys.argv[4]

print("argv[1] : input video file ",input_video_file)
print("argv[2] : output video file ",output_video_file)
print("argv[3] : intrinsic params ",cam_k_file)
print("argv[4] : distortion params ",cam_d_file)

#input video 
input_video = cv2.VideoCapture(input_video_file)


input_width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
input_height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
input_frame_count = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))
input_fps = input_video.get(cv2.CAP_PROP_FPS)

print(" ")
print("input video info")
print("input width ",input_width)
print("input height ",input_height)
print("input fps ",input_fps)
print("input frame total num ",input_frame_count)

cam_k = np.loadtxt(cam_k_file,delimiter=" ")
cam_d = np.loadtxt(cam_d_file,delimiter=" ")
cam_k = np.reshape(cam_k,[3,3])

print(" ")
print("cam k")
print(cam_k)
print("cam d")
print(cam_d)

fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
output_video = cv2.VideoWriter(output_video_file,fourcc,input_fps,(input_width,input_height))

ret,input_image = input_video.read()
img = input_image.copy()
new_cammat = cv2.getOptimalNewCameraMatrix(cam_k, cam_d, (img.shape[1], img.shape[0]), 1)[0]
map = cv2.initUndistortRectifyMap(cam_k, cam_d, np.eye(3), new_cammat, (img.shape[1], img.shape[0]), cv2.CV_32FC1)
np.savetxt("new_cammat.txt",new_cammat,delimiter=",")

for image_num in range(input_frame_count):
    ret,input_image = input_video.read()
    if (ret == False):
        continue

    input_image = input_image.astype('uint8')
    cv2.imshow("test",input_image)
    img = input_image.copy()
    #undist_image = cv2.undistort(input_image,cam_k,cam_d)
    undist_image = cv2.remap(img, map[0], map[1], cv2.INTER_AREA)
    output_video.write(undist_image)
    cv2.imshow("undist",undist_image)
    #print(undist_image.shape)
    cv2.waitKey(1)
    if (image_num%100==0):
        print(image_num,"/",input_frame_count)



input_video.release()
output_video.release()
cv2.destroyAllWindows()

