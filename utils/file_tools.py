

def getNewFile(file_path, add_name):
    file_hierarchy = file_path.rsplit('\\', 1)
    file_name = file_hierarchy[-1]
    name_hierarchy = file_name.split('.')
    print(file_name)

    new_name = '.'.join([name_hierarchy[0] + add_name] + name_hierarchy[1:])
    save_file = '\\'.join([file_hierarchy[0], new_name])
    return save_file

def editPlyScale(read_file, save_file, scale):
    f = open(save_file, 'w')
    is_header = True

    cnt = 0
    for line in open(read_file, 'r'):
        if is_header:
            write = line
            if line == 'end_header\n':
                is_header = False
        else:
            vals = line.split()
            if len(vals) == 3:
                if cnt % 2 == 0:
                    vals[0] = float(vals[0]) * scale
                    vals[1] = float(vals[1]) * scale
                    vals[2] = float(vals[2]) * scale
                cnt += 1
                write = '{} {} {}\n'.format(*vals)
            else:
                write = '{} {} {} {}\n'.format(*vals)
        f.write(write)
    f.close()