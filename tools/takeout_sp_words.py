import utils

# 提前文件中的特殊单词 <word>

def takeout_text(filename):
    lines = utils.read_file(filename)
    res = []
    j = -1
    for i in range(len(lines)):
        if i <= j:
            continue
        line = lines[i]

        l = line.find('~')
        if l != -1:
            r = line.find('~', l + 1)
            if r != -1:
                # 在同一行
                res.append(line[l + 1:r])
            else:
                # 在不同行
                res.append(line[l + 1:])
                j = i + 1
                while (lines[j].find('~') == -1):
                    res.append(lines[j])
                    j = j + 1
                r = lines[j].find('~')
                res.append(lines[j][:r])
                i = j

    return res

if __name__ == '__main__':
    file = 't1.tra'
    res = takeout_text('tra/'+file)
    result = dict()
    for line in res:
        if line.find('<') != -1:
            lpos = line.find('<')
            rpos = line.find('>')
            w = line[lpos:rpos+1]
            # 去重
            result[w] = ''

    lines = []
    for k in result:
        lines.append(k+'#'+k)
    utils.write_file('', 'takeout_spl_words.txt', lines)
    print('执行完成')