---
layout: documentation
title: Developing Your Own Components Tutorial
parent: gem5-standard-library
doc: gem5 documentation
permalink: /documentation/gem5-stdlib/develop-own-components-tutorial
author: Bobby R. Bruce
---

## Developing your own gem5 standard library components

![gem5 component library design](/assets/img/stdlib/gem5-components-design.png)

The above diagram shows the basic design of the gem5 library components.
There are four important abstract classes: `AbstractBoard`, `AbstractProcessor`, `AbstractMemorySystem`, and `AbstractCacheHierarchy`.
Every gem5 component inherits from one of these to be a gem5 component usable in a design.
The `AbstractBoard` must be constructed by specifying an `AbstractProcessor`, `AbstractMemorySystem`, and an `AbstractCacheHierarchy`.
With this design any board may use any combination of components which inherit from `AbstractProcessor`, `AbstractMemorySystem`, and `AbstractCacheHierarchy`.
For example, using the image as a guide, we can add a `SimpleProcessor`, `SingleChannelDDR3_1600` and a `PrivateL1PrivateL2CacheHierarchy` to an `X86Board`.
If we desire, we can swap out the `PrivateL1PrivateL2CacheHierarchy` for another class which inherits from `AbstractCacheHierarchy`.

In this tutorial we will imagine a user wishes to create a new cache hierarchy.
As you can see from the diagram, there are two subclasses which inherit from `AbstractCacheHierarchy`: `AbstractRubyCacheHierarchy` and `AbstractClassicCacheHierarchy`.
While you _can_ inherit directly from `AbstractCacheHierarchy`, we recommend inheriting from the subclasses (depending on whether you wish to develop a ruby or classic cache hierarchy setup).
We will inherit from the `AbstractClassicCacheHierarchy` class to create a classic cache setup.

To begin, we should create a new Python class which inherits from the `AbstractClassicCacheHierarchy`.
In this example we will call this `UniqueCacheHierarchy`, contained within a file `unique_cache_hierarchy.py`:

```python
from gem5.components.cachehierarchies.classic.abstract_classic_cache_hierarchy import AbstractClassicCacheHierarchy
from gem5.components.boards.abstract_board import AbstractBoard

from m5.objects import Port

class UniqueCacheHierarchy(AbstractClassicCacheHierarchy):


    def __init__() -> None:
        AbstractClassicCacheHierarchy.__init__(self=self)

    def get_mem_side_port(self) -> Port:
        pass

    def get_cpu_side_port(self) -> Port:
        pass

    def incorporate_cache(self, board: AbstractBoard) -> None:
        pass
```

As with every abstract base class, there are virtual functions which must be implemented.
Once implemented the `UniqueCacheHierarchy` can be used in simulations.
The `get_mem_side_port` and `get_cpu_side_port` are declared in the [AbstractClassicCacheHierarchy](https://github.com/gem5/gem5/blob/stable/src/python/gem5/components/cachehierarchies/classic/abstract_classic_cache_hierarchy.py), while `incorporate_cache` is declared in the [AbstractCacheHierarchy](https://github.com/gem5/gem5/blob/stable/src/python/gem5/components/cachehierarchies/abstract_cache_hierarchy.py)

The `get_mem_side_port` and `get_cpu_side_port` functions return a `Port` each.
As their name suggests, these are ports used by the board to access the cache hierarchy from the memory side and the cpu side.
These must be specified for all classic cache hierarchy setups.

The `incorporate_cache` function is the function which is called to incorporate the cache into the board.
The contents of this function will vary between cache hierarchy setups but will typically inspect the board it is connected to, and use the board's API to connect the cache hierarchy.

In this example we assume the user is looking to implement a private L1 cache hierarchy, consisting of a data cache and instruction cache for each CPU core.
This has actually already been implemented in the gem5 stdlib as the [PrivateL1CacheHierarchy](https://github.com/gem5/gem5/blob/stable/src/python/gem5/components/cachehierarchies/classic/private_l1_cache_hierarchy.py), but for this example we shall duplicate the effort.

First we start by implementing the `get_mem_side_port` and `get_cpu_side_port` functions:

```python
from gem5.components.cachehierarchies.classic.abstract_classic_cache_hierarchy import AbstractClassicCacheHierarchy
from gem5.components.boards.abstract_board import AbstractBoard

from m5.objects import Port, SystemXBar, BadAddr

class UniqueCacheHierarchy(AbstractClassicCacheHierarchy):

    def __init__(self) -> None:
        AbstractClassicCacheHierarchy.__init__(self=self)
        self.membus =  SystemXBar(width=64)
        self.membus.badaddr_responder = BadAddr()
        self.membus.default = self.membus.badaddr_responder.pio

    def get_mem_side_port(self) -> Port:
        return self.membus.mem_side_ports

    def get_cpu_side_port(self) -> Port:
        return self.membus.cpu_side_ports

    def incorporate_cache(self, board: AbstractBoard) -> None:
        pass
```

Here we have used a simple memory bus.

Next, we implement the `incorporate_cache` function:

```python
from gem5.components.cachehierarchies.classic.abstract_classic_cache_hierarchy import AbstractClassicCacheHierarchy
from gem5.components.cachehierarchies.classic.caches.l1dcache import L1DCache
from gem5.components.cachehierarchies.classic.caches.l1icache import L1ICache
from gem5.components.cachehierarchies.classic.caches.mmu_cache import MMUCache
from gem5.components.boards.abstract_board import AbstractBoard

from m5.objects import Port, SystemXBar, BadAddr, Cache

class UniqueCacheHierarchy(AbstractClassicCacheHierarchy):

    def __init__(self) -> None:
        AbstractClassicCacheHierarchy.__init__(self=self)
        self.membus =  SystemXBar(width=64)
        self.membus.badaddr_responder = BadAddr()
        self.membus.default = self.membus.badaddr_responder.pio

    def get_mem_side_port(self) -> Port:
        return self.membus.mem_side_ports

    def get_cpu_side_port(self) -> Port:
        return self.membus.cpu_side_ports

    def incorporate_cache(self, board: AbstractBoard) -> None:
        # Set up the system port for functional access from the simulator.
        board.connect_system_port(self.membus.cpu_side_ports)

        for cntr in board.get_memory().get_memory_controllers():
            cntr.port = self.membus.mem_side_ports

        self.l1icaches = [
            L1ICache(size="32KiB")
            for i in range(board.get_processor().get_num_cores())
        ]

        self.l1dcaches = [
            L1DCache(size="32KiB")
            for i in range(board.get_processor().get_num_cores())
        ]
        # ITLB Page walk caches
        self.iptw_caches = [
            MMUCache(size="8KiB") for _ in range(board.get_processor().get_num_cores())
        ]
        # DTLB Page walk caches
        self.dptw_caches = [
            MMUCache(size="8KiB") for _ in range(board.get_processor().get_num_cores())
        ]

        if board.has_coherent_io():
            self._setup_io_cache(board)

        for i, cpu in enumerate(board.get_processor().get_cores()):

            cpu.connect_icache(self.l1icaches[i].cpu_side)
            cpu.connect_dcache(self.l1dcaches[i].cpu_side)

            self.l1icaches[i].mem_side = self.membus.cpu_side_ports
            self.l1dcaches[i].mem_side = self.membus.cpu_side_ports

            self.iptw_caches[i].mem_side = self.membus.cpu_side_ports
            self.dptw_caches[i].mem_side = self.membus.cpu_side_ports

            cpu.connect_walker_ports(
                self.iptw_caches[i].cpu_side, self.dptw_caches[i].cpu_side
            )

            int_req_port = self.membus.mem_side_ports
            int_resp_port = self.membus.cpu_side_ports
            cpu.connect_interrupt(int_req_port, int_resp_port)

    def _setup_io_cache(self, board: AbstractBoard) -> None:
        """Create a cache for coherent I/O connections"""
        self.iocache = Cache(
            assoc=8,
            tag_latency=50,
            data_latency=50,
            response_latency=50,
            mshrs=20,
            size="1kB",
            tgts_per_mshr=12,
            addr_ranges=board.mem_ranges,
        )
        self.iocache.mem_side = self.membus.cpu_side_ports
        self.iocache.cpu_side = board.get_mem_side_coherent_io_port()
```

This completes the code we'd need to create our own cache hierarchy.

To use this code, a user can import it as they would any other Python module.
As long as this code is in gem5's python search path, you can import it.
You can also add `import sys; sys.path.append(<path to new component>)` at the beginning of your gem5 runscript to add the path of this new component to the python search path.

## Contributing your component to the gem5 stdlib

Before contributing your component, you will need to move it into the `src/` directory so that it is compiled into the gem5 binary.

### Compiling your component into the gem5 standard library

The gem5 standard library code resides in `src/python/gem5`.
The basic directory structure is as follows:

```
gem5/
    components/                 # All the components to build the system to simulate.
        boards/                 # The boards, typically broken down by ISA target.
            experimental/       # Experimental boards.
        cachehierarchies/       # The Cache Hierarchy components.
            chi/                # CHI protocol cache hierarchies.
            classic/            # Classic cache hierarchies.
            ruby/               # Ruby cache hierarchies.
        memory/                 # Memory systems.
        processors/             # Processors.
    prebuilt/                   # Prebuilt systems, ready to use.
        demo/                   # Prebuilt System for demonstrations. (not be representative of real-world targets).
    resources/                  # Utilities used for referencing and obtaining gem5-resources.
    simulate/                   # A package for the automated running of gem5 simulations.
    utils/                      # General utilities.
```

We recommend putting the `unique_cache_hierarchy.py` in `src/python/gem5/components/cachehierarchies/classic/`.

From then you need to add the following line to `src/python/SConscript`:

```
PySource('gem5.components.cachehierarchies.classic',
    'gem5/components/cachehierarchies/classic/unique_cache_hierarchy.py')
```

Then, when you recompile the gem5 binary, the `UniqueCacheHierarchy` class will be included.
To use it in your own scripts you need only include it:

```python
from gem5.components.cachehierarchies.classic.unique_cache_hierarchy import UniqueCacheHierarchy

...

cache_hierarchy = UniqueCacheHierarchy()

...

```

### gem5 Code contribution and review

If you believe your addition to the gem5 stdlib would be beneficial to the gem5 community, you may submit it as a patch.
Please follow our [Contributing Guidelines](/contributing) if you have not contributed to gem5 before or need a reminder on our procedures.

In addition to our normal contribution guidelines, we strongly advise you do the following to your stdlib contribution:

* **Add Documentation**: Classes and methods should be documented using [reStructured text](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html).
Please look over other source code in the stdlib to see how this is typically done.
* **Use Python Typing**: Utilize the [Python typing module](https://docs.python.org/3/library/typing.html) to specify parameter and method return types.
* **Use relative imports**: Within the gem5 stdlib, relative imports should be used to reference other modules/package in the stdlib (i.e., that contained in `src/python/gem5`).
* **Format using black**: Please format your Python code with [Python black](https://pypi.org/project/black/), with 79 max line widths: `black --line-length=79 <file/directory>`.
**Note**: Python black does not always enforce line lengths.
For example, it will not reduce string lengths.
You may have to manually reduce the length of some lines.

Code will be reviewed via our [Gerrit code review system](https://gem5-review.googlesource.com/) like all other contributions.
We would, however, emphasize that we will not accept patches to the library for simply being functional and tested;
we require some persuasion that the contribution improves the library and benefits the community.
For example, niche components may not be incorporated if they are seen to be low utility while increasing the library's maintenance overhead.
