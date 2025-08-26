import numpy as np
from linkedlists_main import *

'''
    This is the heaps.py module
    It impoements a heap data structure usig numpy arrays and linked lists.
    It contains the DSAHeap class which implments a max heap
    Each entry in the heap is an instance of DSAHeapEntry class which contains:
    - key: Customer Name
    - value: Customer ID
    - address: Customer Address
    - priority: Calculated Priority based on Customer Priority and Delivery Time
    - deliveryStatus: Delivery Status
    - time: Delivery Time

    The heap class contains methods to:
    - priorityCalculation: Calculate the priority based on customer priority and delivery time
    - insert: Insert a new entry into the heap
    - addFromCSV: Add an entry from a CSV file
    - addFromHashes: Add an entry from a hash table
    - extract: Remove the highest priority entry from the heap
    - display: Display the contents of the heap
    - swap: Swap two entries in the heap
    - trickleUp: Move an entry up the heap to maintain the heap property
    - trickleDown: Move an entry down the heap to maintain the heap property
    - heapify: Convert an array into a heap
    - heapSort: Sort the heap
    - loadCSV: Load entries from a CSV file
    - saveCSV: Save the heap to a CSV file
    - isEmpty: Check if the heap is empty
    - saveRemovedItemsToCSV: Save the removed items to a CSV file
    - decreasePriority: Decrease the priority of an entry in the heap
    - increasePriority: Increase the priority of an entry in the heap

    Additionally there is a DijkstraHeap class that is inherited from DSAHeap and is implemented for Dijkstra's algorithm.

    SELF CITING: This code has been adapted from the COMP1002 Practical 08 - Heaps by Muhammad Annas Atif (22224125)

                Muhammad Annas Atif. 2025. COMP1002 Practical 08 - Heaps.
                    Curtin University, Unpublished.
        

'''
class DSAHeap:
    # initialises the heap with a maximum size and an empty numpy array which is the heap array
    def __init__(self, max_size=100000):
        self.heap = DSAHeapEntry()
        self.heapArray = np.zeros(max_size, dtype=DSAHeapEntry)
        self.count = 0
        self.max_size = max_size
        self.deliveredItems = DSALinkedList() # this linked list stores removed parcels from heap which is used to save removed items to CSV file
    
    # this function calculates teh prioirity based on the formula (6 - priorityLevel) / (1000 / time) which is given in the assignment brief
    def priorityCalculation(self, priorityLevel, time):
        # The priority function requires time to be a positive number and priorityLevel to be an integer between 1 and 5 so we check for that
        # if the input is not valid ValueError's are raised for the respective cases and a message is printed
        # then the prioirity is calculated and returned if the input is valid
        try:
            if not isinstance(time, (int, float)) or time <= 0:
                raise ValueError("Time must be a number and must be greater than zero.")
            if not isinstance(priorityLevel, int) or not (1 <= priorityLevel <= 5):
                raise ValueError("Priority must be a number between 1 and 5.")
            calculatedPriority = (6 - priorityLevel) / (1000 / time)
            return calculatedPriority
        except:
            print("Error: Invalid input for priority calculation. Ensure priority is a number between 1 and 5 and time is a positive number.")
            return None

    # this function inserts a new entry into the heap
    # it checks if the heap is full and raises an exception if it is
    # it then calculates the priority using the priorityCalculation function
    # if the priority is valid and time is a positive number it creates a new DSAHeapEntry object and adds it to the heap array
    # it then increments the count and calls the trickleUp function to maintain the heap property which is to ensure that the parent is greater than or equal to its children for a max heap
    # if the priority or time is not valid it raises a ValueError and prints an error message
    # if any other exception occurs it prints an error message
    def insert(self, key, value, address, priority, deliveryStatus, time):
        try:
            if self.count == self.max_size:
                raise Exception("Heap is full")
            
            priority = self.priorityCalculation(priority, time)
            if 0 <= priority <= 5 and int(time) > 0:
                newEntry = DSAHeapEntry(key, value, address, priority, deliveryStatus, time)
                self.heapArray[self.count] = newEntry
                self.count += 1
                self.trickleUp(self.heapArray, self.count - 1)
            else:
                raise ValueError("Priority must be a number between 1 and 5 and time must be a positive number.")
        except ValueError:
            print("Error: Priority must be a number between 1 and 5 and time must be a positive number.")
        except Exception as e:
            print(f"Error adding to heap: {e}")

    # this function adds an entry from a CSV file
    # it fundamentally works the same as the insert function but it does not calculate the priority as that is done in the loadCSV function
    def addFromCSV(self, key, value, address, priority, deliveryStatus, time):
        try:
            if self.count == self.max_size:
                raise Exception("Heap is full")
            if 0 <= priority <= 5 and int(time) > 0:
                newEntry = DSAHeapEntry(key, value, address, priority, deliveryStatus, time)
                self.heapArray[self.count] = newEntry
                self.count += 1
                self.trickleUp(self.heapArray, self.count - 1)
            else:
                raise ValueError("Priority must be a number between 1 and 5 if based on Customer Prioirity, and time must be a positive number.")
        except ValueError:
            print("Error: Priority must be a number between 1 and 5 and time must be a positive number.")
        except Exception as e:
            print(f"Error adding to heap: {e}")

    # this function takes values from module 2 and adds them into the healp.
    # the function works the same as the addFromCSV function but it does not calculate the priority as that is done in the DSAAssignment.py file
    def addFromHashes(self, key, value, address, priority, deliveryStatus, time):
        try:
            if self.count == self.max_size:
                raise Exception("Heap is full")
            newEntry = DSAHeapEntry(key, value, address, priority, deliveryStatus, time)
            self.heapArray[self.count] = newEntry
            self.count += 1
            self.trickleUp(self.heapArray, self.count - 1)
        except Exception as e:
            print(f"Error adding to heap: {e}")

    # the exctract function removes the highest priority entry from the heap
    # it checks if the heap is empty and raises an exception if it is
    # it then sotres the removed entry into a linked list called deliveredItems
    # it decrements the count and replaces the root of the heap with the last entry in the heap
    # it then calls the trickleDown function to maintain the heap property
    # if the heap is empty it raises an exception and prints an error message
    # if any other exception occurs it prints an error message
    # the removed entry is returned
    # the deliveredItems linked list is used to save the removed items to a CSV file later in the saveRemovedItemsToCSV function
    def extract(self):
        try:
            if self.count == 0:
                raise Exception("Heap is empty")
            root = self.heapArray[0]
            self.count -= 1
            self.heapArray[0] = self.heapArray[self.count]
            self.trickleDown(self.heapArray, 0, self.count)
            self.deliveredItems.insertLast(root)
            return root
        except Exception as e:
            print(f"Error removing from heap: {e}")

    # this function displays the contents of the heap
    def display(self):
        try:
            if self.count == 0:
                print("Heap is empty.")
            else:
                for i in range(self.count):
                    print(f"Customer Name: {self.heapArray[i].key}, Customer ID: {self.heapArray[i].value}, Address: {self.heapArray[i].address}, Priority (Calculated): {self.heapArray[i].priority}, Delivery Status: {self.heapArray[i].deliveryStatus}, Time: {self.heapArray[i].time}")
        except Exception as e:
            print(f"Error displaying heap: {e}")

    # this function swaps two entries in the heap array
    # it takes the heap array and the indices of the two entries to be swapped
    # it swaps the entries and returns the heap array
    # this is used in the trickleUp and trickleDown functions to maintain the heap property
    def swap(self, heapArray, idx1, idx2):
        temp = heapArray[idx1]
        heapArray[idx1] = heapArray[idx2]
        heapArray[idx2] = temp
        return heapArray
    
    # these two functions are used to move an entry up or down the heap to maintain the heap property
    # trickleUp moves an entry up the heap if its priority is greater than its parent's priority
    # trickleDown moves an entry down the heap if its priority is less than its children's priority
    def trickleUp(self, heapArray, curIdx):
        if curIdx > 0:
            parentIdx = (curIdx - 1) // 2
            if heapArray[curIdx].priority > heapArray[parentIdx].priority:
                self.swap(heapArray, curIdx, parentIdx)
                self.trickleUp(heapArray, parentIdx)
        return heapArray
    
    def trickleDown(self, heapArray, curIdx, numItems):
        leftChildIdx = 2 * curIdx + 1
        rightChildIdx = leftChildIdx + 1

        if leftChildIdx < numItems:
            largestIdx = leftChildIdx
            if rightChildIdx < numItems:
                if heapArray[rightChildIdx].priority > heapArray[leftChildIdx].priority:
                    largestIdx = rightChildIdx
            if heapArray[largestIdx].priority > heapArray[curIdx].priority:
                self.swap(heapArray, curIdx, largestIdx)
                self.trickleDown(heapArray, largestIdx, numItems)
    
    # this function converts an array into a heap
    # it starts from the last non-leaf node and calls the trickleDown function on each node to maintain the heap property
    # it does a trickleDown for each node from the last non-leaf node to the root node
    # it returns the heap array
    def heapify(self, heapArray, numItems):
        for i in range(numItems // 2 - 1, -1, -1):
            self.trickleDown(heapArray, i, numItems)
        return self.heapArray

    # this function sorts the heap using heap sort
    # it first calls the heapify function to convert the array into a heap
    # then it repeatedly swaps the root of the heap with the last element and calls the trickleDown function to maintain the heap property
    # it returns the sorted heap array
    def heapSort(self, heapArray, numItems):
        self.heapify(heapArray, numItems)
        for i in range(numItems - 1, 0, -1):
            self.swap(heapArray, 0, i)
            self.trickleDown(heapArray, 0, i)
        return heapArray

    # this function decreases the priority of an entry in the heap
    def decreasePriority(self, heapArray, idx, newPriority):
        if idx < self.count:
            heapArray[idx].setPriority(newPriority)
            self.trickleDown(heapArray, idx, self.count)
        else:
            print("Error: Index out of bounds.")
        return heapArray
    
    # this function increases the priority of an entry in the heap
    def increasePriority(self, heapArray, idx, newPriority):
        if idx < self.count:
            heapArray[idx].setPriority(newPriority)
            self.trickleUp(heapArray, idx)
        else:
            print("Error: Index out of bounds.")
        return heapArray  

    # this function loads entries from a CSV file into the heap
    def loadCSV(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 6:
                        key = parts[0]
                        value = parts[1]
                        address = parts[2]
                        priority = parts[3]
                        deliveryStatus = parts[4]
                        time = parts[5]
                        try:
                            priority = float(priority)
                            time = float(time)

                            if priority.is_integer() == True:
                                priority = int(priority)
                                priority = self.priorityCalculation(priority, time)
                                
                        except ValueError:
                            print("Skipping invalid line.")
                        if deliveryStatus != "Delivered":
                            deliveryStatus = "In-Transit"
                        else:
                            deliveryStatus = "Delivered"
                        self.addFromCSV(key, value, address, priority, deliveryStatus, time)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except Exception as e:
            print(f"Failed to load CSV: {e}")

    # this function saves the heap to a CSV file
    def saveCSV(self, filename):
        try:
            with open(filename, 'w') as file:
                for i in range(self.count):
                    file.write(f"{self.heapArray[i].key},{self.heapArray[i].value},{self.heapArray[i].address},{self.heapArray[i].priority},{self.heapArray[i].deliveryStatus},{self.heapArray[i].time}\n")
            print("Heap saved to CSV successfully.")
        except Exception as e:
            print(f"Error saving to CSV: {e}")

    # this function checks if the heap is empty
    def isEmpty(self):
        return self.count == 0

    # this function saves the removed items to a CSV file
    def saveRemovedItemsToCSV(self, filename):
        try:
            with open(filename, 'w') as file:
                current = self.deliveredItems.head
                while current is not None:
                    entry = current.getValue()
                    deliveryStatus = "Delievered"
                    if entry is None:
                        print(f"Skipping a NoneType Entry. Entry: {entry.key},{entry.value},{entry.address},{entry.priority},{entry.deliveryStatus},{entry.time}")
                        current = current.next
                        continue

                    file.write(f"{entry.key},{entry.value},{entry.address},{entry.priority},{deliveryStatus},{entry.time}\n")
                    current = current.next
            print("Removed items saved to CSV successfully.")
        except Exception as e:
            print(f"Error saving to CSV: {e}")

# this class is a class inheritance of DSAHeap and is used for Dijkstra's algorithm
class DijkstraHeap(DSAHeap):
    def add(self, priority, value):
        try:
            if self.count == self.max_size:
                raise Exception("Heap is full")
            priority = int(priority)
            newEntry = DSAHeapEntryDijkstra(priority, value)
            self.heapArray[self.count] = newEntry
            self.count += 1
            self.trickleUp(self.heapArray, self.count - 1)
        except ValueError:
            print("Error: Priority must be a number.")
        except Exception as e:
            print(f"Error adding to heap: {e}")

    def remove(self):
        try:
            if self.count == 0:
                raise Exception("Heap is empty")
            root = self.heapArray[0]
            self.count -= 1
            self.heapArray[0] = self.heapArray[self.count]
            self.trickleDown(self.heapArray, 0, self.count)
            return root
        except Exception as e:
            print(f"Error removing from heap: {e}")

# this is a class inheritance of DSAHeapEntry which is used for Dijkstra's algorithm
class DSAHeapEntryDijkstra():
    def __init__(self, priority=None, value=None):
        self.priority = priority
        self.value = value

    def getPriority(self):
        return self.priority
    
    def setPriority(self, priority):
        self.priority = priority
    
    def getValue(self):
        return self.value
    
    def setValue(self, value):
        self.value = value


class DSAHeapEntry:
    def __init__(self, key = None, value=None, address=None, priority=None, deliveryStatus=None, time=None):
        self.priority = priority
        self.value = value
        self.time = time
        self.key = key
        self.address = address
        self.deliveryStatus = deliveryStatus


    def getPriority(self):
        return self.priority
    
    def setPriority(self, priority):
        self.priority = priority
    
    def getValue(self):
        return self.value
    
    def setValue(self, value):
        self.value = value
    
    def getTime(self):
        return self.time
    
    def getTime(self, time):
        self.time = time
    
    def getKey(self):
        return self.key
    
    def getAddress(self):
        return self.address

    def setDeliveryStatus(self, deliveryStatus):
        self.deliveryStatus = deliveryStatus

    def getDeliveryStatus(self):
        return self.deliveryStatus

