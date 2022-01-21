---
layout: documentation
title: Homework 5 for CS 752
doc: Learning gem5
parent: gem5_101
permalink: /documentation/learning_gem5/gem5_101/homework-5
authors:
---

# Homework 5 for CS 752: Advanced Computer Architecture I (Fall 2015 Section 1 of 1)

**Due Wednesday, 10/28**

**You should do this assignment on your own. No late assignments.**

Person of contact for this assignment: "Nilay Vaish'" <nilay@cs.wisc.edu>

The goal of this assignment is two-fold. First, for you to experience creating a new SimObject in gem5, and second for you to consider tradeoffs in cache design.

An updated cache.py for configuration can be downloaded here <{$urlbase}html/hw5/caches.py>. You can replace the cache.py found in the previous homework here: <{$urlbase}html/hw4-configs.tar.gz>.

## Step 1: Implement NMRU replacement policy

You can follow the tutorial here: <http://pages.cs.wisc.edu/~david/courses/cs752/Spring2015/gem5-tutorial/index.html>
Part 2 of the tutorial will walk you through how to create the NMRU policy.

## Step 2: Implement PLRU replacement policy

Follow similar steps as you did to implement NRU, but implement pseudo-LRU instead.
Psuedo-LRU uses a binary tree to encode which blocks are less recently used than other blocks in the set. These slides from Mikko Lipasti do a good job explaining the PLRU algorithm: <https://ece752.ece.wisc.edu/lect11-cache-replacement.pdf>.

## Step 3: Architectural exploration

This time, the Entil CEO has tasked you with designing the L1 data cache of their new processor based on the out-of-order O3CPU. For this task, the marketing director of Entil claims that most of their customers' workload is in the matrix multiply kernel. Due to it's memory intensity, Entil believe a better cache design could make their processor outperform the competition (AMM, Advanced Micro Machines if you're keeping track). 

A blocked matrix multiply implementation can be downloaded here: <{$urlbase}html/hw5/mm.cpp>. Use an input of 128x128 matrix (./mm 128).

You can choose from three replacement policies for the L1D cache: 'Random', 'NMRU', 'PLRU'. As the associativity increases, the costs for NMRU and PLRU rises, whereas the cost for Random stays the same. Therefore, Random can be used with higher associativities than the other replacement policies. Additionally, because NMRU and PLRU must update the recently used bits in the tag they access, these policies limit the clock rate of the CPU. Note, the max clock of the O3 CPU is 2.3 GHz in this generation.

The constraints for these policies are summarized below.

|            |Random |NMRU   |PLRU    |
|------------|-------|-------|--------|
|Max assoc.  |16     |8      |8       |
|Lookup time |100 ps |500 ps | 666 ps |

Clearly describe in a one page memo to the CEO of Entil, all of the configurations you simulated, the results of your simulations, and your overall conclusion of how to architect the L1 data cache.
Additionally, answer the following specific questions:
* Why does the 16-way set-associative cache perform better/worse/similar to the 8-way set-associative cache?
* Why does Random/NMRU/PLRU/None perform better than the other replacement policies?
* Is the cache replacement/associativity important for this workload, or are you only getting benefits from clock cycle? Explain why the cache architecture is important/unimportant.


##What to Hand In

Turn in your assignment by sending an email message to Nilay Vaish <nilay@cs.wisc.edu> and Prof. David Wood <david@cs.wisc.edu> with the subject line:
"[CS752 Homework5]"

1. The email should contain the name and ID numbers of the student submitting
the assignment. The files below should be attached as a zip file to the email.
2. A patch file containing all the changes you made to gem5.
3. stats.txt and config.ini files for all the simulations.
4. A short report on the questions asked. The report should be in PDF.
