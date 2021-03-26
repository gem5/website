---
layout: documentation
title: Debugging Simulated Code
doc: gem5 documentation
parent: debugging
permalink: /documentation/general_docs/debugging_and_testing/debugging/debugging_simulated_code
author: Bobby R. Bruce
---

# Debugging Simulated Code

gem5 has built-in support for gdb's remote debugger interface. If you are
interested in monitoring what the code on the simulated machine is doing
(the kernel, in FS mode, or program, in SE mode) you can fire up gdb on the
host platform and have it talk to the simulated gem5 system as if it were a
real machine/process (only better, since gem5 executions are deterministic and
gem5's remote debugger interface is guaranteed not to perturb execution on the
simulated system).

If you are simulating a system that uses a different ISA from the host you're
running on, you'll need a cross-architecture gdb; see below for instructions.
If you are simulating the native ISA of your host, you can very likely just use
the pre-installed native gdb.

When gem5 is run, each CPU listens for a remote debugging connection on a TCP
port. The first port allocated is generally 7000, though if a port is in use,
the next port will be tried.

To attach the remote debugger, it's necessary to have a copy of the kernel and
of the source. Also to view the kernel's call stack, you must make sure Linux
was built with the necessary debug configuration parameters enabled. To run the
remote debugger, do the following (assuming host=localhost and port=7000):

```
gdb-multiarch <path-to-linux>/vmlinux
GNU gdb (Ubuntu 8.2-0ubuntu1~18.04) 8.2
Copyright (C) 2018 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

(gdb) target remote <host>:<port>
```

The gem5 simulator is already running and the target remote command connects to
the already running simulator and stops it in the middle of execution. You can
set breakpoints and use the debugger to debug the kernel. It is also possible
to use the remote debugger to debug console code. Setting that up
is similar, but a how to will be left for future work.

If you're using both the remote debugger and the debugger on the simulator, it
is possible to trigger the remote debugger from the main debugger by doing a
`call debugger()`. Before you do this you'll need to figure out what CPU (the
cpu id) you want to debug and set `current_debugger` to that `cpuid`. If you
only have one cpu, then it will be `cpuid 0`, however if there are multiple
cpus you will need to match the cpu id with the corresponding port number for
the remote gdb session. For example, using the following sample output from
gem5, calling the kernel debugger for cpu 3 requires the kernel debugger to be
listening on port 7001.

```
%./build/<ISA>/gem5.debug configs/example/fs.py
...
making dual system
Global frequency set at 1000000000000 ticks per second
Listening for testsys connection on port 3456
Listening for drivesys connection on port 3457
0: testsys.remote_gdb.listener: listening for remote gdb #0 on port 7002
0: testsys.remote_gdb.listener: listening for remote gdb #1 on port 7003
0: testsys.remote_gdb.listener: listening for remote gdb #2 on port 7000
0: testsys.remote_gdb.listener: listening for remote gdb #3 on port 7001
0: drivesys.remote_gdb.listener: listening for remote gdb #4 on port 7004
0: drivesys.remote_gdb.listener: listening for remote gdb #5 on port 7005
0: drivesys.remote_gdb.listener: listening for remote gdb #6 on port 7006
0: drivesys.remote_gdb.listener: listening for remote gdb #7 on port 7007
```

## Getting a cross-architecture gdb

To use a remote debugger with gem5, the most important part is that you have
gdb compiled to work with the target system you're simulating.
The recommended approach is to install the gdb-multiarch package,
providing a single gdb binary usable for multiple ISAs (archs)

```
% sudo apt-get update -y
% sudo apt-get install -y gdb-multiarch
```

It is possible to compile a non-native architecture gdb on
the host machine as an alternative. All that must be done is add the `--target=`
option to configure when you compile gdb. You may also get pre-compiled
debuggers with cross compilers. See Download for links to some cross compilers
that include debuggers.

```
% wget http://ftp.gnu.org/gnu/gdb/<gdb-version>.tar.gz
% tar xfz <gdb-version>.tar.gz
% cd <gdb-version>
% ./configure --target=<isa>
<configure output....>
% make
<make output...this may take a while>
```

The end result is gdb/gdb which will work for remote debugging.

## Target-specific instructions

### ARM Target

If you're planning to debug an ARM kernel you'll need a reasonably new version
of gdb (7.1 or greater). Additionally, you'll have to manually specify the
`tspecs` like this (port number may be different). The `tspec` file is
available in the gdb source code:

```
set remote Z-packet on
set tdesc filename path/to/features/arm-with-neon.xml
symbol-file <path to vmlinux used for gem5>
target remote <ip addr of host running gem5 or if local host 127.0.0.1>:7000
```
