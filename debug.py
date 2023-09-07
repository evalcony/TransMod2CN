import main
import utils

if __name__ == '__main__':
    file = 'QUEST3.TRA'
    res = main.convert('tra/'+file, main.Solver(mode = ''))
    for r in res:
        print(r)
    utils.write_file('', file, res, 'gb18030')    

    # line = "Wilson, I want to know why we're here. I never let anyone use some... bearomancy on me, taking the group away from Sendai and her enclave!"
    # # line = "Wilson, I want to know why we're here. I never let anyone use some... bearomancy on me"
    # res = main.Solver('').solve(line)
    # print(res)