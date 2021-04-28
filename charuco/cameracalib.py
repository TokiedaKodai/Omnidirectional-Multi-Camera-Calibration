# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 14:04:10 2020

@author: genki
"""

import cv2
import numpy as np
import os
import sys
import json
import math
import glob


cam_folder = sys.argv[1]

cam_2d_point_file = cam_folder+"/point/cam2D%03d.txt"
cam_3d_point_file = cam_folder+"/point/cam3D%03d.txt"

cam_valid_id_file = cam_folder+"/point/cam_true_num.txt"

cam_image_file = cam_folder+"/cam/image%05d.png"
cam_image_folder = cam_folder+"/cam/"
cam_image_file_list = sorted(glob.glob(cam_image_folder+"*.png"))

cam_id_list = np.loadtxt(cam_valid_id_file)
print("cam valid id list")
print(cam_id_list)

valid_id_num =  cam_id_list.shape[0]
print("valid id number is ",valid_id_num)
print(cam_id_list[:valid_id_num])

cam_2d_point_list = []
cam_3d_point_list = []

cam_valid_id_list = []

for valid_id in range(valid_id_num):
    valid_image_id = cam_id_list[valid_id]
    cam_2d_point = np.loadtxt(cam_2d_point_file%valid_image_id,delimiter=" ")
    cam_3d_point = np.genfromtxt(cam_3d_point_file%valid_image_id,delimiter=" ")
    cam_2d_point = cam_2d_point[:,1:].astype("float64")
    cam_3d_point = cam_3d_point[:,1:4].astype("float64")
    cam_2d_point = np.reshape(cam_2d_point,[1,cam_2d_point.shape[0],2])
    cam_3d_point = np.reshape(cam_3d_point,[1,cam_3d_point.shape[0],3])
    
    cam_valid_id_list.append(valid_image_id)
    cam_2d_point = np.loadtxt(cam_2d_point_file%valid_image_id,delimiter=" ")
    cam_3d_point = np.genfromtxt(cam_3d_point_file%valid_image_id,delimiter=" ")
    cam_2d_point = cam_2d_point[:,1:].astype("float32")
    cam_3d_point = cam_3d_point[:,1:4].astype("float32")
    cam_2d_point_list.append(cam_2d_point)
    cam_3d_point_list.append(cam_3d_point)
        
        
    
    

print("calibrate calculation start")
cam_dist = np.zeros([8])
cam_k = np.zeros([3,3])
cam_rms, cam_k, cam_d, cam_r, cam_t =  cv2.calibrateCamera(cam_3d_point_list, cam_2d_point_list, (2000,1500),None,cam_dist
                                                                       , flags = cv2.CALIB_RATIONAL_MODEL)



cam_r = np.asarray(cam_r)
cam_t = np.asarray(cam_t)    

print("RMSE : ",cam_rms)
print("intrinsic params")
print(cam_k)
print("distortion params")
print(cam_d)
print("rotate params ",cam_r.shape)
#print(cam_r)
print("trans params ",cam_t.shape)
#print(cam_t)


reproj_folder = cam_folder+"/reproj"
undist_folder = cam_folder+"/undist"
param_folder = cam_folder+"/param"

if (os.path.exists(reproj_folder)==False):
	os.makedirs(reproj_folder)
if (os.path.exists(undist_folder)==False):
	os.makedirs(undist_folder)
if (os.path.exists(param_folder)==False):
	os.makedirs(param_folder)

param_folder = cam_folder+"/param"
np.savetxt(param_folder+"/cam_k.txt",cam_k,delimiter=" ")
np.savetxt(param_folder+"/cam_d.txt",cam_d,delimiter=" ")

cam_r = np.reshape(cam_r,[valid_id_num,3])
cam_t = np.reshape(cam_t,[valid_id_num,3])
np.savetxt(param_folder+"/cam_r.txt",cam_r,delimiter=" ")
np.savetxt(param_folder+"/cam_t.txt",cam_t,delimiter=" ")


reproj_image_file = cam_folder+"/reproj/image%03d.jpg"
undist_image_file = cam_folder+"/undist/image%03d.jpg"


mean_error = 0
tot_error = 0.0
total_point_num = 0
for i in range(len(cam_3d_point_list)):
    image_id = int(cam_valid_id_list[i])
    #print(cam_image_file%image_id)
    cam_image_file = cam_image_file_list[image_id]
    image = cv2.imread(cam_image_file,1)
    imgpoints2,_= cv2.projectPoints(cam_3d_point_list[i], cam_r[i], cam_t[i], cam_k, cam_d)
    #imgpoints2,_ = cv2.fisheye.projectPoints(cam_3d_point_list[i],cam_r[i],cam_t[i],cam_k,cam_d)
    #imgpoints2 = np.reshape(imgpoints2,[imgpoints2.shape[],2])
    #error = cv2.norm(cam_2d_point_list[i],np.reshape(imgpoints2,cam_2d_point_list[i].shape), cv2.NORM_L1)/len(imgpoints2)
    error = 0.0
    #print(cam_2d_point_list[i].shape)
    #print(imgpoints2.shape)
    imgpoints2 = np.reshape(imgpoints2,[imgpoints2.shape[0],2])
    for p_num in range((imgpoints2.shape[0])):
        tmp = imgpoints2[p_num] - cam_2d_point_list[i][p_num]
        #print(tmp)
        tmp = tmp[0]*tmp[0] + tmp[1]*tmp[1]
        error += tmp
        #print(cam_2d_point_list[i][0][p_num])
        image = cv2.circle(image,(int(cam_2d_point_list[i][p_num][0]),int(cam_2d_point_list[i][p_num][1])),5,
                   (0,255,0),2)
        image = cv2.circle(image,(int(imgpoints2[p_num][0]),int(imgpoints2[p_num][1])),5,
                   (0,0,255),2)
    #error = error / len(imgpoints2)
    total_point_num = total_point_num +cam_2d_point_list[i].shape[1]
    
    
    cv2.imwrite(reproj_image_file%image_id,image)
    
    tot_error += error
    print("cam ",image_id," : ",math.sqrt(error/len(imgpoints2)))#," ",len(imgpoints2)," ",cam_2d_point_list[i].shape[0])
print ("total error:" , math.sqrt(tot_error/total_point_num))

for i in range(cam_id_list.shape[0]):
    image_id = int(cam_id_list[i])
    
    image = cv2.imread(cam_image_file%i,1)
    
    
    image = cv2.undistort(image,cam_k,cam_d)
    cv2.imwrite(undist_image_file%image_id,image)
    


