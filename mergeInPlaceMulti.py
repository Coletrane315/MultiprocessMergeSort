import numpy as np
import time
import os
import multiprocessing

def merge(tupleInfo):
    A = tupleInfo[0]
    p = tupleInfo[1]
    q = tupleInfo[2]
    r = tupleInfo[3]
    n1 = q-p+1
    n2 = r-q
    Left = []
    Right = []
    for i in range(n1):
        Left.append(A[p+i])
    Left.append(32767)
    for i in range(n2):
        Right.append(A[q+i+1])
    Right.append(32767)
    i=0
    j=0
    for k in range(p,r+1):
        if (Left[i]<=Right[j]):
            A[k]=Left[i]
            i+=1
        else:
            A[k]=Right[j]
            j+=1
    return

def mergeSort(tupleInfo):
    print(id(tupleInfo[0]))
    p = tupleInfo[1]
    r = tupleInfo[2]
    if p < r:
        q = (p+r)//2
        mergeSort((tupleInfo[0],p,q))
        mergeSort((tupleInfo[0],q+1,r))
        merge((tupleInfo[0],p,q,r))
    return

#Evenly divides the data into some number of segments based on the number of CPU's on the current machine.Attempts to use numpy's split function, but this only works if the size of
#the data n is divisible by the number of sublists being created, otherwise have to customize the algorithm for making the sublists. Because of the way the map function works,
#I needed to alter some of merge sort parameters. merge sort takes in one parameter now, a tuple that contains all the information that it was passed previously. This is because
#there is no easy way to implement the map method of the Pool object of the multiprocessing module on a function with more than one argument. The var dataSet is a list of all of
#the sublists, tupleSet is a list of the form [ (dataSet[0], 0, dataSet[0].size - 1), ...]. The Pool objects works by firstly initiating some number of processes, then I use the map
#method to give it a function and a list of parameters (in this case, tupleSet), then it evenly distributes the work needed to call the function on each element of the list among
#the processes in the pool.
def multiMergeSort(array):
    numCPU = os.cpu_count()
    pool = multiprocessing.Pool(processes=numCPU) #Make pool of processes based on # CPU's
    size = int(array.size / numCPU + 1.0) #Evenly divide the array into segments based on # CPU's
    dataSet = []
    #Attempt to split data using numpy function, only works if array.size % numCPU == 0
    #Otherwise, define the sublists custom. Either way dataSet looks like [ [0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11] ]
    try:
        dataSet = np.split(array, numCPU)
    except:
        for i in range(numCPU):
            dataSet.append(array[i * size: i * size + size])
    print("Data split:")
    print(dataSet)
    print()
    #Packs data into tuples in order to pass them as parameters to mergeSort
    tupleSet = [] 
    for elem in dataSet:
        tupleSet.append([elem, 0, elem.size - 1]) #Not really tuples, forgot tuples immutable and need values to be mutable
    print("Tuple list before mS:")
    print(tupleSet)
    print()
    print(id(tupleSet[0][0]))
    pool.map(mergeSort, tupleSet)
    print("Tuple list after mS")
    print(tupleSet)
    print()
    #We need to know if there is an even number of sublists. If not, pop it off and save it for later
    extraVal = None
    if len(tupleSet) % 2 == 1:
        extraVal = tupleSet.pop(-1)
    
    print("Check 2")
    #At this point, all sublists were sorted. Pair up adjacent sublists and merge them together. Again, pack data into tuples to pass parameters to merge.
    while len(tupleSet) > 1:
        k = 0
        j = 0
        for i in range(int(len(tupleSet) / 2)):
            tmp = tupleSet[j][0].size
            tmpArr = np.concatenate((tupleSet[j][0], tupleSet[j + 1][0]))
            tupleSet.pop(j + 1)
            tupleSet[j] = (tmpArr, 0, tmp - 1, tmpArr.size - 1)
            k += 1
            j += 1
        pool.map(merge, tupleSet)
    finalVal = tupleSet[0][0]
    if extraVal != None:
        tmpArr = tupleSet[0][0] + extraVal[0]
        merge((tmpArr, 0, tupleSet[0][0].size, tmpArr.size))
        finalVal = tmpArr
    print("Check 3")
    return finalVal
        
        
        
        

#Iterates through an array to determine if it is sorted
def isSorted(array):
    for i in range(np.array(array).size - 1):
        if array[i] > array[i + 1]:
            return False
    return True

#Takes in an integer number of elements, makes random array of that length. Merge sorts it, records time. Repeats numExec times and averages time. Returns list [# elements, avg time]
#To experiment, decrease numExec var if you want shorter overall runtime, or increase it if you want a better average of runtime.
def callMerge(numElem):
    total = 0
    numExec = 1
    for i in range(numExec):
        array = np.random.randint(0, 10, numElem)
        print(array)
        clock = time.time()
        array = multiMergeSort(array)
        clock = time.time() - clock
        print(array)
        if isSorted(array): #If sort successful, record runtime, otherwise decrement i so we can try again
            total += clock
        else:
            i -= 1
            print("Sort failed, trying again")
    return [numElem, total / numExec]

#Takes in array of integers meaning number of elements. Iterates over array, passing each element to callMerge. Appends return values of callMerge to a list.
#Returns list of the form [ [# elements, avg time], [# elements, avg time], [# elements, avg time], ...]
def getRuntimes(numElemArray):
    returnArr = []
    for elem in numElemArray:
        returnArr.append(callMerge(elem))
    return returnArr


if __name__ == '__main__':
    lengthArray = [10]
    res = getRuntimes(lengthArray)
    for elem in res:
        print(elem)
        

    



