import os
import sys

sys.path.append("..")
import utils

# 多版本、多文件文件比对
# 1. 文件缺失
# 2. 行缺失

class CompResult:
    def __init__(self):
        print()

def compare(dir_a, dir_b):
    file_list_a = utils.read_dir(dir_a)
    file_list_b = utils.read_dir(dir_b)

    res = []
    sa = set(file_list_a)
    sb = set(file_list_b)

    for file in sa:
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

        r = comp(lines_a, lines_b)
        res.append(file)
        for k in r:
            res.append(k)
        res.append('')

    for file in sb:
        if file not in sa:
            lines_a = []
            lines_b = utils.read_file(dir_b+'/'+file)
            lines_b = parse(lines_b)

            r = comp(lines_a, lines_b)
            res.append(file)
            for k in r:
                res.append(k)
            res.append('')

    for r in res:
        print(r)
    # utils.write_file('', 'version_comp.txt', res)


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
        return True
    if l.endswith('*/'):
        block_signal = False
        return True
    return False

def comp(lines_a, lines_b):
    len_a = len(lines_a)
    len_b = len(lines_b)
    # if len_a < len_b:
    #     min = len_a
    # else:
    #     min = len_b
    # for i in range(min):
    #     num_a = pick_num(lines_a[i])
    #     num_b = pick_num(lines_b[i])
    #     if num_a == num_b:
    #         continue
    #     if num_a == -1 and num_b == -1:
    #         # todo
    #         print('')
    #     if num_a == -1 and num_b != -1:
    #         # todo
    #         print('')

    res = []
    res.append(str(len_a) + ' ' + str(len_b))
    return res


def pick_num(line):
    if line[0] == '@' and line.find('=') != -1:
        pa = line.find('=')
        num = line[1:pa]
        return int(num)
    return -1


if __name__ == '__main__':
    # file_list_a = []
    # file_list_b = []
    # file_list_a.append('output/game_ee.tra')
    # file_list_a.append('output/game.tra')
    # file_list_a.append('output/weidu.tra')
    #
    # file_list_b.append('output_test/game_ee.tra')
    # file_list_b.append('output_test/game.tra')
    # file_list_b.append('output_test/weidu.tra')

    # root_dir = os.path.dirname(os.path.abspath(__file__))
    # path = root_dir + '/resource/' + utils.NAMESPACE
    # compare(path+'/output', path+'/output_test')
    compare('output_test1', 'output_test2')