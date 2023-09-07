import main
import utils

if __name__ == '__main__':
    file = 'WILSONCHRONICLES.TRA'
    # res = main.convert('tra/'+file, main.Solver(mode = 'debug'))
    # for r in res:
    #     print(r)
    # utils.write_file('', file, res, 'gb18030')    

    line = "Casting Time: 1"
    res = main.Solver('debug').solve(line)
    print(res)