# Infinite Fibonacci!!!

arr = [1, 1]

print(arr[0])

while True:
    print(arr[-1])
    tmp = sum(arr)
    arr.append(tmp)
    del arr[0]
