import argparse
import sys

sys.path.append("..")
import utils


# 搜索内容在诸文件中的出现位置，并支持将搜索结果导出为文件

class CtntInfo:

    # file：文件
    # pattern: 匹配特征字符串
    # line_num: 这个文件的行号
    # line: 这个文件中这一行的文本内容
    def __init__(self, file, pattern, line_num, line):
        self.file = file
        self.pattern = pattern
        self.line_num = line_num
        self.line = line

    def info(self):
        return self.file + '|' + self.pattern + '|' + str(self.line_num) + '|' + self.line
def searcher(file_list, ctnt):
    result = []
    for file in file_list:
        flines = utils.read_file(file)

        for i in range(len(flines)):
            pos = flines[i].lower().find(ctnt)
            if pos != -1:
                result.append(CtntInfo(file, ctnt, i, flines[i]))

    return result

def write_result(file, result):
    res = []
    for r in result:
        res.append(r.info())
    utils.write_file('', file, res)

def replace_by_search_result(file, target_str):
    sear_lines = utils.read_file(file)

    if len(sear_lines) == 0:
        return
    args = sear_lines[0].split('|')
    cur_file = args[0]
    source_lines = utils.read_file(cur_file)
    for line in sear_lines:
        args = line.split('|')
        if args[0] == cur_file:
            rep_lines(source_lines, args, target_str)
        else:
            # 写入文件
            f = cur_file.replace('output/','')
            utils.write_file('', f, source_lines)
            print('-' * 10)

            cur_file = args[0]
            source_lines = utils.read_file(cur_file)

            rep_lines(source_lines, args, target_str)

    f = cur_file.replace('output/', '')
    utils.write_file('', f, source_lines)

def rep_lines(source_lines, args, target_str):
    line_num = int(args[2])
    # 完成替换
    print(source_lines[line_num])
    source_lines[line_num] = source_lines[line_num].lower().replace(args[1].lower(), target_str)
    print(source_lines[line_num])

def manage(args):
    if args.s != '':
        param = args.s.lower()
        print('[搜索目标字符]' + param)

        path_prefix = 'output'
        if args.p != '':
            path_prefix = args.p
        # 文件列表
        file_list = all_files(path_prefix)

        # 不区分大小写
        result = searcher(file_list, param)
        write_result('search.txt', result)
        print('任务完成')
    elif args.r != '':
        param = args.r
        print('[替换目标字符]' + param)
        replace_by_search_result('output/search.txt', param)
        print('替换完成')
    elif args.d:
        replace_by_search_result('output/search.txt', '')
        print('替换完成')

# 构造文件名列表，就不需要每次都手动填了
def all_files(path_prefix):
    file_list = []
    for i in range(1, 96):
        file = path_prefix + '/sod_' + str(i) + '.tra'
        file_list.append(file)
    return file_list

# 用法
# python3 ctnt_search.py -s '目标字符串'   # 这会将结果输出到 search.txt中
# python3 ctnt_search.py -r '要替换的成的字符串' # 读取 search.txt文件内容，替换相应字符串
# python3 ctnt_serach.py -d # 将search.txt 中的搜索结果替换成''
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=str, default='', help='匹配字串')
    parser.add_argument('-r', type=str, default='', help='替换结果')
    parser.add_argument('-p', type=str, default='', help='搜索的路径')
    parser.add_argument('-d', action='store_true', help='删除字符串')
    args = parser.parse_args()

    manage(args)