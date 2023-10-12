import main
import utils
import time
import readlogs

# 为合并SoD 定制

# 翻译单文件，但是是立即写入模式，翻译一行写入一行
# 避免因为API调用失败导致整个文件翻译无效的问题
def trans_and_write_append(filename, output_encoding, line_num=0):
    print('*' * 20)
    start_time = time.time()
    main.convert_and_write('tra/' + filename, main.Solver(''), line_num, output_encoding)
    end_time = time.time()
    print("[执行时间]", end_time - start_time, "seconds")

#翻译单文件
def single_trans(filename, log, output_encoding):
    print('*' * 20)
    start_time = time.time()
    # 先写log记录
    log.writelogs(filename)

    res = main.convert('tra/' + filename, main.Solver(''), 'utf-8')

    for r in res:
        print(r)
    # 输出为 output_encoding 字符集
    utils.write_file('', filename, res, output_encoding)

    end_time = time.time()
    print("[执行时间]", end_time - start_time, "seconds")

# 根据区间翻译
def range_trans(file_list, output_encoding):

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
            trans_and_write_append(file, output_encoding, int(line_num))
        else:
            trans_and_write_append(file, output_encoding)
    log.done()
    end_time = time.time()
    print("[总执行时间]", end_time - start_time, "seconds")



# if __name__ == '__main__':
#     # file = 'dia_12.tra'
#     # single_trans(file, log, 'gb18030')
#     #
#     file_list = []
#     for i in range(1, 9):
#         file_list.append('s'+str(i)+'.tra')
#     range_trans(file_list, 'utf-8')

# 临时1
# if __name__ == '__main__':
#     file = 'sola.tra'
#     log = readlogs.ReadLogs()
#     single_trans(file, log, 'gb18030')
#     log.done()

# 临时2
if __name__ == '__main__':
    file_list = []
    file_list.append('solae1.tra')
    file_list.append('solafoe.tra')
    file_list.append('solaint.tra')
    file_list.append('solasoa.tra')
    file_list.append('solatob.tra')
    file_list.append('solavamp.tra')

    range_trans(file_list, 'gb18030')