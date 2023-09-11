import main
import utils
import time
import readlogs


# 翻译单文件，但是是立即写入模式，翻译一行写入一行
# 避免因为API调用失败导致整个文件翻译无效的问题
def trans_and_write_append(filename, line_num=0):
    print('*' * 20)
    start_time = time.time()
    main.convert_and_write('tra/' + filename, main.Solver(''), line_num)
    end_time = time.time()
    print("[执行时间]", end_time - start_time, "seconds")

#翻译单文件
def single_trans(filename, log):
    print('*' * 20)
    start_time = time.time()
    # 先写log记录
    log.writelogs(filename)

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

    log = readlogs.ReadLogs()
    # 读取上次结束文件名
    tup = log.readlogs()
    lastfile = tup[0]
    line_num = tup[1]
    flg = False

    start_time = time.time()
    for file in file_list:
        if not flg and lastfile != '' and file != lastfile:
            print('pass ' + file)
            continue
        else:
            flg = True
        # 翻译
        # single_trans(file, log)
        if file == lastfile:
            trans_and_write_append(file, int(line_num))
        else:
            trans_and_write_append(file)
    log.done()
    end_time = time.time()
    print("[总执行时间]", end_time - start_time, "seconds")



if __name__ == '__main__':
    # file = 'dia_12.tra'
    # trans(file)
    #
    file_list = []
    for i in range(600, 700):
        file_list.append('dia_'+str(i)+'.tra')
    range_trans(file_list)
