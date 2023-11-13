import argparse
import sys

sys.path.append("..")
import utils


# 基于 ripgrep 工具实现的替换
# 1. 用 rg 搜索出结果，保存为 temp.txt 文件
# 2. 解析 temp.txt 文件，进行目标字符串替换

def work(filename, prefix, pattern, target):
    rg_lines = utils.read_file(filename)
    cur_file = ''
    source = []
    cur = 0
    for line in rg_lines:
        rg = line.split(":")
        fname = rg[0]
        fline = rg[1]

        if fname != cur_file:
            if cur_file != '':
                # 写入之前的文件
                utils.write_file('', cur_file, source)
                print()

            # 设置为当前文件
            cur_file = fname
            source = utils.read_file(prefix + cur_file)
            cur = cur+1

        print(line)

        for i in range(len(source)):
            s = source[i]
            if s == fline:
                ns = s.replace(pattern, target)
                source[i] = ns
                break

    utils.write_file('', cur_file, source)
    print()
    print('执行结束')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=str, default='', help='特征字符串')
    parser.add_argument('-r', type=str, default='', help='目标字符串')
    args = parser.parse_args()

    # 特征字符串
    string = args.s
    # 目标字符串
    replace = args.r

    # work('output/temp.txt', 'output/', '<charname>', '<CHARNAME>')
    work('output/temp.txt', 'output/', string, replace)