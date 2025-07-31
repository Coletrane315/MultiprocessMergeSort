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
def callMerge(numElem, funcVariant):
    if numElem % 10000 == 0:
        print("Still working")
    total = 0
    numExec = 5
    for i in range(numExec):
        array = np.random.randint(0, 10, numElem)
        clock = time.time()
        array = funcVariant(array)
        clock = time.time() - clock
        if isSorted(array): #If sort successful, record runtime, otherwise decrement i so we can try again
            total += clock
        else:
            print("Sort failed, trying again")
            i -= 1
    return [numElem, total / numExec]

#Takes an array length 2, index 0 being lower bound and index 1 being upper. Repeatedly compares the runtimes for the middle value of n for regular and multiprocessed merge sort
#until either the disparity between the two variants is <= 0.001 or the upper and lower bounds are equal, as we are dealing with integer values of n only, we can only get so precise.
def compareRegMulti(numElemArr):
    lower = numElemArr[0]
    upper = numElemArr[1]
    mid = int((lower + upper) / 2)
    
    midR = callMerge(mid, mergeSort)
    midM = callMerge(mid, multiMergeSort)
    print(midR)
    print(midM)
    print()
    
    while abs(midR[1] - midM[1]) > 0.001 and upper != lower:
        if midM[1] < midR[1]:
            upper = mid
            mid = int((lower + upper) / 2)
        elif midM[1] > midR[1]:
            lower = mid
            mid = int((lower + upper) / 2)
        midR = callMerge(mid, mergeSort)
        midM = callMerge(mid, multiMergeSort)
        print(midR)
        print(midM)
        print()
    
    return midM
            
def getRuntimes(numElemArr, func):
    results = []
    for elem in numElemArr:
        results.append(callMerge(elem, func))
    return results
    
if __name__ == '__main__':
    #I knew from previous data that multiprocessed was faster at n=100,000 and slower at n=2, so they were good lower and upper bounds.
    #intcpt = compareRegMulti([2, 100000])
    #print("Final Result:")
    #print(intcpt) #intcpt is the value in which multiprocessed becomes faster. Uncomment if want to test this part.
    #Below experimentally confirming the bisection result of n=67,589 being where multiprocessed becomes faster. Will list all runtimes from n=67000 to n=68000.
    arr = np.arange(40000, 90001, 200)
    resR = getRuntimes(arr, mergeSort)
    print("Done with regular")
    resM = getRuntimes(arr, multiMergeSort)
    print("Values of n:")
    for elem in arr:
        print(elem)
    print("\n\n\n\n\n")
    print("Regular Merge Sort Runtimes:")
    for elem in resR:
        print(elem[1])
    print("\n\n\n\n\n")
    print("Multiprocessed Merge Sort Runtimes:")
    for elem in resM:
        print(elem[1] )
    
        
    
    
    

