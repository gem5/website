---
layout: documentation
title: "MOESI CMP token"
doc: gem5 documentation
parent: ruby
permalink: /documentation/general_docs/ruby/MOESI_CMP_token/
author: Jason Lowe-Power
---

# MOESI CMP token

### Protocol Overview

  - This protocol also models a 2-level cache hierarchy.
  - It maintains coherence permission by explicitly exchanging and
    counting tokens.
  - A fix number of token are assigned to each cache block in the
    beginning, the number of token remains unchanged.
  - To write a block, the processor must have all the token for that
    block. For reading at least one token is required.
  - The protocol also has a persistent message support to avoid
    starvation.

### Related Files

  - **src/mem/protocols**
      - **MOESI_CMP_token-L1cache.sm**: L1 cache controller
        specification
      - **MOESI_CMP_token-L2cache.sm**: L2 cache controller
        specification
      - **MOESI_CMP_token-dir.sm**: directory controller specification
      - **MOESI_CMP_token-dma.sm**: dma controller specification
      - **MOESI_CMP_token-msg.sm**: message type specification
      - **MOESI_CMP_token.slicc**: container file

### Controller Description

### **L1 Cache**

| States    | Invariants                                                                                                                                                                                                                                                                                                                                                   |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **MM**    | The cache block is held exclusively by this node and is potentially modified (similar to conventional "M" state).                                                                                                                                                                                                                                            |
| **MM_W** | The cache block is held exclusively by this node and is potentially modified (similar to conventional "M" state). Replacements and DMA accesses are not allowed in this state. The block automatically transitions to MM state after a timeout.                                                                                                              |
| **O**     | The cache block is owned by this node. It has not been modified by this node. No other node holds this block in exclusive mode, but sharers potentially exist.                                                                                                                                                                                               |
| **M**     | The cache block is held in exclusive mode, but not written to (similar to conventional "E" state). No other node holds a copy of this block. Stores are not allowed in this state.                                                                                                                                                                           |
| **M_W**  | The cache block is held in exclusive mode, but not written to (similar to conventional "E" state). No other node holds a copy of this block. Only loads and stores are allowed. Silent upgrade happens to MM_W state on store. Replacements and DMA accesses are not allowed in this state. The block automatically transitions to M state after a timeout. |
| **S**     | The cache block is held in shared state by 1 or more nodes. Stores are not allowed in this state.                                                                                                                                                                                                                                                            |
| **I**     | The cache block is invalid.                                                                                                                                                                                                                                                                                                                                  |

### **L2 cache**

| States | Invariants                                                                                                                                                                                                          |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **NP** | The cache block is held exclusively by this node and is potentially locally modified (similar to conventional "M" state).                                                                                           |
| **O**  | The cache block is owned by this node. It has not been modified by this node. No other node holds this block in exclusive mode, but sharers potentially exist.                                                      |
| **M**  | The cache block is held in exclusive mode, but not written to (similar to conventional "E" state). No other node holds a copy of this block. Stores are not allowed in this state.                                  |
| **S**  | The cache line holds the most recent, correct copy of the data. Other processors in the system may hold copies of the data in the shared state, as well. The cache line can be read, but not written in this state. |
| **I**  | The cache line is invalid and does not hold a valid copy of the data.                                                                                                                                               |

### **Directory controller**

| States | Invariants |
| ------ | ---------- |
| **O**  | Owner .    |
| **NO** | Not Owner. |
| **L**  | Locked.    |
