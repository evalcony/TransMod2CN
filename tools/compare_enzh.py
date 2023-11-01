# 根据搜索词，比较同一个词在en/zh 的表达，并输出到文件
import argparse
import sys

sys.path.append("..")
import utils


def list_comp(en_target):
    result = []
    enzh = utils.get_enzh_files('output')
    zh_file_list = enzh[0]
    en_file_list = enzh[1]

    for i in range(len(en_file_list)):
        # print(i)
        compare(en_file_list[i], zh_file_list[i], en_target, result)

    utils.write_file('', 'compare.txt', result)
    print('执行结束')

def compare(en_file, zh_file, en_target, result):
    elines = utils.read_file(en_file)
    res = []
    for i in range(len(elines)):
        if elines[i].lower().find(en_target) != -1:
            res.append(i)

    if len(res) > 0:
        zlines = utils.read_file(zh_file)
        for i in res:
            result.append(en_file)
            result.append(elines[i])
            if len(zlines) > 0:
                result.append(zlines[i])
            else:
                result.append('缺失')
            result.append('----')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=str, default='', help='追加参数')
    args = parser.parse_args()

    if args.s != '':
        # 不区分大小写
        list_comp(args.s.lower())