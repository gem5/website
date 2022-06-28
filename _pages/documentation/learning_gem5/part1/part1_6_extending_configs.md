---
layout: documentation
title: Extending gem5 for ARM
doc: Learning gem5
parent: part1
permalink: /documentation/learning_gem5/part1/extending_configs
author: Julian T. Angeles, Thomas E. Hansen
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
wget dist.gem5.org/dist/v22-0/test-progs/cpu-tests/bin/arm/Bubblesort
wget dist.gem5.org/dist/v22-0/test-progs/cpu-tests/bin/arm/FloatMM
```

We'll use these to further test our ARM system.

Building gem5 to run ARM Binaries
---------------------------------

Just as we did when we first built our basic x86 system, we run
the same command, except this time we want it to compile with the
default ARM configurations. To do so, we just replace x86 with ARM:  

```
scons build/ARM/gem5.opt -j 20
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
#system.cpu.interrupts[0].pio = system.membus.mem_side_ports
#system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
#system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports
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

ARM Full System Simulation
--------------------------
To run an ARM FS Simulation, there are some changes required to the setup.

If you haven't already, from the gem5 repository's root directory, `cd` into
the directory `util/term/` by running

```bash
$ cd util/term/
```

and then compile the `m5term` binary by running

```bash
$ make
```

The gem5 repository comes with example system setups and configurations. These
can be found in the `configs/example/arm/` directory.

A collection of full system Linux image files are available
[here](https://www.gem5.org/documentation/general_docs/fullsystem/guest_binaries).
Save these in a directory and remember the path to it. For example, you could
store them in

```
/path/to/user/gem5/fs_images/
```

The `fs_images` directory will be assumed to contain the extracted FS images
for the rest of this example.

With the image(s) downloaded, execute the following command in your terminal:

```bash
$ export IMG_ROOT=/absolute/path/to/fs_images/<image-directory-name>
```

replacing "\<image-directory-name\>" with the name of the directory extracted
from the downloaded image file, without the angle-brackets.

We are now ready to run a FS ARM simulation. From the root of the gem5
repository, run:

```bash
$ ./build/ARM/gem5.opt configs/example/arm/fs_bigLITTLE.py \
    --caches \
    --bootloader="$IMG_ROOT/binaries/<bootloader-name>" \
    --kernel="$IMG_ROOT/binaries/<kernel-name>" \
    --disk="$IMG_ROOT/disks/<disk-image-name>" \
    --bootscript=path/to/bootscript.rcS
```

replacing anything in angle-brackets with the name of the directory or file,
without the angle-brackets.

You can then attach to the simulation by, in a different terminal window,
running:

```bash
$ ./util/term/m5term 3456
```

The full details of what the `fs_bigLITTLE.py` script supports can be gotten by
running:

```bash
$ ./build/ARM/gem5.opt configs/example/arm/fs_bigLITTLE.py --help
```

> **An aside on FS simulations:**
>
> Note that FS simulations take a long time; like "1 hour to load the kernel"
> long time! There are ways to "fast-forward" a simulation and then resume the
> detailed simulation at the interesting point, but these are beyond the scope
> of this chapter.

