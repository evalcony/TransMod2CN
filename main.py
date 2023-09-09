import os
import re
import time
import random

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
            wait_time = self._1D10()+10
        elif self.cnt % 10 == 0:
            wait_time = self._1D6()+8
        elif self.cnt % 5 == 0:
            wait_time = self._1D6()
        else:
            wait_time = 1
        
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
        print('原文='+line)

        if line.strip() == '':
            print('')
            return line

        # 一些容易引起翻译错误的，在这里手动翻译，不调用API接口
        tup = self.direct_translate(line)
        res = tup[0]
        if tup[1]:
            print('直译='+res)
            print('')
            return res

        if res.strip() == '':
            print('')
            return res

        # token替换
        res = self.token_replace(res)
        print('token替换='+res)

        if self.mode == 'debug':
            # debug模式下不调用API
            zh = res
        else:
            # 调用API进行翻译
            zh = self.translator.translate(res)
            if self.mode == 'debug':
                print('API结果=' + zh)
            # 计数器
            self.counter.incr()

        # 占位符还原成字典值
        rev_back = self.set_token_back(zh)

        print('')

        # 等待，防止频繁调用报错
        self.counter.wait()

        return rev_back

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
        no_api_trans = False

        line = line.lower()

        # 如果这一行仅仅只有专有名词，则不走token替换
        if line in self.comp_word_dict:
            line = line.replace(line, self.comp_word_dict[line])
            return (line, True)

        # 检查不需要调用 API 的单词 manual_trans_word_dict
        for k,v in self.manual_trans_word_dict.items():
            if k in line:
                # 将key替换为value
                line = line.replace(k, v)
                no_api_trans = True

        # 如果不走API，那么在这里直接尽可能换完
        if no_api_trans:
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
                if w in self.name_dict:
                    line = line.replace(w, self.name_dict[w])

            return (line, True)

        return(line, False)

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
            if k in self.name_dict:
                line = line.replace(k, self.get_token_val(k))

        return line

    # 去除词尾的一些符号
    def word_clear(self, word):
        ele = ['.',',','!',':','?']
        for e in ele:
            if word.find(e) != -1:
                ws = word.split(e)
                return ws[0]
        return word

    def get_token_val(self, k):
        return self._make_token_val(self.token[k])

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
                print('[set_token_back]: m='+idx + ' k=' + k + ' v=' + v)
            line = line.replace(self._make_token_val(idx), v)

        if self.mode == 'debug':
            print('还原后：' + line)
        return line

def convert(filename, solver):
    
    # lines = utils.read_file(filename, 'cp936')
    lines = utils.read_file(filename)
    res = []
    j = -1
    for i in range(len(lines)):
        if i <= j:
            continue
        line = lines[i]

        l = line.find('~')
        if l != -1:
            flag = 1
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
                i = j

    return res


def main():

    # solver
    solver = Solver()

    files = os.listdir('tra/')
    for file in files:
        print(file)
        # 忽略setup.tra文件
        if file.lower() == 'setup.tra':
            continue

        if file.lower().endswith('.tra'):
            res = convert('tra/' + file, solver)
            for r in res:
                print(r)
            utils.write_file('', file, res, 'gb18030')
            print('')
            print('')
            print('-'*30)
            # 做一些单个文件翻译完成之后的工作 todo

if __name__ == '__main__':
    main()
