import os
import re
import time
import random

import readlogs
import utils
from youdao import YouDaoFanyi
from google_trans import GoogleTrans

class Counter:
    def __init__(self, mode):
        self.cnt = 0
        self.mode = mode
    
    def wait(self):
        if self.mode == 'debug':
            return

        if self.cnt % 30 == 0:
            wait_time = self._1D10()+5
        elif self.cnt % 10 == 0:
            wait_time = self._1D6()+3
        elif self.cnt % 5 == 0:
            wait_time = self._1D6()
        else:
            wait_time = 0.8
        
        time.sleep(wait_time)
    
    def _1D10(self):
        return random.randint(1, 10)

    def _1D6(self):
        return random.randint(1, 6)

    def incr(self):
        self.cnt += 1

class Solver:
    def __init__(self, mode=''):
        self.mode = mode
        self.TOKEN_SIGNAL_L = '['
        self.TOKEN_SIGNAL_R = ']'
        # k, v
        self.word_dict = dict()
        # k, token_id
        self.token = dict()
        # token_id, k
        self.token_r = dict()
        # name字典
        self.name_dict = dict()
        # ignore字典 - 忽略指定单词
        self.ignore_dict = dict()
        # sp_word 在 manul_trans_word 词附近的词典，用作特定单词翻译。
        # 这部分词在日常用语和游戏环境用语中，有不同的翻译
        self.sp_word_dict = dict()

        # 复杂字典 k,v
        self.comp_word_dict = dict()
        # 不走API的单词字典, manul_trans_word_dict
        self.manual_trans_word_dict = dict()
        
        # 初始化word_dict，comp_word_dict, manul_trans_word_dict, name_dict, ignore_dict
        self._init_word_dict()
        # 翻译器
        self.translator = self.get_translator()

        # 等待计数器
        self.counter = Counter(mode)

    def solve(self, line):
        # print('[原文] '+line)

        # 忽略空行
        if line.strip() == '':
            return line

        # 如果没有需要翻译的部分，则忽略
        if has_zh(line):
            return line

        # 存档标志
        if line.find('000000') != -1:
            return line
        # 占位符标志
        if line == 'placeholder':
            return line

        # 去除text开头关于声音的标识
        line = self.off_voice(line)

        if line.strip() == '':
            print('')
            line = self.on_voice(line)
            return line

        # 一些容易引起翻译错误的，在这里手动翻译，不调用API接口
        tup = self.direct_translate(line)
        res = tup[0]
        if tup[1]:
            print('[直译] '+res)
            print('')
            # 回复声音的标识位
            res = self.on_voice(res)
            return res

        if res.strip() == '':
            print('')
            res = self.on_voice(res)
            return res

        # 替换token
        res = self.token_replace(res)
        print('[替换token] '+res)

        if self.mode == 'debug':
            # debug模式下不调用API
            zh = res
        else:
            # 调用API进行翻译
            zh = self.translator.translate(res)
            if self.mode == 'debug':
                print('[API结果] ' + zh)
            # 计数器
            self.counter.incr()

        # 占位符还原成字典值
        rev_back = self.set_token_back(zh)

        # 声音标识位还原
        rev_back = self.on_voice(rev_back)

        print('')

        # 等待，防止频繁调用报错
        self.counter.wait()

        return rev_back

    def on_voice(self, line):
        cache = self.voice_cache
        line = cache+line
        self.voice_cache = ''
        return line

    def off_voice(self, line):
        self.voice_cache = ''
        if line[0] == '[' and line.find(']') != -1:
            rp = line.find(']')
            v = line[0:rp+1]
            self.voice_cache = v
            line = line[rp+1:]
        return line

    def get_translator(self):
        use = utils.read_config('appconf.ini')['config']['use']
        if use == 'youdao':
            return YouDaoFanyi('en', 'zh-CHS')
        elif use == 'google':
            return GoogleTrans('auto', 'zh-CN')
        else:
            # 默认返回有道
            return YouDaoFanyi('en', 'zh-CHS')

    # word_dict, comp_word_dict, manual_trans_word_dict, name_dict，这几个字典的key实际存的都是小写
    # 因为共用 token, token_r
    def _init_word_dict(self):
        idx = 1
        idx = self._init_token(utils.read_file('dict/word_dict.txt'), self.word_dict, idx)
        idx = self._init_token(utils.read_file('dict/comp_word_dict.txt'), self.comp_word_dict, idx)
        idx = self._init_token(utils.read_file('dict/manual_trans_word_dict.txt'), self.manual_trans_word_dict, idx)
        idx = self._init_token(utils.read_file('dict/name_dict.txt'), self.name_dict, idx)
        idx = self._init_token(utils.read_file('dict/sp_word_dict.txt'), self.sp_word_dict, idx)

        # 初始化ignore_dict
        self.ignore_dict['lbs.'] = ''
        self.ignore_dict['lb.'] = ''
        self.ignore_dict['ft.'] = ''

    # key 全部转为小写存储和比较
    # 除了token_r 的value,作为翻译的value都不做任何改变
    def _init_token(self, lines, w_dict, idx):
        FIRST = 0
        SECOND = 1
        i = idx
        for l in lines:
            arr = l.split('#')
            key = arr[FIRST].lower()
            w_dict[key] = arr[SECOND]
            self.token[key] = i
            self.token_r[str(i)] = key
            i = i+1
        return i


    def direct_translate(self, line):
        line = line.lower()

        no_api_req = False

        # 如果这一行仅仅只有专有名词，则不走token替换
        if line in self.comp_word_dict:
            line = line.replace(line, self.comp_word_dict[line])
            no_api_req = True
            return (line, no_api_req)

        # 检查不需要调用 API 的单词 manual_trans_word_dict
        for k,v in self.manual_trans_word_dict.items():
            if k in line:
                no_api_req = True
                # 将key替换为value
                line = line.replace(k, v)
                # 在这个上下文，找相关的sp_word
                for sp in self.sp_word_dict:
                    if sp in line:
                        line = line.replace(sp, self.sp_word_dict[sp])
        if len(line) == 0:
            return (line, no_api_req)

        # 坑爹的符号，这2个不是同一个符号
        if (line[0] == '-' or line[0] == '–'):
            if len(line) < 10:
                print('[no_api_req]' + str(no_api_req))
                no_api_req = True
            # 在这个上下文，找相关的sp_word
            for sp in self.sp_word_dict:
                if sp in line:
                    line = line.replace(sp, self.sp_word_dict[sp])

        if no_api_req:
            # 如果不走API，那么在这里直接尽可能换完
            for k,v in self.comp_word_dict.items():
                if k in line:
                    line = line.replace(k, v)

            words = line.split(' ')
            for w in words:
                w = self.word_clear(w)
                # 需要忽略的单词
                if w in self.ignore_dict:
                    line = line.replace(w, '')
                    continue
                # 将w替换为key
                if w in self.word_dict:
                    line = line.replace(w, self.word_dict[w])

            # 替换name
            for w in self.name_dict:
                # 替换name
                if w in words:
                    line = line.replace(w, self.name_dict[w])

        return(line, no_api_req)

    # 做 token 替换. 等翻译结束后，再替换回来
    def token_replace(self, line):

        # 检查复合单词 comp_word_dict 并替换token
        for k,v in self.comp_word_dict.items():
            if k in line:
                line = line.replace(k, self.get_token_val(k))

        words = line.split(' ')

        # 这个要放在前面，因为数据清洗会洗掉单词末尾的.等字符，这里就会导致匹配失败
        # 下面这几个部分的顺序不能变，不然会导致一些翻译上的问题
        for k in self.ignore_dict:
            if k in words:
                line = line.replace(k, '')
                continue

        # 再对 words 做数据清洗，准备下面的正常匹配
        for i in range(len(words)):
            _w = self.word_clear(words[i])
            words[i] = _w

        # 匹配并替换为token
        # 之所以要用 dict 中的k去对line中的单词做匹配，因为dict中的单词匹配顺序是可以控制的，而line中无法控制，这就可能导致一些替换上的问题
        for k in self.word_dict:
            if k in words:
                line = line.replace(k, self.get_token_val(k))

        for k in self.name_dict:
            if k in words:
                line = line.replace(k, self.get_token_val(k))

        return line

    # 去除词尾的一些符号
    def word_clear(self, word):
        ele = ['.',',','!',':','?','\'s']
        for e in ele:
            if word.find(e) != -1:
                ws = word.split(e)
                return ws[0]
        return word

    def get_token_val(self, k):
        return self._make_token_val(self.token[k])

    def get_token(self):
        return (self.token, self.token_r)

    def _make_token_val(self, int_v):
        return self.TOKEN_SIGNAL_L+str(int_v)+self.TOKEN_SIGNAL_R

    def set_token_back(self, line):
        if line == '\n' or line == ' ':
            return line

        # 有时，有道翻译会把半角字符转成全角字符，造成匹配的问题。为了兼容这种情况，要把［］的全角字符转成半角[]
        if line.find('［') != -1:
            line = line.replace('［','[')
        if line.find('］') != -1:
            line = line.replace('］',']')
        if line.find('【') != -1:
            line = line.replace('【', '[')
        if line.find('】') != -1:
            line = line.replace('】', ']')

        # 例子：_7_10 _3_10
        pattern = r'\[(\d+)\]'
        matches = re.findall(pattern, line)
        for idx in matches:
            # 根据idx反向找到key, 即token_r[idx]
            k = self.token_r[idx]
            if k in self.word_dict:
                v = self.word_dict[k]
            elif k in self.comp_word_dict:
                v = self.comp_word_dict[k]
            elif k in self.manual_trans_word_dict:
                v = self.manual_trans_word_dict[k]
            elif k in self.name_dict:
                v = self.name_dict[k]
            else:
                v = ''
            if self.mode == 'debug':
                print('[set_token_back] m='+idx + ' k=' + k + ' v=' + v)
            line = line.replace(self._make_token_val(idx), v)

        if self.mode == 'debug':
            print('[还原后] ' + line)
        return line

def convert(filename, solver, encoding):
    
    lines = utils.read_file(filename, encoding)
    res = []
    j = -1
    for i in range(len(lines)):
        if i <= j:
            continue
        line = lines[i]

        l = line.find('~')
        if l != -1:
            r = line.find('~',l+1)
            if r != -1:
                # 在同一行
                res.append(line[:l+1] + solver.solve(line[l+1:r]) + line[r:])
            else:
                # 在不同行
                res.append(line[:l+1] + solver.solve(line[l+1:]))
                j = i+1
                while (lines[j].find('~') == -1):
                    res.append(solver.solve(lines[j]))
                    j = j+1
                r = lines[j].find('~')
                res.append(solver.solve(lines[j][:r]) + lines[j][r:])
    return res

# 翻译后立刻追加
def convert_and_write(input_file, solver, line_num, output_encoding='utf-8'):
    lines = utils.read_file(input_file)
    file_args = input_file.split('/')
    filename = file_args[-1]
    log = readlogs.ReadLogs()
    # output_encoding = 'gb18030'

    j = -1
    for i in range(len(lines)):
        if i < line_num:
            continue
        if i <= j:
            continue
        line = lines[i]

        # 忽略注释
        if line.startswith('//'):
            continue

        l = line.find('~')
        if l == -1:
            continue

        r = line.find('~', l+1)
        if r != -1:
            # 在同一行
            result = []
            res = line[:l+1] + solver.solve(line[l+1:r]) + line[r:]
            result.append(res)
            do_write_append(log, '', filename, result, output_encoding, i+1)
        else:
            # 在不同行
            result = []
            res = line[:l+1] + solver.solve(line[l+1:])
            result.append(res)
            j = i + 1
            while (lines[j].find('~') == -1):
                res = solver.solve(lines[j])
                result.append(res)
                j = j + 1
            r = lines[j].find('~')
            res = solver.solve(lines[j][:r]) + lines[j][r:]
            result.append(res)

            do_write_append(log, '', filename, result, output_encoding, j+1)

def has_zh(string):
    if string == '':
        return False
    for ch in string:
        if zh_signal(ch):
            return True
    return False

def zh_signal(ch):
    return '\u4e00' <= ch <= '\u9fff'

def do_write_append(log, prefix, filename, lines, encoding, next_line_num):
    for line in lines:
        print('[翻译]'+line)
    utils.write_line_in_append(prefix, filename, lines, encoding)
    log.writelogs(filename, next_line_num)

def main():

    # solver
    solver = Solver()
    log = readlogs.ReadLogs()

    # 读取上次结束文件名
    tup = log.readlogs()
    lastfile = tup[0]
    line_num = tup[1]


    flg = False

    files = os.listdir('tra/')
    for file in files:

        print(file)
        # 忽略setup.tra文件
        if file.lower() == 'setup.tra':
            continue

        if not flg and lastfile != '' and file != lastfile:
            print('pass ' + file)
            continue
        else:
            flg = True

        if file.lower().endswith('.tra'):
            # 先写log记录
            log.writelogs(file)

            res = convert('tra/' + file, solver, 'utf-8')
            for r in res:
                print(r)
            utils.write_file('', file, res, 'gb18030')
            print('')
            print('-'*30)

    log.done()


if __name__ == '__main__':
    main()
