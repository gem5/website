---
layout: documentation
title: Standard Library Overview
parent: gem5-standard-library
doc: gem5 documentation
permalink: /documentation/gem5-stdlib/overview
author: Bobby R. Bruce
---

An overview of the gem5 standard library
========================================

Similar to standard libraries in programming languages, the gem5 standard library is designed to provide users of gem5 with commonly used components, features, and functionality with the goal of improving their productivity.
The gem5 stdlib was introduced in [v21.1](https://gem5.googlesource.com/public/gem5/+/refs/tags/v21.1.0.0) in an alpha-release state (then referred to as "gem5 components"), and has been fully released as of [v21.2](https://gem5.googlesource.com/public/gem5/+/refs/tags/v21.2.0.0).

For users new to the gem5 standard library, the following tutorials may be of help in understanding how the gem5 stdlib may be used to improve the creation of gem5 simulations.
They include a tutorial on building SE and FS simulations, as well as a guide on how to extend the library and contribute.
The [`configs/examples/gem5_library`](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/configs/example/gem5_library/) directory in the gem5 repository also contains example scripts which use the library.

The following subsections give a broad overview of the gem5 stdlib packages and what there intended purposes are.

**Note: The documentation/tutorial/etc. related to the standard library are for the v21.2 release.
Please ensure you have the correct version of gem5 before proceeding.**


The gem5 stdlib components package and its design philosophy
------------------------------------------------------------

The gem5 stdlib components package is the central part of the gem5 stdlib.
With it users can built complex systems from simple components which connect together using standardized APIs.

The metaphor that guided the components package development was that of building a computer using off-the-shelf components.
When building a computer, someone may select components, plug them into a board, and assume the interface between the board and the component have been designed in a way in which they will "just work".
For example, someone can remove a processor from a board and add a different one, compatible with the same socket, without needing to change everything else in their setup.
While there are always limitations to this design philosophy, the components package has a highly modular design with components of the same type being interchangeable with one another as much as is possible.

At the core of the components package is the idea of a _board_.
This plays a similar role to the motherboard in a real-world system.
While it may contain embedded caches, controllers, and other complex components, its main purpose is to expose standardized interfaces for other hardware to be added and handle communication between them.
For example, a memory stick and a processor may be added to a board with the board responsible for communication without the designer of the memory or the processor having to consider this assuming they conform to known APIs.

Typically, a gem5 components package _board_ requires declaration of these three components:

1. The _processor_ : The system processor. A processor component contains at least one _core_ which may be Atomic, O3, Timing, or KVM.
2. The _memory_ system: The memory system, for example, a DDR3_1600.
3. The _cache hierarchies_: This component defines any and all components between the processor and main memory, most notably the cache setup. In the simplest of setups this will connect memory directly to the processor.

A typical usage of the components may therefore look like:

```python

cache_hierarchy = MESITwoLevelCacheHierarchy(
    l1d_size="16kB",
    l1d_assoc=8,
    l1i_size="16kB",
    l1i_assoc=8,
    l2_size="256kB",
    l2_assoc=16,
    num_l2_banks=1,
)

memory = SingleChannelDDR3_1600(size="3GB")

processor = SimpleProcessor(cpu_type=CPUTypes.TIMING, num_cores=1)

board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)
```

The following tutorials go into greater detail on how to use the components package to create gem5 simulations.

The gem5 resources package
--------------------------

The gem5 stdlib's resource package is used to obtain and incorporate resources.
A resource, in the context of gem5, is something used in a simulation, or by a simulation, but not directly used to construct a system to be simulated.
Typically these are applications, kernels, disk images, benchmarks, or tests.

As these resources can be hard to find, or hard to create, we provide pre-built resources as part of [gem5-resources](/documentation/general_docs/gem5_resources).
For example, via gem5-resources, a user may download an Ubuntu 18.04 disk image with known compatibility with gem5.
They need not setup this themselves.

A core feature of the gem5 stdlib resource package is that it allows users to _automatically obtain_ prebuilt gem5 resources for their simulation.
A user may specify in their Python config file that a specific gem5 resource is required and, when run, the package will check if there is a local copy on the host system, and if not, download it.

The tutorials will demonstrate how to use the resource package in greater detail, but for now, a typical pattern is as follows:

```python
from gem5.resources.resource import Resource

resource = Resource("riscv-disk-img")

print(f"The resources is available at {resource.get_local_path()}")
```

This will obtain the `riscv-disk-img` resource and store it locally for use in a gem5 simulation.

The resources package references the [`resources.json` file](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/resources.json) in the [gem5-resources repository](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable) to get info on what resources are available and where they may be downloaded from.
While this is a machine-readable JSON file, users may use it to lookup the resources available.
**We hope in the near future to have a website which renders this in a more human-readable manner**.

The Simulate package
--------------------

**WARNING: The Simulate package is still in a BETA state. APIs in this package may change in future releases of gem5**.

The simulate package is used to run gem5 simulations.
While there is some boilerplate code this module handles on the users behalf, its primary purpose is to provde default behavior and APIs for what we refer to as _Exit Events_.
Exit events are when a simulation exits for a particular reason.

A typical example of an exit event would be a `Workbegin` exit event.
This is used to specify that a Region-of-Interest (ROI) has been reached.
Usually this exit would be used to allow a user to begin logging statistics or to switch to a more detailed CPU model.
Prior to the stdlib, the user would need to specify precisely what the expected behavior was at exit events such as this.
The simulation would exit and the configuration script would contain Python code specifying what to do next.
Now, with the simulate package, there is a default behavior for this kind of event (the stats are reset), and an easy interface to override this behavior with something the user requires.
