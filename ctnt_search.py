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

if __name__ == '__main__':
    file_list = []
    for i in range(700):
        file_list.append('output/done/dia_'+str(i)+'.tra')
    result = searcher(file_list, '维康妮娅·德维尔')
    write_result('_search.txt', result)
    print('任务完成')