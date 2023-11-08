import sys
import argparse

sys.path.append("..")
import utils

# 多版本、多文件文件比对
# 1. 文件缺失
# 2. 行缺失

def compare(dir_a, dir_b, mode):
    # 这里假定文件名都已经转换为小写
    file_list_a = utils.read_dir(dir_a)
    file_list_b = utils.read_dir(dir_b)
    res = []

    sa = set(file_list_a)
    sb = set(file_list_b)

    for file in sa:
        print(file)
        if file in sb:
            # 读取文件
            lines_a = utils.read_file(dir_a+'/'+file)
            lines_b = utils.read_file(dir_b+'/'+file)

            # 忽略空行、忽略注释
            lines_a = parse(lines_a)
            lines_b = parse(lines_b)
        else:
            lines_a = utils.read_file(dir_a+'/'+file)
            lines_b = []

        r = comp(lines_a, lines_b, mode)
        res.append(file)
        for k in r:
            res.append(k)
        res.append('-' * 20)


    for file in sb:
        if file not in sa:
            lines_a = []
            lines_b = utils.read_file(dir_b+'/'+file)
            lines_b = parse(lines_b)

            r = comp(lines_a, lines_b, mode)
            res.append(file)
            for k in r:
                res.append(k)
            res.append('')

    for r in res:
        print(r)
    utils.write_file('', 'version_comp.txt', res)


block_signal = False
def parse(lines):
    res = []
    global block_signal
    block_signal = False
    for line in lines:

        if ignore(line) or block_signal:
            continue
        res.append(line)
    return res

def ignore(line):
    l = line.strip()
    if l == '':
        return True
    if l.startswith('//'):
        return True
    global block_signal
    if l.startswith('/*'):
        block_signal = True
        if l.endswith('*/'):
            block_signal = False
        return True
    if l.endswith('*/'):
        block_signal = False
        return True
    return False

def comp(lines_a, lines_b, mode):
    res = []

    len_a = len(lines_a)
    len_b = len(lines_b)
    if len_a == 0 or len_b == 0:
        res.append(str(len_a) + ' ' + str(len_b))
        res.append('')
        return res

    res.append(str(len_a) + ' ' + str(len_b))
    res.append('')
    i = 0
    j = 0
    while (i < len_a and j < len_b):
        num_a = pick_num(lines_a[i])
        num_b = pick_num(lines_b[j])

        if num_a == -1 and num_b == -1:
            i = i + 1
            j = j + 1
            continue
        if num_a == -1 and num_b != -1:
            if mode == 'detail':
                res.append('[]')
                res.append(lines_b[j])
                res.append('')
            j = j+1
        if num_a != -1 and num_b == -1:
            if mode == 'detail':
                res.append(lines_a[i])
                res.append('[]')
                res.append('')
            i = i+1
        if num_a != -1 and num_b != -1:
            if num_a == num_b:
                i = i+1
                j = j+1
            elif num_a < num_b:
                if mode == 'detail':
                    res.append(lines_a[i])
                    res.append('[]')
                    res.append('')
                i = i+1
            elif num_a > num_b:
                if mode == 'detail':
                    res.append('[]')
                    res.append(lines_b[j])
                    res.append('')
                j = j+1

    while i >= len_a and j < len_b:
        if mode == 'detail':
            res.append('[]')
            res.append(lines_b[j])
            res.append('')
        j = j + 1
    while i < len_a and j >= len_b:
        if mode == 'detail':
            res.append(lines_a[i])
            res.append('[]')
            res.append('')
        i = i + 1

    return res



def pick_num(line):
    if line[0] == '@' and line.find('=') != -1:
        pa = line.find('=')
        num = line[1:pa]
        return int(num)
    return -1


# mode= simple, detail
# simple: 只展示总行数差异
# detail: 精细到行差异
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d1', type=str, default='', help='路径1')
    parser.add_argument('-d2', type=str, default='', help='路径2')
    parser.add_argument('-mode', type=str, default='', help='simple:简单模式 detail:详细模式')
    args = parser.parse_args()

    compare(args.d1, args.d2, args.mode)