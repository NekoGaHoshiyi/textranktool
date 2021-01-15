#from stanfordcorenlp import StanfordCoreNLP
import jieba
import os



flist = os.listdir('./original')
count = 1
index = open('index.txt', 'w', encoding='utf-8')
for filename in flist:
    print(filename)
    with open('./original/'+filename,'r', encoding='utf-8') as news:
            while True:
                line = news.read().strip().replace('\n','')
                if line == '':
                    break
                #string = line.split('^')[1]
                splits = jieba.lcut(line)
                #title = line.split('^')[2]
                title = filename.replace('.txt','')
                index.write(str(count)+'\t\t'+title+'\n')
                with open('./corpus/corpus'+str(count)+'.txt','w', encoding='utf-8') as newssplit:
                    newssplit.write('^'.join(splits)+'\n')
                count += 1
    #break