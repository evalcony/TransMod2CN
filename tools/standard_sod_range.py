# 切分文件，并打印2.6.6.0版本SOD的中文范围，于是无需校对
import sys

sys.path.append("..")
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

def seperate_to_files(sod_lines, zh_lines, output):
    line_cnt = 0
    res1 = []
    res2 = []
    idx = 1
    zh = [0] * (len(zh_lines)+1)
    # '~' 出现次数
    r = 0
    # 非sod汉化行数
    nsod_num = 0
    # 写入当前文件标志
    write_flag = False
    analyse = []
    print('[total:]'+str(len(zh_lines)))

    # 中文、空行，zh[i]=1
    # 非中文、空行,zh[i] = 0
    for i in range(len(sod_lines)):
        l = sod_lines[i]
        if has_zh(l):
            zh[i] = 1
        if l.strip() == '':
            zh[i] = 1
        if l.find('placeholder') != -1:
            zh[i] = 1

    for i in range(len(zh_lines)):
        write_flag = False
        l = zh_lines[i]
        res1.append(l)
        res2.append(sod_lines[i])
        line_cnt += 1

        if zh[i] == 0:
            nsod_num += 1
        r += l.count('~')
        if line_cnt > 500 and r % 2 == 0 and l.count('~') > 0:
            analyse.append('[文件名:]' + 'sod_' + str(idx)+'.tra')
            analyse.append('[待校对行数:]' + str(nsod_num) + '/' + str(len(res1)))
            analyse.append('')

            utils.write_file('', 'sod_' + str(idx) + '.tra', res1)
            utils.write_file('', 'sod_' + str(idx) + '_orig.tra', res2)

            idx += 1
            res1 = []
            res2 = []
            line_cnt = 1
            r = 0
            nsod_num = 0
            write_flag = True
    if not write_flag:
        analyse.append('[文件名:]' + 'sod_' + str(idx) + '.tra')
        analyse.append('[待校对行数:]' + str(nsod_num) + '/' + str(len(res1)))

        utils.write_file('', 'sod_' + str(idx) + '.tra', res1)
        utils.write_file('', 'sod_' + str(idx) + '_orig.tra', res2)

    utils.write_file('', output, analyse)

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

def sub(line):
    if line.strip() == '':
        return ''
    upper = 6
    return line[:min(len(line), upper)]

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
    start_line = 48138
    seperate_to_files(
        # sod 2.6.6 基准文件（从0开始）
        takeout_text('../tra/dialog_sod_2.6.tra', start_line),
        # 汉化后的文件（从@33... 开始）
        takeout_text('../tra/dialog.tra', 0),
        'sod_tag.txt'
    )