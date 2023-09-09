import main
import utils


def test_line():
    # line = "Wilson, I want to know why we're here. I never let anyone use some... bearomancy on me, taking the group away from Sendai and her enclave!"
    line = 'SORCERER: Like Mages, Sorcerers use their arcane might to cast offensive and defensive spells. Unlike Mages, Sorcerers learn their spells automatically and do not need to memorize specific spells each day.'

    # 如果设置mode='debug'，则不会调用API，而且也会打印更详细的信息，而且不会有time.wait()
    res = main.Solver(mode='debug').solve(line)
    print(res)

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
    test_line()

    # to_upper()
