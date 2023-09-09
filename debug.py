import main
import utils


def test_line(mode):
    # line = "Wilson, I want to know why we're here. I never let anyone use some... bearomancy on me, taking the group away from Sendai and her enclave!"
    line = "as the shaman casts this spell, energies gather together from the spirit world and form a pale blue sphere. the shaman can throw the sphere so that it explodes into a burst of ghostly, azure flames, which deliver 1d4 points of magic damage per level of the shaman (up to a maximum of 10d4). there is also a 33% chance that every enemy within the area of effect will be afflicted by the doom spell (-2 不利 to saving throws and attack rolls for 1 回合). a successful save vs. spell halves the damage and negates the doom effect. spirits, fey creatures, elementals, and spectral undead take double damage."
    # line = "It turns out Amnian diamond-water causes a terrible rash. I shall never take a traveling apothecary at his word again"
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
    test_line(mode='')
    # test_file(mode='')

    # to_upper()
