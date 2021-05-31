import argparse
import glob
import numpy as np

import config as cf

def getNewFile(file_path, add_name):
    file_hierarchy = file_path.rsplit('\\', 1)
    file_name = file_hierarchy[-1]
    name_hierarchy = file_name.split('.')
    print(file_name)

    new_name = '.'.join([name_hierarchy[0] + add_name] + name_hierarchy[1:])
    save_file = '\\'.join([file_hierarchy[0], new_name])
    return save_file

def editPlyScale(read_file, save_file):
    f = open(save_file, 'w')
    is_header = True

    for line in open(read_file, 'r'):
        if is_header:
            write = line
            if line == 'end_header\n':
                is_header = False
        else:
            vals = line.split()
            vals[0] = float(vals[0]) / 1000
            vals[1] = float(vals[1]) / 1000
            vals[2] = float(vals[2]) / 1000
            write = '{} {} {} {} {} {}\n'.format(*vals)
        f.write(write)
    f.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='directory')
    args = parser.parse_args()

    directory = args.dir

    if not directory[0] == 'C':
        directory = cf.dir_save + directory

    read_files = sorted(glob.glob(directory + '/*.ply'))
    
    for read_file in read_files:
        save_file = getNewFile(read_file, '_[m]')
        editPlyScale(read_file, save_file)


if __name__ == '__main__':
    main()