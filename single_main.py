import main
import utils
import time

def trans(filename):
    res = main.convert('tra/' + filename, main.Solver(''))
    for r in res:
        print(r)
    # 翻译mod的 .tra 文件要采用这一种
    # 输出为 gb18030 字符集
    # utils.write_file('', file, res, 'gb18030')

    # 输出为 utf-8 字符集
    utils.write_file('', filename, res)

# 翻译单文件
if __name__ == '__main__':
    file = 'dia_9.tra'

    start_time = time.time()

    trans(file)

    end_time = time.time()
    print("[执行时间]", end_time - start_time, "seconds")