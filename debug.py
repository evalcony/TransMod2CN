import main
import utils


def test_line(mode):
    # line = "Wilson, I want to know why we're here. I never let anyone use some... bearomancy on me, taking the group away from Sendai and her enclave!"
    line = "Cornugon's Revenge +2"
    # 如果设置mode='debug'，则不会调用API，而且也会打印更详细的信息，而且不会有time.wait()
    res = main.Solver(mode).solve(line)
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

if __name__ == '__main__':
    # test_line(mode='')
    test_file(mode='debug')

    # to_upper()
