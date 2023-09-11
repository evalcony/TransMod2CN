import argparse

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
def searcher(file_list, cnt):
    result = []
    for file in file_list:
        flines = utils.read_file(file)

        for i in range(len(flines)):
            pos = flines[i].find(cnt)
            if pos != -1:
                result.append(CtntInfo(file, cnt, i, flines[i]))

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

            cur_file = args[0]
            source_lines = utils.read_file(cur_file)

            rep_lines(source_lines, args, target_str)

    f = cur_file.replace('output/', '')
    utils.write_file('', f, source_lines)

def rep_lines(source_lines, args, target_str):
    line_num = int(args[2])
    # 完成替换
    print(source_lines[line_num])
    source_lines[line_num] = source_lines[line_num].replace(args[1], target_str)
    print(source_lines[line_num])
    print('-' * 10)

# def rep_by_line(file, line_num, target_str):
#     lines = utils.read_file(file)
#     lines[line_num] = target_str
#     file = file.repace('output/', '')
#     utils.write_file('', file, lines)

def manage(args):
    if args.p != '':
        file_list = []
        for i in range(850):
            file_list.append('output/done/dia_' + str(i) + '.tra')
        result = searcher(file_list, args.p)
        write_result('_search.txt', result)
        print('任务完成')
    elif args.repl != '':
        replace_by_search_result('output/_search.txt', args.repl)
        print('替换完成')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=str, default='', help='匹配字串')
    parser.add_argument('-repl', type=str, default='', help='替换结果')
    args = parser.parse_args()

    manage(args)