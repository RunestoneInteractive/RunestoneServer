# use memoization to make the recursive Fibonacci
# implementation only take O(n) time and space

MemoTable = {}

def MemoizedFib(n):
    if n <= 2:
        return 1

    if n in MemoTable:
        return MemoTable[n]

    MemoTable[n] = MemoizedFib(n-1) + MemoizedFib(n-2)
    return MemoTable[n]


res = MemoizedFib(10)
