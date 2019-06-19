# -*- coding: UTF-8 -*-
import hashlib
import random
import requests
import time


s = requests.Session()
m = hashlib.md5()

class Dict:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Referer': 'http://fanyi.youdao.com/',
            'contentType': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule&sessionFrom='
        self.base_config()

    def base_config(self):
        s.get('http://fanyi.youdao.com/')

    def translate(self):
        i = '你好'
        salf = str(int(time.time() * 1000) + random.randint(0, 9))
        n = 'fanyideskweb' + i + salf + "rY0D^0'nM0}g5Mm1z%1G4"
        m.update(n.encode('utf-8'))
        sign = m.hexdigest()
        data = {
            'i': i,
            'from': 'AUTO',
            'to': 'pt',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': salf,
            'sign': sign,
            'doctype': 'json',
            'version': "2.1",
            'keyfrom': "fanyi.web",
            'action': "FY_BY_DEFAULT",
            'typoResult': 'false'
        }
        resp = s.post(self.url, headers=self.headers, data=data)
        return resp.json()

dic = Dict()
resp = dic.translate()
print(resp)