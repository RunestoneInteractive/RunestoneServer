# move a stack of n disks from stack a to stack b,
# using tmp as a temporary stack
def TowerOfHanoi(n, a, b, tmp):
    if n == 1:
        b.append(a.pop())
    else:
        TowerOfHanoi(n-1, a, tmp, b)
        b.append(a.pop())
        TowerOfHanoi(n-1, tmp, b, a)
        
stack1 = [4,3,2,1]
stack2 = []
stack3 = []
      
# transfer stack1 to stack3 using Tower of Hanoi rules
TowerOfHanoi(len(stack1), stack1, stack3, stack2)
