import utils
class ReadLogs:
    def readlogs(self):
        lines = utils.read_file('readlogs.txt')
        if len(lines) > 0:
            # 如果以 done 结尾，表示上一次成功执行完成，下次执行时，相当于从新开始执行
            if lines[-1] == 'done':
                return ''
            return lines[-1]
        return ''

    def writelogs(self, file):
        lines = []
        lines.append(file)
        utils.write_logs(lines)

    def done(self):
        lines = ['done']
        utils.write_logs(lines)