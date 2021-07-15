import os
import sys
import glob
import argparse

dir_current = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir_current)
sys.path.append('../')

import config as cf
from utils import file_tools as tool

os.chdir(dir_current)
###########################################################################################

# Parser
parser = argparse.ArgumentParser()
parser.add_argument('name', help='name of save dir')
args = parser.parse_args()

cam = args.cam
idx = args.idx
dir_save = cf.dir_save + args.name + '/'


def main():
    read_files = sorted(glob.glob(dir_save + 'cam12/' + cf.dir_kinect + '*.ply'))
    read_files += sorted(glob.glob(dir_save + 'cam13/' + cf.dir_kinect + '*.ply'))
    read_files += sorted(glob.glob(dir_save + 'cam23/' + cf.dir_kinect + '*.ply'))
    
    for read_file in read_files:
        save_file = tool.getNewFile(read_file, '_[m]')
        tool.editPlyScale(read_file, save_file, 0.001)


if __name__ == '__main__':
    main()