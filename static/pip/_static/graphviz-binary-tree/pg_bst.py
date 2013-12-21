# Binary search tree

class BSTNode:
  def __init__(self, dat):
    self.data = dat
    self.parent = None
    self.left = None
    self.right = None

  def insert(self, dat):
    if dat < self.data:
      if not self.left:
        n = BSTNode(dat)
        self.left = n
        n.parent = self
      else:
        self.left.insert(dat)
    else:
      if not self.right:
        n = BSTNode(dat)
        self.right = n
        n.parent = self
      else:
        self.right.insert(dat)

  def pretty_print(self, level):
    print '  ' * level + str(self.data), '(h=%d)' % self.height()
    if self.left:
      self.left.pretty_print(level + 1)
    if self.right:
      self.right.pretty_print(level + 1)

  def search(self, dat):
    if self.data == dat:
      return self
    elif dat < self.data:
      if self.left:
        return self.left.search(dat)
      else:
        return None
    else:
      assert dat > self.data
      if self.right:
        return self.right.search(dat)
      else:
        return None

  def search_by_rank(self, r):
    if self.rank == r:
      return self
    elif r < self.rank:
      if self.left:
        return self.left.search_by_rank(r)
      else:
        return None
    else:
      assert r > self.rank
      if self.right:
        return self.right.search_by_rank(r)
      else:
        return None

  def predecessor(self):
    if self.left:
      p = self.left
      while p.right:
        p = p.right
      return p
    else:
      p = self.parent
      while p and p.data > self.data:
        p = p.parent
      return p

  def successor(self):
    if self.right:
      s = self.right
      while s.left:
        s = s.left
      return s
    else:
      p = self.parent
      while p and p.data < self.data:
        p = p.parent
      return p

  def preorder(self, callback):
    callback(self)
    if self.left:
      self.left.preorder(callback)
    if self.right:
      self.right.preorder(callback)

  def inorder(self, callback):
    if self.left:
      self.left.inorder(callback)
    callback(self)
    if self.right:
      self.right.inorder(callback)

  def delete(self):
    if self.left and self.right:
      s = self.successor()
      # gypsy switch!
      self.data = s.data
      s.delete()
    elif self.left:
      l_child = self.left
      if self.parent.left == self:
        self.parent.left = l_child
        l_child.parent = self.parent
      elif self.parent.right == self:
        self.parent.right = l_child
        l_child.parent = self.parent
    elif self.right:
      r_child = self.right
      if self.parent.left == self:
        self.parent.left = r_child
        r_child.parent = self.parent
      elif self.parent.right == self:
        self.parent.right = r_child
        r_child.parent = self.parent
    else:
      # no children
      if self.parent:
        if self.parent.left == self:
          self.parent.left = None
        elif self.parent.right == self:
          self.parent.right = None

  def height(self):
    if not self.left and not self.right:
      return 0
    else:
      l_height = r_height = 0
      if self.left:
        l_height = self.left.height()
      if self.right:
        r_height = self.right.height()
      return 1 + max(l_height, r_height)

  def mirror(self):
    n = BSTNode(self.data)
    if self.right:
      n.left = self.right.mirror()
      n.left.parent = n
    if self.left:
      n.right = self.left.mirror()
      n.right.parent = n
    return n


tree = BSTNode(10)
tree.insert(2)
tree.insert(4)
tree.insert(1)
tree.insert(5)
tree.insert(15)
tree.insert(12)

tree.pretty_print(0)

tree.insert(13)
print '---'
tree.pretty_print(0)

print '--- MIRROR ---'
tree.mirror().pretty_print(0)


def search_check(n):
  assert tree.search(n.data) == n

tree.preorder(search_check)

print '---'
def print_successor(n):
  s = n.successor()
  if s:
    print n.data, 'SUCCESSOR:', s.data
  else:
    print n.data, 'NO SUCCESSOR'

tree.preorder(print_successor)

print '---'
def print_predecessor(n):
  p = n.predecessor()
  if p:
    print n.data, 'PREDECESSOR:', p.data
  else:
    print n.data, 'NO PREDECESSOR'

tree.preorder(print_predecessor)

def pred_succ_check(n):
  p = n.predecessor()
  if p:
    assert p.successor() == n
  s = n.successor()
  if s:
    assert s.predecessor() == n
  print n.data, "passed pred_succ_check!"

print '---'
tree.preorder(pred_succ_check)

rank = 0
def augment_with_rank(n):
  global rank
  n.rank = rank
  rank += 1

tree.inorder(augment_with_rank)
print '--- RANKS ---'
def print_with_ranks(n):
  print n.data, 'RANK:', n.rank

tree.preorder(print_with_ranks)

print '--- SEARCH BY RANK ---'
for r in xrange(rank):
  print r, tree.search_by_rank(r).data

print '---'
tree.search(1).delete()
tree.pretty_print(0)
print '---'
tree.search(2).delete()
tree.pretty_print(0)
print '---'
tree.search(5).delete()
tree.pretty_print(0)
print '---'
tree.search(10).delete()
tree.pretty_print(0)
print '---'
tree.search(15).delete()
tree.pretty_print(0)
print '---'
tree.search(12).delete()
tree.pretty_print(0)
print '---'
tree.search(4).delete()
tree.pretty_print(0)


