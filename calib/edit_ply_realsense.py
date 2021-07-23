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

dir_save = cf.dir_save + args.name + '/'


def main():
    for dic in cf.dic_cams:
        directory = dir_save + dic['dir']
        read_files = sorted(glob.glob(directory + cf.dir_realsense + '*.ply'))
    
        for read_file in read_files:
            save_file = tool.getNewFile(read_file, '_[mm]')
            tool.editPlyScale(read_file, save_file, 1000)

        for i in range(2):
            with open(directory + cf.save_param.format('r' + str(dic['cams'][i]), 'k'), 'w') as f:
                f.write(cf.template_param)


if __name__ == '__main__':
    main()