import cv2
from cv2 import aruco
import numpy as np
import argparse

import os
import sys
import glob

import charuco
import config as cf

# Parser
parser = argparse.ArgumentParser()
parser.add_argument('name', help='folder name of images')
args = parser.parse_args()

dir_root = cf.dir_save + args.name + '/'
dir_realsense = dir_root + cf.dir_realsense
dir_kinect = dir_root + cf.dir_kinect
dir_calib = dir_root + cf.dir_calib

file_img = cf.save_image
num = cf.num_capture

os.makedirs(dir_calib, exist_ok=True)

# def readStereoImages(capture):
#     images_1 = []
#     images_2 = []
#     files_1 = []
#     files_2 = []

#     setting = cf.capture_stereo[capture]
#     cams = setting['cams']

#     folder_1 = dir_realsense + setting['dir']
#     folder_2 = dir_kinect + setting['dir']

#     for cam in cams: 
#         for idx in range(num):
#             file_1 = folder_1 + file_img.format(cam, idx)
#             file_2 = folder_2 + file_img.format(cam, idx)
#             img_1 = cv2.imread(file_1)
#             img_2 = cv2.imread(file_2)
#             images_1.append(img_1)
#             images_2.append(img_2)
#             files_1.append(file_1)
#             files_2.append(file_2)
    
#     return images_1,images_2,files_1,files_2

def readStereoImages(dir_1, dir_2, cam):
    images_1 = []
    images_2 = []
    files_1 = []
    files_2 = []

    for idx in range(num):
        file_1 = dir_1 + file_img.format(cam, idx)
        file_2 = dir_2 + file_img.format(cam, idx)
        img_1 = cv2.imread(file_1)
        img_2 = cv2.imread(file_2)
        images_1.append(img_1)
        images_2.append(img_2)
        files_1.append(file_1)
        files_2.append(file_2)
    
    return images_1,images_2,files_1,files_2

def readStereoImagesTwice(capture):
    setting = cf.capture_stereo[capture]
    cams = setting['cams']

    dir_1 = dir_realsense + setting['dir']
    dir_2 = dir_kinect + setting['dir']

    twice_stereo = []
    for cam in cams:
        twice_stereo.append(readStereoImages(dir_1, dir_2, cam))
    return twice_stereo

def getValidImages(images, index):
    valid_images = []
    for img, idx in zip(images, index):
        if idx:
            valid_images.append(img)
    return valid_images
def getValidStereoImages(images_1, images_2, index):
    valid_images_1 = []
    valid_images_2 = []
    for img_1, img_2, idx in zip(images_1, images_2, index):
        if idx:
            valid_images_1.append(img_1)
            valid_images_2.append(img_2)
    return valid_images_1, valid_images_2


def main():
    ar = charuco.Arco()

    for cap in [1, 2]:
        for j in range(2):
            twice_stereo = readStereoImagesTwice(cap)
            
            images_1,images_2,files_1,files_2 = twice_stereo[j]
            allCorners_1,allCorners_2,allIds_1,allIds_2,imsize,index = ar.read_chessboards_stereo(
                images_1,images_2,files_1,files_2
            )
            valid_img_1, valid_img_2 = getValidStereoImages(images_1, images_2, index)
            draw_img_1 = ar.draw_corner(valid_img_1, allCorners_1, allIds_1)
            draw_img_2 = ar.draw_corner(valid_img_2, allCorners_2, allIds_2)

            for i, img in enumerate(draw_img_1):
                cv2.imwrite(dir_calib + 'r_%d-%d_%d.png'%(cap, j, i), img)
            for i, img in enumerate(draw_img_2):
                cv2.imwrite(dir_calib + 'k_%d-%d_%d.png'%(cap, j, i), img)

    # images_1,images_2,files_1,files_2 = readStereoImages(2)
    # for i, img in enumerate(images_1):
    #     cv2.imwrite(dir_calib + '2-1-%d.png'%i, img)
    # for i, img in enumerate(images_2):
    #     cv2.imwrite(dir_calib + '2-2-%d.png'%i, img)

if __name__ == '__main__':
    main()