#/usr/bin/python 
# encoding:utf-8
# __Author__ = Slwhy

import requests
import time
import random
import hashlib
#i = "" + ((new Date).getTime() + parseInt(10 * Math.random(), 10))
i = str(int(time.time()*1000)+random.randint(1,10))
#o = n.md5("fanyideskweb" + t + i + "aNPG!!u6sesA>hBAW1@(-");
t = "please input the word you want to translate:"
u = 'fanyideskweb'
l = 'aNPG!!u6sesA>hBAW1@(-'
src = u + t + i + l    # u 与 l 是固定字符串，t是你要翻译的字符串，i是之前的时间戳
m2 = hashlib.md5()
m2.update(src)
str_sent = m2.hexdigest()

''' 
    i:number
    from:AUTO
    to:AUTO
    smartresult:dict
    client:fanyideskweb
    salt:1515462554510
    sign:32ea4a33c063d174a069959a5df1a115
    doctype:json
    version:2.1
    keyfrom:fanyi.web
    action:FY_BY_REALTIME
    typoResult:false
'''
head = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Content-Length':'200',
    'Connection':'keep-alive',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Host':'fanyi.youdao.com',
    'Origin':'http://fanyi.youdao.com',
    'Referer':'http://fanyi.youdao.com/',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest',
    # 'Cookie': 'YOUDAO_MOBILE_ACCESS_TYPE=1; OUTFOX_SEARCH_USER_ID=833904829@10.169.0.84; OUTFOX_SEARCH_USER_ID_NCOO=1846816080.1245883; fanyi-ad-id=39535; fanyi-ad-closed=1; JSESSIONID=aaaYuYbMKHEJQ7Hanizdw; ___rl__test__cookies=1515471316884'
}
head['Cookie'] = 'OUTFOX_SEARCH_USER_ID=833904829@10.169.0.84; OUTFOX_SEARCH_USER_ID_NCOO=1846816080.1245883;  ___rl__test__cookies='+str(time.time()*1000)
                 # '___rl__test__cookies=1515471316884'

data = {
    'i': t,
    'from':'AUTO',
    'to':'AUTO',
    'smartresult':'dict',
    'client':'fanyideskweb',
    'salt':i,
    'sign':str_sent,
    'doctype':'json',
    'version':'2.1',
    'keyfrom':'fanyi.web',
    'action':'FY_BY_REALTIME',
    'typoResult':'false'
}

s = requests.session()
url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
p = s.post(url,data= data,headers = head)
print(p.text)