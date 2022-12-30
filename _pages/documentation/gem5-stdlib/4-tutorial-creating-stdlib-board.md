---
layout: documentation
title: How To Create Your Own Board Using The gem5 Standard Library
parent: gem5-standard-library
doc: gem5 documentation
permalink: /documentation/gem5-stdlib/develop-stdlib-board
author: Jasjeet Rangi, Kunal Pai
---

## How to Create Your Own Board Using the gem5 Standard Library

In this tutorial we will cover how to create a custom  board using the gem5 Standard Library.


This tutorial is based on the process used to make the _RiscvMatched_, a RISC-V prebuilt board that inherits from `MinorCPU`. This board can be found at `src/python/gem5/prebuilt/riscvmatched`.

This tutorial will create a single-channeled DDR4 memory of size 2 GiB, a core using the MinorCPU and the RISC-V ISA though the same process can be used for another type or size of memory, ISA and core.

Likewise, this tutorial will utilize the UniqueCacheHierarchy made in the [Developing Your Own Components Tutorial](https://www.gem5.org/documentation/gem5-stdlib/develop-own-components-tutorial), though anyother cache hierarchy may be used.

First, we start by importing the components and stdlib features we require.

``` python
from gem5.components.cachehierarchies.classic.unique_cache_hierarchy import UniqueCacheHierarchy
from gem5.components.boards.abstract_system_board import AbstractSystemBoard
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.boards.se_binary_workload import SEBinaryWorkload
from gem5.components.memory import SingleChannelDDR4_2400
from gem5.utils.override import overrides
from gem5.isas import ISA
from typing import List
from m5.objects import AddrRange, IOXBar, Port
from m5.objects import BaseMMU, Port, BaseCPU, Process
from m5.objects.RiscvCPU import RiscvMinorCPU
```

We will begin development by creating a specialized CPU core for our board which inherits from an ISA-specific version of the chosen CPU.
Since our ISA is RISC-V and the CPU type we desire is a MinorCPU, we will inherit from `RiscvMinorCPU`.
This is done so that we can set our own parameters to tailor the CPU it to our requirements.
In our example will override a single parameter:  `decodeToExecuteForwardDelay` (the default is 1).
We have called this new CPU core type `UniqueCPU`.


``` python
class UniqueCPU(RiscvMinorCPU):
    decodeToExecuteForwardDelay = 2
```

As `RiscvMinorCPU` inherits from `BaseCPU`, we can incorporate this into the standard library using `BaseCPUCore`, a Standard Library wrapper for `BaseCPU` objects (source code for this can be found at `src/python/gem5/components/processors/base_cpu_core.py`).
The `BaseCPUCore` takes the `BaseCPU` as an argument during construction.
Ergo, we can do the following:

```python
core = BaseCPUCore(core = UniqueCPU(core_id=0))
```

**Note**: `BaseCPU` objects require a unique `core_id` to be specified upon construction.

Next we must define our processor.
In the gem5 Standard Library a processor is a collection of cores.
In cases, such as ours, we can utilize the library's `BaseCPUProcessor`, a processor which contains `BaseCPUCore` objects (source code can be found in `src/python/gem5/components/processors/base_cpu_processor.py`).
The `BaseCPUProcessor` requires a list of `BaseCPUCore`s.
Therefore:

```python
processor = BaseCPUProcessor(cores = [core])
```

Next we focus on the construction of the board to host our components.
All boards must inherit from `AbstractBoard` and in most cases, gem5's `System` simobject.
Therefore, our board will inherit from `AbstractSystemBoard` in this case; an abstract class that inherits from both.

In order to run simulations with SE mode, we must also inherit from `SEBinaryWorkload`.

All `AbstractBoard`s must specify `clk_freq` (the clock frequency), the `processor`, `memory`, and the `cache_hierarchy`.
We already have our processor, and will use the `UniqueCacheHierarchy` for the `cache_hierarchy` and a `SingleChannelDDR4_2400`, with a size of 2GiB for the memory.

We will call this the `UniqueBoard` and it should look like the following:

``` python
class UniqueBoard(AbstractSystemBoard, SEBinaryWorkload):
    def __init__(
        self,
        clk_freq: str,
    ) -> None:
        core = BaseCPUCore(core = UniqueCPU(core_id=0))
        processor = BaseCPUProcessor(cores = [core])
        memory = SingleChannelDDR4_2400("2GiB")
        cache_hierarchy = UniqueCacheHierarchy()
        super().__init__(
            clk_freq=clk_freq,
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
        )
```

With the contructor complete, we must implement the abstract methods in `AbstractSystemBoard`.
It is useful here to look at the source for `AbstractBoard` in `/src/python/gem5/components/boards/abstract_system_board.py`.

The abstract methods you choose to implement or not will depend on what type of system you are creating.
In our example functions such as `_setup_board`, are unneeded so we will implement them with `pass`.
In other instances we will use `NotImplementedError` for cases where a particular component/feature is not available on this board and an error should be returned if trying to access it.
For example, our board will have no IO bus.
We will therefore implement `has_io_bus` to return `False` and have `get_io_bus` raise a `NotImplementedError` if called.

With the exception of `_setup_memory_ranges`, we do not implement many of the features the `AbstractSystemBoard` requires. The board should look like this:

``` python
class UniqueBoard(AbstractSystemBoard, SEBinaryWorkload):
    def __init__(
        self,
        clk_freq: str,
    ) -> None:
        core = BaseCPUCore(core = UniqueCPU(core_id=0))
        processor = BaseCPUProcessor(cores = [core])
        memory = SingleChannelDDR4_2400("2GiB")
        cache_hierarchy = UniqueCacheHierarchy()
        super().__init__(
            clk_freq=clk_freq,
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
        )

    @overrides(AbstractSystemBoard)
    def _setup_board(self) -> None:
        pass

    @overrides(AbstractSystemBoard)
    def has_io_bus(self) -> bool:
        return False

    @overrides(AbstractSystemBoard)
    def get_io_bus(self) -> IOXBar:
        raise NotImplementedError(
            "UniqueBoard does not have an IO Bus. "
            "Use `has_io_bus()` to check this."
        )

    @overrides(AbstractSystemBoard)
    def has_dma_ports(self) -> bool:
        return False

    @overrides(AbstractSystemBoard)
    def get_dma_ports(self) -> List[Port]:
        raise NotImplementedError(
            "UniqueBoard does not have DMA Ports. "
            "Use `has_dma_ports()` to check this."
        )

    @overrides(AbstractSystemBoard)
    def has_coherent_io(self) -> bool:
        return False

    @overrides(AbstractSystemBoard)
    def get_mem_side_coherent_io_port(self) -> Port:
        raise NotImplementedError(
            "UniqueBoard does not have any I/O ports. Use has_coherent_io to "
            "check this."
        )

    @overrides(AbstractSystemBoard)
    def _setup_memory_ranges(self) -> None:
        memory = self.get_memory()
        self.mem_ranges = [AddrRange(memory.get_size())]
        memory.set_memory_range(self.mem_ranges)
```


This concludes the creation of your custom board for the gem5 standard library.
From this you can create a runscript and test your board:

``` python
from .unqiue_board import UniqueBoard
from gem5.resources.resource import Resource
from gem5.simulate.simulator import Simulator

board = UniqueBoard(clk_freq="1.2GHz")

#As we are using the RISCV ISA, "riscv-hello" should work.
board.set_se_binary_workload(Resource("riscv-hello"))

simulator = Simulator(board=board)
simulator.run()
```
