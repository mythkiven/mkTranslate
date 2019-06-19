# -*- coding: UTF-8 -*-
import hashlib
import random
import requests
import time
import re
import sys
import os
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

PY3 = sys.version_info > (3, )
unicode = str if PY3 else unicode

s = requests.Session()
m = hashlib.md5()

class mkYouDaoTranslator(object):
    def __init__(self):
        self.headers2 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Referer': 'http://fanyi.youdao.com/',
            'contentType': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        self.headers1 = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0',
            'Origin': 'https://ai.youdao.com',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Referer': 'https://ai.youdao.com/product-fanyi.s',
            'contentType': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        self.url2 = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.url1 = 'https://aidemo.youdao.com/trans'

    def translate(self, text, dest, src):
        time.sleep(0.1)
        return self.trans1(text,dest,src)

    def trans1(self, text, dest, src):
        s.get('https://aidemo.youdao.com/trans')
        data1 = {
            'q': text,
            'from': 'Auto',
            'to': dest
        }
        resp = s.post(self.url1, headers=self.headers1, data=data1)
        try:
            if(resp.json()['translation']):
                return resp.json()['translation'][0]
        except:
            print('使用有道备用翻译通道2')
            return self.trans2(text,dest,src)

    def trans2(self, text, dest, src):
        s.get('http://fanyi.youdao.com/')
        salf = str(int(time.time() * 1000) + random.randint(0, 9))
        n = 'fanyideskweb' + text + salf + "rY0D^0'nM0}g5Mm1z%1G4"
        m.update(n.encode('utf-8'))
        sign = m.hexdigest()
        data2 = {
            'i': text,
            'from': 'AUTO',
            'to': dest,
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
        resp = s.post(self.url2, headers=self.headers2, data=data2)
        try:
            return resp.json()['translateResult'][0][0]['tgt']
        except:
            return self.trans3(text,dest,src)

    def trans3(self, text, dest, src):
        print('使用接口，仅支持中英互译,将翻译为英文')
        params = {
            'keyfrom': 'woodcol',
            'key': '1522180019',
            'type': 'data',
            'doctype': 'json',
            'version': '1.1',
            'q': text
        }
        try:
            r = requests.get('http://fanyi.youdao.com/openapi.do', params=params)
            r.raise_for_status()
            self.result = r.json()
            return self.result['translation'][0]
        except RequestException as e:
            print('有道免费接口遭遇封锁，请联系作者:https://github.com/mythkiven/mkTranslate')
            sys.exit()
