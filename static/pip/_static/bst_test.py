from bintree_module import BST
import html_module
import random

t = BST()
html_module.display_img(t.to_graphviz_img())

nums = [e for e in range(10)]
random.shuffle(nums)
for i in nums:
  t.insert(i)
  html_module.display_img(t.to_graphviz_img())
