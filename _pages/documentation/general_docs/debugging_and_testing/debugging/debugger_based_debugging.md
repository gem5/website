---
layout: documentation
title: Debugger-based Debugging
doc: gem5 documentation
parent: debugging
permalink: /documentation/general_docs/debugging_and_testing/debugging/debugger_based_debugging
author: Bobby R. Bruce
---

# Debugger-based Debugging

If traces alone are not sufficient, you'll need to inspect what gem5 is doing
in detail using a debugger (e.g., gdb). You definitely want to use the
`gem5.debug` binary if you reach this point. Ideally, looking at traces should
at least allow you to narrow down the range of cycles in which you think
something is going wrong. The fastest way to reach that point is to use a
`DebugEvent`, which goes on gem5's event queue and forces entry into the
debugger when the specified cycle is reached by sending the process a `SIGTRAP`
signal. You'll need to to start gem5 under the debugger or have the debugger
attached to the gem5 process for this to work.

You can create one or more DebugEvents when you invoke gem5 using the
`--debug-break=100` parameter. You can also create new DebugEvents from the
debugger prompt using the `schedBreak()` function. The following example
session illustrates both of these approaches:

```
% gdb m5/build/<ISA>/gem5.debug
GNU gdb 6.1
Copyright 2002 Free Software Foundation, Inc.
[...]
(gdb) run --debug-break=2000 configs/run.py
Starting program: /z/stever/bk/m5/build/<ISA>/gem5.debug --debug-break=2000 configs/run.py
M5 Simulator System
[...]
warn: Entering event queue @ 0.  Starting simulation...

Program received signal SIGTRAP, Trace/breakpoint trap.
0xffffe002 in ?? ()
(gdb) p curTick
$1 = 2000
(gdb) c
Continuing.

(gdb) call schedBreak(3000)
(gdb) c
Continuing.

Program received signal SIGTRAP, Trace/breakpoint trap.
0xffffe002 in ?? ()
(gdb) p _curTick
$3 = 3000
(gdb)
```

gem5 includes a number of functions specifically intended to be called from the
debugger (e.g., using the gdb `call` command, as in the `schedBreak()` example
above). Many of these are "dump" functions which display internal simulator
data structures. For example, `eventq_dump()` displays the events scheduled on
the main event queue. Most of the other dump functions are associated with
particular objects, such as the instruction queue and the ROB in the detailed
CPU model. These include:

|Function                                    |Effect                                                   |
|:-------------------------------------------|:--------------------------------------------------------|
|`schedBreak(<tick>)`                        |Schedule a `SIGTRAP` to occur at `<tick>`                |
|`setDebugFlag("<flag>")`                    |Enable a debug flag from the debugger                    |
|`clearDebugFlag("<flag>")`                  |Disable a debug flags from the debugger                  |
|`eventqDump()`                              |Print out all events on the event queue                  |
|`takeCheckpoint(<tick>)`                    |Create a checkpoint at cycle `<tick>`                    |
|`SimObject::find("system.qualified.name")`  |Returns the pointer to the object with the specified name|

<!---
The following has been commented out as the link the classic
memory system has yet to be migrated over to the website.

Additional gdb-accessible features for debugging coherence protocols in the
classic memory system are documented [here]{
http://gem5.org/Classic_Memory_System#Debugging}.
-->

## Debugging Python with PDB

You can debug configuration scripts with the [Python debug (PDB)](
https://docs.python.org/3/library/pdb.html) just as you would other Python
scripts. You can enter PDB before your configuration script is executed by
giving the `--pdb` argument to the gem5 binary. Another approach is to put the
following line in your configuration script (e.g., `fs.py` or `se.py`) wherever
you would like to enter the debugger:

```
import pdb; pdb.set_trace()
```

Note that the Python files under `src` are compiled in to the gem5 binary, so you
must rebuild the binary if you add this line (or make other changes) in these
files. Alternatively, you can set the `M5_OVERRIDE_PY_SOURCE` environment
variable to "true" (see `src/python/importer.py`).

See the [official PDB documentation](
https://docs.python.org/3/library/pdb.html) for more details on using PDB.

## Using Valgrind

Valgrind is a dynamic analysis tool used (primarily) to profile a target
application and detect the source of run-time errors, as well as detect memory
leaks.

For Valgrind to function, the target gem5 binary must have been compiled to
include debugging information. Therefore, the `gem5.debug` binaries must be
used.

To run a check using Valgrind, execute the following:

```
valgrind --leak-check=yes --suppressions=util/valgrind-suppressions build/{Target ISA}/gem5.debug {gem5 arguments}
```

The above will run the gem5 and do two things:

1. Give a stack trace if a run-time error is received.
2. Give information about potential memory leaks.

The `util/valgrind-suppressions` file contains a set of warnings that are
reported by Valgrind but are not considered a problem by gem5 developers.
**Valgrind is known to provide false positives. `util/valgrind-suppressions`
should be updated as these false positives are revealed**. More information
about suppressing Valgrind warnings can be found in the [Valgrind User Manual](
http://valgrind.org/docs/manual/manual-core.html#manual-core.suppress).

If a run-time error is received, Valgrind will return an output which looks like
the following (taken from the [Valgrind Quick Start Guide](
http://valgrind.org/docs/manual/quick-start.html)):

```
==19182== Invalid write of size 4
==19182==    at 0x804838F: f (example.c:6)
==19182==    by 0x80483AB: main (example.c:11)
```

In this output:

* 19182 is the process ID
* `Invalid write` is what kind of error.
* Below this error is the stack trace. In this example the leak occurred at
line 6 in `example.c`. This line is contained within function `f` which was
called by the `main` method at line 11 (also in `example.c`).
* `0x804838F` is the code address. This is usually not important.

Valgrind may also return warnings about memory leaks, such as:

```
==19182== 40 bytes in 1 blocks are definitely lost in loss record 1 of 1
==19182==    at 0x1B8FF5CD: malloc (vg_replace_malloc.c:130)
==19182==    by 0x8048385: f (a.c:5)
==19182==    by 0x80483AB: main (a.c:11)
```

The stack trace will tell you where the memory leak occurred. If Valgrind
states that a block of memory was "definitely lost" then there is a memory
leak. However, if Valgrind states that a block was "probably lost", Valgrind
has reason to believe memory is leaking but perhaps not (this is normally if
the code is doing something complex with pointers).

If Valgrind returns an output in which a root cause is difficult to determine,
try running Valgrind with `--track-origins=yes`. This will increase execution
time but will provide more information.

The [Valgrind User Manual](https://valgrind.org/docs/manual/manual.html) should
be consulted for more advanced features.
