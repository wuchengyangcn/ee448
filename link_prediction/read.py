import pandas as pd
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')
train2id = open('train2id.txt', 'w')
entity2id = open('entity2id.txt', 'w')
relation2id = open('relation2id.txt', 'w')
test2id = open('test2id.txt', 'w')
entity = {}
relation = {}
for i in train['Head']:
    if i not in entity:
        entity[i] = len(entity.keys())
for i in train['Tail']:
    if i not in entity:
        entity[i] = len(entity.keys())
for i in train['Relation']:
    if i not in relation:
        relation[i] = len(relation.keys())
entity2id.write(str(len(entity))+'\n')
for i in entity.keys():
    entity2id.write(i+' '+str(entity[i])+'\n')
relation2id.write(str(len(relation))+'\n')
for i in relation.keys():
    relation2id.write(i+' '+str(relation[i])+'\n')
train2id.write(str(len(train['Head']))+'\n')
for i in range(len(train['Head'])):
    train2id.write(str(entity[train['Head'][i]])+' '+str(relation[train['Relation'][i]])+' '+str(entity[train['Tail'][i]])+'\n')
test2id.write(str(len(test['Head']))+'\n')
for i in range(len(test['Head'])):
    test2id.write(str(entity[test['Head'][i]])+' '+str(relation[test['Relation'][i]])+'\n')
train2id.close()
entity2id.close()
relation2id.close()
test2id.close()

edgelist = open('edgelist.txt', 'w')
constraint = open('constraint.txt', 'w')
for i in range(len(train['Head'])):
    edgelist.write(str(entity[train['Head'][i]])+' '+str(entity[train['Tail'][i]])+'\n')
    constraint.write(str(entity[train['Tail'][i]])+' '+str(relation[train['Relation'][i]])+'\n')
edgelist.close()
constraint.close()
