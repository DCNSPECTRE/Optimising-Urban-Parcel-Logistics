
'''
    This is the stacks and queues implementation for my COMP1002 assignment.

    SELF CITING: This code has been adapted from the COMP1002 Practial 03 - Stacks and Queues by Muhammad Annas Atif (22224125)

                Muhammad Annas Atif. 2025. COMP1002 Practical 08 - Stacks and Queues.
                    Curtin University, Unpublished.
'''

from linkedlists_main import DSALinkedList, DSAListNode

class DSAStack:
    def __init__(self):
        self.stack = DSALinkedList()

    def getCount(self):
        return self.stack.size
    
    def isEmpty(self):
        return self.stack.isEmpty()
    
    def push(self, value):
        self.stack.insertFirst(value)
    
    def pop(self):
        if self.stack.peekFirst() is None:
            raise Exception("Stack is empty")
        else: 
            return self.stack.removeFirst()
        
    def top(self):
        if self.stack.peekFirst() is None:
            raise Exception("Stack is empty")
        else:
            return self.stack.peekFirst()
    
    def output(self):
        if self.isEmpty():
            return "[]"
        result = ""
        for value in self.stack:
            result += str(value) + " "
        formatted_result = f"[{result.strip()}]"
        return formatted_result

class DSAQueue:
    def __init__(self):
        self.queue = DSALinkedList()

    def getCount(self):
        return len(self.queue)
    
    def isEmpty(self):
        return self.queue.isEmpty()
    
    def enqueue(self, value):
        self.queue.insertLast(value)

    def dequeue(self):
        if self.queue.peekFirst() is None:
            raise Exception("Queue is empty")
        else:
            return self.queue.removeFirst()
    
    def peek(self):
        if self.queue.peekFirst() is None:
            raise Exception("Queue is empty")
        else:
            return self.queue.peekFirst()
    
    def output(self):
        if self.isEmpty():
            return "[]"
        result = ""
        for value in self.queue:
            result += str(value) + " "
        formatted_result = f"[{result.strip()}]"
        return formatted_result


