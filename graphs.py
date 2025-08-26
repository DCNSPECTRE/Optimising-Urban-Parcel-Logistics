import numpy as np
from linkedlists_main import DSALinkedList, DSAListNode
from stacksandqueues import DSAStack, DSAQueue
from heaps import *


'''
    This is the graphs.py module.
    It contains all of the necessary classes and methods to create and manipulate an undirected graph.
    The graph is represented as an adjacency list and an adjacency matrix.
    The graph can be traversed using BFS, DFS and Dijkstra's algorithm.
    The graph can also be cleared and tested with a sample logistics network graph.

    The graph is uses methods from the DSALinkedList class from linkedlists_main.py and the DSAStack, DSAQueue and DijkstraHeap classes from stacksandqueues.py and heaps.py respectively.
    The graph is implemented using the DSAGraphVertex and DSAGraphEdge classes.

    The functions/methods in this file include:
    - addVertex: Adds a vertex to the graph
    - getVertex: Gets a vertex from the graph by label
    - addEdge: Adds an edge between two vertices in the graph
    - deleteVertex: Deletes a vertex from the graph
    - deleteEdge: Deletes an edge between two vertices in the graph
    - displayAsList: Displays the graph as an adjacency list
    - displayAsMatrix: Displays the graph as an adjacency matrix
    - BFS: Performs a breadth-first search on the graph
    - DFS: Performs a depth-first search on the graph
    - dijkstra: Performs Dijkstra's algorithm on the graph to find the shortest path from a given vertex
    - clearGraph: Clears the graph by removing all vertices and edges
    - sortAdjacentList: Sorts the adjacent list of edges for a vertex in alphabetical order


    SELF CITING: This code has been adapted from the COMP1002 Practial 06 - Graphs by Muhammad Annas Atif (22224125)
                   
                     Muhammad Annas Atif. 2025. COMP1002 Practical 06 - Graphs.
                        Curtin University, Unpublished.
'''


class DSAGraph:
    # the graph here represents an undirected graph using an adjacency list
    # each vertex is represented by a DSAGraphVertex object
    def __init__(self):
        self.vertex = DSALinkedList()

    def getVertex(self, label):
        temp = self.vertex.head
        while temp is not None:
            if temp.value.getLabel() == label:
                return temp.value
            temp = temp.next
        return None
    
    # adds a vertex to the graph
    # if the vertex already exists, it raises an exception

    def addVertex(self, label, value=None):
        if self.getVertex(label) is not None:
            raise Exception("Vertex already exists")
        newVertex = DSAGraphVertex(label, value)
        self.vertex.insertLast(newVertex)

    # adds an edge between two vertices in the graph
    # if one or both vertices do not exist it raises an exception
    # if the edge already exists, it raises an exception
    # if the edge is between the same vertex it raises an exception
    # the edge is initialised as a DSAGraphEdge object
    # the edge is added to the edges list of both vertices
    def addEdge(self, fromLabel, toLabel, weight=1):
        fromVertex = self.getVertex(fromLabel)
        toVertex = self.getVertex(toLabel)

        if fromVertex is None or toVertex is None:
            raise Exception("One or both vertices not found")
        if fromLabel == toLabel:
            raise Exception("Cannot add edge to itself")
        for edge in fromVertex.getEdges():
            if edge.getToVertex().getLabel() == toLabel:
                raise Exception("Edge already exists")
            

        newEdge = DSAGraphEdge(fromVertex, toVertex, weight)
        fromVertex.addEdge(newEdge)
        toVertex.addEdge(DSAGraphEdge(toVertex, fromVertex, weight))  # Add reverse edge for undirected graph otherwise we have a directed graph which is a no no.

    # deletes a vertex from the graph
    # if the vertex does not exist it raises an exception
    # uses the _removeEdge method to remove all edges connected to the vertex
    # uses the _removeVertex method to remove the vertex from the graph
    def deleteVertex(self, label):
        vertex = self.getVertex(label)
        if vertex is None:
            raise Exception("Vertex not found")

        temp = self.vertex.head
        while temp is not None:
            self._removeEdge(temp.value.getEdges(), label)
            temp = temp.next

        self._removeVertex(label)

    # deletes an edge between two vertices in the graph
    # if one or both vertices do not exist it raises an exception
    def deleteEdge(self, fromLabel, toLabel):
        fromVertex = self.getVertex(fromLabel)
        toVertex = self.getVertex(toLabel)

        if fromVertex is None or toVertex is None:
            raise Exception("One or both vertices not found")

        self._removeEdge(fromVertex.getEdges(), toLabel)
        self._removeEdge(toVertex.getEdges(), fromLabel)

    # helper method to remove edges from a vertexs edges list
    # it iterates through the edgelist and removes edges that match the taget label
    # O(N) Search for each edge unless the edge is at the head of the list or tail of the list
    def _removeEdge(self, edgeList, targetLabel):
        temp = DSALinkedList()
        while not edgeList.isEmpty():
            edge = edgeList.removeFirst()
            if edge.getToVertex().getLabel() != targetLabel:
                temp.insertLast(edge)
        while not temp.isEmpty():
            edgeList.insertLast(temp.removeFirst())

    # helper method to remove a vertex from the graph
    # it iterates through the vertex list and removes the vertex that matches the target label
    def _removeVertex(self, label):
        temp = DSALinkedList()
        while not self.vertex.isEmpty():
            v = self.vertex.removeFirst()
            if v.getLabel() != label:
                temp.insertLast(v)
        while not temp.isEmpty():
            self.vertex.insertLast(temp.removeFirst())

    # displays the graph as an adjacency list
    # it iterates through the vertex list and prints the label of each vertex and its edges
    # uses the getEdges function of the DSAGraphVertex class to get edges for each vertex
    def displayAsList(self):
        print("\n=======================================\nAdjacency List:\n=======================================")
        temp = self.vertex.head
        while temp is not None:
            vertex = temp.value
            print(f"Hub/City Intersection: {vertex.getLabel()}: ", end=" ")
            edgeTemp = vertex.getEdges().head
            while edgeTemp is not None:
                edge = edgeTemp.value
                print(f"| {edge.getToVertex().getLabel()} (Travel Time: {edge.getWeight()}) |", end=" ")
                edgeTemp = edgeTemp.next
            print()
            temp = temp.next

    # displays the graph as an adjacency matrix
    # it creates a matrix of size V x V
    # The matrix is made using a linked list where each row is a linked list of edges
    # it iterates through the vertex list and for each vertex it iterates through the edges to fill the matrix based on the edge weights
    # if there is no edge the weight is 0
    # it them prints the matrix by iterating through the rows and columns and extracting the desired values
    def displayAsMatrix(self):
        matrix = DSALinkedList()

        rowVertex = self.vertex.head
        while rowVertex is not None:
            row = DSALinkedList()
            colVertex = self.vertex.head
            while colVertex is not None:
                edgeTemp = rowVertex.value.getEdges().head
                found = False
                while edgeTemp is not None:
                    edge = edgeTemp.value
                    if edge.getToVertex() == colVertex.value:
                        row.insertLast(edge.getWeight())
                        found = True
                        break
                    edgeTemp = edgeTemp.next
                if not found:
                    row.insertLast(0)  # No edge, insert 0
                colVertex = colVertex.next
            matrix.insertLast(row)
            rowVertex = rowVertex.next

        print("\n=======================================\nAdjacency Matrix:\n=======================================")
        rowNode = matrix.head
        while rowNode is not None:
            row = rowNode.value
            colNode = row.head
            while colNode is not None:
                print(colNode.value, end=" ")
                colNode = colNode.next
            print()
            rowNode = rowNode.next

    # this function performs a breadth-first search (BFS) on the graph
    # it starts from a given vertex and explores all its adjacent vertices before proceeding to the next level
    # it uses a queue to keep track of the vertices to be visited (Q) and a depth list made from a linked list to keep track of the depth of each vertex given from (D) (needed in the required output)
    # there is also a temporary queue to keep track of the visited vertices (T).
    # it marks each vertex as visited to avoid cycles and infinite loops
    # it also uses teh sortAdjacentList function to sort the edges of each vertex in alphabetical order
    # the BFS treaversal and Depth list are then printed in a formatted manner
    def BFS(self, reference):
        T = DSAQueue()
        Q = DSAQueue()
        D = DSAQueue()
        depthList = DSALinkedList()


        for vertex in self.vertex:
            vertex.clearVisited()

        v = self.getVertex(reference)
        if v is None:
            raise Exception("Vertex not found")
        v.setVisited(True)
        Q.enqueue(v)
        D.enqueue(0)

        while not Q.isEmpty():
            v = Q.dequeue()
            d = D.dequeue()

            depthList.insertLast(f"{v.getLabel()} | {d}")
            for each in sortAdjacentList(v.getEdges()):
                if not each.getToVertex().getVisited():
                    T.enqueue(v)
                    T.enqueue(each.getToVertex())
                    each.getToVertex().setVisited(True)
                    D.enqueue(d + 1)
                    Q.enqueue(each.getToVertex())
    
        print("\n=======================================\nBFS Traversal (Reachable Zones):\n")
        count = 0
        formatted_output = ""
        while not T.isEmpty():
            v = T.dequeue()
            if count > 0 and count % 2 == 0:
                formatted_output += " , "
            formatted_output += v.getLabel()
            if count % 2 == 0:
                formatted_output += " "
            count += 1
        print(formatted_output.strip())
        print("=======================================\nDepth List (Hops Between Each Hub Intersection):\n")
        count = 0
        while not depthList.isEmpty():
            v = depthList.removeFirst()
            if count > 0:
                print(", ", end="")
            print(v, end=" ")
            count += 1
        print("\n=======================================\n")

    # this function performs a depth-first search (DFS) on the graph
    # it starts from a given vertex and explores as far as possible along each branch before backtracking
    # it uses a stack to keep track of the vertices to be visited (S) and a queue to keep track of the visited vertices (T)
    # it also uses a linked list to keep track of the visited vertices in order to detect cycles
    def DFS(self, reference):
        T = DSAQueue()
        S = DSAStack()
        cycleList = DSALinkedList() # this is the list that will store detected cycles
        visitedList = DSALinkedList() # the visited list is separate from teh cycle list to avoid the DFS algorithm from detecting cycles in the visited list itself

        for vertex in self.vertex: # clears the visited status of all vertices incase the DFS is run multiple times or BFS is run before DFS
            vertex.clearVisited()
        
        # get the starting vertex and raise an exception if it does not exist
        # mark it as visited and push it onto the stack
        # # also insert it into the visited list
        v = self.getVertex(reference)
        if v is None:
            raise Exception("Vertex not found")
        v.setVisited(True)
        S.push(v)
        visitedList.insertLast(v)

        # while the stack is not empty pop the top vertex and explore its adjacent vertices by iterating through its edges
        # if an adjacent vertex is not visitied mark it as visited, enqueue it to the queue, push it onto the stack and insert it into the visited list
        # if a cycle is detected, it is added to the cycle list if it is not already present
        # if the cycle is already present, it is not added again

        while S.isEmpty() == False:
            v = S.top()
            foundUnvisited = False
            for each in sortAdjacentList(v.getEdges()):
                u = each.getToVertex()
                
                # Cycle Detection
                # if the current vertex is the same as the head of the visited list and that list has more than 2 vertices it means a cycle is detected
                # we then create a cycle string that contains the labels of the vertices in the cycle
                if u == visitedList.head.value and visitedList.size > 2:
                    cycleStr = ""
                    temp = visitedList.head
                    while temp is not None:
                        cycleStr += temp.value.getLabel() + " -> "
                        temp = temp.next
                    cycleStr += u.getLabel()

                    # Check if the cycle is already in the list
                    # this is done by itereating through the cycle list and checking if the string is already present
                    # if it is not present it is added to teh cycle list
                    isDuplicate = False
                    tempCycle = cycleList.head
                    while tempCycle is not None:
                        if tempCycle.value == cycleStr:
                            isDuplicate = True
                            break
                        tempCycle = tempCycle.next

                    if not isDuplicate:
                        cycleList.insertLast(cycleStr)
                
                # 
                if not u.getVisited():
                    T.enqueue(v)
                    T.enqueue(u)
                    u.setVisited(True)
                    S.push(u)
                    visitedList.insertLast(u)
                    foundUnvisited = True
                    break
            # if no unvistited adjacent vertices found pop the top vertex from the stack and remove it from the visited list
            # this is done to backtrack and explore other branches of the graph and it is done until stack is empty
            if not foundUnvisited:
                S.pop()
                visitedList.removeLast()
        
        # this prints the DFS traversal and the detected cycles
        print("\n=======================================\nDFS Traversal:\n")
        count = 0
        formatted_output = ""
        while not T.isEmpty():
            v = T.dequeue()
            if count > 0 and count % 2 == 0:
                formatted_output += " , "
            formatted_output += v.getLabel()
            if count % 2 == 0:
                formatted_output += " "
            count += 1
        print(formatted_output.strip())

        print("=======================================\nDetected Cycles:\n")
        temp = cycleList.head
        while temp is not None:
            print(temp.value)
            temp = temp.next
        if cycleList.isEmpty():
            print("No cycles detected.")
            print()
        print("=======================================\n")
        


    def dijkstra(self, startLabel):
        '''

        Geeks for Geeks. 2025. "Introduction to Dijkstra's Shortest Path Algorithm". Geeks for Geeks.
            https://www.geeksforgeeks.org/introduction-to-dijkstras-shortest-path-algorithm/

        '''
        if self.getVertex(startLabel) is None:
            raise Exception("Start vertex not found")
        else:
            for each in self.vertex:
                each.distance = float('inf')
                each.previous = None # by setting the previous vertex to None it allows us avpid cycles in path
                each.setVisited(False) # clears visited status of all vertices incase BFS or DFS is run before Dijkstra's algorithm

            startVertex = self.getVertex(startLabel) 
            startVertex.distance = 0 # distance from start vertex to itself is 0

            heap = DijkstraHeap()
            heap.add(0, startVertex) # we add the start vertex to the heap with distance of 0

            
            while heap.isEmpty() == False: 

                entry = heap.remove() # removes the vertex with the smallest distance from the heap
                currentVertex = entry.getValue() # gets the vertex from the entry
                
                # if the vertex has been visited we skip it or else we mark it as visited
                # this is to avoid cycles and infinite loops
                if currentVertex.getVisited() == True:
                    continue

                currentVertex.setVisited(True) 

                # iterate throug the edges of the current vertex
                # for each edge we get the to vertex and check if it has been visited
                # if it has been visited we skip it
                # if it has not been visited we calculate the new distance from the current vertex to the to vertex
                # if the new distance is less than the current distance of the to vertex we update the distance and previous vertex
                # and add the to vertex to the heap with the new distance
                for each in currentVertex.getEdges():
                    n = each.getToVertex()
                    if n.getVisited():
                        continue

                    newDistance = currentVertex.distance + each.getWeight()
                    if newDistance < n.distance:
                        n.distance = newDistance
                        n.previous = currentVertex
                        heap.add(newDistance, n)
                    
            print("========================================\nDijkstra's Algorithm Result (Shortest Path)\n========================================")
        
            # this prints the shortest path from the start vertex to each vertex in the graph
            for each in self.vertex:
                if each.distance == float('inf'):
                    print(f"Hub/Intersection {each.getLabel()} is unreachable from {startLabel}")
                else:
                    pathList = DSALinkedList()
                    temp = each
                    while temp is not None:
                        pathList.insertFirst(temp.getLabel())
                        temp = temp.previous
                if each.distance > 0 and each.distance != float('inf'):
                    print(f"Shortest path from {startLabel} to {each.getLabel()} is of time {each.distance} minutes, with path: ", end="")
                    count = 0
                    while not pathList.isEmpty():
                        v = pathList.removeFirst()
                        if count > 0:
                            print(",", end="")
                        print(v, end="")
                        count += 1
                    print()
            print("========================================")

    # this function clears the graph by removing all vertices, edges and restting the visited status of all vertices
    # it also resets the distance and previous vertex of all vertices to their initial values
    def clearGraph(self):
        self.vertex = DSALinkedList()
        for vertex in self.vertex:
            vertex.clearVisited()
            vertex.distance = float('inf')
            vertex.previous = None
            vertex.setVisited(False)
        print("Graph cleared successfully.")
    
# this function sorts the adjacent list of edges for a vertex in alphabetical order based on the label of the to vertex
# it uses a temporary linked list to store the edges in sorted order
def sortAdjacentList(adjList):
    sortedList = DSALinkedList()

    for current in adjList:
        inserted = False
        tempList = DSALinkedList()

        while not sortedList.isEmpty():
            v = sortedList.removeFirst()
            if not inserted and current.getToVertex().getLabel() < v.getToVertex().getLabel():
                tempList.insertLast(current)
                inserted = True
            tempList.insertLast(v)

        if not inserted:
            tempList.insertLast(current)

        while not tempList.isEmpty():
            sortedList.insertLast(tempList.removeFirst())

    return sortedList


class DSAGraphVertex:
    def __init__(self, label, value=None):
        self.label = label
        self.value = value
        self.edges = DSALinkedList()
        self.visited = False
        self.distance = float('inf')
        self.previous = None
    
    def getLabel(self):
        return self.label
    
    def getValue(self):
        return self.value
    
    def getEdges(self):
        return self.edges
    
    def getVisited(self):
        return self.visited
    
    def setVisited(self, visited):
        self.visited = visited

    def clearVisited(self):
        self.visited = False

    def addEdge(self, edge):
        self.edges.insertLast(edge)

    def toString(self):
        return f"Label: {self.label}, Value: {self.value}"

class DSAGraphEdge:
    def __init__(self, fromVertex, toVertex, weight=1):
        self.fromVertex = fromVertex
        self.toVertex = toVertex
        self.weight = weight

    def getFromVertex(self):
        return self.fromVertex

    def getToVertex(self):
        return self.toVertex

    def getWeight(self):
        return self.weight

    def setWeight(self, weight):
        self.weight = weight

    def toString(self):
        return f"From: {self.fromVertex.getLabel()}, To: {self.toVertex.getLabel()}, Weight: {self.weight}"


