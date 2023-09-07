import os
import re
import time

import utils
import youdao

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
        self.TOKEN_SIGNAL = '_'
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
        # 初始化word_dict，comp_word_dict, manul_trans_word_dict
        self._init_word_dict()
        # 初始化name_dict
        self._init_name_dict()
        # 翻译器
        self.translator = self.get_translator()

        # 等待计数器
        self.counter = Counter(mode)

    def _init_ignore_dict(self):
        self.ignore_dict['lbs.'] = ''
        self.ignore_dict['lb.'] = ''
        self.ignore_dict['ft.'] = ''
    
    # todo
    # def _init_manul_translate_token_dict(self):
    #     self.manul_translate_token_dict[]

    def solve(self, line):
        # 替换占位符
        tup = self.token_replace(line)
        res = tup[0]
        flag = tup[1]

        # 有道的翻译对中英文混杂的情况翻译不好，故只能放弃对中文名的提前替换
        # 替换name
        # res = self.replace_name(line)

        print('token替换='+res)
        if res.strip() == '':
            return res

        # 一些容易引起翻译错误的，在这里手动翻译，不调用API接口
        # 是否手动翻译
        if flag:
            zh = res
        else:
            # 翻译
            zh = self.translator.translate(res)
            if self.mode == 'debug':
                print('翻译结果='+zh)
        # 占位符还原成字典值
        rev_back = self.set_token_back(zh)

        # 等待，防止频繁调用报错
        self.counter.incr()
        self.counter.wait()

        return rev_back

    def get_translator(self):
        return youdao.YouDaoFanyi()

    # default_word_dict, comp_word_dict, manual_trans_word_dict
    # 因为共用 token, token_r
    def _init_word_dict(self):
        FIRST = 0
        SECOND = 1

        i = 1
        lines = utils.read_file('default_word_dict.txt')
        for l in lines:
            arr = l.split('#')
            self.word_dict[arr[FIRST]] = arr[SECOND]
            self.token[arr[FIRST]] = i
            self.token_r[str(i)] = arr[SECOND]
            i = i+1

        lines = utils.read_file('comp_word_dict.txt')
        for l in lines:
            arr = l.split('#')
            self.comp_word_dict[arr[FIRST]] = arr[SECOND]
            self.token[arr[FIRST]] = i
            self.token_r[str(i)] = arr[SECOND]
            i = i+1
        
        lines = utils.read_file('manual_trans_word_dict.txt')
        for l in lines:
            arr = l.split('#')
            self.manual_trans_word_dict[arr[FIRST]] = arr[SECOND]
            self.token[arr[FIRST]] = i
            self.token_r[str(i)] = arr[SECOND]
            i = i+1


    def _init_name_dict(self):
        lines = utils.read_file('name_dict.txt')
        i = 1
        for l in lines:
            arr = l.split('#')
            self.name_dict[arr[0]] = arr[1]

    def replace_name(self, line):
        for k,v in self.name_dict.items():
            if k in line:
                line = line.replace(k, v)
        return line

    def token_replace(self, line):
        manul_trans_flag = False
        # 先检查符合单词 manual_trans_word_dict token 替换. 等翻译结束后，再替换回来
        # 在这个字典中出现，则不走API
        for k,v in self.manual_trans_word_dict.items():
            if k in line:
                # 将key替换为token占位符
                line = line.replace(k, self.get_token_val(k))
                manul_trans_flag = True

        # 先检查符合单词 comp_word_dict，做 token 替换. 等翻译结束后，再替换回来
        for k,v in self.comp_word_dict.items():
            if k in line:
                # 将key替换为token占位符
                line = line.replace(k, self.get_token_val(k))

        # 再检查普通单词 word_dict，做占位符token替换. 等翻译结束后，再替换回来
        words = line.split(' ')
        for word in words:
            # 忽略单词
            if word in self.ignore_dict:
                line = line.replace(word, '')
                continue
            
            # 将word替换为token占位符
            if word in self.word_dict:
                line = line.replace(word, self.get_token_val(word))

        return (line, manul_trans_flag)

    def get_token_val(self, k):
        return self.TOKEN_SIGNAL+str(self.token[k])+self.TOKEN_SIGNAL

    def set_token_back(self, line):
        if line == '\n' or line == ' ':
            return line
        # 例子：_7_10 _3_10
        pattern = r'_(\d+)_'
        matches = re.findall(pattern, line)
        for m in matches:
            k = self.token_r[m]
            if k in self.word_dict:
                v = self.word_dict[k]
            elif k in self.comp_word_dict:
                v = self.comp_word_dict[k]
            elif k in self.manual_trans_word_dict:
                v = self.manual_trans_word_dict[k]
            else:
                v = ''
            if self.mode == 'debug':
                print('[set_token_back]: m='+m + ' k=' + k + ' v=' + v)
            line = line.replace(self.TOKEN_SIGNAL+m+self.TOKEN_SIGNAL, v)
            if self.mode == 'debug':
                print('还原后：' + line)
        return line

def convert(filename, solver):
    
    lines = utils.read_file(filename, 'cp936')
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
        if file != 'SETUP.TRA':
            res = convert('tra/' + file, solver)
            for r in res:
                print(r)
        utils.write_file('', file, res, 'gb18030')

if __name__ == '__main__':
    main()
