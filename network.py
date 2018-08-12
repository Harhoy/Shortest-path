

#https://www.youtube.com/watch?v=GazC3A4OQTE&t=7s

infty = 10**10

class VertexSet:

    def __init__(self):
        self._items = []

    def addVertex(self,item):
        self._items.append(item)

    def getLen(self):
        return len(self._items)

    def getMin(self):

        smallestVal = infty
        smallestRef = None

        for item in self._items:
            if item.getDist() < smallestVal:
                smallestVal = item.getDist()
                smallestRef = item

        return smallestRef

    def isEmpty(self):
        if len(self._items) > 0:
            return False
        return True

    def remove(self,itemToPop):
        index = 0
        targetId = itemToPop.getId()
        for item in self._items:
            if item.getId() is targetId:
                return self._items.pop(index)
            else:
                index += 1
        return None



class Node:

    def __init__(self,id):
        self._id = id
        self._adjecentEdges = []
        self._adjecentNodes = []
        self._dist = 0
        self._prev = None
        self._cap = 0
        self._charger = False

    def getDist(self):
        return self._dist

    def setDist(self,dist):
        self._dist = dist

    def setPrev(self,prev):
        self._prev = prev

    def getPrev(self):
        return self._prev

    def setCap(self,cap):
        self._cap = cap

    def addEdge(self,edge):
        self._adjecentEdges.append(edge)

    def connectNode(self,node):
        self._adjecentNodes.append(node)

    def adjecentNodes(self):
        return self._adjecentNodes

    def getId(self):
        return self._id

    def setCharge(self):
        self._charger = True

class Edge:

    def __init__(self,nodeA,nodeB,weight):
        self._nodeA = nodeA
        self._nodeB = nodeB
        self._weight = weight

    def getWeight(self):
        return self._weight

    def printInfo(self):
        print("A",self._nodeA.getId(),"B",self._nodeB.getId(),"W",self._weight)

class Charger(Edge):

    def __init__(self,nodeA,nodeB,weight):
        super().__init__(nodeA,nodeB,1)

class Graph:

    def __init__(self):
        self._nodes = []
        self._edges = []

    def getNodes(self):
        return self._nodes

    def getEdges(self):
        return self._edges

    def hasNode(self,id):
        for node in self._nodes:
            if node.getId() == id:
                return True
        return False

    #Legge til node
    def addNode(self,id):
        self._nodes.append(Node(id))

    #Get edge reference
    def getEdge(self,nodeA,nodeB):
        nodeA = self.getRef(nodeA)
        nodeB = self.getRef(nodeB)
        for edge in self._edges:
            if nodeA == edge._nodeA and nodeB == edge._nodeB:
                return edge
        return None

    #Add new edge to graph
    def addEdge(self,idA,idB,weight):
        refA = None
        refB = None
        for node in self._nodes:
            if node._id == idA:
                refA = node
            if node._id == idB:
                refB = node

        newEdge = Edge(refA,refB,weight)
        self._edges.append(newEdge)
        refA.addEdge(newEdge)
        refB.addEdge(newEdge)
        refA.connectNode(refB)
        refB.connectNode(refA)

    #Get object reference based on number
    def getRef(self,no):
        for node in self._nodes:
            if node._id == no:
                return node
        return None

    #Find a path between start and end node
    def findPath(self,start,end,path=[]):
        thisNode = self.getRef(start)
        thatNode = self.getRef(end)
        path = path + [start]
        if thisNode == thatNode:
            return path
        for node in thisNode.adjecentNodes():
            if node.getId() not in path:
                nextNode = node.getId()
                newpath = self.findPath(nextNode,end,path)
                if newpath:
                    return newpath
        return None


def djikstra(graph, source, end):

    #Creating a set of nodes
    set = VertexSet()

    #Initializing set
    for v in graph.getNodes():
        v.setDist(infty)
        v.setPrev(None)
        set.addVertex(v)


    #Setting the value of the first node to zero
    graph.getRef(source).setDist(0)

    #Looping while there are still nodes in the queue
    while not set.isEmpty():

        #Node with minimum distance
        u = set.getMin()

        #Remove from set
        set.remove(u)

        #Looking through all nodes
        for node in u.adjecentNodes():

            #Graph is not directed, so need to check which order the edges are listed in
            if graph.getEdge(u.getId(),node.getId()) == None:
                testDistance = u.getDist() + graph.getEdge(node.getId(),u.getId()).getWeight()
            else:
                testDistance = u.getDist() + graph.getEdge(u.getId(),node.getId()).getWeight()

            #A shorter distance is found
            if testDistance < node.getDist():
                node.setDist(testDistance)
                node.setPrev(u)

    #List of nodes
    s = []
    #End-node
    u = graph.getRef(end)

    #Getting all the nodes
    while u.getPrev() != None:
        s.insert(0,u)
        u = u.getPrev()

    #Inserting the source node
    s.insert(0,graph.getRef(source))

    return s

if __name__ == "__main__":

    #Creating graph
    graph = Graph()

    #Opening data
    data = open("graf.csv",'r')

    #Reading in data
    for line in data:

        #Getting raw data
        lineData = line.split(';')
        nodeA = int(lineData[0])
        nodeB = int(lineData[1])
        weight = float(lineData[2])

        #Adding if node is not present
        if not graph.hasNode(nodeA):
            graph.addNode(nodeA)

        #Adding if node is not present
        if not graph.hasNode(nodeB):
            graph.addNode(nodeB)

        #Adding edge
        graph.addEdge(nodeA,nodeB,weight)

    #Getting optimal path
    s = djikstra(graph,1,16)

    #printing path
    print("Optimal rute")
    for n in s:
        print(n.getId())

'''
graph.addNode(1)
graph.addNode(2)
graph.addNode(3)
graph.addNode(4)
graph.addNode(5)
graph.addNode(6)

graph.addEdge(1,2,1)
graph.addEdge(1,3,2)
graph.addEdge(2,4,5)
graph.addEdge(3,5,3)
graph.addEdge(5,4,2)
graph.addEdge(5,6,3)
graph.addEdge(4,6,1)
'''
