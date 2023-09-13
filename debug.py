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
    lines = utils.read_file('dict/word_dict.txt')
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

if __name__ == '__main__':
    # test_line(mode='')
    # test_file(mode='debug')

    # to_upper()

    # de_blank('temp_dir/temp.txt')

    # print_token()

    line = de_brackets('克拉兹战败后十天，你回到公爵府的房间，[aaa]思绪混乱。你想知道圣战军会对博德之门产生什么影响，却不知答案就在眼前......~ [bd65221]')
    print(line)