title: Iterative Tree Traversal, and Simulating Recursion
date: 2016-8-18 22:15:00

Students sometimes ask, "what's the point of recursion?"
My stock answer is that some problems, like tree traversal, are much easier to solve recursively.<sup><a name="reference1">[1](#footnote1)</a></sup>
But what does an iterative tree traversal look like?
Let's find out!

This is the tree-node I'll be working with (in Python):

    :::python
    class Node:
        def __init__(self, data, left, right):
            self.data = data
            self.left = left
            self.right = right

`left` and `right` are a node's child nodes, or `None` if the node doesn't have a left or right subtree.

I figure that a recursive tree traversal implicitly uses the call stack as its key data structure, so my iterative tree traversal had better have a stack too.
After zero planning and a bit of hacking I got this solution working:

    :::python
    def iterative_traverse(t):
        stack = [t]

        while stack:
            node = stack.pop()
            print(node.data)

            if node.l:
                stack.append(node.l)
            if node.r:
                stack.append(node.r)


When I give it a test tree:

<pre style="text-align: center">
    1 <- root
  2   4      
3    5 6     
</pre>
All the nodes get printed and the loop terminates.
So far so good.
Given that sample tree the algorithm yields 1, 4, 6, 5, 2, 3, which looks like a backwards post-order traversal.
Replacing the stack with a queue seems to produce a level-order traversal.

This is interesting, and it resembles a recursive algorithm because it uses a stack, but the similarities are superficial.
Consider this pre-order traversal for comparison:

    :::python
    def recursive_traverse(t):
        print(t.data)
        if t.l:
            recursive_traverse(t.l)
        if t.r:
            recursive_traverse(t.r)

This looks like my iterative solution; first we print a node's data, then we check to see if there are left and right subtrees to explore.
The recursive code is easy to modify, if I want an in-order traversal all I have to do is move the print statement in between the two recursive calls:

    :::python
    def recursive_traverse(t):
        if t.l:
            recursive_traverse(t.l)
        print(t.data)
        if t.r:
            recursive_traverse(t.r)

Rearranging the statements of my iterative traversal doesn't produce similar results though, if I want an in-order traversal I need entirely new code.<sup><a name="reference2">[2](#footnote2)</a></sup>

Can I write an iterative algorithm that works more like the recursive algorithm?
Let's revisit that idea from earlier about the recursive algorithm implicitly using a call stack as its core data structure.
Here's what is stored on a call stack:

* Function arguments: the values passed to a function.
* Stack variables: variables whose lifetime is defined by a particular function call.
See [automatic variable](https://en.wikipedia.org/wiki/Automatic_variable) and [local variable](https://en.wikipedia.org/wiki/Local_variable), the terminology is fuzzy here because different languages use different words for similar concepts.
* Return Address: which code to return to executing when this function exits
* The calling function's register values: The called function saves the calling function's state so that the calling function's context can be restored when the called function returns.

These components make up a stack frame, the information required to track a function call.
Every time any function is called a stack frame is pushed onto the call stack, and every time a function returns its frame is popped off the call stack.

Let's take another look at a recursive traversal algorithm so we can see which elements of the stack frame we need to simulate in order to traverse a tree with iteration.

    :::python
    def recursive_traverse(t):
        if t.l:
            traverse(t.l)
        print(t.data)
        if t.r:
            traverse(t.r)

This function has an argument, `t`, which refers the (sub)tree to traverse.
My first iterative algorithm stored nodes in its stack and we'll still need to do that going forwards.

There aren't any local variables other than `t`, so I won't make any space for them in my simulated stack frame.

The recursive `traverse` function returns to a previous call of the `traverse` function, or it simply stops executing once the traversal is complete.
This is simpler than what a real call stack has to manage, a real call stack stores a return address to resume execution at when a function call returns.
Since my case is simpler I can leave the return address out of the simulated stack frame.

The last information in a real stack frame are the calling function's register values.
The registers are a computer's scratch space, as a function executes it can load values from memory into registers, do math, and write the results back to memory.
One particularly important register is the Program Counter which stores the line number of the code that should execute next.
This value is saved on the stack when one function calls another so that the original function knows where it left off before calling the other function.
When the subcall returns, the original function restores the program counter register using its stored value and resumes execution.

The recursive traverse function does rely on this element of the stack frame.
The function includes two function calls, and when those calls return the `traverse` needs to know where to resume.

This is the "stack frame" I came up with to organize my new iterative tree traversal:

    :::python
    class stackframe:
        def __init__(self, node):
            self.node = node
            self.execution_step = 1

`node` refers to a node to print or traverse, and the `execution_step` attribute is my program counter analog.
The recursive traversal function has three execution steps: traverse the left subtree, print the node, and traverse the right subtree.
Each node's stack frame records which step it's on in the `execution_step` attribute.

Here is the recursive in-order traversal algorithm translated to use the simulated stack frame.

    :::python
    def fancy_iterative_traverse(root):
        stack = [stackframe(root)]

        while stack:
            context = stack[-1]

            if context.execution_step > 3:
                stack.pop()

            # Step 1: traverse left subtree
            if context.execution_step == 1:
                if context.node.l:
                    stack.append(stackframe(context.node.l))

            # Step 2: process this node
            elif context.execution_step == 2:
                print(context.node.data)

            # Step 3: traverse right subtree
            elif context.execution_step == 3:
                if context.node.r:
                    stack.append(stackframe(context.node.r))

            context.execution_step += 1

This is nice because it's easy to rearrange the code to perform pre-order or post-order traversals instead.
Adding steps would be a pain though, and translating more complex recursive functions would require a more sophisticated simulated call stack.

I'm not aware of any practical applications of this technique, there's no reason to maintain your own specialized call stack instead of using the one provided by your compiler or runtime environment.
It is interesting to apply low-level programming concepts in a high level language though.

<hr>

<a name="footnote1" href="#reference1">1</a>: This is a contrast to the familiar Fibonacci sequence example that is often used to teach recursion.
Calculating Fibonacci numbers recursively is straightforward, but you can do it iteratively just as easily.
Fibonacci is an okay example to begin with but more motivating examples are also required to demonstrate that recursion can be simpler than iteration.

<a name="footnote2" href="#reference2">2</a>: Refer to [Wikipedia's article on tree traversal](https://en.wikipedia.org/wiki/Tree_traversal#Implementations) for examples of other iterative tree traversals.

