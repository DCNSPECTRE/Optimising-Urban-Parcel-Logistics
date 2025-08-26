import numpy as np

'''
    This is the hashes.py module
    It implements a hash table using open addressing linear probing (upon collision jump forward a set amount to a new index)
    Linear probing will 'jump' step size of one every time.
    The hash itself is a maximum heap i.e., it sorts the keys in descending order.
    The hash table is made up of DSAHashEntry objects which contain:
    - key: the customer ID
    - value: the customer name
    - address: the customer address
    - priority: the priority level of the customer (1-5)
    - deliveryStatus: the status of the delivery (Delivered, In Transit, Delayed)
    - time: the delivery time

    The hash table supports the following operations:
    - put: adds a new entry or updates an existing entry
    - get: retrieves the value for a given key
    - hasKey: checks if a key exists in the hash table
    - remove: removes an entry by key
    - loadCSV: loads entries from a CSV file
    - saveCSV: saves entries to a CSV file
    - loadFactor: returns the current load factor of the hash table
    - clear: clears the hash table
    - collisionExample: demonstrates how collisions are handled
    - display: prints the contents of the hash table

    The hash table automatically resizes when the load factor exceeds 0.7 or drops below 0.3. The hashing function used is
    a modified version of the djb2 which is the same one used in Java.

    SELF CITING: This code has been adapted from the COMP1002 Practical 07 - Hashes by Muhammad Annas Atif (22224125)

                    Muhammad Annas Atif. 2025. COMP1002 Practical 07 - Hashes.
                        Curtin University, Unpublished.
'''

class DSAHashEntry:
    # the hash entry class stores the key, value, address, priority, delivery status and time
    def __init__(self, key="", value=None, address=None, priority=None, deliveryStatus=None, time=None):
        self.key = key
        self.value = value
        self.state = 0  # 0 = never used, 1 = used, -1 = formerly used/deleted
        self.address = address  
        self.priority = priority  
        self.deliveryStatus = deliveryStatus
        self.time = time

# this class implelements the hash table using open addressing linear probing
class DSAHashTable:
    def __init__(self, tableSize):
        self.count = 0
        self.actualSize = self._nextPrime(tableSize)
        self.hashArray = np.empty(self.actualSize, dtype=object)
        for i in range(self.actualSize):
            self.hashArray[i] = DSAHashEntry()

    # put method to add a new entry or update an entry
    # if the load factor exceeds 0.7 the table is resized to double its size
    def put(self, key, value, address=None, priority=None, deliveryStatus=None, time=None):
        if (self.count + 1) / self.actualSize > 0.7:
            self._resize(self.actualSize * 2)

        # Find the index for the key
        index = self._findSlot(key)
        if self.hashArray[index].state != 1:  # If the slot is not currently used
            self.count += 1
        self.hashArray[index].key = key
        self.hashArray[index].value = value 
        self.hashArray[index].address = address 
        self.hashArray[index].priority = priority 
        self.hashArray[index].deliveryStatus = deliveryStatus
        self.hashArray[index].time = time
        self.hashArray[index].state = 1  # Mark as used

    # get method to retrieve the value for a given key
    # if the key does not exist an exception is raised
    # if the key exists the value is returned
    def get(self, key):
        index = self._findSlot(key)
        if self.hashArray[index].state != 1:
            raise Exception("Key not found")
        return self.hashArray[index].value

    # is used to check if a key exists in the hash table
    def hasKey(self, key):
        index = self._findSlot(key)
        return self.hashArray[index].state == 1

    # remove method to remove an entry by key
    # if the key does not exist an exception is raised
    # if the key exists the entry is marked as deleted
    # if the load factor drops below 0.3 the table is resized to half its size
    # the minimum size of the table is 7 to ensure it does not become too small
    def remove(self, key):
        index = self._findSlot(key)
        if self.hashArray[index].state == 1:
            self.hashArray[index].state = -1
            self.hashArray[index].key = ""
            self.hashArray[index].value = None
            self.hashArray[index].address = None
            self.hashArray[index].priority = None
            self.hashArray[index].deliveryStatus = None
            self.hashArray[index].time = None
            self.count -= 1
            if self.count / self.actualSize < 0.3:
                self._resize(max(7, self.actualSize // 2))

    # this is the hashing function that is based on the djb2 algorithm this is the same one used in Java
    # it takes a key and returns an index in the hash table
    def _hash(self,key):
        table_size = self.actualSize
        hash_idx = 0
        for char in key:
            hash_idx = (31 * hash_idx + ord(char)) & 0xFFFFFFFF 
        return hash_idx % table_size

    # this method finds the slot for a given key using linear probing
    # if inserting is True it returns the index where the key can be inserted
    # if inserting is False it returns the index where the key is found or where it can be inserted
    # if the table is full an exception is raised
    # giveUp is used to prevent infinite loops in case of a full table
    def _findSlot(self, key, inserting=False):
        hashIdx = self._hash(key)
        origIdx = hashIdx
        giveUp = False

        while not giveUp:
            entry = self.hashArray[hashIdx]
            if entry.state == 0:
                if inserting:
                    return hashIdx
                else:
                    return hashIdx
            elif entry.state == 1 and entry.key == key:
                return hashIdx
            else:
                hashIdx = (hashIdx + 1) % self.actualSize
                if hashIdx == origIdx:
                    giveUp = True

        if inserting:
            raise Exception("Hash table is full")
        return hashIdx
    
    # this method resizes the hash table to a new size
    # it creates a new hash array of the new size and rehashes all the entries from the old array
    # it uses the _nextPrime method to ensure the new size is a prime number
    # prime numbers are good at evenly distributing keys in a hash table
    def _resize(self, newSize):
        oldArray = self.hashArray
        oldSize = self.actualSize
        self.actualSize = self._nextPrime(newSize)
        self.hashArray = np.empty(self.actualSize, dtype=object)
        self.count = 0
        for i in range(self.actualSize):
            self.hashArray[i] = DSAHashEntry()

        for i in range(oldSize):
            if oldArray[i].state == 1:
                self.put(oldArray[i].key, oldArray[i].value, oldArray[i].address, oldArray[i].priority, oldArray[i].deliveryStatus, oldArray[i].time)
     
    # this function finds the next primer number that is greater than or equal to n
    # it is used to ensure the hash table size is a prime number
    def _nextPrime(self, n):
        # this is a helper function to check if a number is prime
        def is_prime(x):
            if x < 2: return False # 0 and 1 are not prime numbers
            for i in range(2, int(x**0.5) + 1): # check divisibility up to the square root of x
                if x % i == 0: # if x is divisible by any number other than 1 and itself, it is not prime
                    return False
            return True
        
        # if the number is not a prime number, increment it until a prime is found
        while not is_prime(n):
            n += 1
        return n
    
    # saves teh current hash table to a CSV file
    def saveCSV(self, filename):
        with open(filename, 'w') as file:
            for i in range(self.actualSize):
                entry = self.hashArray[i]
                if entry.state == 1:
                    file.write(f"{entry.key},{entry.value},{entry.address},{entry.priority},{entry.deliveryStatus},{entry.time}\n")

    # loads entries from a CSV file into the hash table
    def loadCSV(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 6:
                        key, value, address, priority, deliveryStatus, time = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]
                        self.put(key, value, address, priority, deliveryStatus, time)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except Exception as e:
            print(f"Failed to load CSV: {e}")
    
    # calculates the load factor of the hash table
    def loadFactor(self):
        return self.count / self.actualSize
    
    # clears the hash table by resetting the count and reinitialising the hash array
    def clear(self):
        self.count = 0
        self.actualSize = 0
        self.actualSize = self._nextPrime(self.actualSize)
        self.hashArray = np.empty(self.actualSize, dtype=object)
        for i in range(self.actualSize):
            self.hashArray[i] = DSAHashEntry()
        print("Hash table cleared.")
    
    # example of how collisions are handled
    def collisionExample(self):
        print("Collision Example:")
        print(self._hash("aa"))
        print(self._hash("ah"))
        self.put("aa", "value1")
        self.put("ah", "value2")
        for i, entry in enumerate(self.hashArray):
            if entry.state == 1:
                print(f"Index {i}: Customer ID: {entry.key}, Name: {entry.value}, Address: {entry.address}, Priority: {entry.priority}, Delivery Status: {entry.deliveryStatus}, Time: {entry.time}")

    # displays the hash table contents
    def display(self):
        print("Hash Table Contents:")
        for i, entry in enumerate(self.hashArray):
            if entry.state == 1:
                print(f"Index {i}: Customer ID: {entry.key}, Name: {entry.value}, Address: {entry.address}, Priority: {entry.priority}, Delivery Status: {entry.deliveryStatus}, Time: {entry.time}")
            elif entry.state == -1:
                print(f"Index {i}: Formerly used")
            else:
                print(f"Index {i}: Empty")

