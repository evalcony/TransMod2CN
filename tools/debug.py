import main
import utils


def test_line(mode):
    line = "I heard about your talk with Voghiln, <CHARNAME>. Getting him to think about something other than wine and ale is a good idea. I've lost too many people to drink in my time. Anyway, I thought he might like to have these. What do you think?"
    print('len='+str(len(line)))
    # 如果设置mode='debug'，则不会调用API，而且也会打印更详细的信息，而且不会有time.wait()
    solver = main.Solver(mode)
    res = solver.solve(line)
    print(res)

def print_token():
    solver = main.Solver()
    tup = solver.get_token()

def test_file(mode):
    file = 't1.tra'
    res = main.convert('tra/' + file, main.Solver(mode))
    for r in res:
        print(r)

def to_upper():
    lines = utils.read_file('../dict/word_dict.txt')
    utils.to_upper(lines)

def word_clear(word):
    ele = ['.',',','!',':','?']
    for e in ele:
        if word.find(e) != -1:
            ws = word.split(e)
            return ws[0]
    return word

def de_blank(filename):
    lines = utils.read_file(filename)
    res = []
    for line in lines:
        if line != '':
            res.append(line.replace(' ', '#'))
    utils.write_file('', 'de_blank.txt', res)

def de_brackets(line):
    line = line.strip()
    p1 = line.find('[')
    p2 = line.find(']', p1 + 1)

    print(p1)
    print(p2)
    print(len(line))

    while (p2 != -1 and p2+1 != len(line)):
        line = line[:p1]+line[p2+1:]
        print(line)
        print('*'*10)

        p1 = line.find('[')
        p2 = line.find(']', p1 + 1)
        print(p1)
        print(p2)
        print(len(line))

    if p2 != -1:
        line = line[:p1] + line[p2 + 1:]
    return line

def parse_sod_tag_file():
    lines = utils.read_file('../output/sod_tag.txt')
    res = []
    info = ''
    for l in lines:
        if l == '':
            continue
        if l.find('文件名') != -1:
            p = l.find(']')
            info = l[p+1:]
        if l.find("待校对行数") != -1:
            p = l.find(']')
            score = l[p+1:]
            p2 = score.find('/')
            n = int(score[:p2])
            if n < 20:
                continue
            info += ' ' + score
            res.append(info)

    utils.write_file('', 'sod_tag_整理.txt', res)

def single_sig_scan():
    lines = utils.read_file('../output/sod_50_orig.tra')
    res = []
    for l in lines:
        if l.strip() == '':
            res.append('')
        else:
            res.append(str(l.count('~')) + '| ' + l)
            if l.count('~') != 2:
                print(l)
    utils.write_file('', 'test.txt', res)

def scan_reverse(start_point):
    lines = utils.read_file('../output/sod_50_orig.tra')
    res = []
    r_lines = list(reversed(lines))
    for i in range(len(r_lines)):
        if i < start_point:
            continue
        l = r_lines[i]
        if l.strip() == '':
            res.append('')
        else:
            res.append(str(l.count('~')) + '| ' + l)
            if l.count('~') != 2:
                print(l)
    utils.write_file('', 'scan_reverse.txt', res)


# 行尾是否对齐的校验
def check():
    for i in range(1, 96):
        lines1 = utils.read_file('output/sod_'+str(i)+'.tra')
        lines2 = utils.read_file('output/sod_'+str(i)+'_orig.tra')

        print('sod_'+str(i)+'.tra')
        print(lines1[-1])
        print(lines2[-1])
        print('')

if __name__ == '__main__':
    # test_line(mode='')
    # test_file(mode='debug')

    # to_upper()

    # de_blank('temp_dir/temp.txt')

    # print_token()

    # parse_sod_tag_file()

    # single_sig_scan()

    # scan_reverse(1)

    check()