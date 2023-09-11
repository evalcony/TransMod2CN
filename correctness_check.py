import argparse

import utils


# 检验切分文件的正确性
def correctness_check(file_list):
    result_file = []
    result = []
    for file in file_list:
        lines = utils.read_file(file)
        if len(lines) == 0:
            continue

        res = single_correctness_check(lines)

        result_file.append(file)
        result.append(res)

    for i in range(len(result_file)):
        if not result[i]:
            print(result_file[i] + ": " + str(result[i]))
    print('finish')

def single_correctness_check(lines):
    r = 0
    for l in lines:
        r += l.count('~')
    return r % 2 == 0

def single_file_correctness_check(file):
    file_list = []
    file_list.append(file)
    correctness_check(file_list)

def dispatcher(args):
    if args.a:
        # 文件正确性校验
        file_list = []
        for i in range(937):
            file_list.append('tra/' + 'dia_' + str(i) + '.tra')
        correctness_check(file_list)
    elif args.c != '':
        single_file_correctness_check(args.c)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=str, default='', help='校验指定文件')
    parser.add_argument('-a', action='store_true', help='校验全部文件')
    args = parser.parse_args()

    dispatcher(args)