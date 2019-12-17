---
layout: documentation
title: "MOESI hammer"
doc: gem5 documentation
parent: ruby
permalink: /documentation/general_docs/ruby/MOESI_hammer/
author: Jason Lowe-Power
---

# MOESI Hammer

This is an implementation of AMD's Hammer protocol, which is used in
AMD's Hammer chip (also know as the Opteron or Athlon 64). The protocol
implements both the original a HyperTransport protocol, as well as the
more recent ProbeFilter protocol. The protocol also includes a full-bit
directory mode.

### Related Files

  - **src/mem/protocols**
      - **MOESI_hammer-cache.sm**: cache controller specification
      - **MOESI_hammer-dir.sm**: directory controller specification
      - **MOESI_hammer-dma.sm**: dma controller specification
      - **MOESI_hammer-msg.sm**: message type specification
      - **MOESI_hammer.slicc**: container file

### Cache Hierarchy

This protocol implements a 2-level private cache hierarchy. It assigns
separate Instruction and Data L1 caches, and a unified L2 cache to each
core. These caches are private to each core and are controlled with one
shared cache controller. This protocol enforce exclusion between L1 and
L2
caches.

### Stable States and Invariants

| States | Invariants                                                                                                                                                                                                          |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **MM** | The cache block is held exclusively by this node and is potentially locally modified (similar to conventional "M" state).                                                                                           |
| **O**  | The cache block is owned by this node. It has not been modified by this node. No other node holds this block in exclusive mode, but sharers potentially exist.                                                      |
| **M**  | The cache block is held in exclusive mode, but not written to (similar to conventional "E" state). No other node holds a copy of this block. Stores are not allowed in this state.                                  |
| **S**  | The cache line holds the most recent, correct copy of the data. Other processors in the system may hold copies of the data in the shared state, as well. The cache line can be read, but not written in this state. |
| **I**  | The cache line is invalid and does not hold a valid copy of the data.                                                                                                                                               |

### Cache controller

**The notation used in the controller FSM diagrams is described
[here](#Coherence_controller_FSM_Diagrams "wikilink").**

MOESI_hammer supports cache flushing. To flush a cache line, the cache
controller first issues a GETF request to the directory to block the
line until the flushing is completed. It then issues a PUTF and writes
back the cache line.

![MOESI_hammer_cache_FSM.jpg](/assets/img/MOESI_hammer_cache_FSM.jpg
"MOESI_hammer_cache_FSM.jpg")

### Directory controller

MOESI_hammer memory module, unlike a typical directory protocol, does
not contain any directory state and instead broadcasts requests to all
the processors in the system. In parallel, it fetches the data from the
DRAM and forward the response to the requesters.

probe filter: TODO

#### **Stable States and Invariants**

| States | Invariants                                                           |
| ------ | -------------------------------------------------------------------- |
| **NX** | Not Owner, probe filter entry exists, block in O at Owner.           |
| **NO** | Not Owner, probe filter entry exists, block in E/M at Owner.         |
| **S**  | Data clean, probe filter entry exists pointing to the current owner. |
| **O**  | Data clean, probe filter entry exists.                               |
| **E**  | Exclusive Owner, no probe filter entry.                              |

#### **Controller**

**The notation used in the controller FSM diagrams is described
[here](#Coherence_controller_FSM_Diagrams "wikilink").**

![MOESI_hammer_dir_FSM.jpg](/assets/img/MOESI_hammer_dir_FSM.jpg
"MOESI_hammer_dir_FSM.jpg")
