import networkx as nx
import pandas as pd


class Model:
    def __init__(self):
        infile = pd.read_csv('train.csv')
        self.graph = nx.Graph()
        self.kind = {}
        for line in range(len(infile['Head'])):
            self.graph.add_edge(infile['Head'][line], infile['Tail'][line])
            if infile['Relation'][line] == 'work_in':
                self.kind[infile['Tail'][line]] = 'place'
                self.kind[infile['Head'][line]] = 'author'
            if infile['Relation'][line] == 'paper_publish_on':
                self.kind[infile['Tail'][line]] = 'conf'
                self.kind[infile['Head'][line]] = 'paper'
            if infile['Relation'][line] == 'paper_cit_paper':
                self.kind[infile['Tail'][line]] = 'paper'
                self.kind[infile['Head'][line]] = 'paper'
            if infile['Relation'][line] == 'field_is_part_of':
                self.kind[infile['Tail'][line]] = 'big'
                self.kind[infile['Head'][line]] = 'small'
            if infile['Relation'][line] == 'author_is_in_field':
                if infile['Tail'][line] not in self.kind:
                    self.kind[infile['Tail'][line]] = 'field'
                self.kind[infile['Head'][line]] = 'author'
            if infile['Relation'][line] == 'paper_is_in_field':
                if infile['Tail'][line] not in self.kind:
                    self.kind[infile['Tail'][line]] = 'field'
                self.kind[infile['Head'][line]] = 'paper'
            if infile['Relation'][line] == 'paper_is_written_by':
                self.kind[infile['Tail'][line]] = 'author'
                self.kind[infile['Head'][line]] = 'paper'
        self.place = [temp for temp in self.kind.keys() if self.kind[temp] == 'place']
        self.author = [temp for temp in self.kind.keys() if self.kind[temp] == 'author']
        self.conf = [temp for temp in self.kind.keys() if self.kind[temp] == 'conf']
        self.paper = [temp for temp in self.kind.keys() if self.kind[temp] == 'paper']
        self.big = [temp for temp in self.kind.keys() if self.kind[temp] == 'big']
        self.small = [temp for temp in self.kind.keys() if self.kind[temp] == 'small']
        self.field = [temp for temp in self.kind.keys() if self.kind[temp] == 'field']

    def get_place(self, nodes):
        result = {}
        for node in nodes:
            for neighbor in self.graph.neighbors(node):
                if self.kind[neighbor] == 'place':
                    if neighbor not in result:
                        result[neighbor] = 0
                    result[neighbor] += 1
        return result

    def get_conf(self, nodes):
        result = {}
        for node in nodes:
            for neighbor in self.graph.neighbors(node):
                if self.kind[neighbor] == 'conf':
                    if neighbor not in result:
                        result[neighbor] = 0
                    result[neighbor] += 1
        return result

    def get_author(self, nodes):
        result = {}
        for node in nodes:
            for neighbor in self.graph.neighbors(node):
                if self.kind[neighbor] == 'author':
                    if neighbor not in result:
                        result[neighbor] = 0
                    result[neighbor] += 1
        return result

    def get_paper(self, nodes):
        result = {}
        for node in nodes:
            for neighbor in self.graph.neighbors(node):
                if self.kind[neighbor] == 'paper':
                    if neighbor not in result:
                        result[neighbor] = 0
                    result[neighbor] += 1
        return result

    def get_big(self, nodes):
        result = {}
        for node in nodes:
            for neighbor in self.graph.neighbors(node):
                if self.kind[neighbor] == 'big':
                    if neighbor not in result:
                        result[neighbor] = 0
                    result[neighbor] += 1
        return result

    def get_field(self, nodes):
        result = {}
        for node in nodes:
            for neighbor in self.graph.neighbors(node):
                if self.kind[neighbor] == 'big' or self.kind[neighbor] == 'small' or self.kind[neighbor] == 'field':
                    if neighbor not in result:
                        result[neighbor] = 0
                    result[neighbor] += 1
        return result

    def get_small(self, nodes):
        result = {}
        for node in nodes:
            for neighbor in self.graph.neighbors(node):
                if self.kind[neighbor] == 'small':
                    if neighbor not in result:
                        result[neighbor] = 0
                    result[neighbor] += 1
        return result

    def get3(self, vote, head):
        results = list(sorted(vote, key=vote.__getitem__))
        flag = []
        while len(flag) < 3:
            if results:
                top = results.pop()
                if not self.graph.has_edge(head, top):
                    flag.append(top)
            else:
                break
        return flag

    def work_in(self, head):
        vote = {}
        for node in self.author:
            similar = len(list(nx.common_neighbors(self.graph, head, node)))
            if similar != 0:
                for place in list(self.get_place([node]).keys()):
                    if place not in vote:
                        vote[place] = 0
                    vote[place] += similar * 2.5 + 0.4
        return self.get3(vote, head)

    def paper_publish_on(self, head):
        vote = {}
        for node in self.paper:
            similar = len(list(nx.common_neighbors(self.graph, head, node)))
            if similar != 0:
                for conf in list(self.get_conf([node]).keys()):
                    if conf not in vote:
                        vote[conf] = 0
                    vote[conf] += similar * 0.8 - 0.5
        return self.get3(vote, head)

    def author_is_in_field(self, head):
        vote = {}
        papers = list(self.get_paper([head]).keys())
        fields = self.get_field(papers)
        for field in fields.keys():
            if field not in vote:
                vote[field] = 0.0
            vote[field] += fields[field] * 1.5 - 0.2
        return self.get3(vote, head)

    def paper_is_in_field(self, head):
        vote = {}
        authors = list(self.get_author([head]))
        fields =self.get_field(authors)
        for field in fields.keys():
            if field not in vote:
                vote[field] = 0.0
            vote[field] += fields[field] * 0.8 + 0.1
        return self.get3(vote, head)

    def paper_is_written_by(self, head):
        vote = {}
        authors = list(self.get_author([head]).keys())
        papers = self.get_paper(authors)
        for paper in papers.keys():
            if paper == head:
                continue
            authors = list(self.get_author([paper]).keys())
            for author in authors:
                if author not in vote:
                    vote[author] = 0.0
                vote[author] += papers[paper] * 1.1 + 0.2
        return self.get3(vote, head)

    def paper_cit_paper(self, head):
        vote = {}
        fields = list(self.get_field([head]).keys())
        papers = self.get_paper(fields)
        for paper in papers:
            if paper not in vote:
                vote[paper] = 0.0
            vote[paper] += papers[paper] * 1.3 - 0.4
        return self.get3(vote, head)
    
    def field_is_part_of(self, head):
        vote = {}
        authors = list(self.get_author([head]).keys())
        papers = list(self.get_paper([head]).keys())
        bigs1 = self.get_big(authors)
        bigs2 = self.get_big(papers)
        for big in list(bigs1.keys()):
            if big not in vote:
                vote[big] = 0.0
            vote[big] += bigs1[big] * 1.3 + 0.1
        for big in list(bigs2.keys()):
            if big not in vote:
                vote[big] = 0.0
            vote[big] += bigs2[big] * 0.9 - 0.2
        return self.get3(vote, head)


data = Model()
outfile = open('out.csv', 'w')
outfile.write('QueryId,ExpectedTail\n')
test = pd.read_csv('test.csv')
for i in range(len(test['QueryId'])):
    query, head, relation = test['QueryId'][i], test['Head'][i], test['Relation'][i]
    print(query)
    if relation == 'work_in':
        results = data.work_in(head)
    if relation == 'paper_publish_on':
        results = data.paper_publish_on(head)
    if relation == 'author_is_in_field':
        results = data.author_is_in_field(head)
    if relation == 'paper_is_in_field':
        results = data.paper_is_in_field(head)
    if relation == 'paper_is_written_by':
        results = data.paper_is_written_by(head)
    if relation == 'paper_cit_paper':
        results = data.paper_cit_paper(head)
    if relation == 'field_is_part_of':
        results = data.field_is_part_of(head)
    outfile.write(str(query)+','+' '.join(results)+'\n')
outfile.close()
