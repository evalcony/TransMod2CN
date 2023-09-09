import main
import utils


def test_line(mode):
    line = "That one's no better than Sarevok! "
    print('len='+str(len(line)))
    # 如果设置mode='debug'，则不会调用API，而且也会打印更详细的信息，而且不会有time.wait()
    solver = main.Solver(mode)
    res = solver.solve(line)
    print(res)

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

if __name__ == '__main__':
    test_line(mode='')
    # test_file(mode='debug')

    # to_upper()

    # de_blank('temp_dir/temp.txt')
