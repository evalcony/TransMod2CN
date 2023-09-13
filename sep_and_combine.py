import argparse

import utils

# 分离文件，和聚合文件
def takeout_text(filename, start_line=0):
    lines = utils.read_file(filename)
    res = []
    j = -1
    for i in range(len(lines)):
        if i < start_line:
            continue

        if i <= j:
            continue
        line = lines[i]

        l = line.find('~')
        if l != -1:
            r = line.find('~', l + 1)
            if r != -1:
                # 在同一行
                res.append(line[:l + 1] + (line[l + 1:r]) + line[r:])
            else:
                # 在不同行
                res.append(line[:l + 1] + (line[l + 1:]))
                j = i + 1
                while (lines[j].find('~') == -1):
                    res.append((lines[j]))
                    j = j + 1
                r = lines[j].find('~')
                res.append((lines[j][:r]) + lines[j][r:])
                i = j

    return res

def seperate_to_files(lines):
    line_cnt = 0
    res = []
    idx = 1
    # '~' 出现次数
    r = 0
    # 写入当前文件标志
    write_flag = False
    analyse = []
    print('[total:]'+str(len(lines)))
    for i in range(len(lines)):
        write_flag = False
        l = lines[i]
        res.append(l)
        line_cnt += 1

        r += l.count('~')
        if line_cnt > 50 and r % 2 == 0 and l.count('~') > 0:
            analyse.append('[文件名:]' + str(idx)+'.tra' + '  [~个数:]' + str(r) + ' [文件行数:]' + str(len(res)))
            analyse.append('[from:]' + res[0])
            analyse.append('[to:]' + res[-1])
            last = res[-1]
            last = de_brackets(last)
            last = last.strip()
            analyse.append('[是否由~结尾:]' + str(last.endswith('~')) + '|' + last)

            if l.count('~') > 2:
                analyse.append('[异常的~数量] [原文]'+l)
            analyse.append('*'*10)

            utils.write_file('', 'dia_' + str(idx) + '.tra', res)
            idx += 1
            res = []
            line_cnt = 1
            r = 0
            write_flag = True
    if not write_flag:
        utils.write_file('', 'dia_' + str(idx) + '.tra', res)

    utils.write_file('', 'analyse.txt', analyse)

def de_brackets(line):
    line = line.strip()
    p1 = line.find('[')
    p2 = line.find(']', p1 + 1)
    while (p2 != -1 and p2+1 != len(line)):
        line = line[:p1]+line[p2+1:]
        p1 = line.find('[')
        p2 = line.find(']', p1 + 1)

    if p2 != -1:
        line = line[:p1] + line[p2 + 1:]
    return line

def combine_to_file(file_list, output):
    res = []
    for file in file_list:
        lines = utils.read_file(file)
        for l in lines:
            res.append(l)

    utils.write_file('', output, res)

def manage(args):
    if args.s:
        # 文件切分
        start_line = args.f
        seperate_to_files(takeout_text('tra/dialog.tra', start_line))
    elif args.c:
        # 文件整合

        file_list = []
        file_list.append('output/0.tra')
        for i in range(1, args.up):
            file_list.append('output/done/dia_' + str(i) + '.tra')
        combine_to_file(file_list, 'dialog.tra')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', action='store_true', help='文件切分')
    parser.add_argument('-c', action='store_true', help='文件整合')
    parser.add_argument('-f', type=int, default=0, help='起始行数（从0开始）')
    parser.add_argument('-up', type=int, default=1, help='整合文件的文件id上界(必填)')
    args = parser.parse_args()

    manage(args)
