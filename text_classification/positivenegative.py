train = open('train_seg.txt', 'r', encoding='utf-8')
train_label = open('train.csv', 'r')
pos = open('pos.txt', 'w', encoding='utf-8')
neg = open('neg.txt', 'w', encoding='utf-8')
for buffer in train_label.readlines()[1:]:
    line = train.readline()
    if line:
        flag = int(buffer[-2])
        if flag == 1:
            pos.write(line)
        else:
            neg.write(line)
train.close()
train_label.close()
pos.close()
neg.close()