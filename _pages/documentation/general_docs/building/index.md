---
layout: documentation
title: Building gem5
doc: gem5 documentation
parent: building_extras
permalink: /documentation/general_docs/building
authors: Bobby R. Bruce
---

# Building gem5

## Dependencies

* **git** : gem5 uses git for version control.
* **gcc 4.8+**: gcc is used to compiled gem5. Version 4.8+ must be used. We do
not presently support beyond Version 7. (Note:
[Support for gcc 4 may be dropped](https://gem5.atlassian.net/browse/GEM5-218),
and [version >7 may be supported](https://gem5.atlassian.net/browse/GEM5-194)
in future releases of gem5.
* **SCons** : gem5 uses SCons as its build environment.
* **Python 2.7+** : gem5 replies on Python development libraries (due to the
[retirement of Python 2](
http://pyfound.blogspot.com/2019/12/python-2-sunset.html) we are [likely to
migrate to Python 3 in future releases of gem5](
https://gem5.atlassian.net/browse/GEM5-275).
* **protobuf 2.1+** (Optional): The protobuf library is used for trace
generation and playback.
* **Boost** (Optional): The Boost library is a set of general purpose C++
libraries. It is a necessary dependency if you wish to use the SystemC
implementation.

If compiling gem5 on Debian, Ubuntu, or related Linux distributions, you may
install all these dependencies using APT:

```
sudo apt install build-essential git m4 scons zlib1g zlib1g-dev \
    libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev \
    python-dev python libboost-all-dev
```

## Getting the code

```
git clone https://gem5.googlesource.com/public/gem5
```

## Building with SCons

gem5's build system is based on SCons, an open source build system implemented
in Python. You can find more information about scons at <http://www.scons.org>.
The main scons file is called SConstruct and is found in the root of the source
tree. Additional scons files are named SConscript and are found throughout the
tree, usually near the files they're associated with.

Within the root of the gem5 directory, gem5 can be built with SCons using:

```
scons build/{ISA}/gem5.{variant}
```

where `{ISA}` is the target Instruction Set Architecture, and `{variant}`
specifies the compilation settings. For most intents and purposes `opt` is
a good target for compilation.

The valid ISAs are:

* ARCH
* ARM
* NULL
* MIPS
* POWER
* SPARC
* X86

The valid build variants are:

* **debug** has optimizations turned off. This ensures that variables won't be
optimized out, functions won't be unexpectedly inlined, and control flow will
not behave in surprising ways. That makes this version easier to work with in
tools like gdb, but without optimizations this version is significantly slower
than the others. You should choose it when using tools like gdb and valgrind
and don't want any details obscured, but other wise more optimized versions are
recommended.
* **opt** has optimizations turned on and debugging functionality like asserts
and DPRINTFs left in. This gives a good balance between the speed of the
simulation and insight into what's happening in case something goes wrong. This
version is best in most circumstances.
* **fast** has optimizations turned on and debugging functionality compiled
out. This pulls out all the stops performance wise, but does so at the expense
of run time error checking and the ability to turn on debug output. This
version is recommended if you're very confident everything is working correctly
and want to get peak performance from the simulator.
* **prof** is similar to gem5.fast but also includes instrumentation that
allows it to be used with the gprof profiling tool. This version is not needed
very often, but can be used to identify the areas of gem5 that should be
focused on to improve performance.
* **perf** also includes instrumentation, but does so using google perftools,
allowing it to be profiled with google-pprof. This profiling version is
complementary to gem5.prof, and can probably replace it for all Linux-based
systems.

These versions are summarized in the following table.

|Build variant|Optimizations|Run time debugging support|Profiling support|
|-------------|-------------|--------------------------|-----------------|
|**debug**    |             |X                         |                 |
|**opt**      |X            |X                         |                 |
|**fast**     |X            |                          |                 |
|**prof**     |X            |                          |X                |
|**perf**     |X            |                          |X                |

For example, to build gem5 with `opt` and targeting x86:

```
scons build/X86/gem5.opt
```

## Usage

Once compiled, gem5 can then be run using:

```
./build/{ISA}/gem5.{variant} [gem5 options] {simulation script} [script options]
```

Running with the `--help` flag will display all the available options:

```
Usage
=====
  gem5.opt [gem5 options] script.py [script options]

gem5 is copyrighted software; use the --copyright option for details.

Options
=======
--version               show program's version number and exit
--help, -h              show this help message and exit
--build-info, -B        Show build information
--copyright, -C         Show full copyright information
--readme, -R            Show the readme
--outdir=DIR, -d DIR    Set the output directory to DIR [Default: m5out]
--redirect-stdout, -r   Redirect stdout (& stderr, without -e) to file
--redirect-stderr, -e   Redirect stderr to file
--stdout-file=FILE      Filename for -r redirection [Default: simout]
--stderr-file=FILE      Filename for -e redirection [Default: simerr]
--listener-mode={on,off,auto}
                        Port (e.g., gdb) listener mode (auto: Enable if
                        running interactively) [Default: auto]
--listener-loopback-only
                        Port listeners will only accept connections over the
                        loopback device
--interactive, -i       Invoke the interactive interpreter after running the
                        script
--pdb                   Invoke the python debugger before running the script
--path=PATH[:PATH], -p PATH[:PATH]
                        Prepend PATH to the system path when invoking the
                        script
--quiet, -q             Reduce verbosity
--verbose, -v           Increase verbosity

Statistics Options
------------------
--stats-file=FILE       Sets the output file for statistics [Default:
                        stats.txt]
--stats-help            Display documentation for available stat visitors

Configuration Options
---------------------
--dump-config=FILE      Dump configuration output file [Default: config.ini]
--json-config=FILE      Create JSON output of the configuration [Default:
                        config.json]
--dot-config=FILE       Create DOT & pdf outputs of the configuration
                        [Default: config.dot]
--dot-dvfs-config=FILE  Create DOT & pdf outputs of the DVFS configuration
                        [Default: none]

Debugging Options
-----------------
--debug-break=TICK[,TICK]
                        Create breakpoint(s) at TICK(s) (kills process if no
                        debugger attached)
--debug-help            Print help on debug flags
--debug-flags=FLAG[,FLAG]
                        Sets the flags for debug output (-FLAG disables a
                        flag)
--debug-start=TICK      Start debug output at TICK
--debug-end=TICK        End debug output at TICK
--debug-file=FILE       Sets the output file for debug [Default: cout]
--debug-ignore=EXPR     Ignore EXPR sim objects
--remote-gdb-port=REMOTE_GDB_PORT
                        Remote gdb base port (set to 0 to disable listening)

Help Options
------------
--list-sim-objects      List all built-in SimObjects, their params and default
                        values
```

## Using EXTRAS

The [EXTRAS](/documentation/general_docs/building/EXTRAS) scons variable can be
used to build additional directories of source files into gem5 by setting it to
a colon delimited list of paths to these additional directories. EXTRAS is a
handy way to build on top of the gem5 code base without mixing your new source
with the upstream source. You can then manage your new body of code however you
need to independently from the main code base.
