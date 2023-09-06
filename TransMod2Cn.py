import hashlib
import requests
import uuid
import os
import time
import json

import utils

class YouDaoFanyi:
    def __init__(self):

        appconf = utils.read_config('appconf.ini')
        appconf['youdao']['appKey']
        appKey = appconf['youdao']['appKey']  # 应用id
        appSecret = appconf['youdao']['appSecret']  # 应用密钥

        self.YOUDAO_URL = 'https://openapi.youdao.com/api/'
        self.APP_KEY = appKey  # 应用id
        self.APP_SECRET = appSecret  # 应用密钥
        self.langFrom = 'en'  # 翻译前文字语言,auto为自动检查
        self.langTo = 'zh-CHS'  # 翻译后文字语言,auto为自动检查
        self.vocabId = "您的用户词表ID"

    def encrypt(self, signStr):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(signStr.encode('utf-8'))
        return hash_algorithm.hexdigest()

    def truncate(self, q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

    def do_request(self, data):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(self.YOUDAO_URL, data=data, headers=headers)

    def translate(self, q):
        data = {}
        data['from'] = self.langFrom
        data['to'] = self.langTo
        data['signType'] = 'v3'
        curtime = str(int(time.time()))
        data['curtime'] = curtime
        salt = str(uuid.uuid1())
        signStr = self.APP_KEY + self.truncate(q) + salt + curtime + self.APP_SECRET
        sign = self.encrypt(signStr)
        data['appKey'] = self.APP_KEY
        data['q'] = q
        data['salt'] = salt
        data['sign'] = sign
        data['vocabId'] = self.vocabId

        response = self.do_request(data)
        contentType = response.headers['Content-Type']
        result = json.loads(response.content.decode('utf-8'))['translation'][0]
        print(result)
        return result

def read_file(filename):
    lines = []
    root_dir = os.path.dirname(os.path.abspath(__file__))
    print('root_dir:' + root_dir)
    if not os.path.exists(root_dir+'/'+filename):
        print('file not exist')
        return []
    with open(root_dir+'/'+filename, 'r') as file:
        for line in file:
            lines.append(line.replace("\n",""))
    return lines

def write_file(prefix, finename, lines, encoding):
    print('写入文件:', finename)
    root_dir = os.path.dirname(os.path.abspath(__file__))
    path = root_dir+'/schinese/'
    # 防止路径不存在
    if not os.path.exists(path):
        os.makedirs(path)
    dir_file_path = path + '/' + prefix+finename
    if not os.path.exists(dir_file_path):
        open(dir_file_path, 'w').close()
    with open(dir_file_path, 'w', encoding=encoding) as f:
        for m in lines:
            f.write(m+'\n')

def default_words_dict():
    wd = dict()
    lines = read_file('default_words.txt')

    wd[','] = '，'
    wd['.'] = '。'
    wd['<CHARNAME>'] = '<CHARNAME>'
    wd['Roar'] = 'roar'
    wd['Snort'] = 'Snort'
    wd['rff'] = 'rff'
    wd['Grr'] = 'Grr'
    wd['Snuff'] = 'Snuff'
    wd['Groah'] = 'Groah'
    wd['Wilson'] = '威尔逊'



def convert(filename):
    lines = read_file(filename)
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
                zh = translator.translate(line[l+1:r])
                res.append(line[:l+1] + zh + line[r:])
            else:
                # 在不同行
                zh = translator.translate(line[l+1:])
                res.append(line[:l+1] + zh)
                j = i+1
                while (lines[j].find('~') == -1):
                    zh = translator.translate(lines[j])
                    res.append(zh)
                    j = j+1
                r = lines[j].find('~')
                zh = translator.translate(lines[j][:r])
                res.append(zh + line[j][r:])
                i = j
    return res

def get_translator():
    return YouDaoFanyi()

default_words_dict()

# translator = get_translator()

# filename = 'tra/' + 'L#WILC1.TRA'

# res = convert(filename)
# for r in res:
#     print(r)

# write_file('', filename, res, 'gb18030')
