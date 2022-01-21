---
layout: documentation
title: Homework 3 for CS 752
doc: Learning gem5
parent: gem5_101
permalink: /documentation/learning_gem5/gem5_101/homework-3
authors:
---

# Homework 3 for CS 752: Advanced Computer Architecture I (Fall 2015 Section 1 of 1)

**Due 1pm, Tuesday, 9/29**

**You should do this assignment alone. No late assignments.**

The purpose of this assignment is to give you experience with pipelined CPUs.  You will simulate a given program with simple timing cpu to understand the instruction mix of the program.  Then, you will simulate the same program with an pipelined inorder CPU to understand how the latency and bandwidth of different parts of pipeline affect performance.  You will also be exposed to pseudo-instructions that are used for carrying out functions required by the underlying experiment.  This homework is based on exercise 3.6 of CA:AQA 3rd edition.

----

1. The DAXPY loop (double precision aX + Y) is an oft used operation in programs that work with matrices and vectors.  The following code implements DAXPY in C++11.

```cpp
  #include <cstdio>
  #include <random>

  int main()
  {
    const int N = 1000;
    double X[N], Y[N], alpha = 0.5;
    std::random_device rd; std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(1, 2);
    for (int i = 0; i < N; ++i)
    {
      X[i] = dis(gen);
      Y[i] = dis(gen);
    }

    // Start of daxpy loop
    for (int i = 0; i < N; ++i)
    {
      Y[i] = alpha * X[i] + Y[i];
    }
    // End of daxpy loop

    double sum = 0;
    for (int i = 0; i < N; ++i)
    {
      sum += Y[i];
    }
    printf("%lf\n", sum);
    return 0;
  }
```

Your first task is to compile this code statically and simulate it with gem5 using the timing simple cpu.  Compile the program with `-O2` flag to avoid running into unimplemented x87 instructions while simulating with gem5.  Report the breakup of instructions for different op classes.  For this, grep for op_class in the file stats.txt.


2. Generate the assembly code for the daxpy program above by using the `-S` and `-O2` options when compiling with GCC.  As you can see from the assembly code, instructions that are not central to the actual task of the program (computing `aX + Y`) will also be simulated.  This includes the instructions for generating the vectors `X` and `Y`, summing elements in `Y` and printing the sum.  When I compiled the code with `-S`, I got about 350 lines of assembly code, with only about 10-15 lines for the actual daxpy loop.

Usually while carrying out experiments for evaluating a design, one would like to look only at statistics for the portion of the code that is most important.  To do so, typically programs are annotated so that the simulator, on reaching an annotated portion of the code, carries out functions like create a checkpoint, output and reset statistical variables.

You will edit the C++ code from the first part to output and reset stats just before the start of the DAXPY loop and just after it.  For this, include the file `util/m5/m5op.h` in the program.  You will find this file in `util/m5` directory of the gem5 repository.  Use the function `m5_dumpreset_stats()` from this file in your program. This function outputs the statistical variables and then resets them. You can provide 0 as the value for the delay and the period arguments.

To provide the definition of the `m5_dumpreset_stats()`, go to the directory `util/m5` and edit the Makefile.x86 in the following way:

```
  diff --git a/util/m5/Makefile.x86 b/util/m5/Makefile.x86
  --- a/util/m5/Makefile.x86
  +++ b/util/m5/Makefile.x86
  [=@@=] -31,7 +31,7 @@
   AS=as
   LD=ld

  -CFLAGS=-O2 -DM5OP_ADDR=0xFFFF0000
  +CFLAGS=-O2
   OBJS=m5.o m5op_x86.o

   all: m5
```

Execute the command `make -f Makefile.x86` in the directory `util/m5`.  This will create an object file named `m5op_x86.o`.  Link this file with the program for DAXPY.  Now again simulate the program with the timing simple CPU.  This time you should see three sets of statistics in the file stats.txt.  Report the breakup of instructions among different op classes for the three parts of the program.  Provide the fragment of the generated assembly code that starts with call to `m5_dumpreset_stats()` and ends `m5_dumpreset_stats()`, and has the main daxpy loop in between.


3. There are several different types of CPUs that gem5 supports: atomic, timing, out-of-order, inorder and kvm.  Let's talk about the timing and the inorder cpus.  The timing CPU (also known as SimpleTimingCPU) executes each arithmetic instruction in a single cycle, but requires multiple cycles for memory accesses.  Also, it is not pipelined.  So only a single instruction is being worked upon at any time.  The inorder cpu (also known as Minor) executes instructions in a pipelined fashion.  As I understand it has the following pipe stages: fetch1, fetch2, decode and execute.

Take a look at the file `src/cpu/minor/MinorCPU.py`.  In the definition of `MinorFU`, the class for functional units, we define two quantities `opLat` and `issueLat`.  From the comments provided in the file, understand how these two parameters are to be used.  Also note the different functional units that are instantiated as defined in class `MinorDefaultFUPool`.


Assume that the issueLat and the opLat of the FloatSimdFU can vary from 1 to 6 cycles and that they always sum to 7 cycles.  For each decrease in the opLat, we need to pay with a unit increase in issueLat.  Which design of the FloatSimd functional unit would you prefer?  Provide statistical evidence obtained through simulations of the annotated portion of the code.

You can find a skeleton file that extends the minor CPU here <$urlbase}html/cpu.py>. If you use this file, you will have to modify your config scripts to work with it. Also, you'll have to modify this file to support the next part.

4. The Minor CPU has by default two integer functional units as defined in the file MinorCPU.py (ignore the Multiplication and the Division units).  Assume our original Minor CPU design requires 2 cycles for integer functions and 4 cycles for floating point functions.  In our upcoming Minor CPU, we can halve either of these latencies.  Which one should we go for?  Provide statistical evidence obtained through simulations.


## What to Hand In
Turn in your assignment by sending an email message to Prof. David Wood <david@cs.wisc.edu> and Nilay Vaish <nilay@cs.wisc.edu>  with the subject line: "CS752 Homework3".

1. The email should contain the name and ID numbers of the student submitting
the assignment. The files below should be attached as a zip file to the email.

2. A file named daxpy.cpp which is used for testing.  This file should also include the pseudo-instructions (`m5_dumpreset_stats()`) as asked in part 2.  Also provide a file daxpy.s with the fragment of the generated assembly code as asked for in part 2.

3. stats.txt and config.ini files for all the simulations.

4. A short report (200 words) on questions asked.
