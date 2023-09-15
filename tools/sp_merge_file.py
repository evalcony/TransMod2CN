# 将多个文件合并
import sys

sys.path.append("..")
import utils


# 将 file_list 中的文件合并入 master 文件，然后输出为 output
# 依据每行开头的 @xxxx 进行合并，要求每个文件内的 @xxxx 保持有序。但是 file_list 并不要求有序，彼此独立。
# master: 主文件
# file_list: 合并文件
# output: 合并后的文件
def merge_multi_file(master, f2, output, f1_start, f2_start):
    file_encoding = 'utf-8'
    master_line = utils.read_file(master, file_encoding)
    file_lines = utils.read_file(f2, file_encoding)

    m1_lines = pick_from_start(master_line, f1_start)
    m2_lines = pick_from_start(file_lines, f2_start)

    m1_lines = replace_lines(m1_lines, m2_lines)
    utils.write_file('', output, m1_lines, file_encoding)

def pick_from_start(source, start):
    r = []
    for i in range(len(source)):
        if i < start:
            continue
        r.append(source[i])
    return r

def replace_lines(l1s, l2s):
    if len(l2s) == 0:
        return l1s
    len1 = len(l1s)
    len2 = len(l2s)
    p1 = 0
    p2 = 0

    res = []
    while p1 < len1 and p2 < len2:
        # 处理空格行
        if l1s[p1].strip() == '' and l2s[p2].strip() == '':
            p1 +=1
            p2 +=1
            continue
        if l1s[p1].strip() == '' and l2s[p2].strip() != '':
            p1 += 1
            continue
        if l1s[p1].strip() != '' and l2s[p2].strip() == '':
            p2 += 1
            continue

        if l1s[p1].find('=') != -1 and l2s[p2].find('=') != -1:
            n1 = int(pick_order_number(l1s[p1]))
            n2 = int(pick_order_number(l2s[p2]))
            if n1 != n2:
                res.append('error')
                res.append(l1s[p1])
                res.append(l2s[p2])
                res.append('p1=' + str(p1))
                res.append('p2=' + str(p2))
                break
        elif l1s[p1].find('=') != -1 and l2s[p2].find('=') == -1:
            res.append('error!')
            res.append(l1s[p1])
            res.append(l2s[p2])
            res.append('p1=' + str(p1))
            res.append('p2=' + str(p2))
            break
        elif l1s[p1].find('=') == -1 and l2s[p2].find('=') != -1:
            res.append('error!')
            res.append(l1s[p1])
            res.append(l2s[p2])
            res.append('p1=' + str(p1))
            res.append('p2=' + str(p2))
            break

        if has_zh(l2s[p2]):
            l1s[p1] = l2s[p2]

        p1 += 1
        p2 += 1

    utils.write_file('', 'sp_merge_result.txt', res)
    return l1s

# 不包括末尾空行的部分
def range_file_lines(lines):
    first = lines[0]
    j = -1
    while lines[j] == '':
        j = j-1
    end = lines[j]
    return (pick_order_number(first), pick_order_number(end))

def pick_order_number(line):
    d1 = line.find('@')
    d2 = line.find(' ', d1 + 1)
    return line[d1 + 1:d2]

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
    f1_start = 47089   #94882-47089=47793
    f2_start = 48138   #95833-48139=47694
    merge_multi_file(
        'tra/dialog.tra',
        'tra/dialog_sod_2.6.tra',
        'dialog_out.tra',
        f1_start,
        f2_start)
    print('执行结束')
