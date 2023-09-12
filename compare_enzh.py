# 根据搜索词，比较同一个词在en/zh 的表达，并输出到文件
import argparse

import utils


def list_comp(en_target):
    en_file_list = []
    zh_file_list = []
    result = []
    for i in range(3, 936):
        name = 'dia_'+str(i)+'.tra'
        en_file_list.append('tra/'+name)
        zh_file_list.append('output/done/'+name)

    for i in range(len(en_file_list)):
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