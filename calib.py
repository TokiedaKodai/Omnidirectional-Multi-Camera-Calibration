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
parser.add_argument('cam', type=int, help='camera number')
args = parser.parse_args()

dir_root = cf.dir_save + args.name + '/'
dir_calib = dir_root + cf.dir_calib
dir_detect_marker = dir_calib + cf.dir_detect_marker
dir_undist = dir_calib + cf.dir_undist

cam = args.cam

file_img = cf.save_image
num = cf.num_capture

def readImages(num):
    images = []
    for idx in range(num):
        img = cv2.imread(dir_root+file_img.format(cam, idx))
        images.append(img)
    return images

def getValidImages(images, index):
    valid_images = []
    valid_index = []
    for i, (img, idx) in enumerate(zip(images, index)):
        if idx:
            valid_images.append(img)
            valid_index.append(i)
    return valid_images,valid_index

def param2str(param):
    param = list(param)
    string=''
    for line in param:
        for num in line:
            string += str(num) + ','
        string += '\n'
    return string
def param2str2(param):
    param = list(param)
    string=''
    for line in param:
        for num in line:
            string += str(num[0]) + ','
        string += '\n'
    return string

def main():
    os.makedirs(dir_calib, exist_ok=True)
    os.makedirs(dir_detect_marker, exist_ok=True)
    os.makedirs(dir_undist, exist_ok=True)
    
    ar = charuco.Aruco()

    image_files = sorted(glob.glob(dir_root + '*.png'))
    img_num = len(image_files)
    print('Image num: ', img_num)
    images = readImages(img_num)

    allCorners,allIds,imsize,index = ar.read_chessboards(images)

    valid_images, valid_index = getValidImages(images, index)
    print(valid_index)

    draw_images = ar.draw_corner(valid_images, allCorners, allIds)
    for img, idx in zip(draw_images, valid_index):
        cv2.imwrite(dir_detect_marker+'detect_%d.png'%idx, img)

    results = ar.calibrate_camera(allCorners, allIds, imsize)
    ret, camera_matrix, distortion_coefficients, rotation_vectors, translation_vectors = results
    # print(images)
    # print(camera_matrix)
    # print(distortion_coefficients)
    undist_imgs = ar.undist_images(images, camera_matrix, distortion_coefficients)
    for idx, img in enumerate(undist_imgs):
        cv2.imwrite(dir_undist+'undist_%d.png'%idx, img)

    for param in [camera_matrix, distortion_coefficients, rotation_vectors, translation_vectors]:
        param = param2str(param)

    camera_matrix = param2str(camera_matrix)
    distortion_coefficients = param2str(distortion_coefficients)
    rotation_vectors = param2str2(rotation_vectors)
    translation_vectors = param2str2(translation_vectors)

    result_str = '''\
ret:
{ret}
camera matrix:
{cam}
distortion:
{dist}
rotation:
{rot}
translation:
{trans}
'''.format(ret=ret, cam=camera_matrix, dist=distortion_coefficients, rot=rotation_vectors, trans=translation_vectors)
    print(result_str)

    f = open(dir_calib+'calib.txt', 'w')
    f.write(result_str)
    f.close()

if __name__ == '__main__':
    main()