---
layout: documentation
title: "Cache Coherence Protocols"
doc: gem5 documentation
parent: ruby
permalink: /documentation/general_docs/ruby/cache-coherence-protocols/
author: Jason Lowe-Power
---

# Cache Coherence Protocols

## Common Notations and Data Structures

### **Coherence Messages**

These are described in the \<*protocol-name*\>-msg.sm file for each
protocol.

| Message           | Description                                                                                                                                                                                                                     |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ACK/NACK**      | positive/negative acknowledgement for requests that wait for the direction of resolution before deciding on the next action. Examples are writeback requests, exclusive requests.                                               |
| **GETS**          | request for shared permissions to satisfy a CPU's load or IFetch.                                                                                                                                                               |
| **GETX**          | request for exclusive access.                                                                                                                                                                                                   |
| **INV**           | invalidation request. This can be triggered by the coherence protocol itself, or by the next cache level/directory to enforce inclusion or to trigger a writeback for a DMA access so that the latest copy of data is obtained. |
| **PUTX**          | request for writeback of cache block. Some protocols (e.g. MOESI_CMP_directory) may use this only for writeback requests of exclusive data.                                                                                   |
| **PUTS**          | request for writeback of cache block in shared state.                                                                                                                                                                           |
| **PUTO**          | request for writeback of cache block in owned state.                                                                                                                                                                            |
| **PUTO_Sharers** | request for writeback of cache block in owned state but other sharers of the block exist.                                                                                                                                       |
| **UNBLOCK**       | message to unblock next cache level/directory for blocking protocols.                                                                                                                                                           |

### **AccessPermissions**

These are associated with each cache block and determine what operations
are permitted on that block. It is closely correlated with coherence
protocol
states.

| Permissions     | Description                                                                                                                                                                                                                                                                                                                  |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Invalid**     | The cache block is invalid. The block must first be obtained (from elsewhere in the memory hierarchy) before loads/stores can be performed. No action on invalidates (except maybe sending an ACK). No action on replacements. The associated coherence protocol states are I or NP and are stable states in every protocol. |
| **Busy**        | TODO                                                                                                                                                                                                                                                                                                                         |
| **Read_Only**  | Only operations permitted are loads, writebacks, invalidates. Stores cannot be performed before transitioning to some other state.                                                                                                                                                                                           |
| **Read_Write** | Loads, stores, writebacks, invalidations are allowed. Usually indicates that the block is dirty.                                                                                                                                                                                                                             |

### Data Structures

  - **Message Buffers**:TODO
  - **TBE Table**: TODO
  - **Timer Table**: This maintains a map of address-based timers. For
    each target address, a timeout value can be associated and added to
    the Timer table. This data structure is used, for example, by the L1
    cache controller implementation of the MOESI_CMP_directory
    protocol to trigger separate timeouts for cache blocks. Internally,
    the Timer Table uses the event queue to schedule the timeouts. The
    TimerTable supports a polling-based interface, **isReady()** to
    check if a timeout has occurred. Timeouts on addresses can be set
    using the **set()** method and removed using the **unset()** method.

  - **Related Files**:
      - src/mem/ruby/system/TimerTable.hh: Declares the
                TimerTable class
      - src/mem/ruby/system/TimerTable.cc: Implementation of the
                methods of the TimerTable class, that deals with setting
                addresses & timeouts, scheduling events using the event
                queue.

### Coherence controller FSM Diagrams

  - The Finite State Machines show only the stable states
  - Transitions are annotated using the notation "**Event list**" or
    "**Event list : Action list**" or "**Event list : Action list :
    Event list**". For example, Store : GETX indicates that on a Store
    event, a GETX message was sent whereas GETX : Mem Read indicates
    that on receiving a GETX message, a memory read request was sent.
    Only the main triggers and actions are listed.
  - Optional actions (e.g. writebacks depending on whether or not the
    block is dirty) are enclosed within **\[ \]**
  - In the diagrams, the transition labels are associated with the arc
    that cuts across the transition label or the closest arc.

