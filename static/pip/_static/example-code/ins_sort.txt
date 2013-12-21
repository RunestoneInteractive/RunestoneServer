# from: http://www.ece.uci.edu/~chou/py02/python.html
def InsertionSort(A):
    for j in range(1, len(A)):
        key = A[j]
        i = j - 1
        while (i >= 0) and (A[i] > key):
            A[i+1] = A[i]
            i = i - 1
        A[i+1] = key

input = [8, 3, 9, 15, 29, 7, 10]
InsertionSort(input)
print(input)
