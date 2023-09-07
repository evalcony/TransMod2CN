import os
import re
import time

import utils
from youdao import YouDaoFanyi
from google import GoogleTrans

class Counter:
    def __init__(self, mode):
        self.cnt = 0
        self.mode = mode
    
    def wait(self):
        if self.mode == 'debug':
            return

        if self.cnt % 30 == 0:
            time.sleep(10)
        elif self.cnt % 10 == 0:
            time.sleep(5)
        elif self.cnt % 5 == 0:
            time.sleep(2)
        else:
            time.sleep(0.5)

    def incr(self):
        self.cnt += 1

class Solver:
    def __init__(self, mode):
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
        
        # 初始化ignore_dict
        self._init_ignore_dict()
        # 初始化word_dict，comp_word_dict, manul_trans_word_dict, name_dict
        self._init_word_dict()
        # 翻译器
        self.translator = self.get_translator()

        # 等待计数器
        self.counter = Counter(mode)

    def _init_ignore_dict(self):
        self.ignore_dict['lbs'] = ''
        self.ignore_dict['lb'] = ''
        self.ignore_dict['ft'] = ''

    def solve(self, line):

        # 替换占位符
        tup = self.token_replace(line)
        res = tup[0]
        flag = tup[1]

        print('token替换='+res)
        if res.strip() == '':
            return res

        # 一些容易引起翻译错误的，在这里手动翻译，不调用API接口
        # 是否手动翻译
        if flag:
            zh = res
        else:
            if self.mode == 'debug':
                # debug模式下不调用API
                zh = res
            else:
                # 翻译
                zh = self.translator.translate(res)
                # 计数器
                self.counter.incr()
            if self.mode == 'debug':
                print('翻译结果='+zh)
        # 占位符还原成字典值
        rev_back = self.set_token_back(zh)

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

    # word_dict, comp_word_dict, manual_trans_word_dict, name_dict
    # 因为共用 token, token_r
    def _init_word_dict(self):
        idx = 1
        idx = self._init_token(utils.read_file('word_dict.txt'), self.word_dict, idx)
        idx = self._init_token(utils.read_file('comp_word_dict.txt'), self.comp_word_dict, idx)
        idx = self._init_token(utils.read_file('manual_trans_word_dict.txt'), self.manual_trans_word_dict, idx)
        idx = self._init_token(utils.read_file('name_dict.txt'), self.name_dict, idx)
        
    def _init_token(self, lines, w_dict, idx):
        FIRST = 0
        SECOND = 1
        i = idx
        for l in lines:
            arr = l.split('#')
            w_dict[arr[FIRST]] = arr[SECOND]
            self.token[arr[FIRST]] = i
            self.token_r[str(i)] = arr[FIRST]
            i = i+1
        return i

    def token_replace(self, line):
        manul_trans_flag = False
        # 先检查不需要调用 API 的单词 manual_trans_word_dict
        for k,v in self.manual_trans_word_dict.items():
            if k in line:
                # 将key替换为value
                line = line.replace(k, v)
                manul_trans_flag = True

        # 如果不走API，那么在这里直接尽可能换完
        if manul_trans_flag:
            for k,v in self.comp_word_dict.items():
                if k in line:
                    line = line.replace(k, v)
            words = line.split(' ')
            for word in words:
                # 忽略单词
                if word in self.ignore_dict:
                    line = line.replace(word, '')
                    continue
                
                # 将word替换为key
                if word in self.word_dict:
                    line = line.replace(word, self.word_dict[word])
            # 替换name
            for w in words:
                w = self.word_clear(w)
                if w in self.name_dict:
                    line = line.replace(w, self.name_dict[w])
            return (line, True)

        # 如果这一行仅仅只有专有名词，则同样不走token替换
        if line in self.comp_word_dict:
            line = line.replace(line, self.comp_word_dict[line])
            return (line, True)

        # 检查符合单词 comp_word_dict，做 token 替换. 等翻译结束后，再替换回来
        for k,v in self.comp_word_dict.items():
            if k in line:
                # 将key替换为token占位符
                line = line.replace(k, self.get_token_val(k))

        # 检查普通单词 word_dict，做占位符token替换. 等翻译结束后，再替换回来
        words = line.split(' ')
        for word in words:
            word = self.word_clear(word)
            # 忽略单词
            if word in self.ignore_dict:
                line = line.replace(word, '')
                continue
            
            # 将word替换为token占位符
            if word in self.word_dict:
                line = line.replace(word, self.get_token_val(word))


        # 将name替换为token占位符
        words = line.split(' ')
        for w in words:
            w = self.word_clear(w)
            if w in self.name_dict:
                line = line.replace(w, self.get_token_val(w))

        return (line, False)

    # 去除词尾的一些符号
    def word_clear(self, word):
        if word.find('.') != -1:
            ws = word.split('.')
            return ws[0]
        if word.find(',') != -1:
            ws = word.split(',')
            return ws[0]
        if word.find('!') != -1:
            ws = word.split('!')
            return ws[0]
        return word

    def get_token_val(self, k):
        return self._make_token_val(self.token[k])

    def _make_token_val(self, int_v):
        return self.TOKEN_SIGNAL_L+str(int_v)+self.TOKEN_SIGNAL_R

    def set_token_back(self, line):
        if line == '\n' or line == ' ':
            return line
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
                if solver.mode == 'debug':
                    print('翻译str='+line[l+1:r])
                res.append(line[:l+1] + solver.solve(line[l+1:r]) + line[r:])
            else:
                # 在不同行
                res.append(line[:l+1] + solver.solve(line[l+1:]))
                j = i+1
                while (lines[j].find('~') == -1):
                    res.append(solver.solve(lines[j]))
                    j = j+1
                r = lines[j].find('~')
                if solver.mode == 'debug':
                    print('j:' + str(j) + ' r:' + str(r))
                res.append(solver.solve(lines[j][:r]) + lines[j][r:])
                i = j

    return res


def main():

    # solver
    solver = Solver(mode = '')

    files = os.listdir('tra/')
    for file in files:
        print(file)
        # 忽略setup.tra文件
        if file != 'SETUP.TRA':
            res = convert('tra/' + file, solver)
            for r in res:
                print(r)
        utils.write_file('', file, res, 'gb18030')

if __name__ == '__main__':
    main()
