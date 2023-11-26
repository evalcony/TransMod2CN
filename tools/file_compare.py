import sys
import argparse

sys.path.append("..")
import utils

# 单文件逐行比对


def build_lines1():
    line = """@232335 = ~[Hungarian translation credits]Eredeti Baldur Kapuja magyar fordításban részt vettek:

Duke<dukai@EUnet.yu>
SAM<gutasi@mailbox.hu>
KiPéTa<kipeta@netposta.net>
Bandar<berenjia@EUnet.yu>
Jocika<jocika@intermail.hu>
Szoke<szoke@inf.bme.hu>
Maminti<lovelylilac@hotmail.com>
Mr. Grent<Mr.Grent@buli.net>
Myotan<acanadi@ptt.yu>
Sforzan<vlaci@interware.hu>
Kubul<kubul@freemail.hu>
Frankeinstein<frankeinsteins@freemail.hu>
Ner'zhul<mszaszko@rmg.c3.hu>
jnc<jnc@magyaritasok.hu>
Rico<gabor.koroknai@hu.flextronics.com>
Panyi<panyi@magyaritasok.hu>
JoKeR<jokayel@axelero.hu>
Roberto és felesége

Baldur Kapuja: Javított Kiadás magyar fordításban részt vettek:

Roberto és felesége
Nemes<nemes.level@gmail.com>~
@232336 = ~[hungarian translation notes]valamint szeretnénk köszönetünket kifejezni mindenkinek, akik valamilyen formában segítettek a baldur kapuja eredeti vagy javított kiadásának magyarításában, de a fenti listában nem szerepelnek.~
@232337 = ~加入游戏~"""
    lines = line.split('\n')
    return lines

def build_lines2():
    line = """@232335 = ~[Hungarian translation credits]Eredeti Baldur Kapuja magyar fordításban részt vettek:

Duke<dukai@EUnet.yu>
SAM<gutasi@mailbox.hu>
KiPéTa<kipeta@netposta.net>
Bandar<berenjia@EUnet.yu>
Jocika<jocika@intermail.hu>
Szoke<szoke@inf.bme.hu>
Maminti<lovelylilac@hotmail.com>
Mr. Grent<Mr.Grent@buli.net>
Myotan<acanadi@ptt.yu>
Sforzan<vlaci@interware.hu>
Kubul<kubul@freemail.hu>
Frankeinstein<frankeinsteins@freemail.hu>
Ner'zhul<mszaszko@rmg.c3.hu>
jnc<jnc@magyaritasok.hu>
Rico<gabor.koroknai@hu.flextronics.com>
Panyi<panyi@magyaritasok.hu>
JoKeR<jokayel@axelero.hu>
Roberto és felesége

Baldur Kapuja: Javított Kiadás magyar fordításban részt vettek:

Roberto és felesége
Nemes<nemes.level@gmail.com>~
@232336 = ~[Hungarian translation notes]Valamint szeretnénk köszönetünket kifejezni mindenkinek, akik valamilyen formában segítettek a Baldur Kapuja eredeti vagy Javított Kiadásának magyarításában, de a fenti listában nem szerepelnek.~
@232337 = ~加入游戏~"""
    lines = line.split('\n')
    return lines


def comp(f1, f2, start_line_f1, start_line_f2):
    lines1 = utils.read_file(f1)
    lines2 = utils.read_file(f2)

    # lines1 = build_lines1()
    # lines2 = build_lines2()

    i = start_line_f1
    j = start_line_f2

    while i < len(lines1) and j < len(lines2):
        l1 = lines1[i]
        l2 = lines2[j]

        if l1 == '':
            i = i+1
            continue
        if l2 == '':
            j = j+1
            continue

        # 都有序号
        if l1[0:1] == '@' and l2[0:1] == '@':
            o1 = get_order(l1)
            o2 = get_order(l2)

            # 对比同序号内容
            if o1 == o2 and o1 != 'none':

                # 寻找i,j的上界
                i_ed = i+1
                j_ed = j + 1

                while i_ed < len(lines1) and lines1[i_ed].find('@') == -1:
                    i_ed = i_ed+1
                while j_ed < len(lines2) and lines2[j_ed].find('@') == -1:
                    j_ed = j_ed+1

                ii = i
                jj = j
                while ii < i_ed and jj < j_ed:
                    if lines1[ii] == '':
                        ii = ii+1
                        continue
                    if lines2[jj] == '':
                        jj = jj+1
                        continue
                    if lines1[ii] == lines2[jj]:
                        ii = ii+1
                        jj = jj+1
                        continue
                    else:
                        print('行号:' + str(ii) + ' ' + lines1[ii])
                        print('行号:' + str(jj) + ' ' + lines2[jj])
                        ii = ii+1
                        jj = jj+1
                if ii == i_ed:
                    while jj < j_ed:
                        print('行号:' + str(ii-1))
                        print('行号:' + str(jj) + ' ' + lines2[jj])
                        jj = jj+1
                else:
                    while ii < i_ed:
                        print('行号:' + str(ii) + ' ' + lines1[ii])
                        print('行号:' + str(jj-1))
                        ii = ii+1
                i = i_ed
                j = j_ed

            # 序号不同
            else:
                if int(o1) < int(o2):
                    print('行号：' + str(i) + ' ' + str(j) + ' 序号不同')
                    print(l1)
                    i = i+1
                else:
                    print('行号：' + str(i) + ' ' + str(j) + ' 序号不同')
                    print('        ' + l2)
                    j = j + 1

        # 如果有至少一个不为 id 内容
        else:
            if l1[0:1] == '@' and l2[0:1] != '@':
                print('行号:'+ str(i) + ' ' + str(j) + ' 序号不同')
                print(l1 + ' ' + l2)
                j = j+1
            elif l1[0:1] != '@' and l2[0:1] == '@':
                print('行号:' + str(i) + ' ' + str(j) + ' 序号不同')
                print(l1 + ' ' + l2)
                i = i+1
            else:
                if l1 != l2:
                    print('行号:' + str(i) + ' ' + str(j) + ' 不同')
                    print(l1 + ' ' + l2)
                    i = i+1
                    j = j+1
                else:
                    i = i + 1
                    j = j + 1

    if j != len(lines2):
        while j < len(lines2):
            print('    ' + lines2[j])
            j = j+1
    elif i != len(lines1):
        while i < len(lines1):
            print(lines1[i])
            i = i+1


def get_order(string):
    string = string.strip()
    if string[0:1] == '@':
        q = string.find(' ')
        return string[1:q]
    else:
        return 'none'


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f1', type=str, default='', help='文件f1')
    parser.add_argument('-f2', type=str, default='', help='文件f2')
    parser.add_argument('-s1', type=int, default='0', help='f1文件起始行')
    parser.add_argument('-s2', type=int, default='0', help='f2文件起始行')
    # parser.add_argument('-f', action='store_true', help='无追加参数')
    args = parser.parse_args()

    f1 = args.f1
    f2 = args.f2
    s1 = args.s1
    s2 = args.s2

    comp(f1, f2, s1, s2)


    # comp('sod-compare/sod_evalcony.tra', 'sod-compare/sod_master.tra', 48164, 48275)
    # comp('sod-compare/dialog_sod.tra', 'sod-compare/dialog_gb_1118.tra', 1, 48274)
    # comp('sod-compare/dialog_sod.tra', 'sod-compare/dialog_gb_1119.tra', 1, 48269)
    # comp('sod-compare/dialog_sod_orig.tra', 'sod-compare/dialog-m.tra', 48139, 48161)
    # comp('sod-compare/dialog_sod_orig.tra', 'sod-compare/dialog_sod.tra', 48139, 1)
    # comp('sod-compare/dialog_sod_orig.tra', 'sod-compare/dialog_gb_1118.tra', 48139, 48274)
    # comp('sod-compare/sod_evalcony.tra', 'sod-compare/sod_master.tra', 0, 0)

    # comp('sod-compare/dialog_en.tra', 'sod-compare/dialog_luxruay.tra', 48315, 48469)
    

    # comp('comp/bproxy.tra', 'comp/_bproxy.tra', 0, 0)
