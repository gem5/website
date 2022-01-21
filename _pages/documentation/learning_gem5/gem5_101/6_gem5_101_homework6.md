---
layout: documentation
title: Homework 6 - Programming multi-core
doc: Learning gem5
parent: gem5_101
permalink: /documentation/learning_gem5/gem5_101/homework-6
authors:
---


# CS 758: Programming Multicore Processors (Fall 2013 Section 1 of 1)


**GPU: 10/30**

**You should do this assignment alone. No late assignments.**

Filelist for the assignment:
* [Template files]({$urlbase}/handouts/homeworks/hw6-dist.tgz)
* [Intro to using Euler cluster](http://wacc.wisc.edu/documentation/EulerWalkthrough.pdf)

The purpose of this assignment is for you to familiarize yourself with GPGPU computing platforms (CUDA) and to gain experience with GPGPU specific optimizations. For this assignment you will be given a basic implementation of an algorithm which runs on the GPU and you will procedurally improve it applying GPGPU optimization principals.

**Important**:
CUDA can be tricky, especially if you make a mistake. Error messages are often cryptic and uninformative. Start this assignment early! If you run into any problems post on the email list.

## The problem
For this assignment you will again be implementing the Ocean algorithm. You will be comparing the performance of your GPU-optimized algorithm to your solution from Homework 1. A simple solution to homework 1 is also included in the template files feel free to use it if you want.

## The hardware
You will be using the Euler cluster. You should have or soon will receive an email with a username and temporary password. (MAKE SURE YOU RESET YOUR PASSWORD!) Read the above tutorial that describes the hardware configuration.

## Job submission
This assignment was originally set up to submit jobs to the Torque queue.
For this assignment, please just run jobs directly on  `euler01`.

To get started:

```sh
local $ ssh user@euler.wacc.wisc.edu
euler $ ssh euler01
euler01 $ scp <username>@ale-01.cs.wisc.edu:/p/course/cs758-david/public/html/Fall2013/handouts/homeworks/hw6-dist.tgz .
euler01 $ tar -x -f hw6-dist.tgz
euler01 $ mv hw4-dist hw6
euler01 $ cd hw6
euler01 $ make
euler01 $ ./serial_ocean.sh
```

You shouldn't have any problems as long as your code finishes quickly and you don't leave cuda-gdb open for long periods of time (they have come across a few bugs where cuda-gdb sometimes blocks access to all other GPUs).

Information on the hardware provided in the Euler cluster is available [here](http://wacc.wisc.edu/documentation/EulerWalkthrough.pdf). You will use one of the Fermi cards (Tesla 2070/2050 or GTX 480). Each of which as 448 CUDA cores (14 SMs).

Distributed with CUDA 5.5 is an application called `computeprof` which does a good job of concisely representing the performance counters available on the NVidia GPUs. To use this program, you will need to use `@@ssh -X@@` to login to the Euler cluster in order to forward the X server. You can then run it using `@@/usr/local/cuda/5.5.22/cuda/bin/computeprof@@` I recommend sitting on campus while doing this since there is much higher bandwidth. You can use `computeprof` to diagnose the bottlenecks in each implementation of the algorithm.

##  Additional Information
Dan Negrut is currently teaching a GPU Computing course (ME964). If you need additional info for your homework, you may find what you need at his course web page: <http://sbel.wisc.edu/Courses/ME964/2013/>
There is also a forum where students in the class post questions/answers. It is here:
<http://sbel.wisc.edu/Forum/viewforum.php?f=15>

## Step 1: Porting the CPU algorithm
I have included this implementation of the @@ocean_kernel@@ in the [template files]({$urlbase}/handouts/homeworks/hw4-dist.tgz). You can find it in `cuda_ocean_kernels.cu`` after `@@#ifdef VERSION1@@`. Although considerably more verbose, this is a mostly literal translation of the algorithm in `omp_ocean.c` with OpenMP static partitioning. Each thread gets a chunk of locations within the red/black ocean grid and updates those locations. Study this code and be sure to understand how it works.

* Question a) Describe `memory` divergence and why it leads to poorly performing code in the SIMT model.
* Question b) Describe the `memory` divergence behavior of `@@VERSION1@@` of `@@ocean_kernel@@`.
* Question c) Vary the block size / grid size. What is the optimal block / grid size for this implementation of ocean? What is the speedup over 1 block and 1 thread ("single threaded")? Run with an input of `@@4098 4098 100@@`.
* Question d) What is the speedup over the single threaded CPU version? Run with an input of `@@4098 4098 100@@`.

## Step 2: Reduce memory divergence (Convert algorithm to "SIMD")
Implement `@@VERSION2@@` of `@@ocean_kernel@@`. This version of the kernel will take a step towards reducing the memory divergence. Instead of giving each thread a chunk of the array to work on, re-write the algorithm so that the threads in each block work on adjacent elements. (I.e. for a red iteration, thread 0 will work on element 0, thread 1 will work on element 2, thread 3 will work on element 6, etc).

* Question a) Describe where "memory" divergence still exists in this implementation of ocean.
* Question b) Vary the block size / grid size. What is the optimal block / grid size for this implementation of ocean?
* Question c) How does this version compare to VERSION1? Run with the optimal block sizes for each respectively and an input of `@@4098 4098 100@@`.

## Step 3: Further reduce memory divergence (Modify data structure to be GPU-centric).
Implement `@@VERSION3@@` of `@@ocean_kernel@@`. Instead of using one flat array to represent the ocean grid, split it into two arrays, one for the red cells and one for the black cells. You should start by writing two other kernels which will split the grid object into red_grid and black_grid and take red/black_grid and put them back into the grid object.

If you're feeling adventurous, feel free to add any other optimizations to this implementation. Just describe them in your write-up.

* Question a) How does the performance of this version compare to VERSION2? Is this what you expected?
* Question b) Time each kernel and the memory copies separately (ocean_kernel, and (un)split_array_kernel). Which actions are taking the most execution time? How does this affect the overall execution time of the algorithm? (`computeprof` does a good job summarizing this data)
* Question c) Vary the block size / grid size. What is the optimal block / grid size for this implementation of ocean? Does it change when you change the problem size?
* Question d) Describe "branch" divergence and why it leads to poorly performing code in the SIMT model. Does your code exhibit any branch divergence? If so, where?
* Question e) Given each node in the Euler cluster has 2 Intel Xeon E5520 processors and the GPUs have 448 CUDA cores (GTX480/C2050/C2070) how do you think the performance of your GPU version will compare to the CPU version? 
* Question f) Run either your OpenMP version of ocean or the one in the template files. How does the performance of the CPU version of Ocean compare to the GPU version, better or worse? Why do you think this is? Use omp_ocean.sh to submit the OpenMP version. Run with problem sizes 1026, 2050, 4098, and 8194 with 100 timesteps.
* Question g) What do you think of CUDA? SIMT programming in general?



## Tips and Tricks
* Start early.
* Be mindful that Professor Dan Negrut has been gracious to allow us to use his computing resources for this assignment.

## What to Hand In
Please turn this homework in on **paper** at the beginning of lecture. You must include:
* A printout of your GPU kernels
* Answers to all of the questions and supporting graphs.
**Important:** Include your name on EVERY page.