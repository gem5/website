---
layout: documentation
title: Homework 4 for CS 752
doc: Learning gem5
parent: gem5_101
permalink: /documentation/learning_gem5/gem5_101/homework-4
authors:
---

# Homework 4 for CS 752: Advanced Computer Architecture I (Fall 2015 Section 1 of 1)


** Due Monday, 10/7**

**You should do this assignment on your own. No late assignments.**

Person of contact for this assignment: **Nilay Vaish** <nilay@cs.wisc.edu>.


This homework is experimental in nature since I thought of this only
yesterday (28 September, 2015).  It deals with two different methods of
exploiting instruction level parallelism: "branch prediction" and "predication".

Consider the following piece of code:
```cpp
  if (x < y)
     x = y;
```

There at least two ways in which we can generate the assembly code for this.

1. using branches:

```
    compare x, y
    jump if not less L
    move x, y
  L:
```

2. using conditional move:

```
  compare x, y
  conditionally move x to y.
```

Which version should one prefer?  We will try to get some understanding of
this question in this homework.


1. Here are some [posts](http://yarchive.net/comp/linux/cmov.html) on cmov from
Linus Torvalds, the creator and maintainer of the Linux operating system.
Linus has provided a short piece of C code for measuring the performance
of branches and conditional moves.  Run the code on your x86 favorite
processor and report the timing numbers for the two versions `choose()`
function.  You should run each version at least 10 times.  Report both the average
execution time and the standard deviation in the run times.
If you see too much variation in the run times,  run for more iterations.  This
should typically stabilize the performance.


2. Now simulate the same two versions with gem5 using the out-of-order
(default configuration) processor.  Lower the number of iterations to
1,000,000 since 100,000,000 is lot of iterations for gem5.  Again report
which option performs the best.  Also report the total number of
branches predicted and the number of branches predicted incorrectly.

----

3. A paper on [branch avoiding algorithms](http://dl.acm.org/citation.cfm?id=2755580)
was published at SPAA 2015.  The authors suggest that graph algorithms that avoid branches
may perform better than algorithms that use branches.  Let's try to verify this claim.

The paper provides two versions of an algorithm for computing the
connected components in an undirected graph.  The first version uses
branching and the second one uses conditional moves.  I implemented
both the versions, but there is a slight problem.  The first version can
be implemented in C++ directly, but the second one requires use of CMOV
instruction.  I was not able to get this instruction working with inline
assembly, but with raw assembly things work.  So along with the [C++1 source code](http://pages.cs.wisc.edu/~david/courses/cs752/Fall2015/html/hw4/connected-components.cpp), I am providing you the GCC generated-[assembly code](http://pages.cs.wisc.edu/~david/courses/cs752/Fall2015/html/hw4/connected-components.s) and the [statically compiled executable](http://pages.cs.wisc.edu/~david/courses/cs752/Fall2015/html/hw4/connected-components).  Note that
you would not be able to generate exactly the same assembly code and the executable
by compiling the C++11 source.  This is because I modified the generated assembly
code to get cmov working.  I am also providing three graphs [small](http://pages.cs.wisc.edu/~david/courses/cs752/Fall2015/html/hw4/small.graph), [medium](http://pages.cs.wisc.edu/~david/courses/cs752/Fall2015/html/hw4/medium.graph) and [large](http://pages.cs.wisc.edu/~david/courses/cs752/Fall2015/html/hw4/large.graph.gz) that you will use for your experiments.  Read the C++ source to understand how to supply
options to the executable.

a. Run both the versions (with branches and with cmov) on an x86 processor and report
the run time performance for the provided input files.  Do this exercise only for large graph.
Provide data as asked in part 1.

b. Run both the versions with gem5, report the performance of the two
versions for the annotated portion of the code, the number of predicted
branches, % of incorrectly predicted branches.  You need to do this only for small and medium graphs, not for the large one.
Provide data asked in part 2 again.

## What to Hand In
Turn in your assignment by sending an email message to Nilay Vaish <nilay@cs.wisc.edu>
and Prof. David Wood <david@cs.wisc.edu> with the subject line:"
[CS752 Homework4]"

**Please turn in your homework in the form of a PDF file.**

* Answers for questions in step 1
* Answers for questions in step 2
* Answers for questions in step 3
