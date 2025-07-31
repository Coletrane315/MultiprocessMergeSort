import numpy as np
import time

def merge(A,p,q,r):
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

def mergeSort(A,p,r):
    if p < r:
        q = (p+r)//2
        mergeSort(A,p,q)
        mergeSort(A,q+1,r)
        merge(A,p,q,r)
    return

def isSorted(array):
    for i in range(array.size - 1):
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
        #print(array)
        clock = time.time()
        mergeSort(array, 0, numElem - 1)
        clock = time.time() - clock
        #print(array)
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

def main():
    dataSizes = [1000, 10000, 100000, 1000000, 1500000, 2000000, 2250000, 2500000, 2750000, 3000000] #This is the basic input
    runtimeData = getRuntimes(dataSizes)
    for elem in runtimeData:
        print(elem[0])
    for elem in runtimeData:
        print(elem[1])

main()
    



