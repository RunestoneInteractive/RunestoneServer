..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


Parse Tree
~~~~~~~~~~

With the implementation of our tree data structure
complete, we now look at an example of how a tree can be used to solve
some real problems. In this section we will look at parse trees. Parse
trees can be used to represent real-world constructions like sentences or mathematical expressions.

.. _fig_nlparse:

.. figure:: Figures/nlParse.png
   :align: center
   :alt: image

   Figure 1: A Parse Tree for a Simple Sentence

:ref:`Figure 1 <fig_nlparse>` shows the hierarchical structure of a simple
sentence. Representing a sentence as a tree structure allows us to work
with the individual parts of the sentence by using subtrees.

.. _fig_meparse:

.. figure:: Figures/meParse.png
   :align: center
   :alt: image

   Figure 2: Parse Tree for :math:`((7+3)*(5-2))`

We can also represent a mathematical expression such as
:math:`((7 + 3) * (5 - 2))` as a parse tree, as shown in
:ref:`Figure 2 <fig_meparse>`. We have already looked at fully parenthesized
expressions, so what do we know about this expression? We know that
multiplication has a higher precedence than either addition or
subtraction. Because of the parentheses, we know that before we can do
the multiplication we must evaluate the parenthesized addition and
subtraction expressions. The hierarchy of the tree helps us understand
the order of evaluation for the whole expression. Before we can evaluate
the top-level multiplication, we must evaluate the addition and the
subtraction in the subtrees. The addition, which is the left subtree,
evaluates to 10. The subtraction, which is the right subtree, evaluates
to 3. Using the hierarchical structure of trees, we can simply replace
an entire subtree with one node once we have evaluated the expressions
in the children. Applying this replacement procedure gives us the
simplified tree shown in :ref:`Figure 3 <fig_mesimple>`.

.. _fig_mesimple:

.. figure:: Figures/meSimple.png
   :align: center
   :alt: image

   Figure 3: A Simplified Parse Tree for :math:`((7+3)*(5-2))`

In the rest of this section we are going to examine parse trees in more
detail. In particular we will look at

-  How to build a parse tree from a fully parenthesized mathematical
   expression.

-  How to evaluate the expression stored in a parse tree.

-  How to recover the original mathematical expression from a parse
   tree.

The first step in building a parse tree is to break up the expression
string into a list of tokens. There are four different kinds of tokens
to consider: left parentheses, right parentheses, operators, and
operands. We know that whenever we read a left parenthesis we are
starting a new expression, and hence we should create a new tree to
correspond to that expression. Conversely, whenever we read a right
parenthesis, we have finished an expression. We also know that operands
are going to be leaf nodes and children of their operators. Finally, we
know that every operator is going to have both a left and a right child.

Using the information from above we can define four rules as follows:

#. If the current token is a ``'('``, add a new node as the left child
   of the current node, and descend to the left child.

#. If the current token is in the list ``['+','-','/','*']``, set the
   root value of the current node to the operator represented by the
   current token. Add a new node as the right child of the current node
   and descend to the right child.

#. If the current token is a number, set the root value of the current
   node to the number and return to the parent.

#. If the current token is a ``')'``, go to the parent of the current
   node.

Before writing the Python code, let’s look at an example of the rules
outlined above in action. We will use the expression
:math:`(3 + (4 * 5))`. We will parse this expression into the
following list of character tokens ``['(', '3', '+',``
``'(', '4', '*', '5' ,')',')']``. Initially we will start out with a
parse tree that consists of an empty root node. :ref:`Figure 4 <fig_bldExpstep>`
illustrates the structure and contents of the parse tree, as each new
token is processed.

.. _fig_bldExpstep:

.. figure:: Figures/buildExp1.png
   :align: center
   :alt: image



.. figure:: Figures/buildExp2.png
   :align: center
   :alt: image



.. figure:: Figures/buildExp3.png
   :align: center
   :alt: image



.. figure:: Figures/buildExp4.png
   :align: center
   :alt: image


.. figure:: Figures/buildExp5.png
   :align: center
   :alt: image


.. figure:: Figures/buildExp6.png
   :align: center
   :alt: image


.. figure:: Figures/buildExp7.png
   :align: center
   :alt: image


.. figure:: Figures/buildExp8.png
   :align: center
   :alt: image


   Figure 4: Tracing Parse Tree Construction

Using :ref:`Figure 4 <fig_bldExpstep>`, let’s walk through the example step by
step:

a) Create an empty tree.

b) Read ( as the first token. By rule 1, create a new node as the left
   child of the root. Make the current node this new child.

c) Read 3 as the next token. By rule 3, set the root value of the
   current node to 3 and go back up the tree to the parent.

d) Read + as the next token. By rule 2, set the root value of the
   current node to + and add a new node as the right child. The new
   right child becomes the current node.

e) Read a ( as the next token. By rule 1, create a new node as the left
   child of the current node. The new left child becomes the current
   node.

f) Read a 4 as the next token. By rule 3, set the value of the current
   node to 4. Make the parent of 4 the current node.

g) Read \* as the next token. By rule 2, set the root value of the
   current node to \* and create a new right child. The new right child
   becomes the current node.

h) Read 5 as the next token. By rule 3, set the root value of the
   current node to 5. Make the parent of 5 the current node.

i) Read ) as the next token. By rule 4 we make the parent of \* the
   current node.

j) Read ) as the next token. By rule 4 we make the parent of + the
   current node. At this point there is no parent for + so we are done.

From the example above, it is clear that we need to keep track of the
current node as well as the parent of the current node. The tree
interface provides us with a way to get children of a node, through the
``getLeftChild`` and ``getRightChild`` methods, but how can we keep
track of the parent? A simple solution to keeping track of parents as we
traverse the tree is to use a stack. Whenever we want to descend to a
child of the current node, we first push the current node on the stack.
When we want to return to the parent of the current node, we pop the
parent off the stack.

Using the rules described above, along with the ``Stack`` and
``BinaryTree`` operations, we are now ready to write a Python function
to create a parse tree. The code for our parse tree builder is presented
in :ref:`ActiveCode 1 <lst_buildparse>`.

.. _lst_buildparse:



.. activecode::  parsebuild
    :caption: Building a Parse Tree
    :nocodelens:

    from pythonds.basic.stack import Stack
    from pythonds.trees.binaryTree import BinaryTree

    def buildParseTree(fpexp):
        fplist = fpexp.split()
        pStack = Stack()
        eTree = BinaryTree('')
        pStack.push(eTree)
        currentTree = eTree
        for i in fplist:
            if i == '(':            
                currentTree.insertLeft('')
                pStack.push(currentTree)
                currentTree = currentTree.getLeftChild()
            elif i not in ['+', '-', '*', '/', ')']:  
                currentTree.setRootVal(int(i))
                parent = pStack.pop()
                currentTree = parent
            elif i in ['+', '-', '*', '/']:       
                currentTree.setRootVal(i)
                currentTree.insertRight('')
                pStack.push(currentTree)
                currentTree = currentTree.getRightChild()
            elif i == ')':          
                currentTree = pStack.pop()
            else:
                raise ValueError
        return eTree

    pt = buildParseTree("( ( 10 + 5 ) * 3 )")
    pt.postorder()  #defined and explained in the next section


The four rules for building a parse tree are coded as the first four
clauses of the ``if`` statement on lines 11, 15,
19, and 24 of :ref:`ActiveCode 1 <lst_buildparse>`. In each case you
can see that the code implements the rule, as described above, with a
few calls to the ``BinaryTree`` or ``Stack`` methods. The only error
checking we do in this function is in the ``else`` clause where we
raise a ``ValueError`` exception if we get a token from the list that we
do not recognize.

Now that we have built a parse tree, what can we do with it? As a first
example, we will write a function to evaluate the parse tree, returning
the numerical result. To write this function, we will make use of the
hierarchical nature of the tree. Look back at :ref:`Figure 2 <fig_meparse>`.
Recall that we can replace the original tree with the simplified tree
shown in :ref:`Figure 3 <fig_mesimple>`. This suggests that we can write an
algorithm that evaluates a parse tree by recursively evaluating each
subtree.

As we have done with past recursive algorithms, we will begin the design
for the recursive evaluation function by identifying the base case. A
natural base case for recursive algorithms that operate on trees is to
check for a leaf node. In a parse tree, the leaf nodes will always be
operands. Since numerical objects like integers and floating points
require no further interpretation, the ``evaluate`` function can simply
return the value stored in the leaf node. The recursive step that moves
the function toward the base case is to call ``evaluate`` on both the
left and the right children of the current node. The recursive call
effectively moves us down the tree, toward a leaf node.

To put the results of the two recursive calls together, we can simply
apply the operator stored in the parent node to the results returned
from evaluating both children. In the example from :ref:`Figure 3 <fig_mesimple>`
we see that the two children of the root evaluate to themselves, namely
10 and 3. Applying the multiplication operator gives us a final result
of 30.

The code for a recursive ``evaluate`` function is shown in
:ref:`Listing 1 <lst_eval>`. First, we obtain references to the left and the
right children of the current node. If both the left and right children
evaluate to ``None``, then we know that the current node is really a
leaf node. This check is on line 7. If the current node is not
a leaf node, look up the operator in the current node and apply it to
the results from recursively evaluating the left and right children.

To implement the arithmetic, we use a dictionary with the keys ``'+', '-', '*'``, and
``'/'``. The values stored in the dictionary are functions from Python’s
operator module. The operator module provides us with the functional
versions of many commonly used operators. When we look up an operator in
the dictionary, the corresponding function object is retrieved. Since
the retrieved object is a function, we can call it in the usual way
``function(param1,param2)``. So the lookup ``opers['+'](2,2)`` is
equivalent to ``operator.add(2,2)``.

.. _lst_eval:

**Listing 1**

.. sourcecode:: python

    def evaluate(parseTree):
        opers = {'+':operator.add, '-':operator.sub, '*':operator.mul, '/':operator.truediv}
         
        leftC = parseTree.getLeftChild()
        rightC = parseTree.getRightChild()
    
        if leftC and rightC:
            fn = opers[parseTree.getRootVal()]
            return fn(evaluate(leftC),evaluate(rightC))
        else:
            return parseTree.getRootVal()


.. highlight:: python
    :linenothreshold: 500

Finally, we will trace the ``evaluate`` function on the parse tree we
created in :ref:`Figure 4 <fig_bldExpstep>`. When we first call ``evaluate``, we
pass the root of the entire tree as the parameter ``parseTree``. Then we
obtain references to the left and right children to make sure they
exist. The recursive call takes place on line 9. We begin
by looking up the operator in the root of the tree, which is ``'+'``.
The ``'+'`` operator maps to the ``operator.add`` function call, which
takes two parameters. As usual for a Python function call, the first
thing Python does is to evaluate the parameters that are passed to the
function. In this case both parameters are recursive function calls to
our ``evaluate`` function. Using left-to-right evaluation, the first
recursive call goes to the left. In the first recursive call the
``evaluate`` function is given the left subtree. We find that the node
has no left or right children, so we are in a leaf node. When we are in
a leaf node we just return the value stored in the leaf node as the
result of the evaluation. In this case we return the integer 3.

At this point we have one parameter evaluated for our top-level call to
``operator.add``. But we are not done yet. Continuing the left-to-right
evaluation of the parameters, we now make a recursive call to evaluate
the right child of the root. We find that the node has both a left and a
right child so we look up the operator stored in this node, ``'*'``, and
call this function using the left and right children as the parameters.
At this point you can see that both recursive calls will be to leaf
nodes, which will evaluate to the integers four and five respectively.
With the two parameters evaluated, we return the result of
``operator.mul(4,5)``. At this point we have evaluated the operands for
the top level ``'+'`` operator and all that is left to do is finish the
call to ``operator.add(3,20)``. The result of the evaluation of the
entire expression tree for :math:`(3 + (4 * 5))` is 23.

