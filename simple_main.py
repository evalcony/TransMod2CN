import main
import utils


# 翻译单文件
if __name__ == '__main__':
    file = 'total_t1.tra'
    res = main.convert('tra/'+file, main.Solver(''))
    for r in res:
        print(r)
    # 翻译mod的 .tra 文件要采用这一种
    # 输出为 gb18030 字符集
    # utils.write_file('', file, res, 'gb18030')

    # 输出为 utf-8 字符集
    utils.write_file('', file, res)