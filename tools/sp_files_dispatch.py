
import sys

sys.path.append("..")
import utils


def parse_sod_tag_file():
    lines = utils.read_file('output/sod_tag.txt')
    res = []
    info = ''
    for l in lines:
        if l == '':
            continue
        if l.find('文件名') != -1:
            p = l.find(']')
            info = l[p+1:]
        if l.find("待校对行数") != -1:
            p = l.find(']')
            score = l[p+1:]
            p2 = score.find('/')
            n = int(score[:p2])
            info += ' ' + score
            res.append(info)

    utils.write_file('', 'sod_tag_整理.txt', res)

def dispatch(people_num):
    sod_tag_info = utils.read_file('output/sod_tag_整理.txt')
    file_name = []
    sod_num = []
    zh_num = []
    # 总量
    total_sod = 0
    total_zh = 0
    for i in range(len(sod_tag_info)):
        info = sod_tag_info[i]
        p1 = info.find(' ')
        p2 = info.find('/')
        num = int(info[p1+1:p2])
        t = int(info[p2+1:])
        file_name.append(info[:p1])
        total_sod += num
        sod_num.append(num)
        zh_num.append(t-num)
        total_zh += t-num

    POWER = 0.8

    # 平均
    np_average = (total_sod + total_zh) // people_num
    power_average = (total_sod + int(total_zh * POWER)) // people_num

    output_res = []

    r = 0
    job = 0
    j = 0

    for file_num in range(len(sod_tag_info)):
        if file_num < j:
            continue
        j = file_num
        p_person_total = 0
        np_person_total = 0
        while j < len(sod_tag_info) and p_person_total + sod_num[j] + zh_num[j]*POWER < power_average:
            p_single_file = sod_num[j] + int(zh_num[j] * POWER)
            np_single_file = sod_num[j] + zh_num[j]
            p_person_total += p_single_file
            np_person_total += np_single_file
            output_res.append('文件名:'+file_name[j]
                  + '英文:' + str(sod_num[j])
                  + ' 中文(加权):' + str(int(zh_num[j] * POWER))
                  + ' 中文:' + str(zh_num[j])
                  + ' 单文件总计(加权):' + str(p_single_file)
                  + ' 单文件总计:' + str(np_single_file)
                  )
            j += 1
        if j+1 < len(sod_tag_info):
            if p_person_total + sod_num[j] + zh_num[j]*POWER <= power_average * 1.05:
                p_single_file = sod_num[j] + int(zh_num[j] * POWER)
                np_single_file = sod_num[j] + zh_num[j]
                p_person_total += p_single_file
                np_person_total += np_single_file
                output_res.append('文件名:' + file_name[j]
                                  + '英文:' + str(sod_num[j])
                                  + ' 中文(加权):' + str(int(zh_num[j] * POWER))
                                  + ' 中文:' + str(zh_num[j])
                                  + ' 单文件总计(加权):' + str(p_single_file)
                                  + ' 单文件总计:' + str(np_single_file)
                )
                j += 1
        job += 1

        output_res.append('编号:' + str(job))
        output_res.append('个人工作量总计(加权):' + str(p_person_total))
        output_res.append('个人工作量总计:' + str(np_person_total))
        output_res.append('*'*10)
        output_res.append('')
        r += np_person_total


    output_res.append('原sod未汉化部分总计:' + str(total_sod))
    output_res.append('原sod已汉化部分总计:' + str(total_zh))
    output_res.append('每人工作量(加权平均):' + str(power_average))
    output_res.append('每人工作量(平均):' + str(np_average))
    output_res.append('加权系数' + str(POWER))
    output_res.append('总工作量:' + str(r))

    utils.write_file('', '工作量统计和分配.txt', output_res)


if __name__ == '__main__':
    parse_sod_tag_file()

    dispatch(8)