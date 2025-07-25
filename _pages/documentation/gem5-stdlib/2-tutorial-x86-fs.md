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

First, we build the ALL binary. This will allow us to run simulations for any ISA, including X86:

```sh
scons build/ALL/gem5.opt -j <number of threads>
```

If you are using a prebuilt gem5 binary, this step is not necessary.

To start, create a new Python file.
We will refer to this as `x86-ubuntu-run.py`.

To begin we add our import statements:

```python
from gem5.coherence_protocol import CoherenceProtocol
from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (
    MESITwoLevelCacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_switchable_processor import (
    SimpleSwitchableProcessor,
)
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires
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
KVM will only work if the host platform and the simulated ISA are the same (e.g., X86 host and X86 simulation). You can learn more about using KVM with gem5 [here](https://www.gem5.org/documentation/general_docs/using_kvm/).

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
    isa=ISA.X86,
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
workload = obtain_resource("x86-ubuntu-24.04-boot-with-systemd")
board.set_workload(workload)
```

The `obtain_resource` function acquires the X86 Ubuntu 24.04 boot workload.
This workload contains a kernel resource, parameters to the kernel, a disk image resource, and a string indicating the underlying function that gem5 uses when `board.set_workload()` is called.
You can see these details under the [Raw](https://resources.gem5.org/resources/x86-ubuntu-24.04-boot-with-systemd/raw?database=gem5-resources&version=3.0.0) tab of of the gem5 Resources website page for this workload.

You can also use `set_kernel_disk_workload()` instead of `set_workload()` and set the disk image and kernel resources separately.
This can be used when you want to use your own resources, or a combination of resources that is not provided as a workload on [the gem5 resources website](resources.gem5.org).

**Note: If a user wishes to use their own resource (that is, a resource not prebuilt as part of gem5-resources), they may follow the tutorial [here](../general_docs/gem5_resources). A tutorial is also available at the [2024 gem5 bootcamp website](https://bootcamp.gem5.org/#02-Using-gem5/02-gem5-resources)**

When using the `set_kernel_disk_workload()` function, you can also pass an optional `readfile_contents` argument.
This will be run as a bash script after the system boots up, and can be used to launch a benchmark after the system boots if the disk image has benchmarks installed.
An example can be found [here](https://resources.gem5.org/resources/x86-ubuntu-24.04-npb-ua-b/raw?database=gem5-resources&version=2.0.0)

Finally, we specify how the simulation is to be run with the following:

```python
def exit_event_handler():
    print("First exit: kernel booted")
    yield False  # gem5 is now executing systemd startup
    print("Second exit: Started `after_boot.sh` script")
    # The after_boot.sh script is executed after the kernel and systemd have
    # booted.
    # Here we switch the CPU type to Timing.
    print("Switching to Timing CPU")
    processor.switch()
    yield False  # gem5 is now executing the `after_boot.sh` script
    print("Third exit: Finished `after_boot.sh` script")
    # The after_boot.sh script will run a script if it is passed via
    # readfile_contents. This is the last exit event before the simulation exits.
    yield True


simulator = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.EXIT: exit_event_handler(),
    },
)
simulator.run()
```

The important thing to note here is the `on_exit_event` argument.
Here we can override default behavior.

The `on_exit_event` parameter is a Python dictionary of exit events and [Python generators](https://wiki.python.org/moin/Generators).
In this tutorial we use the `exit_event_handler` generator to handle exit events of the type `ExitEvent.EXIT`.
There are three `EXIT` exit events in the Ubuntu 24.04 disk image resource used by the workload.
If an exit event handler is not defined, the simulation will end after the first exit event, which takes place after the kernel finishes booting.
Yielding `False` allows the simulation to continue, while yielding `True` ends the simulation.
After the second exit event, we switch the cores from KVM to TIMING, then yield `False` to continue the simulation.
After the third exit event, we yield `True`, ending the simulation.

This completes the setup of our script. To execute the script we run:

```bash
./build/ALL/gem5.opt x86-ubuntu-run.py
```

If you are using a pre-built binary, you can execute the simulation with:

```sh
gem5 hello-world.py
```

You can see the output of the simulator in `m5out/system.pc.com_1.device`.

Below is the configuration script in full.
It mirrors closely the example script at `configs/example/gem5_library/x86-ubuntu-run-with-kvm.py` in the gem5 repository.

```python
from gem5.coherence_protocol import CoherenceProtocol
from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (
    MESITwoLevelCacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_switchable_processor import (
    SimpleSwitchableProcessor,
)
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires

requires(
    isa_required=ISA.X86,
    coherence_protocol_required=CoherenceProtocol.MESI_TWO_LEVEL,
    kvm_required=True,
)

cache_hierarchy = MESITwoLevelCacheHierarchy(
    l1d_size="32KiB",
    l1d_assoc=8,
    l1i_size="32KiB",
    l1i_assoc=8,
    l2_size="256KiB",
    l2_assoc=16,
    num_l2_banks=1,
)

memory = SingleChannelDDR3_1600(size="2GiB")

processor = SimpleSwitchableProcessor(
    starting_core_type=CPUTypes.KVM,
    switch_core_type=CPUTypes.TIMING,
    isa=ISA.X86,
    num_cores=2,
)

board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

workload = obtain_resource("x86-ubuntu-24.04-boot-with-systemd")
board.set_workload(workload)


def exit_event_handler():
    print("First exit: kernel booted")
    yield False  # gem5 is now executing systemd startup
    print("Second exit: Started `after_boot.sh` script")
    # The after_boot.sh script is executed after the kernel and systemd have
    # booted.
    # Here we switch the CPU type to Timing.
    print("Switching to Timing CPU")
    processor.switch()
    yield False  # gem5 is now executing the `after_boot.sh` script
    print("Third exit: Finished `after_boot.sh` script")
    # The after_boot.sh script will run a script if it is passed via
    # readfile_contents. This is the last exit event before the simulation exits.
    yield True


simulator = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.EXIT: exit_event_handler(),
    },
)
simulator.run()

```

To recap what we learned in this tutorial:

* The `requires` function can be used to specify the gem5 and host requirements for a script.
* The `SimpleSwitchableProcessor` can be used to create a setup in which cores can be switched out for others.
* The `X86Board` can be used to set up full-system simulations.
* Its workload can be set via either `set_workload()` for workload resources, or via `set_kernel_disk_workload()` for separate kernel and disk image resources.
* The `set_kernel_disk_workload()` function accepts a `readfile_contents` argument.
This is processed as a script to be executed after the system boot is complete.
* The `Simulator` module allows for the overriding of exit events using Python generators.
