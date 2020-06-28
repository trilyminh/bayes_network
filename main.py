import abc
import random
import numpy as np

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

    def setChilds(self, childs):
        self.childs = childs

    def setParents(self, parents):
        self.parents = parents


class DGraphModel(AbstractGraph):
    def __init__(self, name):
        self.name = name
        self.listVertex = []

    def add(self, name, rangeValue):
        newVertex = Vertex(name, rangeValue)
        self.listVertex.append(newVertex)

    def connect(self, vertex1, vertex2):
        print("Add connect to text")

    def getListVertex(self):
        return self.listVertex


bayes = DGraphModel("Bayes")
bayes.add("difficulty", ["easy", "hard"])
bayes.add("intelligence", ["low", "high"])
bayes.add("grade", ["a", "b", "c"])
bayes.add("sat", ["low", "high"])
bayes.add("letter", ["weak", "strong"])


def getLabelFromDP(dP):
    iRandom = random.uniform(0, 1)
    totalP = 0

    for label in range(len(dP)):
        totalP += dP[label]
        if iRandom < totalP:
            return label


M = 1000000

fModel = open("model.txt", "r")
lineCount = 1
numNode = 1
matrixRelation = {}
matrixAttributes = {}
matrixProbability = {}

for line in fModel:
    if lineCount == 1:
        numNode = int(line)
    else:
        line = line.rstrip()
        elementNode = line.split(";")

        if elementNode[1] != '':
            matrixRelation[elementNode[0]] = elementNode[1].split(",")
        else:
            matrixRelation[elementNode[0]] = []

        matrixAttributes[elementNode[0]] = elementNode[2].split(",")

        attributeShape = tuple(int(shape) for shape in elementNode[3].split(","))
        probabiltyNode = [float(probabilty) for probabilty in elementNode[4].split(",")]
        matrixProbability[elementNode[0]] = np.reshape(probabiltyNode, attributeShape)
    lineCount += 1
    if lineCount > numNode + 1:
        break


# matrixRelation = {
#     "D" : [],
#     "I" : [],
#     "G" : ['I','D'],
#     "S" : ['I'],
#     "L" : ['G'],
# }
# matrixProbability = {
#     "D" : {
#         "easy": 0.6, "difficulty": 0.4
#     },
#     "I" : {
#         "low": 0.7, "high": 0.3
#     },
#     "S": {
#         "low": {
#             "low": 0.95, "high": 0.05
#         },
#         "high": {
#             "low": 0.2, "high": 0.8
#         }
#     },
#     "G" : {
#         "low": {
#             "easy" : {
#                 "a": 0.3, "b": 0.4, "c": 0.3
#             },
#             "difficulty": {
#                 "a": 0.05, "b": 0.25, "c": 0.7
#             }
#         },
#         "high": {
#             "easy":{
#                 "a": 0.9, "b": 0.08, "c": 0.02
#             },
#             "difficulty": {
#                 "a": 0.5, "b": 0.3, "c": 0.2
#             }
#         }
#     },
#     "L" : {
#         "a" : {
#             "weak" : 0.1, "strong" :0.9
#         },
#         "b" : {
#             "weak" : 0.4, "strong" :0.6
#         },
#         "c" : {
#             "weak" : 0.99, "strong" :0.01
#         }
#     }
# }

def compareCondition(sample, condition):
    for label in condition:
        expected = condition[label]
        if expected != sample[label]:
            return False
    return True

def calculateProbability(results,preCondition,postCondition):
    M = len(results)
    if len(preCondition):
        countPreCondition = 0
        countPostCondition  = 0
        for sample in results:
            if compareCondition(sample, preCondition):
                countPreCondition += 1
                if compareCondition(sample, postCondition):
                    countPostCondition += 1
        return countPostCondition / countPreCondition
    else:
        countPostCondition  = 0
        for sample in results:
            if compareCondition(sample,postCondition):
                countPostCondition += 1
        return countPostCondition / M

def generateSample(matrixProbability,matrixRelation):

    results = []
    for i in range(1, M + 1):
        sampleLabel = {}
        for label in matrixProbability:
            parents = matrixRelation[label]
            labelParents=[]
            for parent in parents:
                labelParents.append(sampleLabel[parent])
            labelParents.insert(0,label)

            # access probability
            probabilityLabel = matrixProbability
            for keyAccess in labelParents:
                probabilityLabel = probabilityLabel[keyAccess]

            sampleLabel[label] = getLabelFromDP(probabilityLabel)

        results.append(sampleLabel)
    return results
print("Generate example\n")
results = generateSample(matrixProbability,matrixRelation)
print("Finish example\n")

# PreCondition = {
#     "D": "easy",
#     "L" : "strong"
# }
# PostCondition = {
#     "D": "easy",
#     "L": "strong",
#     "I" : "low",
# }

fTest = open("test.txt", "r")
lineCount = 1
numQuestion = 1
PreCondition = {}
PostCondition = {}

for line in fTest:
    if lineCount == 1:
        numQuestion = int(line)
    else:
        line = line.rstrip()
        elementQuestions = line.split(";")

        # for elementQuestion in elementQuestions:
        nodeQuestions = elementQuestions[0].split(",")
        for sNodeQuestion in nodeQuestions:
            nodeQuestion = sNodeQuestion.split("=")
            PostCondition[nodeQuestion[0]] = nodeQuestion[1]

        if elementQuestions[1] != '':
            PreCondition = PostCondition.copy()
            nodeQuestions = elementQuestions[1].split(",")
            for sNodeQuestion in nodeQuestions:
                nodeQuestion = sNodeQuestion.split("=")
                PreCondition[nodeQuestion[0]] = nodeQuestion[1]
        print(PreCondition)
        print(PostCondition)

    lineCount += 1

PreCondition = {
    "difficulty": 0,
    "letter" : 1
}
PostCondition = {
    "difficulty": 0,
    "letter" : 1,
    "intelligence" : 0,
}


fTest = open("test.txt", "r")
lineCount = 1
numQuestion = 1


answers = []
for line in fTest:
    if lineCount == 1:
        numQuestion = int(line)
    else:
        print("Check question "+str(lineCount)+"\n")

        line = line.rstrip()
        PreCondition = {}
        PostCondition = {}

        elementQuestions = line.split(";")

        for elementQuestion in elementQuestions:
            nodeQuestions = elementQuestion.split(",")
            for sNodeQuestion in nodeQuestions:
                if sNodeQuestion != '':
                    nodeQuestion = sNodeQuestion.split("=")
                    PostCondition[nodeQuestion[0]] = matrixAttributes[nodeQuestion[0]].index(nodeQuestion[1])

        if elementQuestions[1] != '':
            nodeQuestions = elementQuestions[1].split(",")
            for sNodeQuestion in nodeQuestions:
                if sNodeQuestion != '':
                    nodeQuestion = sNodeQuestion.split("=")
                    PreCondition[nodeQuestion[0]] = matrixAttributes[nodeQuestion[0]].index(nodeQuestion[1])

        answer = calculateProbability(results, PreCondition, PostCondition)
        print(answer)
        answers.append(answer)
    lineCount += 1



f = open("output.txt", "w")
lineCount = 1
for answer in answers:
    if lineCount != len(answers):
        f.write(str(answer)+"\n")
    else:
        f.write(str(answer))
    lineCount += 1
f.close()
