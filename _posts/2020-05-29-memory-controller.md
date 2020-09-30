---
layout: post
title:  "Memory controller updates for new DRAM technologies, NVM interfaces and flexible memory topologies"
author: Wendy Elsasser and Nikos Nikoleris
date:   2020-05-27
---

## Adding LPDDR5 support to DRAMCtrl

LPDDR5 is currently in mass production for use in multiple markets including mobile, automotive, AI, and 5G. This technology is expected to become the mainstream Flagship Low-Power DRAM by 2021 with anticipated longevity due to proposed speed grade extensions. The specification defines a flexible architecture and multiple options to optimize across different use cases, trading off power, performance, reliability and complexity.  To evaluate these tradeoffs, the gem5 model has been updated with LPDDR5 configurations and architecture support.

LPDDR5 is mostly an evolutionary uptick from LPDDR4 with 3 key motivations: flexibility, performance, and power. The specification offers a multitude of options to enable varied use-cases with a user programmable bank architecture and new lower power features to balance power and performance tradeoffs. Similar to previous generations, LPDDR5 increases the data rates and the current version of the specification supports data-rates up to 6.4Gbps (giga-bits per second) for a maximum I/O bandwidth of 12.8GB/s (giga-bytes per second) with a 16-bit channel. A new clocking architecture is defined leveraging concepts from other technologies like GDDR, but with a low-power twist. With the new clocking architecture, commands are transferred at a lower frequency with some commands requiring multiple clock cycles. The new clocking architecture also includes the additional requirement of data clock synchronization, potentially done dynamically as bursts issue. Due to these changes, additional considerations are required to ensure adequate command bandwidth in some high-speed scenarios. These new LPDDR5 features require new checks and optimizations in gem5 to ensure the model integrity when comparing to real hardware.

Support for multi-cycle commands and lower frequency command transfer motivated a new check in gem5 to verify command bandwidth. The DRAM controller historically did not verify contention on the command bus and assumed unlimited command bandwidth. With the evolution of new technologies this assumption is not always valid. One potential solution is to align all commands to a clock boundary and ensure that two commands are not issued simultaneously. Given that the gem5 model is not a cycle accurate model, this solution was deemed overly complicated. Alternatively, a rolling window has been defined and the model calculates the maximum number of commands that can issue within that window. Prior to issuing a command, the model will verify that the window in which the command will issue still has slots available. If the slots are full, the command will be shifted to the next window. This will be done until a window with a free command slot is found. The window is currently defined by the time required to transfer a burst, which is typically defined by the tBURST parameter.

At higher data rates, the ability to transfer a burst seamlessly depends on the bank architecture in LPDDR5. When configured using a bank group architecture, which defines a total of 16 banks split across 4 bank groups, a burst of 32 cannot be transferred seamlessly. The data instead will be transferred with gaps in the middle of the burst. Essentially half the burst will be transferred in 2 cycles, followed by a 2-cycle gap, with the second half of the burst transferred after the gap. To mitigate the effect on data bus utilization and IO bandwidth, LPDDR5 supports interleaved bursts. The gem5 model has also been updated to support burst interleaving and with these changes, the model is able to achieve high data bus utilization as expected (and in many cases required).

All of these changes will be discussed in the gem5 workshop. In the workshop, we will review LPDDR5 requirements and detail the changes made in gem5. While these changes have been incorporated specifically for LPDDR5, some of them are also applicable to other memory technologies. I look forward to the discussion in the workshop!

### Workshop Presentation

<iframe width="960" height="540"
src="https://www.youtube.com/embed/ttJ9_I_Avyc" frameborder="0"
allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
allowfullscreen style="max-width: 960px"></iframe>

## Refactoring the DRAMCtrl and creating an initial NVM interface

The gem5 DRAM controller provides the interface to external, user addressable memory, which is traditionally DRAM. The controller consists of 2 main components: the memory controller and the DRAM interface. The memory controller includes the port connecting to the on-chip fabric. It receives command packets from the fabric, enqueues them into the read and write queues and manages the command scheduling algorithm for read and write requests. The DRAM interface contains media specific information that defines the architecture and timing parameters of the DRAM, and manages the media specific operations like activation, precharge, refresh and low power modes.

With the advent of SCM (storage class memory), emerging NVM could also exist on a memory interface, potentially alongside DRAM. NVM support could simply be layered on top of the existing DRAM controller with the changes integrated into the current DRAM interface. However, with a more systematic approach, the model could be modified to provide a mechanism that enables easier integration of new interfaces to support future memory technologies. To do this, the memory controller has been refactored. Instead of a single DRAM controller (DRAMCtrl) object, two objects have been defined: DRAMCtrl and DRAMInterface. Memory configurations are now defined as a DRAM interface and the DRAM specific parameters and functions have been moved from the controller to the interface. This includes the DRAM architecture, timing and IDD parameters. To connect the two objects, a new parameter has been defined in the DRAM controller Python object. This parameter, ‘dram’, is a pointer to the DRAM interface.

```
    # Interface to volatile, DRAM media
    dram = Param.DRAMInterface(NULL, "DRAM interface")
```

Functions specific to DRAM opcodes have also been pulled out of the controller and moved to the interface. For example, the Rank class and associated functions are now defined within the interface. The DRAM interface is defined as an AbstractMemory, enabling an address range to be defined for the actual media interface instead of the controller. With this change, the controller has been modified to be a ClockedObject.

Now, the DRAM controller is a generic memory controller and non-DRAM interfaces can be defined and easily connected. In that regard, an initial NVM interface, NVMInterface, has been defined, which mimics the behavior of NVDIMM-P. Similar to the DRAM interface, the NVM interface is defined as an AbstractMemory, with an address range defined for the interface. A new parameter, ‘nvm’, has been defined in Python to connects the controller to the NVM interface when configured.

```
    # Interface to non-volatile media
    nvm = Param.NVMInterface(NULL, "NVM interface")
```

The NVM interface is media agnostic and simply defines read and write operations. The intent of the interface is to support a wide variety of media types, many less performant than DRAM. While DRAM is accessed with deterministic timing, internal operations within the NVM could create longer tail latency distributions requiring non-deterministic delays. To manage non-determinism, the reads have been split into 2 stages: Read Request and Data Burst. The first stage, the Read Request simply issues a read command and schedules a ReadReady event. The event will be triggered when the read completes and data is available. At that time, the NVM interface will trigger a controller event to issue a data burst.

While the write latency and write bandwidth of emerging NVM is typically magnitudes faster than FLASH, for many technologies it is not yet on par with DRAM. To mitigate the longer write delay and lower bandwidth, the NVM interface in gem5 models a near NVM write buffer. This buffer offloads write commands and data from the memory controller and provides push-back when full, inhibiting further write command from issuing until an entry is popped. The entries are popped when the write completes, using parameters defined in the NVM Interface.

After refactoring the controller and creating unique DRAM and NVM interfaces, a variety of potential memory sub-system topologies are possible in gem5. A system can incorporate NVM and DRAM on a single channel or have dedicated channels defined per media. Configurations can be defined to provide a multitude of scenarios for NVM+DRAM simulations to analyze the tradeoffs of new memory technologies and methods to optimize future memory subsystems.

### Workshop Presentation

<iframe width="960" height="540"
src="https://www.youtube.com/embed/t2PRoZPwwpk" frameborder="0"
allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
allowfullscreen style="max-width: 960px"></iframe>
