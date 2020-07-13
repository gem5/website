---
layout: documentation
title: Extending gem5 to run ARM binaries 
doc: Learning gem5
parent: part1
permalink: /documentation/learning_gem5/part1/extending_configs
author: Julian T. Angeles 
---

Extending gem5 for ARM
======================

This chapter assumes you've already built a basic x86 system with
gem5 and created a simple configuration script. 

Downloading ARM Binaries
------------------------

Let's start by downloading some ARM benchmark binaries. Begin
from the root of the gem5 folder:

```
mkdir -p cpu_tests/benchmarks/bin/arm
cd cpu_tests/benchmarks/bin/arm
wget gem5.org/dist/current/gem5/cpu_tests/benchmarks/bin/arm/Bubblesort
wget gem5.org/dist/current/gem5/cpu_tests/benchmarks/bin/arm/FloatMM
```

We'll use these to further test our ARM system.

Building gem5 to run ARM Binaries
---------------------------------

Just as we did when we first built our basic x86 system, we run
the same command, except this time we want it to compile with the
default ARM configurations. To do so, we just replace x86 with ARM:  

```
scons build/ARM/gem5.opt -j20
```

When compilation is finished you should have a working gem5 executable
at `build/ARM/gem5.opt`.

Modifying simple.py to run ARM Binaries
---------------------------------------

Before we can run any ARM binaries with our new system, we'll have
to make a slight tweak to our simple.py.

If you recall when we created our simple configuration script, it was
noted that we did not have to connect the PIO and interrupt ports to
the memory bus for any ISA other than for an x86 system. So let's
remove those 3 lines:

```
system.cpu.createInterruptController()
#system.cpu.interrupts[0].pio = system.membus.master
#system.cpu.interrupts[0].int_master = system.membus.slave
#system.cpu.interrupts[0].int_slave = system.membus.master

system.system_port = system.membus.slave
```

You can either delete or comment them out as above. Next let's set
the processes command to one of our ARM benchmark binaries:

```
process.cmd = ['cpu_tests/benchmarks/bin/arm/Bubblesort']
```

If you'd like to test a simple hello program as before, just
replace x86 with arm:

```
process.cmd = ['tests/test-progs/hello/bin/arm/linux/hello']
```

Running gem5
------------

Simply run it as before, except replace X86 with ARM:

```
build/ARM/gem5.opt configs/tutorial/simple.py
```

If you set your process to be the Bubblesort benchmark, your
output should look like this:

```
gem5 Simulator System.  http://gem5.org
gem5 is copyrighted software; use the --copyright option for details.

gem5 compiled Oct  3 2019 16:02:35
gem5 started Oct  6 2019 13:22:25
gem5 executing on amarillo, pid 77129
command line: build/ARM/gem5.opt configs/tutorial/simple.py

Global frequency set at 1000000000000 ticks per second
warn: DRAM device capacity (8192 Mbytes) does not match the address range assigned (512 Mbytes)
0: system.remote_gdb: listening for remote gdb on port 7002
Beginning simulation!
info: Entering event queue @ 0.  Starting simulation...
info: Increasing stack size by one page.
warn: readlink() called on '/proc/self/exe' may yield unexpected results in various settings.
      Returning '/home/jtoya/gem5/cpu_tests/benchmarks/bin/arm/Bubblesort'
-50000
Exiting @ tick 258647411000 because exiting with last active thread context
```
