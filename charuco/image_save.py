# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 17:16:29 2020

@author: genki
"""

import os
import cv2
import numpy as np
import sys

print("argv[1] : input video file")
print("argv[2] : output image folder")
print("argv[3] : image sampling num")

input_video_file = sys.argv[1]
output_image_folder = sys.argv[2]
image_sampling_num = int(sys.argv[3])


print("argv[1] : input video file ",input_video_file)
print("argv[2] : output image file format ",output_image_folder)
print("argv[3] : image sampling num ",image_sampling_num)

input_video = cv2.VideoCapture(input_video_file)
total_video_frame = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))
print("total video frame : ",total_video_frame)

if (os.path.exists(output_image_folder)==False):
    os.makedirs(output_image_folder)

cur_image_num = 0

for i in range(total_video_frame):
    ret,image = input_video.read()
    print(i)
    
    if (ret == False):
        continue
    if (i%10 == 0):
        #image = image[:,252:252+1496]
        cv2.imwrite(output_image_folder+"/image%05d.png"%cur_image_num,image)
        cur_image_num += 1
        continue

    continue
    print("frame ",i)
   

    #cv2.imwrite("tmp/tmp.png",image)
    #image = cv2.imread("tmp/tmp.png",0)
    #image = image.astype('float32')
    #image = image[:,:,2]
    #det = cv2.split(image)
    #image = det[0]
    image = image.astype('uint8')
    cv2.imshow("image",image)
    k = cv2.waitKey(0)

    if k==32:
        cv2.imwrite(output_image_folder+"/image%05d.png"%cur_image_num,image)
        cur_image_num += 1
    else:
        continue

    #cv2.imwrite(output_image_file_format%(i/image_sampling_num),image)
cv2.destroyAllWindows()
input_video.release()
