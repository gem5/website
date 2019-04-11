---
title: "ASPLOS 2008"
date: 2018-05-13T18:51:37-04:00
draft: false
weight: 1000
---

Using the M5 Simulator ASPLOS 2008 Tutorial Sunday March 2nd, 2008

## Introduction

This half-day tutorial will introduce participants to the [M5 simulator
system](Main_Page "wikilink"). M5 is a modular platform for computer
system architecture research, encompassing system-level architecture as
well as processor microarchitecture.

We will be discussing version 2.0 of the M5 simulator and specifically
its new features including:

  - Multiple ISA support (Alpha, ARM, MIPS, and SPARC)
  - An execute-in-execute out-of-order SMT CPU timing model, with no
    SimpleScalar license encumbrance
  - Message-oriented interface for memory system objects, designed to
    simplify the development of non-bus interconnects
  - New caches models that are easier to modify
  - New multi-level bus-based coherence protocol
  - More extensive Python integration and scripting support
  - Performance improvements
  - Generating checkpoints for simpoints



Because the primary focus of the M5 development team has been simulation
of network-oriented server workloads, M5 incorporates several features
not commonly found in other simulators.

  - Full-system simulation using unmodified Linux 2.4/2.6, FreeBSD, or
    Solaris (More are on the way)
  - Detailed timing of I/O device accesses and DMA operations
  - Accurate, deterministic simulation of multiple networked systems
  - Flexible, script-driven configuration to simplify specification of
    complex multi-system configurations
  - Included network workloads such as Apache, NAT, and NFS
  - Support for storing results from multiple simulations in a unified
    database (e.g. MySQL) for automated reporting and graph generation

M5 also integrates a number of other desirable features, including
pervasive object orientation, multiple interchangeable CPU models, an
event-driven memory system model, and multiprocessor capability.
Additionally, M5 is also capable of application-only simulation using
syscall emulation.

M5 is freely distributable under a BSD-style license, and does not
depend on any commercial or restricted-license software.

## Intended Audience

Researchers in academia or industry looking for a free, open-source,
full-system simulation environment for processor, system, or platform
architecture studies. Please register via the
[ASPLOS 2008](http://research.microsoft.com/asplos08/registration.htm)
web page.

## Tentative Topics

The following topics will be discussed in detail during the tutorial:

  - M5 structure
  - Object structures
  - Specifying configurations
  - Object serialization (checkpoints)
  - Events
  - CPU models
  - Memory/Cache models
  - I/O devices
  - Full-system modeling
  - Statistics
  - Debugging techniques
  - ISA description language
  - Future directions

## Speakers

  - Ali G. Saidi is a Ph.D. candidate in the EECS Department at the
    University of Michigan, and wrote much of the platform code for
    Linux full-system simulation. He received a BS in electrical
    engineering from the University of Texas at Austin and an MSE in
    computer science and engineering from the University of Michigan.

<!-- end list -->

  - Steven K. Reinhardt is an associate professor in the EECS Department
    at the University of Michigan, and a principal developer of M5. He
    received a BS from Case Western Reserve University and an MS from
    Stanford University, both in electrical engineering, and a PhD in
    computer science from the University of Wisconsin-Madison. While at
    Wisconsin, he was the principal developer of the Wisconsin Wind
    Tunnel parallel architecture simulator.

<!-- end list -->

  - Nathan L. Binkert is currently a Senior Research Scientist with HP
    Labs and a principal developer of M5. He received a BSE in
    electrical engineering and an MS and a PhD in computer science both
    from the University of Michigan. As an intern at Compaq VSSAD, he
    was a principal developer of the ASIM simulator, currently in
    widespread use at Intel.

<!-- end list -->

  - Steve Hines is a Ph.D. candidate in the CS Department at Florida
    State University, and created the ARM port of M5. He received a BS
    from Illinois Institute of Technology and an MS from Florida State
    University.

__NOTOC__

