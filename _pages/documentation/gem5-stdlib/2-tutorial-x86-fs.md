---
layout: documentation
title: X86 Full-System Tutorial
parent: gem5-standard-library
doc: gem5 documentation
permalink: /documentation/gem5-stdlib/x86-full-system-tutorial
author: Bobby R. Bruce
---

## Building an x86 full-system simulation with the gem5 standard library

One of the key ideas behind the gem5 standard library is to allow users to simulate, big, complex systems, with minimal effort.
This is done by making sensible assumptions about the nature of the system to simulate and connecting components in a manner which "makes sense."
While this takes away some flexibility, it massively simplifies simulating typical hardware setups in gem5.
The overarching philosophy is to make the _common case_ simple.

In this tutorial we will build an X86 simulation, capable of running a full-system simulation, booting an Ubuntu operating system, and running a benchmark.
This system will utilize gem5's ability to switch cores, allowing booting of the operating system in KVM fast-forward mode and switching to a detailed CPU model to run the benchmark, and use a MESI Two Level Ruby cache hierarchy in a dual-core setup.
Without using the gem5 library this would take several hundred lines of Python, forcing the user to specify details such as every IO component and exactly how the cache hierarchy is setup.
Here, we will demonstrate how simple this task can be with using the gem5 standard library.

As we focus on X86, we must must build the gem5 X86 binary:

```sh
scons build/X86/gem5.opt -j <number of threads>
```

To start, create a new Python file.
We will refer to this as `x86-ubuntu-run.py`.

To begin we add our import statements:

```python
from gem5.utils.requires import requires
from gem5.components.boards.x86_board import X86Board
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import MESITwoLevelCacheHierarchy
from gem5.components.processors.simple_switchable_processor import SimpleSwitchableProcessor
from gem5.coherence_protocol import CoherenceProtocol
from gem5.isas import ISA
from gem5.components.processors.cpu_types import CPUTypes
from gem5.resources.resource import Resource
from gem5.simulate.simulator import Simulator
from gem5.simulate.exit_event import ExitEvent
```

As in other Python scripts, these are simply classes/functions needed in our script.
They are all included as part of the gem5 binary and therefore do not need to obtained elsewhere.

A good start is to use the `requires` function to specify what kind of gem5 binary/setup is required to run the script:

```python
requires(
    isa_required=ISA.X86,
    coherence_protocol_required=CoherenceProtocol.MESI_TWO_LEVEL,
    kvm_required=True,
)
```

Here we state that we need gem5 compiled to run the X86 ISA and support the MESI Two Level protocol.
We also require the host system to have KVM.
**NOTE: Please ensure your host system supports KVM. If your system does not please remove the `kvm_required` check here**.
KVM will only work if the host platform and the simulated ISA are the same (e.g., X86 host and X86 simulation).

<!-- Can we provide a link to how to know if you have kvm? Related:https://gem5.atlassian.net/browse/GEM5-684-->

This `requires` call is not required but provides a good safety net to those running the script.
Errors that occur due to incompatible gem5 binaries may not make much sense otherwise.

Next we start specifying the components in our system.
We start with the _cache hierarchy_:

```python
cache_hierarchy = MESITwoLevelCacheHierarchy(
    l1d_size="32KiB",
    l1d_assoc=8,
    l1i_size="32KiB",
    l1i_assoc=8,
    l2_size="256KiB",
    l2_assoc=16,
    num_l2_banks=1,
)
```

Here we setup a MESI Two Level (ruby) cache hierarchy.
Via the constructor we set the L1 data cache and L1 instruction cache to 32 KiB, and the L2 cache to 256 KiB.

Next we setup the _memory system_:

```python
memory = SingleChannelDDR3_1600(size="2GiB")
```

This is quite simple and should be intuitive: A single channel DDR3 1600 setup of size 2GiB.
**Note:** by default the `SingleChannelDDR3_1600` component has a size of 8GiB.
However, due to [a known limitation with the X86Board](https://gem5.atlassian.net/browse/GEM5-1142), we cannot use a memory system greater than 3GiB.
We therefore must set the size.

Next we setup the _processor_:

```python
processor = SimpleSwitchableProcessor(
    starting_core_type=CPUTypes.KVM,
    switch_core_type=CPUTypes.TIMING,
    num_cores=2,
)
```

Here we are utilizing the gem5 standard library's special `SimpleSwitchableProcessor`.
This processor can be used for simulations in which a user wants to switch out one type of core for another during a simulation.
The `starting_core_type` parameter specifies which CPU type to start a simulation with.
In this case a KVM core.
**(Note: If your host system does not support KVM, this simulation will not run. You must change this to another CPU type, such as `CPUTypes.ATOMIC`)**
The `switch_core_type` parameter specifies which CPU type to switch to in a simulation.
In this case we'll be switching from KVM cores to TIMING cores.
The final parameter, `num_cores`, specifies the number of cores within the processor.

With this processor a user can call `processor.switch()` to switch to and from the starting cores and the switch cores, which we will demonstrate later on in this tutorial.

Next we add these components to the _board_:

```python
board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)
```

Here we use the `X86Board`.
This is a board used to simulate a typical X86 system in full-system mode.
As a minimum, the board needs the `clk_freq`, `processor`, `memory`, and `cache_hierarchy` parameters specified.
This finalizes our system design.

Now we set the workload to run on the system:

```python
command = "m5 exit;" \
        + "echo 'This is running on Timing CPU cores.';" \
        + "sleep 1;" \
        + "m5 exit;"

board.set_kernel_disk_workload(
    kernel=Resource("x86-linux-kernel-5.4.49",),
    disk_image=Resource("x86-ubuntu-18.04-img"),
    readfile_contents=command,
)
```

The `X86Board`'s `set_kernel_disk_workload` function requires a `kernel` and `disk_image` to be set.
Both these are obtainable from the gem5 resources repository.
Therefore, via the `Resource` class, we specify `x86-linux-kernel-5.4.49` for the Kernel (a Linux kernel, version 5.4.49, compiled to X86) and `x86-ubuntu-18.04-img` for the disk image (a disk image containing Ubuntu 18.04, for X86).
The `Resource` class will automatically retrieve these resources if they are not already present on the host system.
**Note: If a user wishes to use their own resource (that is, a resource not prebuilt as part of gem5-resources), they may follow the tutorial [here](../general_docs/gem5_resources.md)**

The `x86-ubuntu-18.04-img` has been designed to boot the OS, automatically login, and run `m5 readfile`.
The `m5 readfile` will read a file and execute it.
The contents of this file are specified via the `readfile_contents` parameter.
Therefore the value of` readfile_contents` will be executed on system startup.
**Note: `readfile_contents` is an optional argument. If it is not specified in `set_kernel_disk_workload` the simulation will exit after boot**.
This behavior is specific to the `x86-ubuntu-18.04-img` disk image and is not true for all disk images.

In this tutorial the script first runs `m5 exit`.
This temporarily exits the simulation allowing us to switch the CPUs from `KVM` to `TIMING`.
Then, when the simulation is resumed, the echo and sleep statements are executed (on the `TIMING` CPUs) and `m5 exit` is called again, thus exiting and completing the simulation.
Users may inspect `m5out/system.pc.com_1.device` to see the echo output.

Finally, we specify how the simulation is to be run with the following:

```python
simulator = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.EXIT : (func() for func in [processor.switch]),
    },
)
simulator.run()
```

The important thing to note here is the `on_exit_event` argument.
Here we can override default behavior.
The `m5 exit` command triggers an `EXIT` exit event in the `Simulator` module.
By default this exits the simulation run completely.
In our case we want the first `m5 exit` call to switch processors from KVM to TIMING cores.

The `on_exit_event` parameter is a Python dictionary of exit events and [Python generators](https://wiki.python.org/moin/Generators).
In this tutorial we are setting `ExitEvent.Exit` to the generator `(func() for func in [processor.switch])`.
This means the `processor.switch` function is called on the first yield of the generator (that is, on the first instance of `m5 exit`).
After this the generator is exhausted and the `Simulator` module will return to the default `Exit` exit event behavior.


This completes the setup of our script, to execute the script we run:

```
./build/X86/gem5.opt x86-ubuntu-run.py
```

You can see the output of the simulator in `m5out/system.pc.com_1.device`.

Below is the configuration script in full.
It mirrors closely the example script at `configs/example/gem5_library/x86-ubuntu-run.py` in the gem5 repository.

```python
from gem5.utils.requires import requires
from gem5.components.boards.x86_board import X86Board
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (MESITwoLevelCacheHierarchy,)
from gem5.components.processors.simple_switchable_processor import SimpleSwitchableProcessor
from gem5.coherence_protocol import CoherenceProtocol
from gem5.isas import ISA
from gem5.components.processors.cpu_types import CPUTypes
from gem5.resources.resource import Resource
from gem5.simulate.simulator import Simulator
from gem5.simulate.exit_event import ExitEvent

# This runs a check to ensure the gem5 binary is compiled to X86 and supports
# the MESI Two Level coherence protocol.
requires(
    isa_required=ISA.X86,
    coherence_protocol_required=CoherenceProtocol.MESI_TWO_LEVEL,
    kvm_required=True,
)

# Here we setup a MESI Two Level Cache Hierarchy.
cache_hierarchy = MESITwoLevelCacheHierarchy(
    l1d_size="32KiB",
    l1d_assoc=8,
    l1i_size="32KiB",
    l1i_assoc=8,
    l2_size="256kB",
    l2_assoc=16,
    num_l2_banks=1,
)

# Setup the system memory.
# Note, by default DDR3_1600 defaults to a size of 8GiB. However, a current
# limitation with the X86 board is it can only accept memory systems up to 3GB.
# As such, we must fix the size.
memory = SingleChannelDDR3_1600("2GiB")

# Here we setup the processor. This is a special switchable processor in which
# a starting core type and a switch core type must be specified. Once a
# configuration is instantiated a user may call `processor.switch()` to switch
# from the starting core types to the switch core types. In this simulation
# we start with KVM cores to simulate the OS boot, then switch to the Timing
# cores for the command we wish to run after boot.
processor = SimpleSwitchableProcessor(
    starting_core_type=CPUTypes.KVM,
    switch_core_type=CPUTypes.TIMING,
    num_cores=2,
)

# Here we setup the board. The X86Board allows for Full-System X86 simulations.
board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

# This is the command to run after the system has booted. The first `m5 exit`
# will stop the simulation so we can switch the CPU cores from KVM to timing
# and continue the simulation to run the echo command, sleep for a second,
# then, again, call `m5 exit` to terminate the simulation. After simulation
# has ended you may inspect `m5out/system.pc.com_1.device` to see the echo
# output.
command = "m5 exit;" \
        + "echo 'This is running on Timing CPU cores.';" \
        + "sleep 1;" \
        + "m5 exit;"

# Here we set the Full System workload.
# The `set_workload` function for the X86Board takes a kernel, a disk image,
# and, optionally, a the contents of the "readfile". In the case of the
# "x86-ubuntu-18.04-img", a file to be executed as a script after booting the
# system.
board.set_kernel_disk_workload(
    kernel=Resource("x86-linux-kernel-5.4.49",),
    disk_image=Resource("x86-ubuntu-18.04-img"),
    readfile_contents=command,
)

simulator = Simulator(
    board=board,
    on_exit_event={
        # Here we want override the default behavior for the first m5 exit
        # exit event. Instead of exiting the simulator, we just want to
        # switch the processor. The 2nd 'm5 exit' after will revert to using
        # default behavior where the simulator run will exit.
        ExitEvent.EXIT : (func() for func in [processor.switch]),
    },
)
simulator.run()
```

To recap what we learned in this tutorial:

* The `requires` function can be used to specify the gem5 and host requirements for a script.
* The `SimpleSwitchableProcessor` can be used to create a setup in which cores can be switched out for others.
* The `X86Board` can be used to setup full-system simulations.
Its `set_kernel_disk_workload` is used specify the kernel and disk image to use.
* The `set_kernel_disk_work` accepts a `readfile_contents` argument.
This is used to set the contents of the file to be read via gem5's `m5 readfile` function.
With the `x86-ubuntu-18.04-img` this is processed as a script to be executed after the system boot is complete.
* The `Simulator` module allows for the overriding of exit events using Python generators.
