
'''
    This is the linked list implementation for my COMP1002 assignment.

    This is a doubly linked and doubly ended linked list implementation.

    SELF CITING: This code has been adapted from the COMP1002 Practial 04 - Linked Lists by Muhammad Annas Atif (22224125)

                Muhammad Annas Atif. 2025. COMP1002 Practical 04 - Linked Lists.
                    Curtin University, Unpublished.
'''

class DSAListNode:
    def __init__(self, data):
        self.value = data
        self.next = None
        self.prev = None
    
    def getValue(self):
        return self.value
    
    def getNext(self):
        return self.next
    
    def getPrev(self):
        return self.prev
    
    def setNext(self, newNext):
        self.next = newNext

    def setPrev(self, newPrev):
        self.prev = newPrev


class DSALinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0 
    
    def isEmpty(self):
        return self.head is None and self.tail is None
    
    def peekFirst(self):
        if self.isEmpty():
            raise Exception("List is empty")
        return self.head.getValue()

    def peekLast(self):
        if self.isEmpty():
            raise Exception("List is empty")
        return self.tail.getValue()
    
    def insertFirst(self, newItem):
        newNode = DSAListNode(newItem)

        if self.isEmpty():
            self.head = newNode
            self.tail = newNode
        else:
            newNode.setNext(self.head)
            self.head.setPrev(newNode)
            self.head = newNode
        self.size += 1
    
    def insertLast(self, newItem):
        newNode = DSAListNode(newItem)

        if self.isEmpty():
            self.head = newNode
            self.tail = newNode
        else:
            self.tail.setNext(newNode)
            newNode.setPrev(self.tail)
            self.tail = newNode
        self.size += 1
    
    def removeFirst(self):
        if self.isEmpty():
            raise Exception("List is empty")
        removedValue = self.head.getValue()
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.getNext()
            self.head.setPrev(None)
        self.size -= 1
        return removedValue

    def removeLast(self):
        if self.isEmpty():
            raise Exception("List is empty")
        removedValue = self.tail.getValue()
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.getPrev()
            self.tail.setNext(None)
        self.size -= 1
        return removedValue

    def __len__(self):
        return self.size

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.getValue()
            current = current.getNext()
            
