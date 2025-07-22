---
layout: documentation
title: Hello World Tutorial
parent: gem5-standard-library
doc: gem5 documentation
permalink: /documentation/gem5-stdlib/hello-world-tutorial
author: Bobby R. Bruce
---

<!-- The full code example at the bottom of the page works fine and 
is up to date
 -->

## Building a "Hello World" example with the gem5 standard library

In this tutorial we will cover how to create a very basic simulation using gem5 components.
This simulation will setup a system consisting of a single-core processor, running in Atomic mode, connected directly to main memory with no caches, I/O, or other components.
The system will run an X86 binary in syscall emulation (SE) mode.
The binary will be obtained from gem5-resources and which will print a "Hello World!" string to stdout upon execution.

To start we must compile the ALL build for gem5:

```sh
# In the root of the gem5 directory
scons build/ALL/gem5.opt -j <number of threads>
```

As of gem5 v24.1, the ALL build includes all Ruby protocols and all ISAs. If you are using a prebuilt gem5 binary, this step is not necessary.

Then a new Python file should be created (we will refer to this as `hello-world.py` going forward).
The first lines in this file should be the needed imports:

```python
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
```

All these libraries are included inside the compiled gem5 binary.
Therefore, you will not need to obtain them from elsewhere.
`from gem5.` indicates we are importing from the `gem5` standard library, and the lines starting with `from gem5.components` are importing components from the gem5 components package.
The `from gem5.resources` line means we are importing from the resources package, and `from gem5.simulate`, the simulate package.
All these packages, `components`, `resources`, and `simulate` are part of the gem5 standard library.

Next we begin specifying the system.
The gem5 library requires the user to specify four main components: the _board_, the _cache hierarchy_, the _memory system_, and the _processor_.

Let's start with the _cache hierarchy_:

```python
cache_hierarchy = NoCache()
```

Here we are using `NoCache()`.
This means, for our system, we are stating there is no cache hierarchy (i.e., no caches).
In the gem5 library the cache hierarchy is a broad term for anything that exists between the processor cores and main memory.
Here we are stating the processor is connected directly to main memory.

Next we declare the _memory system_:

```python
memory = SingleChannelDDR3_1600("1GiB")
```

There exists many memory components to choose from within `gem5.components.memory`.
Here we are using a single-channel DDR3 1600, and setting its size to 1 GiB.
It should be noted that setting the size here is technically optional.
If not set, the `SingleChannelDDR3_1600` will default to 8 GiB.

Then we consider the _processor_:

```python
processor = SimpleProcessor(cpu_type=CPUTypes.ATOMIC, num_cores=1, isa=ISA.X86)
```

A processor in `gem5.components` is an object which contains a number of gem5 CPU cores, of a particular or varying type (`ATOMIC`, `TIMING`, `KVM`, `O3`, etc.).
The `SimpleProcessor` used in this example is a processor where all the CPU Cores are of an identical type.
It requires two arguments: the `cpu_type`, which we set to `ATOMIC`, and `num_cores`, the number of cores, which we set to one.

Finally we specify which _board_ we are using:

```python
board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)
```

While the constructor of each board may vary, they will typically require the user to specify the _processor_, _memory system_, and _cache hierarchy_, as well as the clock frequency to use.
In this example we use the `SimpleBoard`.
The `SimpleBoard` is a very basic system with no I/O which only supports SE-mode and can only work with "classic" cache hierarchies.

At this point in the script we have specified everything we require to simulate our system.
Of course, in order to run a meaningful simulation, we must specify a workload for this system to run.
To do so we add the following lines:

```python
binary = obtain_resource("x86-hello64-static")
board.set_se_binary_workload(binary)
```

The `obtain_resource` function takes a string which specifies which resource, from [gem5-resources](/documentation/general_docs/gem5_resources), is to be obtained for the simulation.
All the gem5 resources can be found on the [gem5 Resources website](https://resources.gem5.org).

If the resource is not present on the host system it'll be automatically downloaded.
In this example we are going to use the `x86-hello-64-static` resource;
an x86, 64-bit, statically compiled binary which will print "Hello World!" to stdout.
After specifying the resource we set the workload via the board's `set_se_binary_workload` function.
As the name suggests `set_se_binary_workload` is a function used to set a binary to be executed in Syscall Execution mode.

You can see and search for available resources on the [gem5 resources website](https://resources.gem5.org/).

This is all that is required to setup your simulation.
From this you simply need to construct and run the `Simulator`:

```python
simulator = Simulator(board=board)
simulator.run()
```

As a recap, your script should look like the following:

```python
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

# Obtain the components.
cache_hierarchy = NoCache()
memory = SingleChannelDDR3_1600("1GiB")
processor = SimpleProcessor(cpu_type=CPUTypes.ATOMIC, num_cores=1, isa=ISA.X86)

# Add them to the board.
board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

# Set the workload.
binary = obtain_resource("x86-hello64-static")
board.set_se_binary_workload(binary)

# Setup the Simulator and run the simulation.
simulator = Simulator(board=board)
simulator.run()
```

It can then be executed with:

```sh
./build/ALL/gem5.opt hello-world.py
```

If you are using a pre-built binary, you can execute the simulation with:

```sh
gem5 hello-world.py
```

If setup correctly, the output will look something like:

```text
info: Using default config
Global frequency set at 1000000000000 ticks per second
src/mem/dram_interface.cc:690: warn: DRAM device capacity (8192 Mbytes) does not match the address range assigned (1024 Mbytes)
src/base/statistics.hh:279: warn: One of the stats is a legacy stat. Legacy stat is a stat that does not belong to any statistics::Group. Legacy stat is deprecated.
board.remote_gdb: Listening for connections on port 7005
src/sim/simulate.cc:199: info: Entering event queue @ 0.  Starting simulation...
src/sim/syscall_emul.hh:1117: warn: readlink() called on '/proc/self/exe' may yield unexpected results in various settings.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
Hello world!
```

It should be obvious from this point that a _board's_ parameters may be altered to test other designs.
For example, if we want to test a `TIMING` CPU setup we'd change our _processor_ to:

```python
processor = SimpleProcessor(cpu_type=CPUTypes.TIMING, num_cores=1, isa=ISA.X86)
```

This is all that is required.
The gem5 standard library will reconfigure the design as is necessary.

As another example, consider swapping out a component for another.
In this design we decided on `NoCache` but we could use another classic cache hierarchy, such as `PrivateL1CacheHierarchy`.
To do so we'd change our `cache_hierarchy` parameter:

```python
# We import the cache hierarchy we want.
from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy import PrivateL1CacheHierarchy

...

# Then set it.
cache_hierarchy = PrivateL1CacheHierarchy(l1d_size="32KiB", l1i_size="32KiB")
```

Note here that `PrivateL1CacheHierarchy` requires the user to specify the L1 data and instruction cache sizes to be constructed.
No other part of the design need change.
The gem5 standard library will incorporate the cache hierarchy as required.

To recap on what was learned in this tutorial:

* A system can be built with the gem5 components package using _processor_, _cache hierarchy_, _memory system_, and _board_ components.
* Generally speaking, components of the same type are interchangeable as much as is possible. E.g., different _cache hierarchy_ components may be swapped in and out of a design without reconfiguration needed in other components.
* _boards_ contain functions to set workloads.
* The resources package may be used to obtain prebuilt resources from gem5-resources.
These are typically workloads that may be run via set workload functions.
* The simulate package can be used to run a board within a gem5 simulation.
