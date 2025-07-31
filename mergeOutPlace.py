import numpy as np
import time

def mergeSort(array):
    if array.size == 1:
        return array
    q = array.size // 2
    left = mergeSort(array[:q])
    right = mergeSort(array[q:])
    return merge(left, right)

def merge(leftSide, rightSide):
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
        array = mergeSort(array)
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

def getRatios(arr):
    return arr[:, 1] / (arr[:, 0] * np.log2(arr[:, 0]))

def main():
    lengthArray = [1000, 10000, 100000, 1000000, 1500000, 2000000, 2250000, 2500000, 2750000, 3000000]
    res = getRuntimes(lengthArray)
    #ratios = getRatios(res)
    for elem in res:
        print(elem[0])
    print()
    for elem in res:
        print(elem[1])
    print()
        

    
    
    
main()
