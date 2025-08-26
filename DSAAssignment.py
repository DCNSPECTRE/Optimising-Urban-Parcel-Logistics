from graphs import DSAGraph
from hashes import DSAHashTable
from heaps import DSAHeap, DSAHeapEntry
from linkedlists_main import *
from stacksandqueues import *
from DSAsorts import *
import time as tme
import sys

'''

    DSAAssignment.py
    Student ID: 22224125
    Name: Muhammad Annas Atif
    Completed: 27/05/2025
    
    Details:
    This is the main assignment run file for the 2025 Semester 1 COMP1002 - Data Strucutres and Algorithms Final Assignment
    Run this file to access all of the featuresets of the assignment.

    Contains:
    1. loadCSVTestCases
    2. arrayConversion
    3. graphRoutePlanning
    4. hashCustomerLookup
    5. heapParcelScheduling
    6. sortDeliveryRecords
    7. testCases
    8. main

'''

# Set the recursion limit to a higher value to allow for 1000 element sorting in the test cases.
sys.setrecursionlimit(2000)

'''
Loads CSV file for test cases. Takes the CSV file and takes lines from the desired start to end line.
Returns a linked list of DSAHeapEntry objects. This method allows it to keep the other data for the test cases such as priority, delivery status, customer ID, etc.
It also allows me to integrate it with my modified DSASorts file.

It inputs the filename, the start line and end line.
It outputs the linked list of DSAHeapEntry objects.

'''
def loadCSVTestCases(self, filename, start, end):
    CSVrecords = DSALinkedList()
    lineNumber = 0
    # This will check to see if the file exists and if not, it will raise a FileNotFoundError and give a message.
    try:
        with open(filename, 'r') as file:
            for line in file:
                lineNumber += 1 # This will increment the line number for each line read
                # This will check the bounds of the readzone
                if lineNumber < start:
                    continue
                if lineNumber > end:
                    print("Reached end of read zone.")
                    break

                parts = line.strip().split(',') # This will split the line by commas
                # This will check if the line has the correct number of parts and raise an error if it does not and skip the line
                if len(parts) == 6:
                    key = parts[0]
                    value = parts[1]
                    address = parts[2]
                    priority = parts[3]
                    deliveryStatus = parts[4]
                    time = parts[5]

                    #This will check if the priority and time are valid inputs, partiularly for the priority calculation function in the heaps.py file.
                    #This is done to consider importing cases where prioirity has not been calcualted yet.
                    try:
                        priority = float(priority)
                        time = float(time)

                        if priority.is_integer() == True:
                            priority = int(priority)
                            priority = self.priorityCalculation(priority, time)
                            
                    except ValueError:
                        print("Skipping invalid line.")
                    deliveryStatus = "Delivered"

                    # Create a DSAHeapEntry object and insert it into the linked list
                    entry = DSAHeapEntry(key, value, address, priority, deliveryStatus, time)
                    CSVrecords.insertLast(entry)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"Failed to load CSV: {e}")
    return CSVrecords

'''# This converts the linked list of DSAHeapEntry objects to a numpy array from the above function'''
def arrayConversion(array):
    CSVrecords = array
    if CSVrecords is None or CSVrecords.isEmpty():
        print("Check CSV File.")
    
    #Sets teh size of the array to the number of elements in the linked list
    elements = CSVrecords.size

    #begins the conversion to the numpy array at the head of teh linked list and increments through the list until the end and returns the numpy array
    currentNode = CSVrecords.head
    idx = 0
    sortingArray = np.empty(elements, dtype=object)
    while currentNode is not None and idx < elements:
        sortingArray[idx] = currentNode.getValue()
        currentNode = currentNode.getNext()
        idx += 1
    
    return sortingArray

'''
    This is the function that runs the Graph Based Route Planning Module (Module 1)
    It gives the user a menu which allows them to add and remove both Hubs and Routes
    It also give the user the ability to show the structure of the graph as a list/matrix
    Also allows for BFS and DFS search and the shortest path which has been sourced from
    https://www.geeksforgeeks.org/introduction-to-dijkstras-shortest-path-algorithm/

    There is also a test graph that is used to demo the requirements as outlined in the tasksheet

    This module is linked with the graphs.py file which contains all of the actual functions of the menu.
'''
def graphRoutePlanning(graph):
    while True:
        print("\n======================================= Graph Based Route Planning =======================================")
        print("1. Add Location/Hub/Intersection (Vertex)")
        print("2. Add Route (Edge)")
        print("3. Delete Location (Vertex)")
        print("4. Delete Route (Edge)")
        print("5. Display as List")
        print("6. Display as Matrix")
        print("7. Breadth-First Search")
        print("8. Depth-First Search")
        print("9. Dijkstra's Shortest Path")
        print("10. Test Graph")
        print("11. Clear Graph")
        print("12. Back to Main Menu")
        choice = input("Select option: ")
        try:
            if choice == "1":
                label = input("Enter location name: ")
                graph.addVertex(label)
                print(f"Location '{label}' added.")
            elif choice == "2":
                fromLabel = input("From location: ")
                toLabel = input("To location: ")
                while True:
                    try:
                        weight = int(input("Distance/weight: "))
                        if weight <= 0:
                            print("Weight must be a positive integer.")
                            continue
                        break
                    except ValueError:
                        print("Invalid input. Please enter a positive integer for the weight.")
                graph.addEdge(fromLabel, toLabel, weight)
                print(f"Route from '{fromLabel}' to '{toLabel}' added.")   
            elif choice == "3":
                label = input("Enter vertex label to delete: ")
                graph.deleteVertex(label)
                print(f"Vertex '{label}' deleted.")
            elif choice == "4":
                fromLabel = input("Enter from vertex label: ")
                toLabel = input("Enter to vertex label: ")
                graph.deleteEdge(fromLabel, toLabel)
                print(f"Edge deleted between '{fromLabel}' and '{toLabel}'.")  
            elif choice == "5":
                graph.displayAsList()
            elif choice == "6":
                graph.displayAsMatrix()
            elif choice == "7":
                start = input("Start location: ")
                graph.BFS(start)
            elif choice == "8":
                start = input("Start location: ")
                graph.DFS(start)
            elif choice == "9":
                start = input("Start location: ")
                graph.dijkstra(start)
            elif choice == "10":
                    '''
                    This is the test graph and below you can see that the function will output the test case and demonstrate the requirements of the tasksheet
                    '''
                    print("\n=======================================\nTesting Logistics Network Graph:\n=======================================")
                    print("Creating a sample graph with vertices and edges...\n")
                    print("City Hubs / Intersections: A, B, C, D, E, F, G, M")
                    print("Roads / Paths: A-B, A-D, A-C, B-E, E-F, E-G, F-G, D-F, D-C")
                    print("Travel Times (in minutes): A-B: 10, A-D: 1, A-C: 2, B-E: 1, E-F: 5, E-G: 12, F-G: 2, D-F: 8, D-C: 7")
                    print("Disconnected City Hub: M")
                    print("Cycle: A-B-E-F-D-A from Hub A")
                    print("Cycle: A-B-E-F-D-C-A from Hub A")
                    print("=======================================")
                    print("Creating the graph...\n")

                    graph.addVertex("A")
                    graph.addVertex("B")
                    graph.addVertex("C")
                    graph.addVertex("D")
                    graph.addVertex("E")
                    graph.addVertex("F")
                    graph.addVertex("G")
                    graph.addVertex("M")

                    graph.addEdge("A", "B", 10)
                    graph.addEdge("A", "D", 1)
                    graph.addEdge("A", "C", 2)
                    graph.addEdge("B", "E", 1)
                    graph.addEdge("E", "F", 5)
                    graph.addEdge("E", "G", 12)
                    graph.addEdge("F", "G", 2)
                    graph.addEdge("D", "F", 8)
                    graph.addEdge("D", "C", 7)

                    graph.displayAsList()
                    graph.displayAsMatrix()
                    # Test BFS and DFS
                    graph.BFS("A")
                    graph.DFS("A")
                    graph.dijkstra("A")
                    print("\nGraph test completed.")
            elif choice == "11":
                graph.clearGraph()
            elif choice == "12":
                break
            else:
                print("Invalid option.")
        except Exception as e:
            print("Error:", e)


'''
    This is function runs the hash based customer look up for module 2.
    It inputs the respective hash table, a heap for Dijkstra's shortest path algorithm and the actual graph of interest.

    This module interface allows users to add/update/remove customers, and check there existance. It also shows the load
    factor of the heap.

    It also allows for the clearing of the hashtable, loading one from a CSV, saving one to a CSV and displaying.

    This module also allows interoperability with Module 3 i.e., you can bring data from module 3 back into this module.

    There is also a collision example which is a requirement of the tasksheet 
'''

def hashCustomerLookup(hashTable, heap, graph):
    while True:
        print("\n======================================= Hash Based Customer Look Up =======================================")
        print("1. Add/Update Customer")
        print("2. Look Up Customer")
        print("3. Remove Customer")
        print("4. Check Customer Exists")
        print("5. Show Load Factor")
        print("6. Clear Hash Table")
        print("7. Load from CSV")
        print("8. Save to CSV") 
        print("9. Collision Example")
        print("10. Display Hash Table")
        print("11. Load from Module Three")
        print("12. Back to Main Menu")
        choice = input("Select option: ")
        try:
            if choice == "1":
                while True:
                    graph.displayAsList()
                    print("=======================================")
                    startNode = input("Start Node: ")
                    if not startNode or "," in startNode:
                        print("Start node cannot be blank and cannot contain commas.")
                        continue
                    key = input("Customer ID: ")
                    if not key or "," in key:
                        print("Customer ID cannot be blank and cannot contain commas.")
                        continue
                    name = input("Name: ")
                    if not name or "," in name:
                        print("Name cannot be blank and cannot contain commas.")
                        continue
                    # The module does a sanity check to see if there even is a graph that has been intiialised
                    address = input("Address: ")
                    startVertex = graph.getVertex(startNode)
                    if not startVertex or "," in startNode:
                        print(f"Start node: {startNode} not found. Please setup the graph. Use OPTION 8 in the Route Planning Module")
                        break
                    # There is a sanity check here too to see if there is a valid destination. It does this by checking to see if the destination
                    # is an element by using the "getVertex" function in the graphs.py file, and it then confirms it is reachable from the starting node
                    # by using dijkstra's shortest path algorithm nd checking if the time is not equal to infinity, which indicates no connection.
                    # it also outputs the time taken to reach the destination which goes into the hashtable put function
                    # if the checks fail then it outputs an error via exception handling
                    targetVertex = graph.getVertex(address)
                    if not targetVertex or "," in address:
                        print(f"Address: {address} not found in the graph. Valid locations are:")
                        graph.displayAsList()
                        continue
                    if address == startNode:
                        print(f"Address cannot be start hub {startNode}. Please choose a destination")
                        continue
                    try:
                        graph.dijkstra(startNode)
                        time = targetVertex.distance

                        if time == float('inf'):
                            print(f"Address: {address} is unreachable from {startNode}. Please choose a reachable destintion.")
                            continue
                        print(f"Calculated Time: {time} minutes.")
                    except Exception as e:
                        print(f"Error during route calculation: {e}")
                        continue
                    # ensures the priority remains in the set range of 1 to 5 as dictated in the assignment tasksheet.
                    # raises and error if it is not in the range
                    try:
                        priority = int(input("Priority (1-5): "))
                        if priority < 1 or priority > 5:
                            print("Priority must be an integer between 1 and 5.")
                            continue
                    except ValueError:
                        print("Priority must be an integer between 1 and 5.")
                        continue
                    # as per the dynamic status check as outlined in module 2's description in the task sheet
                    # adding a parcel means it has not been delivered yet
                    status = "Not Delivered"
                    break
                # If the start node exists, then we add all the above collected info into the hashtable
                if graph.getVertex(startNode):
                    hashTable.put(key, name, address, priority, status, time)
                    print("Customer added/updated.")
            # Retreives customer by customer ID
            elif choice == "2":
                key = input("Customer ID: ")
                print("Customer:", hashTable.get(key))
            # removed customer via customer ID
            elif choice == "3":
                key = input("Customer ID: ")
                hashTable.remove(key)
                print("Customer removed.")
            # Checks the existence of customer via ID
            elif choice == "4":
                key = input("Customer ID: ")
                print("Exists" if hashTable.hasKey(key) else "Does not exist")
            # Load factor of heap
            elif choice == "5":
                print(f"Load Factor: {hashTable.loadFactor()}")
            # clears hash table
            elif choice == "6":
                hashTable.clear()
                print("Hash table cleared.")
            # loads a hashtable from a CSV file
            elif choice == "7":
                filename = input("Enter CSV filename to load: ")
                hashTable.loadCSV(filename)
                print("Hash table loaded from CSV.")
            # saves the hash table to a CSV file
            elif choice == "8":
                filename = input("Enter CSV filename to save: ")
                hashTable.saveCSV(filename)
                print("Hash table saved to CSV.")
            # collision example which is defined by the collisionExample function in hashes.py
            elif choice == "9":
                print("=========================================================")
                ht = DSAHashTable(7)
                ht.collisionExample()
                ht.clear()
                print("=========================================================")
            # displays teh hash table
            elif choice == "10":
                print("=========================================================")
                print("Current Hash Table:")
                print("=========================================================")   
                hashTable.display()
                print("=========================================================")   
            # clears the existing hash table and loads data from module 3
            elif choice == "11":
                hashTable.clear()
                for i in range(heap.count):
                    hashTable.put(heap.heapArray[i].key,heap.heapArray[i].value,heap.heapArray[i].address,heap.heapArray[i].priority,heap.heapArray[i].deliveryStatus,heap.heapArray[i].time)
            elif choice == "12":
                break
            else:
                print("Invalid option.")
        except Exception as e:
            print("Error:", e)

'''
    This function runs the menu for module 3 of the assignment which is the heap based parcel scheduling
    
    It inputs the heap, the hash table for module interoperability and the graph for interoperability between modules 1 and 2.

    The user is given the option to add a parcel manually without going back to the hash table

    The user can also remove parcels of the highest CALCULATED priority and then set the delievery status to "delivered", then it adds
    the delivered parcel to a separate linkedlist as defined in the heaps extract() function, where the delivery records can later be exported for record keeping and sorting.

    The user can also display the heap, and import data for heap sorting through a CSV file and they can also export the sorted heap to a CSV.

    The user can also call info from Module 2 without doing CSV imports for module interoperability.

    Finally the user can save the removed items as mentioned earlier to a CSV file for sorting and record keeping

    *Note: Heap sorting is done on a Max Heap --> higher prioirity items favored so we can easily remove the highest priority delivery instead of reversing the order 
    if a min heap was to be used.
'''

def heapParcelScheduling(heap, hashTable, graph):
    while True:
        print("\n======================================= Heap Based Parcel Scheduling =======================================")
        print("1. Add Parcel")
        print("2. Remove Highest Priority Parcel (Delivered Package)")
        print("3. Display Heap")
        print("4. Load from CSV")
        print("5. Save to CSV")
        print("6. Load from Module Two")
        print("7. Save removed items to CSV")
        print("8. Back to Main Menu")

        choice = input("Select option: ")
        try:
            # This is for adding parcels manually to the heap instead of taking them from the Hash Table.
            # It checks for blank inputs which it will deny and re-ask for an input similar to the previous modules.
            # It will also cehcek for valid start and end nodes using Dijkstra's algorithm.
            # It will also check to ensure there is actually a graph loaded.
            if choice == "1":
                while True:
                    graph.displayAsList()
                    print("=======================================")
                    startNode = input("Start Node: ")
                    if not startNode or "," in startNode:
                        print("Start node cannot be blank.")
                        continue
                    key = input("Customer ID: ")
                    if not key or "," in key:
                        print("Customer ID cannot be blank.")
                        continue
                    name = input("Name: ")
                    if not name or "," in name:
                        print("Name cannot be blank.")
                        continue
                    # Check for graph even existing
                    address = input("Address: ")
                    startVertex = graph.getVertex(startNode)
                    if not startVertex:
                        print(f"Start node: {startNode} not found. Please setup the graph. Use OPTION 8 in the Route Planning Module")
                        break
                    # check for valid destinations and determine the time for that distance such that it can be inputted into the heap insert function
                    targetVertex = graph.getVertex(address)
                    if not targetVertex:
                        print(f"Address: {address} not found in the graph. Valid locations are:")
                        graph.displayAsList()
                        continue
                    if address == startNode:
                        print(f"Address cannot be start hub {startNode}. Please choose a destination")
                        continue
                    try:
                        graph.dijkstra(startNode)
                        time = targetVertex.distance

                        if time == float('inf'):
                            print(f"Address: {address} is unreachable from {startNode}. Please choose a reachable destintion.")
                            continue
                        print(f"Calculated Time: {time} minutes.")
                    except Exception as e:
                        print(f"Error during route calculation: {e}")
                        continue
                    #check that the customer prioirity is between 1 and 5 before it is processed using the formula to find delivery priority. 
                    try:
                        priority = int(input("Priority (1-5): "))
                        if priority < 1 or priority > 5:
                            print("Priority must be an integer between 1 and 5.")
                            continue
                    except ValueError:
                        print("Priority must be an integer between 1 and 5.")
                        continue
                    #set the deliverys status to in-transit when heap sorted.
                    status = "In Transit"
                    break
                if graph.getVertex(startNode):
                    heap.insert(key, name, address, priority, status, time)
                    print("Customer added/updated.")
                #The required heap outputs on each addition to the heap
                print("Parcel added.")
                print("=======================================================================")
                print(f"Customer ID: {key} | Priority: {heap.priorityCalculation(priority, time)}, Delivery Time: {time}, Customer Priority: {priority}")
                print("=======================================================================")
                print("Current Heap:")
                print("=======================================================================")
                heap.display()
            
            # the extract function removes the highest prioirty item on each extraction. This is then printed
            # The extract function will store the removed delivery in a linked list as outlined in heaps.py
            # which is why it also prints that "Removed item saved for export"
            elif choice == "2":
                removed = heap.extract()
                if removed:
                    print("Removed parcel:")
                    print("=======================================================================")
                    print(f"Removed: Priority: {removed.priority}, Customer ID: {removed.value}, Delivery Time: {removed.time}")
                    print("=======================================================================")
                    print("Current Heap after removal:")
                    print("=======================================================================")
                    heap.display()
                    print("=======================================================================")
                    print("Removed item saved for export.")
                    print("=======================================================================")
                else:
                    print("Heap is empty.")
            # prints the current heap
            elif choice == "3":
                print("========================================================================")
                print("Current Heap:")
                print("=======================================================================")
                heap.display()
            # Loads heap from a CSV File
            elif choice == "4":
                filename = input("Enter CSV filename to load: ")
                heap.loadCSV(filename)
                print("Heap loaded from CSV.")
            # Saves heap to CSV file
            elif choice == "5":
                filename = input("Enter CSV filename to save: ")
                heap.saveCSV(filename)
                print("Heap saved to CSV.")
            # this function loads data from module 2
            elif choice == "6":
                for i, entry in enumerate(hashTable.hashArray):
                    if entry.state == 1: # Check if the heap entry is active
                        # since we are potentially working with priorities that may have already been processed, the algorithm here checks to see if we need to reprocess the priority
                        # if it finds that the priority is an integer it will convert it to the calculated priority using the heap.priorityCalculation function
                        # if it is already a float it will just add it to the heap
                        try:
                            priority = float(entry.priority)
                            time = float(entry.time)
                            if priority.is_integer() == True:
                                customerPriority = int(entry.priority)
                                priority = heap.priorityCalculation(customerPriority, time)
                        except ValueError:
                            print("Skipping invalid entries.")
                        #defines the delivery status as in-transit as per the tasksheet requirementsfor dynamic status updates
                        deliveryStatus = "In-Transit"
                        heap.addFromHashes(entry.key, entry.value, entry.address, priority, deliveryStatus, entry.time)
                print("Data Loaded.")
            # saves the removed heap items (delivered) to a CSV file
            elif choice == "7":
                filename = input("Enter CSV filename to save: ")
                heap.saveRemovedItemsToCSV(filename)
                print("Heap saved to CSV.")    
            elif choice == "8":
                break
            else:
                print("Invalid option.")
        except Exception as e:
            print("Error:", e)

'''
    This is is one part of module 4 which is the sorting of delivery records.

    It allows the user to sort the delivery records from module 3

    It inputs the heap which contains the delivery records and allows the user to sort them using Quick Sort and Merge Sorts.

    It inputs the heap and uses the heapArray to get the delivery records.

    It then outputs the sorted records as well as the time it took to sort them.

'''

def sortDeliveryRecords(heap):
    if heap.isEmpty():
        print("\nNo delivery records to sort (Heap is empty).")
        return

    recordsArray = np.copy(heap.heapArray[0:heap.count])

    while True:
        print("\n======================================================================== Sort Delivery Records Menu ========================================================================")
        print("1. Merge Sort")
        print("2. Quick Sort")
        print("3. Back to Main Menu")
        choice = input("Select an option (1-3): ")

        sortedArray = None
        sortableArray = None # initialise the sortable array
        sortTime = 0.0 
        sortableArray = np.copy(recordsArray) # makes a fresh copy of the records array to sort

        if choice == "1":
            print("\n======================================================================== Sorting using Merge Sort ========================================================================")
            startTime = tme.time() # starts the timer
            sortedArray = mergeSort(sortableArray) # runs the sort on the array that has been formatted for sorting
            endTime = tme.time() # ends the timer
            sortTime = endTime - startTime # calculates the time by taking the difference in time
            print(f"Merge Sort complete in {sortTime} seconds.") # prints the time taken to sort the array
        elif choice == "2":
            print("\n======================================================================== Sorting using Quick Sort ========================================================================")
            startTime = tme.time() # starts the timer
            sortedArray = quickSort(sortableArray) # runs the sort on the array that has been formatted for sorting
            endTime = tme.time() # ends the timer
            sortTime = endTime - startTime # calculates the time by taking the difference in time
            print(f"Quick Sort complete in {sortTime} seconds.") # prints the time taken to sort the array
        elif choice == "3":
            break
        else:
            print("Invalid choice.")
            continue
        
        # If the sorted array is not the default initialsied state i.e., not None/empty, then it will print the sorted array.
        if sortedArray is not None and len(sortedArray) > 0:
            print("\n======================================================================== Sorted Delivery Records (by Time) ========================================================================")
            # This will iterate through each element of the sorted array which is a DSAHeapEntry object
            # it will then extract the priority, time, key, value, address and delivery status from the object
            # and print them in a formatted manner
            for record in sortedArray:
                try:
                    priority = float(record.priority)
                    deliveryTime = float(record.time)
                    print(f" Time: {deliveryTime} | Customer ID: {record.key}, Name: {record.value}, Addr: {record.address}, Priority: {priority}")
                except (ValueError, TypeError):
                    print(f"Invalid data.")
            print("======================================================================================================================================================================================")

        elif sortedArray is not None:
             print("Sorted array is empty.")

'''
    This is the second half of the module 4 which is the test cases for the sorting algorithms

    It allows the user to test the sorting algorithms on different sets of data from a CSV file

    It inputs the heap and the CSV filename to load the test cases from

    It then loads the test cases from the CSV file and converts them to an array for sorting.

    It then outputs the sorted records as well as the time it took to sort them.

    The CSV file is read using the loadCSVTestCases function which then converts the records, a linked list of DSAHeapEntry objects, to a numpy array for sorting.
'''

def testCases(heap):
    print("======================================================================== TEST CASES ========================================================================")
    filename = input("Enter CSV filename: ")

    while True:
        print("1. 100 Items Sorts")
        print("2. 500 Items Sorts")
        print("3. 1000 Item Sorts")
        print("4. Back to Menu")
        choice = input("Select an option (1-4): ")


        '''
            This first choice will run the quick and merge sorts on the first 3 sets of 100 items of the CSV file.
            This will results in three sets of data being sorted:
                1. Random Order Data
                2. Nearly Sorted Data
                3. Reverse Data 
            It will then print the sorted records and the time it took to sort them.

        '''
        if choice == "1":
            CSVRecords = loadCSVTestCases(heap, filename, 2, 101)
            testArray = arrayConversion(CSVRecords)

            startTime = tme.time()
            sortedArray = mergeSort(testArray)
            endTime = tme.time()
            sortTime = endTime - startTime
            print("\n================================================================================================================================================")
            print(f"Merge sort complete in {sortTime} - Random Order Data")
            print("================================================================================================================================================")
            for record in sortedArray:
                priority = float(record.priority)
                deliveryTime = float(record.time)
                print(f" Time: {deliveryTime} | Customer ID: {record.key}, Name: {record.value}, Addr: {record.address}, Priority: {priority}")


            startTime = tme.time()
            sortedArray = quickSort(testArray)
            endTime = tme.time()
            sortTime = endTime - startTime
            print("\n================================================================================================================================================")
            print(f"Quick sort complete in {sortTime} - Random Order Data")
            print("================================================================================================================================================")
            for record in sortedArray:
                priority = float(record.priority)
                deliveryTime = float(record.time)
                print(f" Time: {deliveryTime} | Customer ID: {record.key}, Name: {record.value}, Addr: {record.address}, Priority: {priority}")
            print("================================================================================================================================================")

            CSVRecords = loadCSVTestCases(heap, filename, 104, 203)
            testArray = arrayConversion(CSVRecords)

            startTime = tme.time()
            sortedArray = mergeSort(testArray)
            endTime = tme.time()
            sortTime = endTime - startTime
            print("\n================================================================================================================================================")
            print(f"Merge sort complete in {sortTime} - Nearly Sorted Data")
            print("================================================================================================================================================")
            for record in sortedArray:
                priority = float(record.priority)
                deliveryTime = float(record.time)
                print(f" Time: {deliveryTime} | Customer ID: {record.key}, Name: {record.value}, Addr: {record.address}, Priority: {priority}")

            startTime = tme.time()
            sortedArray = quickSort(testArray)
            endTime = tme.time()
            sortTime = endTime - startTime
            print("\n================================================================================================================================================")
            print(f"Quick sort complete in {sortTime} - Nearly Sorted Data")
            print("================================================================================================================================================")
            for record in sortedArray:
                priority = float(record.priority)
                deliveryTime = float(record.time)
                print(f" Time: {deliveryTime} | Customer ID: {record.key}, Name: {record.value}, Addr: {record.address}, Priority: {priority}")
            print("================================================================================================================================================")

            CSVRecords = loadCSVTestCases(heap, filename, 206, 305)
            testArray = arrayConversion(CSVRecords)

            startTime = tme.time()
            sortedArray = mergeSort(testArray)
            endTime = tme.time()
            sortTime = endTime - startTime
            print("\n================================================================================================================================================")
            print(f"Merge sort complete in {sortTime} - Reverse Data")
            print("================================================================================================================================================")
            for record in sortedArray:
                priority = float(record.priority)
                deliveryTime = float(record.time)
                print(f" Time: {deliveryTime} | Customer ID: {record.key}, Name: {record.value}, Addr: {record.address}, Priority: {priority}")

            startTime = tme.time()
            sortedArray = quickSort(testArray)
            endTime = tme.time()
            sortTime = endTime - startTime
            print("\n================================================================================================================================================")
            print(f"Quick sort complete in {sortTime} - Reverse Data")
            print("================================================================================================================================================")
            for record in sortedArray:
                priority = float(record.priority)
                deliveryTime = float(record.time)
                print(f" Time: {deliveryTime} | Customer ID: {record.key}, Name: {record.value}, Addr: {record.address}, Priority: {priority}")
            print("================================================================================================================================================")
        
        '''
            This second choice will run the quick and merge sorts on the subsequent 3 sets of 500 items of the CSV file.
            This will results in three sets of data being sorted:
                1. Random Order Data
                2. Nearly Sorted Data
                3. Reverse Data 
            It will then print the sorted records and the time it took to sort them.

        '''
        if choice == "2":
            CSVRecords = loadCSVTestCases(heap, filename, 308, 807)
            testArray = arrayConversion(CSVRecords)

            startTime = tme.time()
            sortedArray = mergeSort(testArray)
            endTime = tme.time()
            sortTime = endTime - startTime
            print("\n================================================================================================================================================")
            print(f"Merge sort complete in {sortTime} - Random Order Data")
            print("================================================================================================================================================")
            for record in sortedArray:
                priority = float(record.priority)
                deliveryTime = float(record.time)
                print(f" Time: {deliveryTime} | Customer ID: {record.key}, Name: {record.value}, Addr: {record.address}, Priority: {priority}")


            startTime = tme.time()
            sortedArray = quickSort(testArray)
            endTime = tme.time()
            sortTime = endTime - startTime
            print("\n================================================================================================================================================")
            print(f"Quick sort complete in {sortTime} - Random Order Data")
            print("================================================================================================================================================")
            for record in sortedArray:
                priority = float(record.priority)
                deliveryTime = float(record.time)
                print(f" Time: {deliveryTime} | Customer ID: {record.key}, Name: {record.value}, Addr: {record.address}, Priority: {priority}")
            print("================================================================================================================================================")

            CSVRecords = loadCSVTestCases(heap, filename, 810, 1309)
            testArray = arrayConversion(CSVRecords)

            startTime = tme.time()
            sortedArray = mergeSort(testArray)
            endTime = tme.time()
            sortTime = endTime - startTime
            print("\n================================================================================================================================================")
            print(f"Merge sort complete in {sortTime} - Nearly Sorted Data")
            print("================================================================================================================================================")
            for record in sortedArray:
                priority = float(record.priority)
                deliveryTime = float(record.time)
                print(f" Time: {deliveryTime} | Customer ID: {record.key}, Name: {record.value}, Addr: {record.address}, Priority: {priority}")

            startTime = tme.time()
            sortedArray = quickSort(testArray)
            endTime = tme.time()
            sortTime = endTime - startTime
            print("\n================================================================================================================================================")
            print(f"Quick sort complete in {sortTime} - Nearly Sorted Data")
            print("================================================================================================================================================")
            for record in sortedArray:
                priority = float(record.priority)
                deliveryTime = float(record.time)
                print(f" Time: {deliveryTime} | Customer ID: {record.key}, Name: {record.value}, Addr: {record.address}, Priority: {priority}")
            print("================================================================================================================================================")

            CSVRecords = loadCSVTestCases(heap, filename, 1312, 1811)
            testArray = arrayConversion(CSVRecords)

            startTime = tme.time()
            sortedArray = mergeSort(testArray)
            endTime = tme.time()
            sortTime = endTime - startTime
            print("\n================================================================================================================================================")
            print(f"Merge sort complete in {sortTime} - Reverse Data")
            print("================================================================================================================================================")
            for record in sortedArray:
                priority = float(record.priority)
                deliveryTime = float(record.time)
                print(f" Time: {deliveryTime} | Customer ID: {record.key}, Name: {record.value}, Addr: {record.address}, Priority: {priority}")

            startTime = tme.time()
            sortedArray = quickSort(testArray)
            endTime = tme.time()
            sortTime = endTime - startTime
            print("\n================================================================================================================================================")
            print(f"Quick sort complete in {sortTime} - Reverse Data")
            print("================================================================================================================================================")
            for record in sortedArray:
                priority = float(record.priority)
                deliveryTime = float(record.time)
                print(f" Time: {deliveryTime} | Customer ID: {record.key}, Name: {record.value}, Addr: {record.address}, Priority: {priority}")
            print("================================================================================================================================================")

        '''
            This first choice will run the quick and merge sorts on the subsequent 3 sets of 1000 items of the CSV file.
            This will results in three sets of data being sorted:
                1. Random Order Data
                2. Nearly Sorted Data
                3. Reverse Data 
            It will then print the sorted records and the time it took to sort them.

        '''
        if choice == "3":
            CSVRecords = loadCSVTestCases(heap, filename, 1814, 2813)
            testArray = arrayConversion(CSVRecords)

            startTime = tme.time()
            sortedArray = mergeSort(testArray)
            endTime = tme.time()
            sortTime = endTime - startTime
            print("\n================================================================================================================================================")
            print(f"Merge sort complete in {sortTime} - Random Order Data")
            print("================================================================================================================================================")
            for record in sortedArray:
                priority = float(record.priority)
                deliveryTime = float(record.time)
                print(f" Time: {deliveryTime} | Customer ID: {record.key}, Name: {record.value}, Addr: {record.address}, Priority: {priority}")


            startTime = tme.time()
            sortedArray = quickSort(testArray)
            endTime = tme.time()
            sortTime = endTime - startTime
            print("\n================================================================================================================================================")
            print(f"Quick sort complete in {sortTime} - Random Order Data")
            print("================================================================================================================================================")
            for record in sortedArray:
                priority = float(record.priority)
                deliveryTime = float(record.time)
                print(f" Time: {deliveryTime} | Customer ID: {record.key}, Name: {record.value}, Addr: {record.address}, Priority: {priority}")
            print("================================================================================================================================================")

            CSVRecords = loadCSVTestCases(heap, filename, 2816, 3815)
            testArray = arrayConversion(CSVRecords)

            startTime = tme.time()
            sortedArray = mergeSort(testArray)
            endTime = tme.time()
            sortTime = endTime - startTime
            print("\n================================================================================================================================================")
            print(f"Merge sort complete in {sortTime} - Nearly Sorted Data")
            print("================================================================================================================================================")
            for record in sortedArray:
                priority = float(record.priority)
                deliveryTime = float(record.time)
                print(f" Time: {deliveryTime} | Customer ID: {record.key}, Name: {record.value}, Addr: {record.address}, Priority: {priority}")

            startTime = tme.time()
            sortedArray = quickSort(testArray)
            endTime = tme.time()
            sortTime = endTime - startTime
            print("\n================================================================================================================================================")
            print(f"Quick sort complete in {sortTime} - Nearly Sorted Data")
            print("================================================================================================================================================")
            for record in sortedArray:
                priority = float(record.priority)
                deliveryTime = float(record.time)
                print(f" Time: {deliveryTime} | Customer ID: {record.key}, Name: {record.value}, Addr: {record.address}, Priority: {priority}")
            print("================================================================================================================================================")

            CSVRecords = loadCSVTestCases(heap, filename, 3818, 4817)
            testArray = arrayConversion(CSVRecords)

            startTime = tme.time()
            sortedArray = mergeSort(testArray)
            endTime = tme.time()
            sortTime = endTime - startTime
            print("\n================================================================================================================================================")
            print(f"Merge sort complete in {sortTime} - Reverse Data")
            print("================================================================================================================================================")
            for record in sortedArray:
                priority = float(record.priority)
                deliveryTime = float(record.time)
                print(f" Time: {deliveryTime} | Customer ID: {record.key}, Name: {record.value}, Addr: {record.address}, Priority: {priority}")

            startTime = tme.time()
            sortedArray = quickSort(testArray)
            endTime = tme.time()
            sortTime = endTime - startTime
            print("\n================================================================================================================================================")
            print(f"Quick sort complete in {sortTime} - Reverse Data")
            print("================================================================================================================================================")
            for record in sortedArray:
                priority = float(record.priority)
                deliveryTime = float(record.time)
                print(f" Time: {deliveryTime} | Customer ID: {record.key}, Name: {record.value}, Addr: {record.address}, Priority: {priority}")
            print("================================================================================================================================================")


        elif choice == "4":
            break    
            

'''
    This is the main function that runs the program.
    It creates the graph, hash table and heap objects and then displays the main menu.
    It then calls the appropriate functions based on the user's choice.
'''
def main():
    graph = DSAGraph()
    hashTable = DSAHashTable(1)
    heap = DSAHeap(100)

    while True:
        print("\n--- Delivery System Main Menu ---")
        print("1. Graph Based Route Planning")
        print("2. Hash Based Customer Look Up")
        print("3. Heap Based Parcel Scheduling")
        print("4. Sorting Delivery Records")
        print("5. Test Sorts")
        print("6. Exit")
        choice = input("Select an option (1-5): ")
        if choice == "1":
            graphRoutePlanning(graph)
        elif choice == "2":
            hashCustomerLookup(hashTable, heap, graph)
        elif choice == "3":
            heapParcelScheduling(heap, hashTable,graph)
        elif choice == "4":
            sortDeliveryRecords(heap)
        elif choice == "5":
            testCases(heap)
        elif choice == "6":
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please select from 1-5.")

if __name__ == "__main__":
    main()
