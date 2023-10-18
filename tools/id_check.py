import sys

sys.path.append("..")
import utils


def work():
    en_file_list = []
    zh_file_list = []
    for i in range(1, 96):
        # 英文源文件
        en_file_list.append('output/orig/' + 'sod_' + str(i) + '_orig.tra')
        # 汉化文件
        zh_file_list.append('output/' + 'sod_' + str(i) + '.tra')

    res = []

    for i in range(len(zh_file_list)):
        zh_file = zh_file_list[i]
        en_file = en_file_list[i]

        zh_lines = utils.read_file(zh_file)
        en_lines = utils.read_file(en_file)

        if zh_lines[0].startswith('@'):
            z_r = zh_lines[0].split(' ')
            e_r = en_lines[0].split(' ')
            if z_r[0] != e_r[0]:
                print(zh_file)
                print(z_r[0])
                print(e_r[0])
                print('')
        if zh_lines[-1].startswith('@'):
            z_r = zh_lines[-1].split(' ')
            e_r = en_lines[-1].split(' ')
            if z_r[0] != e_r[0]:
                print(zh_file)
                print(z_r[0])
                print(e_r[0])

        res.append(zh_file)
        res.append(zh_lines[0])
        res.append(en_lines[0])
        res.append('')
        res.append(zh_lines[-1])
        res.append(en_lines[-1])
        res.append('-'*20)

    utils.write_file('', 'id_check.txt', res)
    print('校验完成')

# 用于进行文件的比对
# 比较2个文件的行首、行尾，确保两个文件的的范围一致
if __name__ == '__main__':
    work()