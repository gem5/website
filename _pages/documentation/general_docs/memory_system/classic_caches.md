---
layout: documentation
title: "Classic caches"
doc: gem5 documentation
parent: memory_system
permalink: /documentation/general_docs/memory_system/classic_caches/
author: Jason Lowe-Power
---

# Classic Caches

The default cache is a non-blocking cache with MSHR (miss status holding
register) and WB (Write Buffer) for read and write misses. The Cache can
also be enabled with prefetch (typically in the last level of cache).

There are multiple possible [replacement policies](/documentation/general_docs/memory_system/replacement_policies) and [indexing
policies](/documentation/general_docs/memory_system/indexing_policies) implemented in gem5. These define, respectively, the possible
blocks that can be used for a block replacement given an address, and
how to use the address information to find a block\'s location. By
default the cache lines are replaced using [LRU (least recently used)](/documentation/general_docs/memory_system/replacement_policies),
and indexed with the [Set Associative](/documentation/general_docs/memory_system/indexing_policies) policy.


# Interconnects

### Crossbars

The two types of traffic in the crossbar are memory-mapped packets and
snooping packets. The memory-mapped requests go down the memory
hierarchy, and responses go up the memory hierarchy (same route back).
The snooping requests go horizontally and up the cache hierarchy,
snooping responses go horizontally and down the hierarchy (same route
back). Normal snoops go horizontally and express snoops go up the cache
hierarchy.

![Bus Connections](/assets/img/Bus.png)

### Bridges

### Others...

# Debugging

There is a feature in the classic memory system for displaying the coherence state of a particular block from within the debugger (e.g., gdb). This feature is built on the classic memory system's support for functional accesses. (Note that this feature is currently rarely used and may have bugs.)

If you inject a functional request with the command set to PrintReq, the packet traverses the memory system (like a regular functional request) but on any object that matches (other queued packet, cache block, etc.) it simply prints out some information about that object.

There's a helper method on Port called printAddr() that takes an address and builds an appropriate PrintReq packet and injects it. Since it propagates using the same mechanism as a normal functional request, it needs to be injected from a port where it will propagate through the whole memory system, such as at a CPU. There are helper printAddr() methods on MemTest, AtomicSimpleCPU, and TimingSimpleCPU objects that simply call printAddr() on their respective cache ports. (Caveat: the latter two are untested.)

Putting it all together, you can do this:

```
(gdb) set print object
(gdb) call SimObject::find(" system.physmem.cache0.cache0.cpu")
$4 = (MemTest *) 0xf1ac60
(gdb) p (MemTest*)$4
$5 = (MemTest *) 0xf1ac60
(gdb) call $5->printAddr(0x107f40)

system.physmem.cache0.cache0
  MSHRs
    [107f40:107f7f] Fill   state:
      Targets:
        cpu: [107f40:107f40] ReadReq
system.physmem.cache1.cache1
  blk VEM
system.physmem
  0xd0
```

... which says that cache0.cache0 has an MSHR allocated for that address to serve a target ReadReq from the CPU, but it's not in service yet (else it would be marked as such); the block is valid, exclusive, and modified in cache1.cache1, and the byte has a value of 0xd0 in physical memory.

Obviously it's not necessarily all the info you'd want, but it's pretty useful. Feel free to extend. There's also a verbosity parameter that's currently not used that could be exploited to have different levels of output.

Note that the extra "p (MemTest*)$4" is needed since although "set print object" displays the derived type, internally gdb still considers the pointer to be of the base type, so if you try and call printAddr directly on the $4 pointer you get this:

```
(gdb) call $4->printAddr(0x400000)
Couldn't find method SimObject::printAddr
```
