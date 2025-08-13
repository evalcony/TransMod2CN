import main
import utils
import time
import readlogs
import argparse

# 翻译单文件，但是是立即写入模式，翻译一行写入一行
# 避免因为API调用失败导致整个文件翻译无效的问题
def trans_and_write_append(filename, output_encoding='utf-8', line_num=0):
    print('*' * 20)
    start_time = time.time()
    lines = utils.read_file('tra/' + filename)
    solver = main.Solver('')
    solver.convert(lines, filename, line_num, output_encoding)
    end_time = time.time()
    print("[执行时间]", end_time - start_time, "seconds")

#翻译单文件
def single_trans(filename, log, output_encoding='utf-8', mode=''):
    print('*' * 20)
    start_time = time.time()
    # 先写log记录
    log.writelogs(filename)
    solver = main.Solver(mode)
    lines = utils.read_file('tra/'+filename)
    res = solver.batch_convert(lines, filename, output_encoding)

    for r in res:
        print(r)
    print('finish')
    end_time = time.time()
    print("[执行时间]", end_time - start_time, "seconds")

# 根据区间翻译
def range_trans(file_list, output_encoding='utf-8'):

    log = readlogs.ReadLogs()
    # 读取上次结束文件名
    tup = log.readlogs()
    lastfile = tup[0]
    line_num = tup[1]
    flg = False

    start_time = time.time()
    file_list.sort()
    for file in file_list:
        print(file)
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

def process(args):
    if args.ed == -1 or args.st == -1:
        exit()
    file_list = []
    for i in range(args.st, args.ed):
        file_list.append('dia_' + str(i) + '.tra')
    log = readlogs.ReadLogs()

    for file in file_list:
        if args.test:
            mode = 'debug'
        else:
            mode = ''
        single_trans(file, log, args.outfilecode, mode)
        if mode == '':
            waittime = 3 + main.Counter('')._1D10()
            print('等待' + str(waittime) + '秒')
            time.sleep(waittime)

def process_list(file_list):
    log = readlogs.ReadLogs()

    for file in file_list:
        single_trans(file, log)
        waittime = 3 + main.Counter('')._1D10()
        print('等待' + str(waittime) + '秒')
        time.sleep(waittime)

def generate_file_list():
    # file_list = ['dia_7.tra','dia_22.tra','dia_23.tra','dia_25.tra','dia_26.tra','dia_40.tra','dia_41.tra','dia_45.tra','dia_49.tra','dia_323.tra','dia_324.tra','dia_329.tra','dia_331.tra','dia_333.tra','dia_335.tra','dia_336.tra','dia_339.tra']
    # return file_list
    return []

if __name__ == '__main__':
    # file = 'dia_12.tra'
    # single_trans(file, log, 'gb18030')
    #
    parser = argparse.ArgumentParser()
    parser.add_argument('-st', type=int, default=-1, help='起始文件号')
    parser.add_argument('-ed', type=int, default=-1, help='终止文件号')
    parser.add_argument('-outfilecode', type=str, default='utf-8', help='输出文件编码')
    parser.add_argument('-test', action='store_true', default=False, help='测试模式')

    args = parser.parse_args()
    process(args)
    # process_list(generate_file_list())

# 临时1
# if __name__ == '__main__':
#     file = 'le#inter.tra'
#     log = readlogs.ReadLogs()
#     single_trans(file, log, 'utf-8')
#     log.done()

# # 临时2
# if __name__ == '__main__':
#     file_list = []
#     file_list.append('setup.tra')
#
#     range_trans(file_list, output_encoding='utf-8')

# 临时3 翻译指定目录下文件
# if __name__ == '__main__':
#     file_list = []
#     files = utils.read_tras()
#     for file in files:
#         if file.lower().find('.tra') != -1:
#             file_list.append(file)
#     range_trans(file_list, output_encoding='utf-8')