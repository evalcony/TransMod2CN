import utils


def comp(f1, f2, start_line):
    lines1 = utils.read_file(f1)
    lines2 = utils.read_file(f2)

    for i in range(len(lines1)):
        if i < start_line:
            continue
        l1 = lines1[i]
        l2 = lines2[i]

        if l1 == '' and l2 == '':
            continue
        if l1[0:1] != '@' and l2[0:1] != '@':
            continue

        if l1[:6] == l2[:6]:
            continue
        else:
            print('nubmer='+str(i))
            print(l1[:6])
            print(l2[:6])

            print(l1)
            print(l2)
            break
if __name__ == '__main__':
    comp('tra/dialog.tra', 'tra/dialog_sod_2.6.tra', 38830)
