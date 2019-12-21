---
layout: documentation
title: "Compiling Workloads"
doc: gem5 documentation
parent: compiling_workloads
permalink: /documentation/general_docs/compiling_workloads/
author: "Hoa Nguyen"
---

# Compiling Workloads

## Cross Compilers

A cross compiler is a compiler set up to run on one ISA but generate binaries which run on another. 
You may need one if you intend to simulate a system which uses a particular ISA, Alpha for instance, but don't have access to actual Alpha hardware.  

There are various sources for cross compilers. The following are some of them.

1. [ARM](https://packages.debian.org/stretch/gcc-arm-linux-gnueabihf).
2. [RISC-V](https://github.com/riscv/riscv-gnu-toolchain).

## QEMU

Alternatively, you can use QEMU and a disk image to run the desired ISA in emulation. 
To create more recent disk images, see [this page](/documentation/general_docs/fullsystem/disk). 
The following is a youtube video of working with image files using qemu on Ubuntu 12.04 64bit. 
<iframe width="560" height="315" src="https://www.youtube.com/embed/Oh3NK12fnbg" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
