import main
import utils


# 翻译单文件
if __name__ == '__main__':
    file = 'total_t1.tra'
    res = main.convert('tra/'+file, main.Solver(''))
    for r in res:
        print(r)
    # utils.write_file('', file, res, 'gb18030')
    utils.write_file('', file, res)