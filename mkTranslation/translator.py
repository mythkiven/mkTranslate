# -*- coding:utf-8 -*-
import os
import re
import sys
import json
import string
import requests
from mkTranslation.translate_google import mkGoogleTranslator
sys.path.append("..")

class mkTranslator(object):

    def get_file(self,path):
        if(not os.path.exists(path)):
            pathArray = path.split('/')
            fileName = pathArray[len(pathArray)-1]
            return os.path.join(os.path.abspath('.'),fileName)
        return path

    def translate_i18ns(self,dest,word,language):
        if(not language):
            return 'null'
        tlanguage ='translations.'+language
        uri = "https://i18ns.com/translate/_search"
        headers = {"Content-Type":"application/json","Authorization":"Basic aTE4bnM6KioqKioq","user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0"}
        body = json.dumps({"query": {"simple_query_string":{"query":word,"fields":[tlanguage],"minimum_should_match": "100%","default_operator": "AND","analyzer": "smartcn"}}}) 
        response = requests.post(url=uri,data=body,headers=headers,timeout=120)
        if response.status_code != 200 :
            return 'null'
        txd = []
        try:
            tx=json.loads(response.text,encoding="UTF-8")
            txd=tx['hits']['hits'][0]['_source']['translations']
        except Exception as e:
            return 'null'
        if(len(txd)>1):
            isExist = False
            for x in txd:
                if(language == x['lang']):
                    orit = json.dumps(x[language],ensure_ascii=False)
                    orit = orit.replace('[','').replace(']','').replace('"','')
                    if(word == orit):
                        isExist = True
            if(isExist):
                for x in txd:
                    if(dest == x['lang']):
                        print('use \'https://i18ns.com/\' translation '+word+' to '+x[dest][0] + ',others use google translation')
                        return x[dest][0]+''
        return 'null'

    def translate(self,word,destination,language):
        if(len(word)==0):
            return 'null'
        try:
            tx = self.translate_i18ns(destination,word,language)
            if(tx != 'null'):
                return tx
        except Exception as e:
            print('')
        return mkGoogleTranslator().translate(word, dest=destination).text

    def fix_tx(self,txt):
        print(txt)
        if(txt.find('% ld')!=-1 or txt.find('% @')!=-1):
            tsing = re.search(r'%\s*(@|ld)\s*/\s*%\s*(ld|@)',txt)
            if(tsing):
                tsing = tsing.group(0)
                txt = txt.replace(tsing,tsing.replace(' ',''))
        return txt

    def write_tx(self,oldfile,newfile,reg,creg,des,lan):
        f = open(oldfile)
        line = f.readline()
        txd = ''
        while line:
            line = line.replace('\n','')
            if(len(line)==0):
                line = f.readline()
                continue
            originLine = line
            print('original:'+originLine)
            line = re.findall(reg,line)
            if(len(line) and line[0]):
                txc = self.translate(line[0],des,lan)
                if(len(txc)):
                    originLine = re.sub(reg,creg.replace('content',txc), originLine)
                else:
                    print('translate fail:' + line)
            elif(reg==creg==r'text'):
                originLine = self.translate(originLine,des,lan)
            else:
                print('skip: '+originLine)
            originLine = self.fix_tx(originLine)
            print('translated:'+originLine)
            txd += originLine + '\n'
            print('-----')
            line = f.readline()
        f = open(newfile,'w+')
        f.write(txd)
        f.close()
    def translate_text(self,text, destination,language):
        print(mkGoogleTranslator().translate_text(text, dest=destination).text)
    def translate_doc(self,filepath, destination,language):
        filepath = self.get_file(filepath)
        pathArray = filepath.split('/')
        oldFileName = pathArray[len(pathArray)-1]
        fileType = oldFileName.split('.')[len(oldFileName.split('.'))-1]
        currentPath =  filepath.replace('/' + oldFileName,'') if len(pathArray)>2 else  os.path.abspath('.')
        newFile = os.path.join(currentPath, 'translate_'+destination+'_'+oldFileName)
        txd = ''
        print('translating..')

        # text
        if(fileType.lower() == 'text' or  fileType.lower() == 'txt'):
            self.write_tx(filepath,newFile,r"text",r"text",destination,language)
            print('translation completed')

        # oc:xx.string
        elif(fileType.lower() == 'strings'):
            self.write_tx(filepath,newFile,r"=\s*\"(.+?)\"\s*;",'="'+'content'+'";',destination,language)
            print('translation completed')
        # java:xx.xml
        elif(fileType.lower() == 'xml'):
            self.write_tx(filepath,newFile,r">\s*(.+?)\s*</string>",'>'+'content'+'</string>',destination,language)
            print('translation completed')
        else:
            f = open(filepath)
            line = f.readline()
            while line:
                if(len(line)):
                    txd += self.translate(line,destination,language)+'\n'
                line = f.readline()
            f.close()
            f = open(newFile,'w+')
            f.write(txd)
            f.close()
            print('translation completed')