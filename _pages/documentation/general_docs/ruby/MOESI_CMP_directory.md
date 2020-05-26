---
layout: documentation
title: "MOESI CMP directory"
doc: gem5 documentation
parent: ruby
permalink: /documentation/general_docs/ruby/MOESI_CMP_directory/
author: Jason Lowe-Power
---

# MOESI CMP Directory

### Protocol Overview

  - TODO: cache hierarchy

<!-- end list -->

  - In contrast with the MESI protocol, the MOESI protocol introduces an
    additional **Owned** state.
  - The MOESI protocol also includes many coalescing optimizations not
    available in the MESI protocol.

### Related Files

  - **src/mem/protocols**
      - **MOESI_CMP_directory-L1cache.sm**: L1 cache controller
        specification
      - **MOESI_CMP_directory-L2cache.sm**: L2 cache controller
        specification
      - **MOESI_CMP_directory-dir.sm**: directory controller
        specification
      - **MOESI_CMP_directory-dma.sm**: dma controller specification
      - **MOESI_CMP_directory-msg.sm**: message type specification
      - **MOESI_CMP_directory.slicc**: container file

### L1 Cache Controller

#### **Stable States and Invariants**

| States    | Invariants                                                                                                                                                                                                                                                                                                                                                   |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **MM**    | The cache block is held exclusively by this node and is potentially modified (similar to conventional "M" state).                                                                                                                                                                                                                                            |
| **MM_W** | The cache block is held exclusively by this node and is potentially modified (similar to conventional "M" state). Replacements and DMA accesses are not allowed in this state. The block automatically transitions to MM state after a timeout.                                                                                                              |
| **O**     | The cache block is owned by this node. It has not been modified by this node. No other node holds this block in exclusive mode, but sharers potentially exist.                                                                                                                                                                                               |
| **M**     | The cache block is held in exclusive mode, but not written to (similar to conventional "E" state). No other node holds a copy of this block. Stores are not allowed in this state.                                                                                                                                                                           |
| **M_W**  | The cache block is held in exclusive mode, but not written to (similar to conventional "E" state). No other node holds a copy of this block. Only loads and stores are allowed. Silent upgrade happens to MM_W state on store. Replacements and DMA accesses are not allowed in this state. The block automatically transitions to M state after a timeout. |
| **S**     | The cache block is held in shared state by 1 or more nodes. Stores are not allowed in this state.                                                                                                                                                                                                                                                            |
| **I**     | The cache block is invalid.                                                                                                                                                                                                                                                                                                                                  |

#### **FSM Abstraction**

**The notation used in the controller FSM diagrams is described
[here](#Coherence_controller_FSM_Diagrams "wikilink").**

![MOESI_CMP_directory_L1cache_FSM.jpg](/assets/img/MOESI_CMP_directory_L1cache_FSM.jpg
"MOESI_CMP_directory_L1cache_FSM.jpg")

#### **Optimizations**

| States | Description                                                                                                                                                                                                                              |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SM** | A GETX has been issued to get exclusive permissions for an impending store to the cache block, but an old copy of the block is still present. Stores and Replacements are not allowed in this state.                                     |
| **OM** | A GETX has been issued to get exclusive permissions for an impending store to the cache block, the data has been received, but all expected acknowledgments have not yet arrived. Stores and Replacements are not allowed in this state. |

**The notation used in the controller FSM diagrams is described
[here](#Coherence_controller_FSM_Diagrams "wikilink").**

![MOESI_CMP_directory_L1cache_optim_FSM.jpg](/assets/img/MOESI_CMP_directory_L1cache_optim_FSM.jpg
"MOESI_CMP_directory_L1cache_optim_FSM.jpg")

### L2 Cache Controller

#### **Stable States and Invariants**

<table>
<thead>
<tr>
<th> Intra-chip Inclusion </th>
<th> Inter-chip Exclusion </th>
<th> States </th>
<th> Description
</th>
</tr>
</thead>
<tbody>
<tr>
<td> <b><span style="color:#808080">Not in any L1 or L2 at this chip</span></b> </td>
<td> <b>May be present at other chips</b> </td>
<td> <b>NP/I</b> </td>
<td> The cache block at this chip is invalid.
</td></tr>
<tr>
<td rowspan="6"> <b><span style="color:#00CC99">Not in L2, but in 1 or more L1s at this chip</span></b> </td>
<td rowspan="3"><b>May be present at other chips</b> </td>
<td> <b>ILS</b> </td>
<td> The cache block is not present at L2 on this chip. It is shared locally by L1 nodes in this chip.
</td></tr>
<tr>
<td> <b>ILO</b> </td>
<td> The cache block is not present at L2 on this chip. Some L1 node in this chip is an owner of this cache block.
</td></tr>
<tr>
<td> <b>ILOS</b> </td>
<td> The cache block is not present at L2 on this chip. Some L1 node in this chip is an owner of this cache block. There are also L1 sharers of this cache block in this chip.
</td></tr>
<tr>
<td rowspan="3"><b>Not present at any other chip</b> </td>
<td> <b>ILX</b> </td>
<td> The cache block is not present at L2 on this chip. It is held in exclusive mode by some L1 node in this chip.
</td></tr>
<tr>
<td> <b>ILOX</b> </td>
<td> The cache block is not present at L2 on this chip. It is held exclusively by this chip and some L1 node in this chip is an owner of the block.
</td></tr>
<tr>
<td> <b>ILOSX</b> </td>
<td> The cache block is not present at L2 on this chip. It is held exclusively by this chip. Some L1 node in this chip is an owner of the block. There are also L1 sharers of this cache block in this chip.
</td></tr>
<tr>
<td rowspan="3"> <b><span style="color:#99CCFF">In L2, but not in any L1 at this chip</span></b> </td>
<td rowspan="2"><b>May be present at other chips</b> </td>
<td> <b>S</b> </td>
<td> The cache block is not present at L1 on this chip. It is held in shared mode at L2 on this chip and is also potentially shared across chips.
</td></tr>
<tr>
<td> <b>O</b> </td>
<td> The cache block is not present at L1 on this chip. It is held in owned mode at L2 on this chip. It is also potentially shared across chips.
</td></tr>
<tr>
<td> <b>Not present at any other chip</b> </td>
<td> <b>M</b> </td>
<td> The cache block is not present at L1 on this chip. It is present at L2 on this chip and is potentially modified.
</td></tr>
<tr>
<td rowspan="3"> <b><span style="color:#CC99FF">Both in L2, and 1 or more L1s at this chip</span></b> </td>
<td rowspan="2"><b>May be present at other chips</b> </td>
<td> <b>SLS</b> </td>
<td> The cache block is present at L2 in shared mode on this chip. There exists local L1 sharers of the block on this chip. It is also potentially shared across chips.
</td></tr>
<tr>
<td> <b>OLS</b> </td>
<td> The cache block is present at L2 in owned mode on this chip. There exists local L1 sharers of the block on this chip. It is also potentially shared across chips.
</td></tr>
<tr>
<td> <b>Not present at any other chip</b> </td>
<td> <b>OLSX</b> </td>
<td> The cache block is present at L2 in owned mode on this chip. There exists local L1 sharers of the block on this chip. It is held exclusively by this chip.
</td></tr>
</tbody>
</table>

#### **FSM Abstraction**

The controller is described in 2 parts. The first picture shows
transitions between all "intra-chip inclusion" categories and within
categories 1, 3, 4. Transitions within category 2 (Not in L2, but in 1
or more L1s at this chip) are shown in the second picture.

**The notation used in the controller FSM diagrams is described
[here](#Coherence_controller_FSM_Diagrams "wikilink"). Transitions
involving other chips are annotated in
<span style="color:#CC3300">brown</span>.**

![MOESI_CMP_directory_L2cache_FSM_part_1.jpg](/assets/img/MOESI_CMP_directory_L2cache_FSM_part_1.jpg
"MOESI_CMP_directory_L2cache_FSM_part_1.jpg")

The second picture below expands the central hexagonal portion of the
above picture to show transitions within category 2 (Not in L2, but in 1
or more L1s at this chip).

**The notation used in the controller FSM diagrams is described
[here](#Coherence_controller_FSM_Diagrams "wikilink"). Transitions
involving other chips are annotated in
<span style="color:#CC3300">brown</span>.**

![MOESI_CMP_directory_L2cache_FSM_part_2.jpg](/assets/img/MOESI_CMP_directory_L2cache_FSM_part_2.jpg
"MOESI_CMP_directory_L2cache_FSM_part_2.jpg")

### Directory Controller

#### **Stable States and
Invariants**

| States | Invariants                                                                                                                                                                      |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **M**  | The cache block is held in exclusive state by only 1 node (which is also the owner). There are no sharers of this block. The data is potentially different from that in memory. |
| **O**  | The cache block is owned by exactly 1 node. There may be sharers of this block. The data is potentially different from that in memory.                                          |
| **S**  | The cache block is held in shared state by 1 or more nodes. No node has ownership of the block. The data is consistent with that in memory (Check).                             |
| **I**  | The cache block is invalid.                                                                                                                                                     |

#### **FSM Abstraction**

**The notation used in the controller FSM diagrams is described
[here](#Coherence_controller_FSM_Diagrams "wikilink").**

![MOESI_CMP_directory_dir_FSM.jpg](/assets/img/MOESI_CMP_directory_dir_FSM.jpg
"MOESI_CMP_directory_dir_FSM.jpg")

### Other features

#### **Timeouts**:

