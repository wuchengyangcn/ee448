from json import loads
from time import time
import jieba

start = time()
stop_words = []
for line in open('stop_words.txt', encoding='utf_8').readlines():
    stop_words.append(line.strip())

num = 0
outfile = open('train_seg.txt', 'w')
for buffer in open('train.json', encoding='utf-8').readlines():
    line = ''
    for char in loads(buffer)['content']:
        if 19968 <= ord(char) <= 40869:
            line += char
    raw = list(jieba.cut(line, cut_all=False))
    temp = []
    for word in raw:
        if word not in stop_words:
            temp.append(word)
    outfile.write(' '.join(temp)+'\n')
    num += 1
    print(num)
outfile.close()

outfile = open('test_seg.txt', 'w')
for buffer in open('test.json', encoding='utf-8').readlines():
    line = ''
    for char in loads(buffer)['content']:
        if 19968 <= ord(char) <= 40869:
            line += char
    raw = list(jieba.cut(line, cut_all=False))
    temp = []
    for word in raw:
        if word not in stop_words:
            temp.append(word)
    outfile.write(' '.join(temp)+'\n')
outfile.close()

end = time()
print(end-start)
