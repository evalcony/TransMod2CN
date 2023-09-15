# 将多个文件合并

import sys

sys.path.append("..")
import utils


# 将 file_list 中的文件合并入 master 文件，然后输出为 output
# 依据每行开头的 @xxxx 进行合并，要求每个文件内的 @xxxx 保持有序。但是 file_list 并不要求有序，彼此独立。
# master: 主文件
# file_list: 合并文件
# output: 合并后的文件
def merge_multi_file(master, file_list, output):
    master_line = utils.read_file(master)
    file_encoding = 'utf-8'
    file_dict = dict()
    for file in file_list:
        file_lines = utils.read_file(file, file_encoding)
        file_dict[file] = file_lines
    master_line = replace_lines(master_line, file_dict)
    utils.write_file('', output, master_line, file_encoding)

def replace_lines(master_lines, file_dict):
    for file in file_dict:
        print(file)
        lines = file_dict[file]
        if len(lines) == 0:
            continue
        tup = range_file_lines(lines)

        # master_lines
        m_start = binsearch(master_lines, tup[0])
        m_end = binsearch(master_lines, tup[1])
        j = 0

        print(str(m_start) + ' ' + str(m_end))

        print(master_lines[m_start])
        print(master_lines[m_end])
        print('-'*10)

        # for i in range(m_start, m_end + 1):
        #     print(master_lines[i])
        # print('-----------------------')
        for i in range(m_start, m_end+1):
            master_lines[i] = lines[j]
            j += 1

        # for i in range(m_start, m_end + 1):
        #     print(master_lines[i])
        # print('%' * 20)
        # print('')

    return master_lines

def range_file_lines(lines):
    first = lines[0]
    j = -1
    while lines[j] == '':
        j = j-1
    end = lines[j]
    return (pick_order_number(first), pick_order_number(end))

def pick_order_number(line):
    p1 = line.find('@')
    if p1 == -1:
        return -1
    p2 = line.find(' ', p1+1)
    return line[p1+1:p2]

def binsearch(master_lines, order_num):
    l, r = 0, len(master_lines) - 1
    while l <= r:
        mid = (l + r) // 2
        m_order = pick_order_number(master_lines[mid])
        while m_order == -1:
            mid -= 1
        if int(m_order) == int(order_num):
            return mid
        elif int(m_order) < int(order_num):
            l = mid + 1
        else:
            r = mid - 1
    return -1

if __name__ == '__main__':
    files_list = []
    files_list.append('output/s' + str(1) + '.tra')
    # for i in range(1, 9):
    #     files_list.append('output/s_'+str(i)+'.tra')
    merge_multi_file('output/dialog_out.tra', files_list, 'dialog_merge.tra')