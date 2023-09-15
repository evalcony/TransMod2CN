import sys

sys.path.append("..")
import utils


def single_seperate_to_file_test():

    zh_lines = utils.read_file('../output/sod_89.tra')
    sod_lines = utils.read_file('../output/sod_89_orig.tra')

    line_cnt = 0
    res1 = []
    idx = 1
    zh = ['0'] * (len(zh_lines) + 1)
    # '~' 出现次数
    r = 0
    # 非sod汉化行数
    nsod_num = 0
    # 写入当前文件标志
    write_flag = False
    print('[total:]' + str(len(zh_lines)))

    # 中文、空行，zh[i]=1
    # 非中文、空行,zh[i] = 0
    for i in range(len(sod_lines)):
        l = sod_lines[i]
        if has_zh(l):
            zh[i] = '1'
        if l.strip() == '':
            zh[i] = '1'
        if l.find('placeholder') != -1:
            zh[i] = '1'

    for i in range(len(zh_lines)):
        write_flag = False
        l = zh_lines[i]
        res1.append(l)
        line_cnt += 1

        if zh[i] == '0':
            nsod_num += 1
        r += l.count('~')
        if line_cnt > 500 and r % 2 == 0 and l.count('~') > 0:
            zh.append('[文件名:]' + 'sod_' + str(idx) + '.tra')
            zh.append('[待校对行数:]' + str(nsod_num) + '/' + str(len(res1)))
            zh.append('')

            utils.write_file('', 'sep_test_' + str(idx) + '_zh.tra', zh)
            utils.write_file('', 'sep_test_' + str(idx) + '.tra', res1)
            idx += 1
            res1 = []
            line_cnt = 1
            r = 0
            nsod_num = 0
            write_flag = True
        else:
            print(str(line_cnt) + '|'+str(r))
    if not write_flag:
        utils.write_file('', 'sep_test_' + str(idx) + '.tra', res1)

def has_zh(string):
    if string == '':
        return False
    for ch in string:
        if zh_signal(ch):
            return True
    return False

def zh_signal(ch):
    return '\u4e00' <= ch <= '\u9fff'

if __name__ == '__main__':
    single_seperate_to_file_test()