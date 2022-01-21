---
layout: documentation
title: Homework 1 for CS 752
doc: Learning gem5
parent: gem5_101
permalink: /documentation/learning_gem5/gem5_101/homework-1
authors:
---

# Homework 1 for CS 752: Advanced Computer Architecture I (Fall 2015 Section 1 of 1)

**Due Monday, 9/14**

**You should do this assignment on your own. No late assignments**

Person of contact for this assignment: Nilay Vaish  <nilay@cs.wisc.edu>

For this assignment, you will go through the first few parts of the gem5 tutorial we are currently constructing. This gem5 tutorial is a current work-in-progress and may have typos and bugs in it. Feedback about errors, big or small, is appreciated. Please email <powerjg@cs.wisc.edu> with subject "gem5-tutorial comments" with any comments or errors you find.

## Step 1: complete Part I of the gem5 tutorial

There are currently four (three complete) chapters of this tutorial. The first chapter covers downloading and building gem5. The second chapter walks you through creating a simple configuration script and how to run gem5. The third chapter adds some complexity to your first script by adding a two-level cache hierarchy. And the fourth section (incomplete as of this writing) goes through the gem5 output and how to understand the statistics.

The tutorial does include links to the final scripts at the end of each section. However, it's in your best interest to walk through the tutorial step-by-step and create the scripts yourself.

## Step 2: Write an interesting application

Write a program that implements Sieve of Eratosthenes and outputs one single integer at the end: the number of prime numbers <= 100,000,000. Compile your program as a static binary.  The output should be: 5761455.

## Step 3: Use gem5!

Here, you will run your application in gem5 and change the CPU model, CPU frequency, and memory configuration and describe the changes in performance.

* Run your sieve program in gem5 instead of the 'hello' example. '''Choose an appropriate input size.''' You should use something large enough that the application is interesting, but not too large that gem5 takes more than 10 minutes to execute a simulation. I found that 1,000,000 on my machine takes about 5 minutes. ''Note: The MinorCPU (next step) takes about 10x longer than TimingSimpleCPU takes.''
* Change the CPU model from TimingSimpleCPU to MinorCPU. Hint: you may want to add a command line parameter to control the CPU model.
* Vary the CPU clock from 1 GHz to 3 GHz (in steps of 500 MHz) with both CPU models. Hint: again, you may want to add a command line parameter for the frequency.
* Change the memory configuration from DDR3_1600_x64 to DDR3_2133_x64 (DDR3 with a faster clock) and LPDDR2_S4_1066_x32 (low-power DRAM often found in mobile devices).

## What to Hand In
Turn in your assignment by sending an email message to Nilay Vaish <nilay@cs.wisc.edu> and Prof. David Wood <david@cs.wisc.edu> with the subject line:
"[CS752 Homework1]"

* The email should contain the name and ID numbers of the student submitting the assignment. The files below should be attached as a zip file to the email.
* A file named sieve.c with the implementation of sieve of Eratosthenes.
* A file named sieve-config.py (and any other necessary files) that was used to run gem5. This file should be set up to use TimingSimpleCPU at 1 GHz and DDR3_1600_x64 by default. '''Also bring a print out of this to class'''
* A file named report.pdf containing a short report with your observations and conclusions from the experiment. This report should contain answers to the following questions:
    * Which CPU model is more sensitive to changing the CPU frequency? Why do you think this is?
    * Which CPU model is more sensitive to the memory technology? Why?
    * Is the sieve application more sensitive to the CPU frequency or the memory technology? Why?
    * If you were to use a different application, do you think your conclusions would change? Why?

**Bring a paper copy of your report to class on Monday!**


