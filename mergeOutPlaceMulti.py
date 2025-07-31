import numpy as np
import time
import os
import multiprocessing

def mergeSort(array):
    if array.size == 1:
        return array
    q = array.size // 2
    left = mergeSort(array[:q])
    right = mergeSort(array[q:])
    return merge((left, right))

def merge(tupleInfo):
    leftSide = tupleInfo[0]
    rightSide = tupleInfo[1]
    i = j = k = 0
    arr = np.zeros(leftSide.size + rightSide.size, dtype=int)
    k = 0
    while k < arr.size and i < leftSide.size and j < rightSide.size:
        if leftSide[i] <= rightSide[j]:
            arr[k] = leftSide[i]
            i += 1
        else:
            arr[k] = rightSide[j]
            j += 1
        k += 1
    while i < leftSide.size:
        arr[k] = leftSide[i]
        i += 1
        k += 1
    while j < rightSide.size:
        arr[k] = rightSide[j]
        j += 1
        k += 1
    return arr

def multiMergeSort(array):
    numCPU = os.cpu_count() #Get # CPU's in machine
    pool = multiprocessing.Pool(processes=numCPU) #Creates that many processes
    size = int(array.size / numCPU + 1.0) #Divides data into numCPU segments
    dataSet = []
    try: #Attempts to divide evenly with numpy function, but requires array.size % numCPU == 0.
        dataSet = np.split(array, numCPU)
    except: #Otherwise, use custom algorithm to make sublists
        for i in range(numCPU):
            dataSet.append(array[i * size: i * size + size])
    #dataSet is of form [ [0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], ...]
    dataSet = pool.map(mergeSort, dataSet) #Use map function of Pool object to apply mergeSort to each element of dataSet. After this call, each sublist is sorted
    #Goal is to merge adjacent pairs of sublists in dataSet, so need to determine if there is an odd or even number of sublists. For me, it will always be even because numCPU = 4
    extraVal = None
    if len(dataSet) % 2 == 1:
        extraVal = dataSet.pop(-1) #Pop off last sublist if len(dataset) is odd so they can be paired up evenly. This extra value will be merged in at the very end.
        
    #Condense adjacent pairs of sublists into tuples, so 8 sublists will be condensed into 4 tuples. Each tuple passed to merge, which returns the sorted merged array.
    #Now we have 4 sublists, pair them into 2 tuples, merge. Now we have 2 sublists, pair into tuple, merge into one final list. Done
    while len(dataSet) > 1:
        j = 0
        for i in range(int(len(dataSet) / 2)): #Runs one time for each pair of sublists in dataSet. If 8 sublists, will run 4 times.
            dataSet[j] = (dataSet[j], dataSet[j + 1]) #Store tuple of adjacent sublists in the first value. This will be (leftSide, rightSide) tuple passed to merge
            dataSet.pop(j + 1) #Now that dataSet[j] and dataSet[j + 1] both stored in dataSet[j], we can just remove dataSet[j + 1]
            j += 1 #Increment loop control. Since we removed an element, only have to increment by 1 instead of 2 to find the first of the next pair of sublists.
        dataSet = pool.map(merge, dataSet) #Apply merge to each element of dataSet. After this call, the length of dataSet gets halved.
        #Repeat until there is only one left
    finalVal = dataSet[0]
    if extraVal != None: #If there was an odd number of sublists, merge the extra from earlier with the final list we just got.
        finalVal = merge((finalVal, extraVal))
    return np.array(finalVal)
    
    
        

def isSorted(array):
    for i in range(array.size - 1):
        if array[i] > array[i + 1]:
            return False
    return True

#Takes in an integer number of elements, makes random array of that length. Merge sorts it, records time. Repeats 10 times and averages time. Returns list [# elements, avg time]
def callMerge(numElem):
    total = 0
    numExec = 1
    for i in range(numExec):
        array = np.random.randint(0, 10, numElem)
        #print(array)
        clock = time.time()
        array = multiMergeSort(array)
        clock = time.time() - clock
        #print(array)
        if isSorted(array): #If sort successful, record runtime, otherwise decrement i so we can try again
            total += clock
        else:
            i -= 1
    return [numElem, total / numExec]

def getRuntimes(numElemArray):
    returnArr = []
    for elem in numElemArray:
        returnArr.append(callMerge(elem))
    return returnArr

def getRatios(arr): #runtimeArr parameter looks like [ [size, runtime], [size, runtime], ... ]
    return arr[:, 1] / (arr[:, 0] * np.log2(arr[:, 0]))

    
if __name__ == '__main__':
    lengthArray = [1000, 10000, 100000, 1000000, 1500000, 2000000, 2250000, 2500000, 2750000, 3000000]
    res = getRuntimes(lengthArray)
    #ratios = getRatios(res)
    for elem in res:
        print(elem[0])
    print()
    for elem in res:
        print(elem[1])
