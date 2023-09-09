import main
import utils
import time

#翻译单文件
def trans(filename):
    print('*' * 20)
    start_time = time.time()

    res = main.convert('tra/' + filename, main.Solver(''))
    for r in res:
        print(r)
    # 翻译mod的 .tra 文件要采用这一种
    # 输出为 gb18030 字符集
    # utils.write_file('', file, res, 'gb18030')

    # 输出为 utf-8 字符集
    utils.write_file('', filename, res)

    end_time = time.time()
    print("[执行时间]", end_time - start_time, "seconds")

# 根据区间翻译
def range_trans(file_list):
    print('')

    start_time = time.time()
    for file in file_list:
        trans(file)

    end_time = time.time()
    print("[总执行时间]", end_time - start_time, "seconds")


if __name__ == '__main__':
    # file = 'dia_12.tra'
    # trans(file)

    file_list = []
    for i in range(130, 140):
        file_list.append('dia_'+str(i)+'.tra')
    range_trans(file_list)