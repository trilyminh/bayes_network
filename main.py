import abc
import random
class AbstractGraph(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add(self):
        pass

    @abc.abstractmethod
    def connect(self, vertex1, vertex2):
        pass

class Vertex:
    def __init__(self, name, rangeValue):
        self.name = name
        self.rangeValue = rangeValue
        self.childs = []
        self.parents = []

    def setChilds(self,childs):
        self.childs = childs

    def setParents(self, parents):
        self.parents = parents

class DGraphModel(AbstractGraph):
    def __init__(self, name):
        self.name = name
        self.listVertex = []

    def add(self, name, rangeValue):
        newVertex =  Vertex(name,rangeValue)
        self.listVertex.append(newVertex)

    def connect(self, vertex1, vertex2):
       print("Add connect to text")

    def getListVertex(self):
        return self.listVertex


bayes = DGraphModel("Bayes")
bayes.add("difficulty",["easy","hard"])
bayes.add("intelligence",["low","high"])
bayes.add("grade",["a","b","c"])
bayes.add("sat",["low","high"])
bayes.add("letter",["weak","strong"])

for vertex in bayes.getListVertex():
    print(vertex.rangeValue)
    
print("Abc")
M = 100



def getLabelFromDP(dP):
    iRandom = random.uniform(0, 1)
    totalP = 0

    for label in dP:
        totalP += pD[label]
        if iRandom < totalP:
            return label

M = 100000
pD = {"easy":0.75,"difficulty":0.25}
statsD = dict.fromkeys(pD.keys(),0)
for i in range(1,M+1):
    label = getLabelFromDP(pD)
    statsD[label] = statsD[label] + 1
print(statsD)
print(statsD["difficulty"]/sum(statsD.values()))