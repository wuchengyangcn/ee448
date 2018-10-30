import pandas as pd
import numpy as np
import networkx as nx
test = pd.read_csv('test.csv')
graph = nx.DiGraph()
e2i = {}
i2e = {}
for line in open('train.csv', 'r').readlines()[1:]:
    head, relation, tail = line.strip().split(',')
    graph.add_edge(head, tail)
for line in open('entity2id.txt', 'r').readlines()[1:]:
    [u, v] = line.strip().split()
    e2i[u] = int(v)
    i2e[int(v)] = u
r2i = {}
for line in open('relation2id.txt', 'r').readlines()[1:]:
    [u, v] = line.strip().split()
    r2i[u] = int(v)
classes = {}
for line in open('constraint.txt', 'r'):
    [u, v] = line.strip().split()
    if int(v) not in classes:
        classes[int(v)] = [int(u)]
    else:
        if int(u) not in classes[int(v)]:
            classes[int(v)].append(int(u))
union = []
for temp in classes[0]:
    if temp not in union:
        union.append(temp)
for temp in classes[1]:
    if temp not in union:
        union.append(temp)
classes[0] = union
classes[1] = union
vectors = {}
embeddings = open('embeddings256.txt', 'r')
line = embeddings.readline().strip()
for line in embeddings:
    total = line.strip().split(' ')
    temp = []
    for i in total[1:]:
        temp.append(float(i))
    vectors[int(total[0])] = temp
embeddings.close()
result = open('results.csv', 'w')
result.write('QueryId,ExpectedTail'+'\n')
for i in range(len(test['QueryId'])):
    print(i)
    queryid, head, relation = test['QueryId'][i], e2i[test['Head'][i]], r2i[test['Relation'][i]]
    head_vec = vectors[head]
    dim = len(head_vec)
    min_distance = 30000
    distances = []
    for tail in classes[relation]:
        tail_vec = vectors[tail]
        temp = 0.0
        for element in range(dim):
            temp += (head_vec[element] - tail_vec[element]) * (head_vec[element] - tail_vec[element])
            # temp += abs(head_vec[element] - tail_vec[element])
        distances.append(temp)
    temp = np.array(distances)
    flags = []
    while len(flags) < 3:
        pos = np.argmin(temp)
        temp[pos] = 30000
        if not graph.has_edge(i2e[head], i2e[classes[relation][pos]]):
            flags.append(pos)
    result.write(str(queryid)+','+i2e[classes[relation][flags[0]]]+' '+i2e[classes[relation][flags[1]]]+' ' +
                 i2e[classes[relation][flags[2]]]+'\n')
result.close()
