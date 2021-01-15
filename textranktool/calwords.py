import os
import codecs
import math
import operator
import json

def fun(filepath):  # 遍历文件夹中的所有文件，返回文件list
    arr = []
    for root, dirs, files in os.walk(filepath):
        for fn in files:
            arr.append(root+"/"+fn)
    return arr
def getridofsw(lis, swlist):  # 去除文章中的停用词
    afterswlis = []
    for i in lis:
        if str(i) in swlist:
            continue
        else:
            afterswlis.append(str(i))
    return afterswlis
def toword(txtlis):  # 将一片文章按照‘^’切割成词表，返回list
    wordlist = []
    alltxt = ''
    for i in txtlis:
        alltxt = alltxt+str(i)
    ridenter = alltxt.replace('\n', '')
    wordlist = ridenter.split('^')
    return wordlist
def read(path):  # 读取txt文件，并返回list
    f = open(path, encoding="utf8")
    data = []
    for line in f.readlines():
        if line.strip() == '':
            continue
        data.append(line)
    return data
def getstopword(path):  # 获取停用词表
    swlis = []
    for i in read(path):
        outsw = str(i).replace('\n', '')
        swlis.append(outsw)
    return swlis
def cal(lis):
    dic = {}
    jsonlist = []
    for word in lis:
        word = word.strip()
        if word == '':
            continue
        if word in dic:
            dic[word] += 1
        else:
            dic[word] = 1
    for key,value in dic.items():
        jdic = {}
        jdic['x'] = key
        jdic['value'] = value
        jdic['category'] = '0'
        jsonlist.append(jdic)
    jsonlist.sort(key = lambda x:x["value"],reverse=True)
    return jsonlist

def main():
    swpath = r'停用词表.txt'#停用词表路径
    swlist = getstopword(swpath)  # 获取停用词表列表

    filepath = r'corpus'
    filelist = fun(filepath)

    for i in filelist:
        afterswlis = getridofsw(toword(read(str(i))), swlist)  # 获取每一篇已经去除停用的词表
        jsonlist = cal(afterswlis)
        jsonstr = json.dumps(jsonlist, ensure_ascii=False, indent=4)
        f = codecs.open('./cal/'+i.split('/')[-1], 'w', 'utf8')
        f.write(jsonstr)
        f.close()
    

if __name__ == '__main__':
    main()