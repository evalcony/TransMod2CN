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
        if True:
            return q
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
