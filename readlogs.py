import utils
class ReadLogs:
    def readlogs(self):
        lines = utils.read_file('readlogs.txt')
        if len(lines) > 0:
            # 如果以 done 结尾，表示上一次成功执行完成，下次执行时，相当于从新开始执行
            # filename|line_number
            if lines[-1] == 'done':
                return ('','0')
            args = lines[-1].split('|')
            return (args[0], args[1])
        return ('','0')

    def writelogs(self, file, line_num=0):
        lines = []
        lines.append(file+'|'+str(line_num))
        utils.write_logs(lines)

    def done(self):
        lines = ['done']
        utils.write_logs(lines)

if __name__ == '__main__':
    a = '1|2|3'
    arr = a.split('|')
    for e in arr:
        print(e)