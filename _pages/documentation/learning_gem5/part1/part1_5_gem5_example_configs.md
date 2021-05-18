---
layout: documentation
title: Using the default configuration scripts
doc: Learning gem5
parent: part1
permalink: /documentation/learning_gem5/part1/example_configs/
author: Jason Lowe-Power
---


Using the default configuration scripts
=======================================

In this chapter, we'll explore using the default configuration scripts
that come with gem5. gem5 ships with many configuration scripts that
allow you to use gem5 very quickly. However, a common pitfall is to use
these scripts without fully understanding what is being simulated. It is
important when doing computer architecture research with gem5 to fully
understand the system you are simulating. This chapter will walk you
through some important options and parts of the default configuration
scripts.

In the last few chapters you have created your own configuration scripts
from scratch. This is very powerful, as it allows you to specify every
single system parameter. However, some systems are very complex to set
up (e.g., a full-system ARM or x86 machine). Luckily, the gem5
developers have provided many scripts to bootstrap the process of
building systems.

A tour of the directory structure
---------------------------------

All of gem5's configuration files can be found in `configs/`. The
directory structure is shown below:

    configs/boot:
    bbench-gb.rcS  bbench-ics.rcS  hack_back_ckpt.rcS  halt.sh

    configs/common:
    Benchmarks.py   Caches.py  cpu2000.py    FileSystemConfig.py  GPUTLBConfig.py   HMC.py       MemConfig.py   Options.py     Simulation.py
    CacheConfig.py  cores      CpuConfig.py  FSConfig.py          GPUTLBOptions.py  __init__.py  ObjectList.py  SimpleOpts.py  SysPaths.py

    configs/dist:
    sw.py

    configs/dram:
    lat_mem_rd.py  low_power_sweep.py  sweep.py

    configs/example:
    apu_se.py  etrace_replay.py  garnet_synth_traffic.py  hmctest.py    hsaTopology.py  memtest.py  read_config.py  ruby_direct_test.py      ruby_mem_test.py     sc_main.py
    arm        fs.py             hmc_hello.py             hmc_tgen.cfg  memcheck.py     noc_config  riscv           ruby_gpu_random_test.py  ruby_random_test.py  se.py

    configs/learning_gem5:
    part1  part2  part3  README

    configs/network:
    __init__.py  Network.py

    configs/nvm:
    sweep_hybrid.py  sweep.py

    configs/ruby:
    AMD_Base_Constructor.py  CHI.py        Garnet_standalone.py  __init__.py              MESI_Three_Level.py  MI_example.py      MOESI_CMP_directory.py  MOESI_hammer.py
    CHI_config.py            CntrlBase.py  GPU_VIPER.py          MESI_Three_Level_HTM.py  MESI_Two_Level.py    MOESI_AMD_Base.py  MOESI_CMP_token.py      Ruby.py

    configs/splash2:
    cluster.py  run.py

    configs/topologies:
    BaseTopology.py  Cluster.py  CrossbarGarnet.py  Crossbar.py  CustomMesh.py  __init__.py  MeshDirCorners_XY.py  Mesh_westfirst.py  Mesh_XY.py  Pt2Pt.py

Each directory is briefly described below:

**boot/**
:   These are rcS files which are used in full-system mode. These files
    are loaded by the simulator after Linux boots and are executed by
    the shell. Most of these are used to control benchmarks when running
    in full-system mode. Some are utility functions, like
    `hack_back_ckpt.rcS`. These files are covered in more depth in the
    chapter on full-system simulation.

**common/**
:   This directory contains a number of helper scripts and functions to
    create simulated systems. For instance, `Caches.py` is similar to
    the `caches.py` and `caches_opts.py` files created in previous
    chapters.

    `Options.py` contains a variety of options that can be set on the
    command line. Like the number of CPUs, system clock, and many, many
    more. This is a good place to look to see if the option you want to
    change already has a command line parameter.

    `CacheConfig.py` contains the options and functions for setting
    cache parameters for the classic memory system.

    `MemConfig.py` provides some helper functions for setting the memory
    system.

    `FSConfig.py` contains the necessary functions to set up full-system
    simulation for many different kinds of systems. Full-system
    simulation is discussed further in it's own chapter.

    `Simulation.py` contains many helper functions to set up and run
    gem5. A lot of the code contained in this file manages saving and
    restoring checkpoints. The example configuration files below in
    `examples/` use the functions in this file to execute the gem5
    simulation. This file is quite complicated, but it also allows a lot
    of flexibility in how the simulation is run.

**dram/**
:   Contains scripts to test DRAM.

**example/**
:   This directory contains some example gem5 configuration scripts that
    can be used out-of-the-box to run gem5. Specifically, `se.py` and
    `fs.py` are quite useful. More on these files can be found in the
    next section. There are also some other utility configuration
    scripts in this directory.

**learning_gem5/**
:   This directory contains all gem5 configuration scripts found in the
    learning\_gem5 book.

**network/**
:   This directory contains the configurations scripts for a HeteroGarnet
    network.

**nvm/**
:   This directory contains example scripts using the NVM interface.

**ruby/**
:   This directory contains the configurations scripts for Ruby and its
    included cache coherence protocols. More details can be found in the
    chapter on Ruby.

**splash2/**
:   This directory contains scripts to run the splash2 benchmark suite
    with a few options to configure the simulated system.

**topologies/**
:   This directory contains the implementation of the topologies that
    can be used when creating the Ruby cache hierarchy. More details can
    be found in the chapter on Ruby.

Using `se.py` and `fs.py`
-------------------------

In this section, I'll discuss some of the common options that can be
passed on the command line to `se.py` and `fs.py`. More details on how
to run full-system simulation can be found in the full-system simulation
chapter. Here I'll discuss the options that are common to the two files.

Most of the options discussed in this section are found in Options.py
and are registered in the function `addCommonOptions`. This section does
not detail all of the options. To see all of the options, run the
configuration script with `--help`, or read the script's source code.

First, let's simply run the hello world program without any parameters:

```
build/X86/gem5.opt configs/example/se.py --cmd=tests/test-progs/hello/bin/x86/linux/hello
```

And we get the following as output:

    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 version 21.0.0.0
    gem5 compiled May 17 2021 18:05:59
    gem5 started May 18 2021 00:33:42
    gem5 executing on amarillo, pid 85168
    command line: build/X86/gem5.opt configs/example/se.py --cmd=tests/test-progs/hello/bin/x86/linux/hello

    Global frequency set at 1000000000000 ticks per second
    warn: No dot file generated. Please install pydot to generate the dot file and pdf.
    warn: DRAM device capacity (8192 Mbytes) does not match the address range assigned (512 Mbytes)
    0: system.remote_gdb: listening for remote gdb on port 7005
    **** REAL SIMULATION ****
    info: Entering event queue @ 0.  Starting simulation...
    Hello world!
    Exiting @ tick 5943000 because exiting with last active thread context

However, this isn't a very interesting simulation at all! By default,
gem5 uses the atomic CPU and uses atomic memory accesses, so there's no
real timing data reported! To confirm this, you can look at
m5out/config.ini. The CPU is shown on line 51:

    [system.cpu]
    type=AtomicSimpleCPU
    children=interrupts isa mmu power_state tracer workload
    branchPred=Null
    checker=Null
    clk_domain=system.cpu_clk_domain
    cpu_id=0
    do_checkpoint_insts=true
    do_statistics_insts=true

To actually run gem5 in timing mode, let's specify a CPU type. While
we're at it, we can also specify sizes for the L1 caches.

```
build/X86/gem5.opt configs/example/se.py --cmd=tests/test-progs/hello/bin/x86/linux/hello --cpu-type=TimingSimpleCPU --l1d_size=64kB --l1i_size=16kB
```

    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 version 21.0.0.0
    gem5 compiled May 17 2021 18:05:59
    gem5 started May 18 2021 00:36:10
    gem5 executing on amarillo, pid 85269
    command line: build/X86/gem5.opt configs/example/se.py --cmd=tests/test-progs/hello/bin/x86/linux/hello --cpu-type=TimingSimpleCPU --l1d_size=64kB --l1i_size=16kB

    Global frequency set at 1000000000000 ticks per second
    warn: No dot file generated. Please install pydot to generate the dot file and pdf.
    warn: DRAM device capacity (8192 Mbytes) does not match the address range assigned (512 Mbytes)
    0: system.remote_gdb: listening for remote gdb on port 7005
    **** REAL SIMULATION ****
    info: Entering event queue @ 0.  Starting simulation...
    Hello world!
    Exiting @ tick 454646000 because exiting with last active thread context

Now, let's check the config.ini file and make sure that these options
propagated correctly to the final system. If you search
`m5out/config.ini` for "cache", you'll find that no caches were created!
Even though we specified the size of the caches, we didn't specify that
the system should use caches, so they weren't created. The correct
command line should be:

```
build/X86/gem5.opt configs/example/se.py --cmd=tests/test-progs/hello/bin/x86/linux/hello --cpu-type=TimingSimpleCPU --l1d_size=64kB --l1i_size=16kB --caches
```

    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 version 21.0.0.0
    gem5 compiled May 17 2021 18:05:59
    gem5 started May 18 2021 00:37:03
    gem5 executing on amarillo, pid 85560
    command line: build/X86/gem5.opt configs/example/se.py --cmd=tests/test-progs/hello/bin/x86/linux/hello --cpu-type=TimingSimpleCPU --l1d_size=64kB --l1i_size=16kB --caches

    Global frequency set at 1000000000000 ticks per second
    warn: No dot file generated. Please install pydot to generate the dot file and pdf.
    warn: DRAM device capacity (8192 Mbytes) does not match the address range assigned (512 Mbytes)
    0: system.remote_gdb: listening for remote gdb on port 7005
    **** REAL SIMULATION ****
    info: Entering event queue @ 0.  Starting simulation...
    Hello world!
    Exiting @ tick 31680000 because exiting with last active thread context

On the last line, we see that the total time went from 454646000 ticks
to 31680000, much faster! Looks like caches are probably enabled now.
But, it's always a good idea to double check the `config.ini` file.

    [system.cpu.dcache]
    type=Cache
    children=power_state replacement_policy tags
    addr_ranges=0:18446744073709551615
    assoc=2
    clk_domain=system.cpu_clk_domain
    clusivity=mostly_incl
    compressor=Null
    data_latency=2
    demand_mshr_reserve=1
    eventq_index=0
    is_read_only=false
    max_miss_count=0
    move_contractions=true
    mshrs=4
    power_model=
    power_state=system.cpu.dcache.power_state
    prefetch_on_access=false
    prefetcher=Null
    replace_expansions=true
    replacement_policy=system.cpu.dcache.replacement_policy
    response_latency=2
    sequential_access=false
    size=65536
    system=system
    tag_latency=2
    tags=system.cpu.dcache.tags
    tgts_per_mshr=20
    warmup_percentage=0
    write_allocator=Null
    write_buffers=8
    writeback_clean=false
    cpu_side=system.cpu.dcache_port
    mem_side=system.membus.cpu_side_ports[2]

Some common options `se.py` and `fs.py`
---------------------------------------

All of the possible options are printed when you run:

```
build/X86/gem5.opt configs/example/se.py --help
```

Below are a few important options from that list:


* `--cpu-type=CPU_TYPE`

    * The type of cpu to run with. This is an important parameter to always set. The default is atomic, which doesn’t perform a timing simulation.

* `--sys-clock=SYS_CLOCK`

    * Top-level clock for blocks running at system speed.

* `--cpu-clock=CPU_CLOCK`

    * Clock for blocks running at CPU speed. This is separate from the system clock above.

* `--mem-type=MEM_TYPE`

    * Type of memory to use. Options include different DDR memories, and the ruby memory controller.

* `--caches`

    * Perform the simulation with classic caches.

* `--l2cache`

    * Perform the simulation with an L2 cache, if using classic caches.

* `--ruby`

    * Use Ruby instead of the classic caches as the cache system simulation.

* `-m TICKS, --abs-max-tick=TICKS`

    * Run to absolute simulated tick specified including ticks from a restored checkpoint. This is useful if you only want simulate for a certain amount of simulated time.

* `-I MAXINSTS, --maxinsts=MAXINSTS`

    * Total number of instructions to simulate (default: run forever). This is useful if you want to stop simulation after a certain number of instructions has been executed.

* `-c CMD, --cmd=CMD`

    * The binary to run in syscall emulation mode.

* `-o OPTIONS, --options=OPTIONS`

    * The options to pass to the binary, use ” ” around the entire string. This is useful when you are running a command which takes options. You can pass both arguments and options (e.g., –whatever) through this variable.

* `--output=OUTPUT`

    * Redirect stdout to a file. This is useful if you want to redirect the output of the simulated application to a file instead of printing to the screen. Note: to redirect gem5 output, you have to pass a parameter before the configuration script.

* `--errout=ERROUT`

    * Redirect stderr to a file. Similar to above.
