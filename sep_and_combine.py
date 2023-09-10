import utils

# 分离文件，和聚合文件
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

def seperate_to_files(lines):
    cnt = 1
    res = []
    idx = 1
    for l in lines:
        res.append(l)
        cnt += 1
        # 这个数值的设定不能太小，因为考虑到其中的单对话多段落的情况
        if cnt > 50 and l.find('~') != -1:
            # 要么以~作为收尾，要么有2个~。不然会引起 sovler 解析错误
            pos = l.find('~')
            if pos+1 <= len(l) or l[pos+1:].find('~') != -1:
                # 保存文件
                utils.write_file('', 'dia_'+str(idx)+'.tra', res)
                idx += 1
                res = []
                cnt = 1
    utils.write_file('', 'dia_' + str(idx) + '.tra', lines)

if __name__ == '__main__':
    file = 'total_t1.tra'
    res = takeout_text('tra/' + file)

    seperate_to_files(res)

