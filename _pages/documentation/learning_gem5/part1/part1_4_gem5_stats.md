---
layout: documentation
title: Understanding gem5 statistics and output
doc: Learning gem5
parent: part1
permalink: /documentation/learning_gem5/part1/gem5_stats/
author: Jason Lowe-Power
---


Understanding gem5 statistics and output
========================================

In addition to any information which your simulation script prints out,
after running gem5, there are three files generated in a directory
called `m5out`:

**config.ini**
:   Contains a list of every SimObject created for the simulation and
    the values for its parameters.

**config.json**
:   The same as config.ini, but in json format.

**stats.txt**
:   A text representation of all of the gem5 statistics registered for
    the simulation.

config.ini
----------

This file is the definitive version of what was simulated. All of the
parameters for each SimObject that is simulated, whether they were set
in the configuration scripts or the defaults were used, are shown in
this file.

Below is pulled from the config.ini generated when the `simple.py`
configuration file from
[simple-config-chapter](http://www.gem5.org/documentation/learning_gem5/part1/simple_config/)
is run.

    [root]
    type=Root
    children=system
    eventq_index=0
    full_system=false
    sim_quantum=0
    time_sync_enable=false
    time_sync_period=100000000000
    time_sync_spin_threshold=100000000

    [system]
    type=System
    children=clk_domain cpu dvfs_handler mem_ctrl membus
    boot_osflags=a
    cache_line_size=64
    clk_domain=system.clk_domain
    default_p_state=UNDEFINED
    eventq_index=0
    exit_on_work_items=false
    init_param=0
    kernel=
    kernel_addr_check=true
    kernel_extras=
    kvm_vm=Null
    load_addr_mask=18446744073709551615
    load_offset=0
    mem_mode=timing

    ...

    [system.membus]
    type=CoherentXBar
    children=snoop_filter
    clk_domain=system.clk_domain
    default_p_state=UNDEFINED
    eventq_index=0
    forward_latency=4
    frontend_latency=3
    p_state_clk_gate_bins=20
    p_state_clk_gate_max=1000000000000
    p_state_clk_gate_min=1000
    point_of_coherency=true
    point_of_unification=true
    power_model=
    response_latency=2
    snoop_filter=system.membus.snoop_filter
    snoop_response_latency=4
    system=system
    use_default_range=false
    width=16
    master=system.cpu.interrupts.pio system.cpu.interrupts.int_slave system.mem_ctrl.port
    slave=system.cpu.icache_port system.cpu.dcache_port system.cpu.interrupts.int_master system.system_port

    [system.membus.snoop_filter]
    type=SnoopFilter
    eventq_index=0
    lookup_latency=1
    max_capacity=8388608
    system=system

Here we see that at the beginning of the description of each SimObject
is first its name as created in the configuration file surrounded by
square brackets (e.g., `[system.membus]`).

Next, every parameter of the SimObject is shown with its value,
including parameters not explicitly set in the configuration file. For
instance, the configuration file sets the clock domain to be 1 GHz (1000
ticks in this case). However, it did not set the cache line size (which
is 64 in the `system`) object.

The `config.ini` file is a valuable tool for ensuring that you are
simulating what you think you're simulating. There are many possible
ways to set default values, and to override default values, in gem5. It
is a "best-practice" to always check the `config.ini` as a sanity check
that values set in the configuration file are propagated to the actual
SimObject instantiation.

stats.txt
---------

gem5 has a flexible statistics generating system. gem5 statistics is
covered in some detail on the [gem5 wiki
site](http://www.gem5.org/Statistics). Each instantiation of a SimObject
has it's own statistics. At the end of simulation, or when special
statistic-dumping commands are issued, the current state of the
statistics for all SimObjects is dumped to a file.

First, the statistics file contains general statistics about the
execution:

    ---------- Begin Simulation Statistics ----------
    simSeconds                                   0.000057                       # Number of seconds simulated (Second)
    simTicks                                     57467000                       # Number of ticks simulated (Tick)
    finalTick                                    57467000                       # Number of ticks from beginning of simulation (restored from checkpoints and never reset) (Tick)
    simFreq                                  1000000000000                       # The number of ticks per simulated second ((Tick/Second))
    hostSeconds                                      0.03                       # Real time elapsed on the host (Second)
    hostTickRate                               2295882330                       # The number of ticks simulated per host second (ticks/s) ((Tick/Second))
    hostMemory                                     665792                       # Number of bytes of host memory used (Byte)
    simInsts                                         6225                       # Number of instructions simulated (Count)
    simOps                                          11204                       # Number of ops (including micro ops) simulated (Count)
    hostInstRate                                   247382                       # Simulator instruction rate (inst/s) ((Count/Second))
    hostOpRate                                     445086                       # Simulator op (including micro ops) rate (op/s) ((Count/Second))

    ---------- Begin Simulation Statistics ----------
    simSeconds                                   0.000490                       # Number of seconds simulated (Second)
    simTicks                                    490394000                       # Number of ticks simulated (Tick)
    finalTick                                   490394000                       # Number of ticks from beginning of simulation (restored from checkpoints and never reset) (Tick)
    simFreq                                  1000000000000                       # The number of ticks per simulated second ((Tick/Second))
    hostSeconds                                      0.03                       # Real time elapsed on the host (Second)
    hostTickRate                              15979964060                       # The number of ticks simulated per host second (ticks/s) ((Tick/Second))
    hostMemory                                     657488                       # Number of bytes of host memory used (Byte)
    simInsts                                         6225                       # Number of instructions simulated (Count)
    simOps                                          11204                       # Number of ops (including micro ops) simulated (Count)
    hostInstRate                                   202054                       # Simulator instruction rate (inst/s) ((Count/Second))
    hostOpRate                                     363571                       # Simulator op (including micro ops) rate (op/s) ((Count/Second))

The statistic dump begins with
`---------- Begin Simulation Statistics ----------`. There may be
multiple of these in a single file if there are multiple statistic dumps
during the gem5 execution. This is common for long running applications,
or when restoring from checkpoints.

Each statistic has a name (first column), a value (second column), and a
description (last column preceded by \#) followed by the unit of the
statistic.

Most of the statistics are self explanatory from their descriptions. A
couple of important statistics are `sim_seconds` which is the total
simulated time for the simulation, `sim_insts` which is the number of
instructions committed by the CPU, and `host_inst_rate` which tells you
the performance of gem5.

Next, the SimObjects' statistics are printed. For instance, the CPU
statistics, which contains information on the number of syscalls,
statistics for cache system and translation buffers, etc.

    system.clk_domain.clock                          1000                       # Clock period in ticks (Tick)
    system.clk_domain.voltage_domain.voltage            1                       # Voltage in Volts (Volt)
    system.cpu.numCycles                            57467                       # Number of cpu cycles simulated (Cycle)
    system.cpu.numWorkItemsStarted                      0                       # Number of work items this cpu started (Count)
    system.cpu.numWorkItemsCompleted                    0                       # Number of work items this cpu completed (Count)
    system.cpu.dcache.demandHits::cpu.data           1941                       # number of demand (read+write) hits (Count)
    system.cpu.dcache.demandHits::total              1941                       # number of demand (read+write) hits (Count)
    system.cpu.dcache.overallHits::cpu.data          1941                       # number of overall hits (Count)
    system.cpu.dcache.overallHits::total             1941                       # number of overall hits (Count)
    system.cpu.dcache.demandMisses::cpu.data          133                       # number of demand (read+write) misses (Count)
    system.cpu.dcache.demandMisses::total             133                       # number of demand (read+write) misses (Count)
    system.cpu.dcache.overallMisses::cpu.data          133                       # number of overall misses (Count)
    system.cpu.dcache.overallMisses::total            133                       # number of overall misses (Count)
    system.cpu.dcache.demandMissLatency::cpu.data     14301000                       # number of demand (read+write) miss ticks (Tick)
    system.cpu.dcache.demandMissLatency::total     14301000                       # number of demand (read+write) miss ticks (Tick)
    system.cpu.dcache.overallMissLatency::cpu.data     14301000                       # number of overall miss ticks (Tick)
    system.cpu.dcache.overallMissLatency::total     14301000                       # number of overall miss ticks (Tick)
    system.cpu.dcache.demandAccesses::cpu.data         2074                       # number of demand (read+write) accesses (Count)
    system.cpu.dcache.demandAccesses::total          2074                       # number of demand (read+write) accesses (Count)
    system.cpu.dcache.overallAccesses::cpu.data         2074                       # number of overall (read+write) accesses (Count)
    system.cpu.dcache.overallAccesses::total         2074                       # number of overall (read+write) accesses (Count)
    system.cpu.dcache.demandMissRate::cpu.data     0.064127                       # miss rate for demand accesses (Ratio)
    system.cpu.dcache.demandMissRate::total      0.064127                       # miss rate for demand accesses (Ratio)
    system.cpu.dcache.overallMissRate::cpu.data     0.064127                       # miss rate for overall accesses (Ratio)
    system.cpu.dcache.overallMissRate::total     0.064127                       # miss rate for overall accesses (Ratio)
    system.cpu.dcache.demandAvgMissLatency::cpu.data 107526.315789                       # average overall miss latency ((Cycle/Count))
    system.cpu.dcache.demandAvgMissLatency::total 107526.315789                       # average overall miss latency ((Cycle/Count))
    system.cpu.dcache.overallAvgMissLatency::cpu.data 107526.315789                       # average overall miss latency ((Cycle/Count))
    system.cpu.dcache.overallAvgMissLatency::total 107526.315789                       # average overall miss latency ((Cycle/Count))
    ...
    system.cpu.mmu.dtb.rdAccesses                    1123                       # TLB accesses on read requests (Count)
    system.cpu.mmu.dtb.wrAccesses                     953                       # TLB accesses on write requests (Count)
    system.cpu.mmu.dtb.rdMisses                        11                       # TLB misses on read requests (Count)
    system.cpu.mmu.dtb.wrMisses                         9                       # TLB misses on write requests (Count)
    system.cpu.mmu.dtb.walker.power_state.pwrStateResidencyTicks::UNDEFINED     57467000                       # Cumulative time (in ticks) in various power states (Tick)
    system.cpu.mmu.itb.rdAccesses                       0                       # TLB accesses on read requests (Count)
    system.cpu.mmu.itb.wrAccesses                    7940                       # TLB accesses on write requests (Count)
    system.cpu.mmu.itb.rdMisses                         0                       # TLB misses on read requests (Count)
    system.cpu.mmu.itb.wrMisses                        37                       # TLB misses on write requests (Count)
    system.cpu.mmu.itb.walker.power_state.pwrStateResidencyTicks::UNDEFINED     57467000                       # Cumulative time (in ticks) in various power states (Tick)
    system.cpu.power_state.pwrStateResidencyTicks::ON     57467000                       # Cumulative time (in ticks) in various power states (Tick)
    system.cpu.thread_0.numInsts                        0                       # Number of Instructions committed (Count)
    system.cpu.thread_0.numOps                          0                       # Number of Ops committed (Count)
    system.cpu.thread_0.numMemRefs                      0                       # Number of Memory References (Count)
    system.cpu.workload.numSyscalls                    11                       # Number of system calls (Count)

Later in the file is memory controller statistics. This has information like
the bytes read by each component and the average bandwidth used by those
components.

    system.mem_ctrl.bytesReadWrQ                        0                       # Total number of bytes read from write queue (Byte)
    system.mem_ctrl.bytesReadSys                    23168                       # Total read bytes from the system interface side (Byte)
    system.mem_ctrl.bytesWrittenSys                     0                       # Total written bytes from the system interface side (Byte)
    system.mem_ctrl.avgRdBWSys               403153113.96105593                       # Average system read bandwidth in Byte/s ((Byte/Second))
    system.mem_ctrl.avgWrBWSys                 0.00000000                       # Average system write bandwidth in Byte/s ((Byte/Second))
    system.mem_ctrl.totGap                       57336000                       # Total gap between requests (Tick)
    system.mem_ctrl.avgGap                      158386.74                       # Average gap between requests ((Tick/Count))
    system.mem_ctrl.requestorReadBytes::cpu.inst        14656                       # Per-requestor bytes read from memory (Byte)
    system.mem_ctrl.requestorReadBytes::cpu.data         8512                       # Per-requestor bytes read from memory (Byte)
    system.mem_ctrl.requestorReadRate::cpu.inst 255033323.472601681948                       # Per-requestor bytes read from memory rate ((Byte/Second))
    system.mem_ctrl.requestorReadRate::cpu.data 148119790.488454252481                       # Per-requestor bytes read from memory rate ((Byte/Second))
    system.mem_ctrl.requestorReadAccesses::cpu.inst          229                       # Per-requestor read serviced memory accesses (Count)
    system.mem_ctrl.requestorReadAccesses::cpu.data          133                       # Per-requestor read serviced memory accesses (Count)
    system.mem_ctrl.requestorReadTotalLat::cpu.inst      6234000                       # Per-requestor read total memory access latency (Tick)
    system.mem_ctrl.requestorReadTotalLat::cpu.data      4141000                       # Per-requestor read total memory access latency (Tick)
    system.mem_ctrl.requestorReadAvgLat::cpu.inst     27222.71                       # Per-requestor read average memory access latency ((Tick/Count))
    system.mem_ctrl.requestorReadAvgLat::cpu.data     31135.34                       # Per-requestor read average memory access latency ((Tick/Count))
    system.mem_ctrl.dram.bytesRead::cpu.inst        14656                       # Number of bytes read from this memory (Byte)
    system.mem_ctrl.dram.bytesRead::cpu.data         8512                       # Number of bytes read from this memory (Byte)
    system.mem_ctrl.dram.bytesRead::total           23168                       # Number of bytes read from this memory (Byte)
    system.mem_ctrl.dram.bytesInstRead::cpu.inst        14656                       # Number of instructions bytes read from this memory (Byte)
    system.mem_ctrl.dram.bytesInstRead::total        14656                       # Number of instructions bytes read from this memory (Byte)
    system.mem_ctrl.dram.numReads::cpu.inst           229                       # Number of read requests responded to by this memory (Count)
    system.mem_ctrl.dram.numReads::cpu.data           133                       # Number of read requests responded to by this memory (Count)
    system.mem_ctrl.dram.numReads::total              362                       # Number of read requests responded to by this memory (Count)
    system.mem_ctrl.dram.bwRead::cpu.inst       255033323                       # Total read bandwidth from this memory ((Byte/Second))
    system.mem_ctrl.dram.bwRead::cpu.data       148119790                       # Total read bandwidth from this memory ((Byte/Second))
    system.mem_ctrl.dram.bwRead::total          403153114                       # Total read bandwidth from this memory ((Byte/Second))
    system.mem_ctrl.dram.bwInstRead::cpu.inst    255033323                       # Instruction read bandwidth from this memory ((Byte/Second))
    system.mem_ctrl.dram.bwInstRead::total      255033323                       # Instruction read bandwidth from this memory ((Byte/Second))
    system.mem_ctrl.dram.bwTotal::cpu.inst      255033323                       # Total bandwidth to/from this memory ((Byte/Second))
    system.mem_ctrl.dram.bwTotal::cpu.data      148119790                       # Total bandwidth to/from this memory ((Byte/Second))
    system.mem_ctrl.dram.bwTotal::total         403153114                       # Total bandwidth to/from this memory ((Byte/Second))
    system.mem_ctrl.dram.readBursts                   362                       # Number of DRAM read bursts (Count)
    system.mem_ctrl.dram.writeBursts                    0                       # Number of DRAM write bursts (Count)
