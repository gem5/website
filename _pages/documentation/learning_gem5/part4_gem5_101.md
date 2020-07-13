---
layout: documentation
title: gem5 101
doc: Learning gem5
parent: learning_gem5
permalink: /documentation/learning_gem5/gem5_101/
authors: Swapnil Haria
---

# gem5 101

This is a six part course which will help you pick up the basics of gem5, and
illustrate some common uses. This course is based around the assignments from a
particular offering of architecture courses, CS 752 and CS 757, taught at the
University of Wisconsin-Madison.

## First steps with gem5, and Hello World!
[Part I](http://pages.cs.wisc.edu/~david/courses/cs752/Fall2015/wiki/index.php?n=Main.Homework1)

In part I, you will first learn to download and build gem5 correctly, create a simple configuration script for a simple system, write a simple C program and run a gem5 simulation. You will then introduce a two-level cache hierarchy in your system (fun stuff). Finally, you get to view the effect of changing system parameters such as memory types, processor frequency and complexity on the performance of your simple program.

## Getting down and dirty
[Part II](http://pages.cs.wisc.edu/~david/courses/cs752/Fall2015/wiki/index.php?n=Main.Homework2)

For part II, we had used gem5 capabilities straight out of the box. Now, we will witness the flexibility and usefulness of gem5 by extending the simulator functionality. We walk you through the implementation of an x86 instruction (FSUBR), which is currently missing from gem5. This will introduce you to gem5's language for describing instruction sets, and illustrate how instructions are decoded and broken down into micro-ops which are ultimately executed by the processor.

## Pipelining solves everything
[Part III](http://pages.cs.wisc.edu/~david/courses/cs752/Fall2015/wiki/index.php?n=Main.Homework3)

From the ISA, we now move on to the processor micro-architecture. Part III introduces the various different cpu models implemented in gem5, and analyzes the performance of a pipelined implementation. Specifically, you will learn how the latency and bandwidth of different pipeline stages affect overall performance. Also, a sample usage of gem5 pseudo-instructions is also included at no additional cost.

## Always be experimenting
[Part IV](http://pages.cs.wisc.edu/~david/courses/cs752/Fall2015/wiki/index.php?n=Main.Homework4)

Exploiting instruction-level parallelism (ILP) is a useful way of improving single-threaded performance. Branch prediction and predication are two common techniques of exploiting ILP. In this part, we use gem5 to verify the hypothesis that graph algorithms that avoid branches perform better than algorithms that use branches. This is a useful exercise in understanding how to incorporate gem5 into your research process.

## Cold, hard, cache
[Part V](http://pages.cs.wisc.edu/~david/courses/cs752/Fall2015/wiki/index.php?n=Main.Homework5)

After looking at the processor core, we now turn our attention to the cache hierarchy. We continue our focus on experimentation, and consider tradeoffs in cache design such as replacement policies and set-associativity. Furthermore, we also learn more about the gem5 simulator, and create our first simObject!

## Single-core is so two-thousand and late
[Part VI](http://pages.cs.wisc.edu/~markhill/cs757/Spring2016/wiki/index.php?n=Main.Homework3)

For this last part, we go both multi-core and full system at the same time! We analyze the performance of a simple application on giving it more computational resources (cores). We also boot a full-fledged unmodified operating system (Linux) on the target system simulated by gem5. Most importantly, we teach you how to create your own, simpler version of the dreaded fs.py configuration script, one that you can feel comfortable modifying.

## Complete!
Congrats, you are now familiar with the fundamentals of gem5. You are now allowed to wear the “Bro, do you even gem5?” t-shirt (if you manage to find one).


# Credits
A lot of people have been involved over the years in developing the assignments for these courses. If we have missed out on anyone, please add them here.
 * Multifacet research group at University of Wisconsin-Madison
 * Profs Mark Hill, David Wood
 * Jason Lowe-Power
 * Nilay Vaish
 * Lena Olson
 * Swapnil Haria
 * Jayneel Gandhi


 <div class="alert alert-dark" role="alert">
 Any questions or queries regarding this tutorial should be
 directed towards the gem5-users mailing list, and not the individual
 contacts listed in the assignment.
 </div>
