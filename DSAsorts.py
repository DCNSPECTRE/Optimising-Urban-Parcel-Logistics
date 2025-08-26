#
# Data Structures and Algorithms COMP1002
#
# Python file to hold all sorting methods
#


'''

    This file contains the implementation of various sorting algorithms.
    - Merge Sort
    - Quick Sort

    Each sorting algorithm is implemented as a function that takes a list of objects
    and sorts them based on a time attribute of the objects. 
    The sorting is done in-place meanin the original list is modified to be sorted.
    The algorithms are designed to work with objects that have a time attribute,
    which is expected to be a numeric value (e.g., float or int).


    SELF CITING: This code has been adapted from the COMP1002 Practial 09 - Advanced Sorting Algorithms by Muhammad Annas Atif (22224125)

                Muhammad Annas Atif. 2025. COMP1002 Practical 09 - Advanced Sorting.
                    Curtin University, Unpublished.
'''


import numpy as np
import random

'''
    This is the merge sort algorithm.
    It recursively divides the list into halves, sorts each half and then merges the sorted halves back together. 
    The merge function combines sublists into a single sorted list.

'''
def mergeSort(A):
    """ mergeSort - front-end for kick-starting the recursive algorithm """
    _mergeSortRecurse(A, 0, len(A) - 1)
    return A

'''
    this is the recursive function for merge sort.
    It divides the list into halves until each half has one element then merges them back together in sorted order.
'''
def _mergeSortRecurse(A, leftIdx, rightIdx):
    if leftIdx < rightIdx:
        midIdx = (leftIdx + rightIdx) // 2

        _mergeSortRecurse(A, leftIdx, midIdx)
        _mergeSortRecurse(A, midIdx + 1, rightIdx)
        merge(A, leftIdx, midIdx, rightIdx)
    
    else:
        return A

'''
    this is the merge function for merge sort.
    It takes two sorted halves of the list and merges them into a single sorted list.
'''
def merge(A, leftIdx, midIdx, rightIdx):
    tempArr = np.empty(rightIdx - leftIdx + 1, dtype=object)
    i = leftIdx
    j = midIdx + 1
    k = 0

    while i <= midIdx and j <=  rightIdx: 
        if float(A[i].time) < float(A[j].time):
            tempArr[k] = A[i]
            i += 1
        else:
            tempArr[k] = A[j]
            j += 1
        k += 1
    
    for i in range(i, midIdx + 1):
        tempArr[k] = A[i]
        k += 1
    
    for j in range(j, rightIdx + 1):
        tempArr[k] = A[j]
        k += 1

    for k in range(leftIdx, rightIdx + 1):
        A[k] = tempArr[k - leftIdx]
    
    return A

'''
    This isthe quick sort algorithm.
    It selects a pivot element and partitions the list into two halves one with elements less than the pivot and one with elements greater than the pivot.
    the algorithm then recursively sorts each half.

'''
def quickSort(A):
    """ quickSort - front-end for kick-starting the recursive algorithm
    """
    _quickSortRecurse(A, 0, len(A) - 1)
    return A

'''
    this is the recursive function for quick sort.
    It selects a pivot element and partitions the list into two halves one with elements less than the pivot and one with elements greater than the pivot.
    The algorithm then recursively sorts each half.

'''
def _quickSortRecurse(A, leftIdx, rightIdx):
    if rightIdx > leftIdx: 
        pivotIdx = leftIdx  
        newPivotIdx = _doPartitioning(A, leftIdx, rightIdx, pivotIdx)

        _quickSortRecurse(A, leftIdx, newPivotIdx - 1)
        _quickSortRecurse(A, newPivotIdx + 1, rightIdx)
    
    else: 
        return A
        
'''
    This function performs the partitioning step of the quick sort algorithm.
    It takes a pivot element and rearranges the elements in the list such that all elements less than the pivot are on the left side and all elements greater than the pivot are on the right side.
'''
def _doPartitioning(A, leftIdx, rightIdx, pivotIdx):
    pivotValTime = float(A[pivotIdx].time)
    pivotVal = A[pivotIdx]

    A[pivotIdx] = A[rightIdx]
    A[rightIdx] = pivotVal

    currIdx = leftIdx

    for i in range(leftIdx, rightIdx):
        if float(A[i].time) < pivotValTime:
            temp = A[currIdx]
            A[currIdx] = A[i]
            A[i] = temp
            currIdx += 1
            
    newPivotIdx = currIdx
    A[rightIdx] = A[newPivotIdx]
    A[newPivotIdx] = pivotVal

    return newPivotIdx

