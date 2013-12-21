# TODO: how do you set the BACKGROUND COLOR of a GraphViz node ... fill=?


# example code snippet to visualize, which uses '#break' as a breakpoint
# feel free to clean up however you like
'''
from bintree_module import TNode
import html_module

r = TNode('a',
          left=TNode('b0',
                     left=TNode('c0',
                                right=TNode('d1')),
                     right=TNode('c1',
                                 left=TNode('d3'),
                                 right=TNode('d4'))),
          right=TNode('b1',
                      left=TNode('c2')))

def highlight_and_display(root):
    def f(node):
        node.highlight()
        html_module.display_img(root.to_graphviz_img()) #break
        node.reset_style()
    return f

def preorder(t, visitfn):
    if not t:
        return
    visitfn(t)
    preorder(t.left, visitfn)
    preorder(t.right, visitfn)

preorder(r, highlight_and_display(r))
'''


from collections import defaultdict

import GChartWrapper
import html_module

import sys
is_python3 = (sys.version_info[0] == 3)

if is_python3:
  import io as cStringIO
else:
  import cStringIO

ID = 0

# somewhat inspired by bst.py from MIT 6.006 OCW
# http://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/search.htm
class TNode:
  def __init__(self, dat, left=None, right=None):
    self.data = dat
    self.parent = None
    self.left = left
    self.right = right

    if self.left:
      self.left.parent = self
    if self.right:
      self.right.parent = self

    self.__penwidth = 1 # thickness of node border

    # HTML-like RGB hex values - e.g., "#bb0000"
    self.__color = None # border color
    self.__fill = None  # internal node color

    # assign unique IDs in node creation order
    global ID
    self.id = 'n' + str(ID)
    ID += 1

  def disconnect(self):
    self.left = None
    self.right = None
    self.parent = None

  def set_border_color(self, col):
    self.__color = col

  def set_fill(self, col):
    self.__fill = col

  def set_width(self, w):
    assert w > 0
    self.__penwidth = w

  def highlight(self):
    self.__color = 'red'
    self.__penwidth = 2

  def reset_style(self):
    self.__color = None
    self.__fill = None
    self.__penwidth = 1

  def is_leaf(self):
    return not (self.left or self.right)

  def graphviz_str(self):
    ret = '%s[label="%s"' % (self.id, str(self.data)) # convert to str() for display
    if self.__penwidth > 1:
      ret += ',penwidth=%d' % self.__penwidth
    if self.__color:
      ret += ',color="%s"' % self.__color
    if self.__fill:
      ret += ',fill="%s"' % self.__fill
    ret += ']'
    return ret

  def __str__(self):
    return 'TNode(%s)' % repr(self.data)


  # render a binary tree of TNode objects starting at self in a pretty
  # GraphViz format using the balanced tree hack from
  # http://www.graphviz.org/content/FaqBalanceTree
  def graphviz_render(self, ios, compress=False):
    separator = '\n'
    if compress:
      separator=','
    ios.write('digraph G{')

    if not compress:
      ios.write('\n')
    
    queue = [] # each element is (node, level #)

    # Key: level number
    # Value: sorted list of node IDs at that level (including phantom nodes)
    nodes_by_level = defaultdict(list)


    def render_phantom(parent_id, suffix):
      phantom_id = parent_id + '_phantom_' + suffix
      ios.write('%s [label="",width=.1,style=invis]%s' % (phantom_id, separator))
      ios.write('%s->%s [style=invis]%s' % (parent_id, phantom_id, separator))
      return phantom_id

    def bfs_visit():
      # base case
      if not queue:
        return

      n, level = queue.pop(0)

      ios.write(n.graphviz_str() + separator) # current node
      if n.left or n.right:
        if n.left:
          ios.write('%s->%s%s' % (n.id, n.left.id, separator))
          queue.append((n.left, level+1))
          nodes_by_level[level+1].append(n.left.id)
        else:
          # insert phantom to make tree look good
          ph_id = render_phantom(n.id, 'L')
          nodes_by_level[level+1].append(ph_id)

        # always insert invisible middle phantom
        ph_id = render_phantom(n.id, 'M')
        nodes_by_level[level+1].append(ph_id)

        if n.right:
          ios.write('%s->%s%s' % (n.id, n.right.id, separator))
          queue.append((n.right, level+1))
          nodes_by_level[level+1].append(n.right.id)
        else:
          # insert phantom to make tree look good
          ph_id = render_phantom(n.id, 'R')
          nodes_by_level[level+1].append(ph_id)

      bfs_visit() # recurse!

    queue.append((self, 1))
    bfs_visit()

    if not compress:
      ios.write('\n')

    # make sure all nodes at the same level are vertically aligned
    for level in nodes_by_level:
      node_ids = nodes_by_level[level]
      if len(node_ids) > 1:
        ios.write(('{rank=same %s [style=invis]}' % '->'.join(node_ids)) + separator)

    ios.write('}') # cap it off


  def to_graphviz_string(self):
    s = cStringIO.StringIO()
    self.graphviz_render(s, True)
    return s.getvalue()

  def to_graphviz_img(self):
    return GChartWrapper.GraphViz(self.to_graphviz_string())


# from MIT 6.006 OCW
# http://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/search.htm
class BST(object):
    """
Simple binary search tree implementation.
This BST supports insert, find, and delete-min operations.
Each tree contains some (possibly 0) BSTnode objects, representing nodes,
and a pointer to the root.
"""

    def __init__(self):
        self.root = None

    def to_graphviz_img(self):
        if self.root:
            return GChartWrapper.GraphViz(self.root.to_graphviz_string())
        else:
            return ''

    def insert(self, t):
        """Insert data t into this BST, modifying it in-place."""
        new = TNode(t)
        if self.root is None:
            self.root = new
        else:
            node = self.root
            while True:
                if t < node.data:
                    # Go left
                    if node.left is None:
                        node.left = new
                        new.parent = node
                        break
                    node = node.left
                else:
                    # Go right
                    if node.right is None:
                        node.right = new
                        new.parent = node
                        break
                    node = node.right
        return new

    def find(self, t):
        """Return the node for data t if is in the tree, or None otherwise."""
        node = self.root
        while node is not None:
            if t == node.data:
                return node
            elif t < node.data:
                node = node.left
            else:
                node = node.right
        return None

    def delete_min(self):
        """Delete the minimum data (and return the old node containing it)."""
        if self.root is None:
            return None, None
        else:
            # Walk to leftmost node.
            node = self.root
            while node.left is not None:
                node = node.left
            # Remove that node and promote its right subtree.
            if node.parent is not None:
                node.parent.left = node.right
            else: # The root was smallest.
                self.root = node.right
            if node.right is not None:
                node.right.parent = node.parent
            parent = node.parent
            node.disconnect()
            return node, parent

    def __str__(self):
        if self.root is None:
            return 'empty tree'
        else:
            return 'tree with root: %s' % str(self.root)

if __name__ == "__main__":
  # simple test tree
  r = TNode('a',
            left=TNode('b0',
                       left=TNode('c0',
                                  right=TNode('d1')),
                       right=TNode('c1',
                                   left=TNode('d3'),
                                   right=TNode('d4'))),
            right=TNode('b1',
                        left=TNode('c2',
                                   left=TNode('d2'))))

  f = open('test.dot', 'w')
  r.graphviz_render(f)
  f.close()

  '''
  t = BST()
  import random
  nums = range(10)
  random.shuffle(nums)
  for i in nums:
    t.insert(i)

  f = open('test.dot', 'w')
  t.root.graphviz_render(f)
  f.close()
  '''


'''
/* balanced tree hack from http://www.graphviz.org/content/FaqBalanceTree */

/*
digraph G {
  a -> b0
  xb [label="",width=.1,style=invis]
  a -> xb [style=invis]
  a -> b1

  {rank=same b0 -> xb -> b1 [style=invis]}

  b0 -> c0
  xc [label="",width=.1,style=invis]
  b0 -> xc [style=invis]
  b0 -> c1

  {rank=same c0 -> xc -> c1 [style=invis]}
}
*/
'''

'''
from bintree_module import TNode
import html_module

r = TNode('a',
          left=TNode('b0',
                     left=TNode('c0',
                                right=TNode('d1')),
                     right=TNode('c1',
                                 left=TNode('d3'),
                                 right=TNode('d4'))),
          right=TNode('b1',
                      left=TNode('c2')))

def highlight_and_display(root):
    def f(node):
        node.highlight()
        html_module.display_img(root.to_graphviz_img()) #break
        node.reset_style()
    return f

def preorder(t, visitfn):
    if not t:
        return
    visitfn(t)
    preorder(t.left, visitfn)
    preorder(t.right, visitfn)

preorder(r, highlight_and_display(r))
'''

'''
from bintree_module import BST
import html_module
import random

t = BST()
html_module.display_img(t.to_graphviz_img())

nums = range(10)
random.shuffle(nums)
for i in nums:
  t.insert(i)
  html_module.display_img(t.to_graphviz_img())
'''

# insertion into a BST with each step animated
#
# TODO: think of a more elegant way to separate out algorithm from HTML
# rendering code
'''
import html_module, GChartWrapper, random
from bintree_module import TNode

class BST:
    def __init__(self):
        self.root = None
        
    def to_graphviz_img(self):
        if self.root:
            return GChartWrapper.GraphViz(self.root.to_graphviz_string())
        else:
            return ''        
        
    def insert(self, t):
        """Insert data t into this BST, modifying it in-place."""
        new = TNode(t)
        if self.root is None:
            self.root = new
        else:
            node = self.root
            while True:
                node.highlight()
                html_module.display_img(self.to_graphviz_img()) #break
                node.reset_style()
                if t < node.data:
                    # Go left
                    if node.left is None:
                        node.left = new
                        new.parent = node

                        new.highlight()
                        html_module.display_img(self.to_graphviz_img()) #break
                        new.reset_style()

                        break
                    node = node.left
                else:
                    # Go right
                    if node.right is None:
                        node.right = new
                        new.parent = node

                        new.highlight()
                        html_module.display_img(self.to_graphviz_img()) #break
                        new.reset_style()

                        break
                    node = node.right
        return new

t = BST()
nums = range(10)
random.shuffle(nums)
for i in nums:
      t.insert(i)
'''
