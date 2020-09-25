---
layout: post
title:  "X86 Linux Boot Status on gem5-19"
author: Ayaz Akram
date:   2020-03-09
categories: project
---

![gem5-linux-logo](/assets/img/blog/gem5-linux.png)

The frequency of changes pushed to gem5 is increasing with time.
This makes it important to have an up-to-date idea of what is working with gem5 and what is not.
The booting of the Linux kernel is a very important benchmark to ascertain the working status of gem5, considering that gem5 is a full-system simulator which should be able to simulate a modern operating system.
However, the state of support of latest Linux kernel versions on gem5 is hard to discover, and, previously available Linux kernels or configuration files on gem5 website are quite old.
[gem5-19](https://www.gem5.org/project/2020/02/25/gem5-19.html) has also been released recently.

We thereby ran tests to discover where gem5-19 stands in terms of its ability to boot the latest releases of the Linux kernel.
In this post, we will discuss the results of these tests.

## Configuration Space

The possible configuration space when simulating a Linux boot on gem5 is large.
To test gem5-19, we evaluated multiple configurations, taking into account five Linux kernels, four CPU models, two memory systems, two Linux boot types, and four CPU core counts

We conducted these tests using the X86 ISA.
Our methodology should extend easily to other ISAs as well, but we haven't run these tests, yet.
We welcome other contributors to run these tests!

Following are the details of each of these:

### Linux Kernel

We evaluated gem5 using the five latest LTS (long term support) kernels shown below.
We plan on continuing to test the LTS kernel releases and the most recent kernel on each gem5 release.

- v4.4.186 (released on 2016-01-10)
- v4.9.186 (released on 2016-12-11)
- v4.14.134 (released on 2017-11-12)
- v4.19.83 (released on 2018-10-22)
- v5.4 (released on 2019-11-24)

### CPU Model

We used four CPU models supported in gem5:

- **kvmCPU:** A CPU that does not do any timing simulation, but rather uses actual hardware to run the simulated code. It is mainly used for fast forwarding.
- **AtomicSimpleCPU:** This CPU also does not do any timing simulation and uses atomic memory accesses. It is mostly used for fast forwarding and cache warming.
- **TimingSimpleCPU:** This is a single cycle CPU model except for memory operations (it uses timing memory accesses).
- **O3CPU:** This is a detailed and highly configurable out of order CPU model (it does timing simulation for both CPU and memory).

### Memory System

There are two main memory systems supported in gem5 (which are used in these tests):

- **Classic:** The Classic memory system is fast and easily configurable and supports atomic accesses, but lacks cache coherence fidelity and flexibility (it models a simplified coherence protocol).
- **Ruby:**  The Ruby memory system models a detailed cache memory with detailed cache coherence protocols. However, it does not support atomic accesses and is slower compared to the classic memory system.

### Boot Type

Boot type refers to the kind of process which will take over once the kernel loads.
We use two different options:

- **init:** A custom init script which exits the system using the m5 exit instruction.
- **systemd:** Systemd is the default init system that makes the system ready for use by initializing different services and managing user processes.

## gem5art

We used [gem5art](https://gem5art.readthedocs.io/en/latest/index.html) (library for **a**rtifacts, **r**eproducibility, and **t**esting) to perform these experiments.
gem5art helps us to conduct gem5 experiments in a more structured and reproducible way.
We will, however, defer the detailed discussion on gem5art for a future blog post.
The gem5 configuration scripts used to run these experiments are available in the [gem5art repo](https://github.com/darchr/gem5art/tree/master/docs/gem5-configs/configs-boot-tests/) and the details of how these experiments were run using gem5art can be found in the [gem5art boot tutorial](https://gem5art.readthedocs.io/en/latest/tutorials/boot-tutorial.html).
The disk image and Linux kernel binaries we used are available from the following links (**warning:** the sizes of these files range from few MBs to 2GB):

- [disk image (GZIPPED)](http://dist.gem5.org/dist/current/images/x86/ubuntu-18-04/base.img.gz) (**Note:** /root/.bashrc in this disk image contains `m5 exit`, which will make the guest terminate the simulation as soon as it boots)
- [vmlinux-4.4.186](http://dist.gem5.org/dist/current/kernels/x86/static/vmlinux-4.4.189)
- [vmlinux-4.9.186](http://dist.gem5.org/dist/current/kernels/x86/static/vmlinux-4.9.186)
- [vmlinux-4.14.134](http://dist.gem5.org/dist/current/kernels/x86/static/vmlinux-4.14.134)
- [vmlinux-4.19.83](http://dist.gem5.org/dist/current/kernels/x86/static/vmlinux-4.19.83)
- [vmlinux-5.4.49](http://dist.gem5.org/dist/current/kernels/x86/static/vmlinux-5.4.49)

## Linux Booting Status

Figure 1 and 2 show the results of these experiments with the classic memory system for the init and systemd boot types respectively.
Figure 3 and 4 show the results of these experiments for the ruby memory system for the init and systemd boot types respectively.
All possible status outputs (shown in the figures below) are defined as follows:

- **timeout:** experiment did not finish in a reasonable amount of time (8 hours: this time was chosen as we found similar successful cases did not exceed this limit on the same host machine).
- **not-supported:** cases which are not yet supported in gem5.
- **success:** cases where Linux booted successfully.
- **sim-crash:** cases where gem5 crashed.
- **kernel-panic:** cases where kernel went into panic during simulation.

When using a classic memory system, KVM and Atomic CPU models always work.
TimingSimple CPU always works for a single core, but fails to boot the kernel for multiple CPU cores.
The O3 CPU model fails to simulate kernel booting in most of the cases (the only success is init boot type with two Linux kernel versions).

![Linux boot status for classic memory system and init boot](/assets/img/blog/boot_classic_init.png)
<br>
*Figure 1: Linux boot status for classic memory system and init boot*


![Linux boot status for classic memory system and systemd boot](/assets/img/blog/boot_classic_systemd.png)
<br>
*Figure 2: Linux boot status for classic memory system and systemd boot*

As shown in Figure 3 and 4, for Ruby memory system, KVM and Atomic CPU models seem to work except for a couple of cases where even the KVM CPU model times out.
TimingSimple CPU works up to 2 cores, but fails for 4 and 8 cores.
The O3 CPU model fails to simulate Linux booting or times out in all cases.

![Linux boot status for ruby memory system and init boot](/assets/img/blog/boot_ruby_init.png)
<br>
*Figure 3: Linux boot status for ruby memory system and init boot*

![Linux boot status for ruby memory system and systemd boot](/assets/img/blog/boot_ruby_systemd.png)
<br>
*Figure 4: Linux boot status for ruby memory system and systemd boot*

The raw data/results of these experiments is available from this [link](http://dist.gem5.org/boot-test-results/boot_tests.zip) (warning: file size of ~40MB).

## Moving Forward

Researchers mostly fast-forward simulations during Linux boot to avoid the problems seen above or end up using older kernel versions.
This leads to uncertainty in simulation results and conclusions drawn from such experiments.
As a community, we should not overlook these problems and try to enable gem5 to successfully run these boot tests.
There are a few JIRA issues
([GEM5-359](https://gem5.atlassian.net/projects/GEM5/issues/GEM5-359), [GEM5-360](https://gem5.atlassian.net/projects/GEM5/issues/GEM5-360))
open to document these problems with the hope of eventually fixing them.
A gem5 [issue](https://gem5.googlesource.com/public/gem5/+/de24aafc161f348f678e0e0fc30b1ff2d145043b) related to TimingSimple CPU with Ruby memory system has already been fixed on the develop branch and will be part of gem5-20.

Furthermore, we need to repeat these tests for new releases of gem5, and as new Linux kernels become available.
We hope to keep the gem5 community up-to-date with the outcome of these tests via a new page on the gem5 website soon.
