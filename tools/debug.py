import sys

sys.path.append("..")
import utils
import main


def test_line(mode):
    line = "When asked about his past, SOLAUFEIN adds little beyond what you already know. As one of a small number of good Drow he will always be an outcast. Solaufein prefers not to speak of his old life in Ust Natha. The memory of the time he shared with Phaere before she was turned against him is too poignant and the memory of her eventual hatred and death is too cruel. Still, Solaufein will admit to being the leader of the Male Fighters' Guild in Ust Natha. He is also a magician of no small talent. When Phaere was taken from him he became a fervent (but secret) follower of Eilistraee Silverhair. He can be given to brooding melancholy."
    print('len='+str(len(line)))
    # 如果设置mode='debug'，则不会调用API，而且也会打印更详细的信息，而且不会有time.wait()
    solver = main.Solver(mode)
    res = solver.solve(line)
    print(res)

def comp():
    line = '@54137 = ~Ever pragmatic, ja? You look at your situation with such clear eyes. But Voghiln the Mighty is saddened at the sight of you.~ [BD54137]'
    en_target = 'Voghiln the Mighty'
    if line.lower().find(en_target.lower()) != -1:
        print(line)
    else:
        print('not find')

def print_token():
    solver = main.Solver()
    tup = solver.get_token()

def test_file(mode):
    file = 't1.tra'
    res = main.convert('tra/' + file, main.Solver(mode))
    for r in res:
        print(r)

def to_upper():
    lines = utils.read_dict('dict/word_dict.txt')
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

def single_sig_scan():
    lines = utils.read_file('output/sod_50_orig.tra')
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
    lines = utils.read_file('output/sod_50_orig.tra')
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

    # check()

    # comp()
    # print('test')
    files = utils.read_tras()
    print(files)