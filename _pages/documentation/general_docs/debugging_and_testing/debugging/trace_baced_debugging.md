---
layout: documentation
title: Trace-based Debugging
doc: gem5 documentation
parent: debugging
permalink: /documentation/general_docs/debugging_and_testing/debugging/trace_based_debugging
author: Bobby R. Bruce
---

# Trace-based Debugging

## Introduction

The simplest method of debugging is to have gem5 print out traces of what it's
doing. The simulator contains many DPRINTF statements that print trace messages
describing potentially interesting events. Each DPRINTF is associated with a
debug flag (e.g., `Bus`, `Cache`, `Ethernet`, `Disk`, etc.). To turn on the
messages for a particular flag, use the `--debug-flags` command line argument.
Multiple flags can be specified by giving a list of strings, e.g.:

```
build/<ISA>/gem5.opt --debug-flags=Bus,Cache configs/examples/fs.py
```

would turn on a group of debug flags related to instruction execution but leave
out Tick (timing) information. This is useful if you want to compare execution
between two runs where the same instructions execute but at different rates.

Note that the gem5.fast binary does not support tracing; part of what makes it
faster than gem5.opt is that the DPRINTF code is compiled out.

The `--debug-flags` command line option should come after the gem5 executable
but before the simulation script. This is because debug flags are handled by
gem5 itself, and whether command line options are before or after the
simulation script determine if they're for gem5 or the script.

```
Debugging Options
-----------------
--debug-break=TIME[,TIME]
                        Tick to create a breakpoint
--debug-help            Print help on debug flags
--debug-flags=FLAG[,FLAG]
                        Sets the flags for debug output (-FLAG disables a
                        flag)
--debug-start=TIME      Start debug output at TIME (must be in ticks)
--debug-file=FILE       Sets the output file for debug [Default: cout]
--debug-ignore=EXPR     Ignore EXPR sim objects
```

The complete list of debug/trace flags can be seen by running gem5 with the
`--debug-help` option.

If you find that events of interest are not being traced, feel free to add
DPRINTFs yourself. You can add new debug flags simply by adding `DebugFlag()`
command to any SConscript file (preferably the one nearest where you are using
the new flag). If you use a debug flag in a C++ source file, you would need to
include the header file `debug/<name of debug flag>.hh` in that file.

For more complex bugs, the trace can be useful in simply identifying points in
the simulation where more in-depth investigation is needed. The `--debug-break`
option lets you re-run your simulation under a debugger and stop on a
particular tick as identified by the trace. You can also schedule breakpoints
and enable or disable debug flags from within the debugger itself. See the page
on Debugger Based Debugging for more information.

### The Exec debug flag

The `Exec` compound debug flag is very useful because it turns on instruction
tracing in gem5. It makes the simulator print a disassembled version of each
instruction as it finishes executing, along with other useful information like
the time, pc, the address if it was a memory instruction, etc. These individual
pieces of information can be turned on and off with the base debug flags Exec
controls. For example, you can disable the use of function symbol names in
place of absolute PC addresses (if they're available) by turning off the
ExecSymbol flag (e.g., `--debug-flags=Exec,-ExecSymbol`).

If some supposedly innocuous change has caused gem5 to stop working correctly,
you can compare trace outputs from before and after the change using the
tracediff script in the `src/util` directory. Comments in the script describe
how to use it.

### Reducing trace file size

Trace file can become very large very quickly, but they also compress very well
(e.g. about 90%). If you'd like to make gem5 output a compressed trace, just
add a `.gz` extension to the output file name. For example
`--debug-file=trace.out` will produce an uncompressed file as normal, but
`--debug-file=trace.out.gz` will produce a gzip compressed file. You can use
the zcat program and pipes to process the output. The editor vim also can
uncompress gzip compressed files in memory.

## The tracediff and rundiff utilities

`tracediff` and `rundiff` utilities allow the simple diffing of two streams of
trace data from gem5 to find any differences. It's very handy for debugging why
regression tests fail, figuring out why your minor code change seems to cause
some unrelated execution problem, or comparing the execution of CPU models.

Both utilities are found in the `util` directory. `rundiff` is a simple
diff-like program. Unlike regular diff, this script does not read in the entire
input before comparing its inputs, so it can be used on lengthy outputs piped
from other programs (e.g., gem5 traces). `tracediff` is a front end for
`rundiff` that provides an easy way to run two similar copies of gem5 and diff
their outputs. It takes a common gem5 command line with embedded alternatives
and executes the two alternative commands in separate subdirectories with
output piped to rundiff.

Script arguments are handled uniformly as follows:

* If the argument does not contain a '|' character, it is appended to both
command lines.
* If the argument has a '|" character in it, the text on either size of the '|'
is appended to the respective command lines. Note that you'll have to quote the
arg or escape the '|' with a backslash so that the shell doesn't thing you're
doing a pipe or put quotes around it.
* Arguments with '#' characters are split at those characters, processed for
alternatives ('|'s) as independent terms, then pasted back into a single
argument (without the '#'s). (Sort of inspired by the C preprocessor '##' token
pasting operator.)

In other words, the arguments should look like the command line you want to
run, with '|' used to list the alternatives for the parts that you want to
differ between the two runs.

For example:

```
 % tracediff gem5.opt --opt1 '--opt2|--opt3' --opt4
# would compare these two runs:
gem5.opt --opt1 --opt2 --opt4
gem5.opt --opt1 --opt3 --opt4

% tracediff 'path1|path2#/m5.opt' --opt1 --opt2
# would compare these two runs:
path1/gem5.opt --opt1 --opt2
path2/gem5.opt --opt1 --opt2
```

If you want to add arguments to one run only, just put a '|' in with text only
on one side (`--onlyOn1|`). You can do this with multiple arguments together
too (`|-a -b -c` adds three args to the second run only).

The `-n` argument to tracediff allows you to preview the two generated command
lines without running them.

For tracediff to be useful some trace flags must be enabled. The most common
trace flags to use with tracediff are `--debug-flags=Exec,-ExecTicks` which
removes the timestamp from each trace making it suitable to diff when slight
timing variations are present.

Tracediff is also useful for comparing CPU models when one fails and the other
doesn't. In this case it's best to create a checkpoint before the problem
occurs (this can be done by just creating a bunch of checkpoints and finding
one that fails). If the failure occurs in kernel code, use the
`-ExecUser` debug flag, on the other hand if it occurs in user code try the
`-ExecKernel` debug flag to isolate user code in the trace. You can then
compare the traces and see when the execution diverges.

### Comparing traces across machines

Sometimes gem5 executions differ inexplicably across different environments,
and you'd like to use rundiff to help pinpoint where they diverge. Rather than
try and reproduce those environments on the same machine, you can use netcat
with rundiff to compare traces from gem5 instances running on separate systems
across the network.

First, start rundiff running on one machine, configured to compare the trace
output from a local instance of gem5 with the output of a netcat "server".
Since the network is likely to be the bottleneck, we'll compress the trace
going across netcat, which means we need to uncompress it as it arrives. For
example (choosing port number 33335 arbitrarily):

```
util/rundiff 'gem5.opt --debug-flag=Exec <gem5 args> |' 'nc -d -l 33335 | gunzip -c |' >& tracediff.out &
```

Now go to the second machine, start a copy of gem5 there, and ship its
compressed trace output to the netcat instance running on the first machine.
For example:

```
gem5.opt --debug-flag=Exec <gem5 args> |& gzip -c |& nc <hostname> 33335
```

## Internal Exec tracing implementation (InstTracer)

The "Trace-based debugging" section above talked about how to use the `Exec`
trace flag to print information about each instruction as it completes. That
functionality is actually implemented by an `InstTracer` object which collects
information about instructions as the execute. These objects can be swapped
out, and different objects can do different things with the information they
collect. For instance, the `IntelTrace` object prints out a trace in a
different format which is compatible with an external tool. The objects can
also do more than just print a trace. `NativeTrace` objects send information
about architectural state over a socket to the statetrace tool (described
below) instruction by instruction to validate execution. `InstTracer` objects
are `SimObjects` which are assigned to the `tracer` parameter of each CPU. If
you want to install a different tracer, just assign it to that parameter on the
CPU of interest.

When writing your own `InstTracer`, you'll write at least two different
classes, one which inherits from `InstTracer` and one that inherits from
`InstRecord`. The `InstTracer` class's main responsibility is to generate
`InstRecord` objects which are associated with a particular instruction. By
subclassing `InstTracer`, you'll be able to return your own specialized version
of `InstRecord` which is the class that really does most of the work.

The `InstRecord` class have a number of fields which hold information about the
history of an instruction. For instance, `InstRecord` records the instruction's
PC, what address it used if it accessed memory, a "data" value which it
produced (multiple data values aren't handled), etc. The `InstRecord` function
also has a pointer to a `ThreadContext` which can be used to read out
architectural state. When an instruction is finished executing, the
`InstRecord`'s `dump()` virtual function is called to process the record. For
the default `InstTracer`, this is where the instruction's assembly language
form, etc., is printed which is the output you see when you turn on `Exec`. For
`NativeTrace`, this is where architectural state is gathered up to send to
statetrace.

## Comparing traces with a real machine

The statetrace tool runs alongside gem5 and compares execution of a workload on
a real machine with execution in gem5. In the simulator and the real system,
the workload is allowed to run one instruction at a time. After each
instruction, architectural state is collected and compared and any differences
are reported. It can be tricky to get it set up and producing useful results
(described below), but it's an extremely valuable tool for debugging because it
tends to quickly pinpoint exactly where a problem is coming from, likely saving
many hours of painful debugging per bug.

### Native Trace

In gem5, a NativeTrace `InstTracer` object (described above) needs to be
installed on the CPU that will run the workload of interest. When execution
starts, the tracer will wait for the state trace utility to connect to it.
Then, after each instruction executes, it uses the `ThreadContext` pointer in
the `InstRecord` object to gather architectural state from the currently
running process. It also reads in architectural state gather by state trace
through the connection they established. The two versions of state are
compared, and any meaningful differences are reported. The exact makeup of the
state and how it should be compared is very ISA dependent on ISA, so each ISA
defines its own version of NativeTrace. These specialized classes can handle
things like expected differences when registers may become undefined, or
situations where execution skips ahead for one reason or another.

### statetrace utility

The statetrace utility is found in the util directory and is responsible for
running the workload on the real machine. It uses the ptrace mechanism provided
by the Linux kernel to single step the target process and to access its state.
It uses scons, but is independent of scons as used by the rest of gem5. To
build a version of statetrace suitable for a particular ISA, use the
`build/${ARCH}/statetrace` target where `${ARCH}` is replaced by the ISA of
interest. Currently recognized values for `${ARCH}` are `amd64`, `arm`, `i686`,
and `sparc`. You can override the compiler used for any ISA using the CXX scons
argument, and the compiler used for a particular ISA with `${ARCH}CXX`. For
instance, to build an arm version of statetrace, you could run:

```
cd util/statetrace
scons ARMCXX=arm-softfloat-linux-gnueabi-g++ build/arm/statetrace
```

statetrace accepts four flags, `-h` to print the help, `--host` to specify what
ip and port gem5 is listening at, `-i` to print out what's on the initial stack
frame, and `-nt` to disable tracing. `-nt` is typically used with `-i` to get
information about a processes initial stack without running it. The end of the
command line options is marked with two dashes. Next, put the command line you
want statetrace to run.

The exact text of the program name and arguments matters because these will be
passed to the process on its stack. Longer values take up more room on the
stack, that displaces other items to different addresses, and statetrace clog
up with lots of unimportant differences. For instance, if you need to run a
program found in your home directory in a gem5 subdirectory and you run this
command:

```
statetrace -- ~/gem5/my_benchmark arg1 arg2
```

You must also override arg0 in gem5 to be `~/gem5/my_benchmark`.

### Tuning

statetrace is a very sensitive system, and any minor difference between
simulated execution and real execution could produce lots and lots of spurious
differences. In order to get useful information from statetrace you'll need to
adjust the real system and gem5 so that everything lines up perfectly. I
normally create a patch which has all the modifications I've made to gem5 for
statetrace. Then I can easily remove them or reapply them for as I find and fix
problems. Mercurial queues is useful for managing that patch and patches for my
fixes. The following is an incomplete list of the differences you may have to
correct.

Address randomization: To improve security, Linux will randomize the address
space of processes, moving around their stack and heap areas. This makes it
harder for an attacker to predict what memory will look like, but it also
thoroughly defeats statetrace. To disable it, echo `0` into
`/proc/sys/kernel/randomize_va_space`. You'll almost certainly need root
permissions to do that.

argv values: Be sure to use _exactly_ the same text for each argument to your
program in gem5 and on the real system. This includes arg0, the program name.

File block size: Glibc uses the block size associated with a file to decide how
to buffer it. Different behavior will throw off execution and prevent
statetrace from working. You can change the block size gem5 reports in the
`convertStatBuf` and `convertStat64Buf` functions in `src/sim/syscall_emul.hh`.

Initial stack contents: Depending on your version of Linux, the contents of the
initial stack may be different. You can use the `-i` and `-nt` options to print
out the content of the initial stack on the real machine. statetrace attempts
to interpret the initial stack so you can more easily see what's on it. You'll
need to adjust how gem5 sets up the stack to match your real system. This code
is typically in a file called `process.cc` in the appropriate arch directory.
gem5's code has been painstakingly constructed so that it sets up a stack as
identically to Linux as possible, but the underlying mechanism would change.
Also, Linux puts a collection of auxiliary vectors on the initial stack. These
are type, value pairs which let the kernel provide extra information to the
process as it starts. From time to time Linux introduces a new type of
auxiliary vector and adds it to the stack. You may need to dig into the Linux
source and emulate any new entries.

### Caveats

Because statetrace is very sensitive to any changes in execution, it can't be
used with programs that don't behave in very predictable ways. For instance, if
a program reads in a random value from `/dev/random` and uses that in a
calculation (or worse in control flow) then that program can't be used. Less
obviously, if the program relies on the system time which is unpredictable, it
also can't be used. Generally speaking, many benchmarks try to be very
deterministic so that they can be used to generate reproducible data. That
makes them work well with statetrace.

Statetrace can't be used at the operating system level for at least two main
reasons. First, no system is implemented or will be implemented in the
foreseeable future for single stepping an operating system. Second, real
operating systems are not determinstic. Interrupts from hardware devices will
almost certainly come in at unpredictable times, some devices will return
unpredictable data, and gem5 is much less likely to exactly match the behavior
of a system at that level where firmware and other implementation details are
non longer abstracted away. Second the amount of state that's relevant at the
system level is typically larger than at the user level, especially in complex
ISAs like `x86`. Gathering, comparing, and transporting all that extra state
would significantly impact performance.

Not all implementations of ptrace actually work properly. For instance when I
last used statetrace with `ARM`, certain functions called into a region of
memory set up by the kernel which had kernel specific implementations of for
various operations. Ptrace relied on software breakpoints which work by
replacing the next instruction in the program with one that will trap. Because
the region of memory really belonged to the kernel, ptrace couldn't modify it
to install a breakpoint. The process "escaped" single stepped execution and
quickly ran to completion, leaving gem5 waiting for an update that never came.

statetrace isn't able to track changes to memory. Because memory is very large
and there isn't a convenient way to detect modifications to it, statetrace only
tracks register based architectural state. If an instruction changes registers
correctly but stores the wrong value to memory and/or to the wrong address,
that problem may not be detected for many instructions. Fortunately, those
sorts of errors are the exception.

To compare execution to a real machine, you ideally need to have a real machine
at your disposal. It's still quite possible, however, to run statetrace inside
an emulator like qemu. That's likely a little slower and compares execution
against the emulator and not real hardware, but it can still help identify
bugs.

### ISA support

Currently `SPARC`, `ARM`, and `x86` support state. ARM's support is currently
the most sophisticated, only sending differences in state across the connection
which improves performance, and only printing when differences start or stop
which reduces output and improves readability. Those features are planned to be
ported to the other ISAs. Hopefully that code can be factored out and put into
the base `NativeTrace` class so that all ISAs can use it easily.
