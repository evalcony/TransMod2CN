import main
import utils


# 翻译单文件
if __name__ == '__main__':
    file = 'SETUP.TRA'
    res = main.convert('tra/'+file, main.Solver())
    for r in res:
        print(r)
    utils.write_file('', file, res, 'gb18030') 