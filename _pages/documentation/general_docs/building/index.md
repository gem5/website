---
layout: documentation
title: Building gem5
doc: gem5 documentation
parent: building_extras
permalink: /documentation/general_docs/building
authors: Bobby R. Bruce
---

# Building gem5

## Supported operating systems and environments

gem5 has been designed with a Linux environment in mind. We test regularly
on **Ubuntu 18.04** and **Ubuntu 20.04** to ensure gem5 functions well in
these environments. Though **any Linux based OS should function if the correct
dependencies are installed**. We ensure that gem5 is compilable with both gcc
and clang (see [Dependencies](#dependencies)  below for compiler version
information).

**Mac OS should work when compiling using the clang compiler**, with all other
dependencies installed. However, at present, we do not officially test our
builds on Mac OS. **We therefore cannot guarantee the same stability for those
wishing to compile and run gem5 in Mac OS as we can in Linux-based systems**.
[In later versions of gem5, we hope to more effectively support Mac OS through
improved testing](https://gem5.atlassian.net/browse/GEM5-538).

As of gem5 21.0, **we support building and running gem5 with Python 3.6+
only.**. gem5 20.0 was our last version of gem5 to provide support for Python
2.

If running gem5 in a suitable OS/environment is not possible, we have provided
pre-prepared [Docker](https://www.docker.com/) images which may be used to
compile and run gem5. Please see our [Docker](#docker) section below for more
information on this.

## Dependencies

* **git** : gem5 uses git for version control.
* **gcc**: gcc is used to compiled gem5. **Version >=7 must be used**. We
support up to gcc Version 10.
* **Clang**: Clang can also be used. At present, we support Clang 6 to
Clang 11 (inclusive).
* **SCons** : gem5 uses SCons as its build environment. SCons 3.0 or greater
must be used.
* **Python 3.6+** : gem5 relies on Python development libraries. gem5 can be
compiled and run in environments using Python 3.6+.
* **protobuf 2.1+** (Optional): The protobuf library is used for trace
generation and playback.
* **Boost** (Optional): The Boost library is a set of general purpose C++
libraries. It is a necessary dependency if you wish to use the SystemC
implementation.

### Setup on Ubuntu 18.04

If compiling gem5 on Ubuntu 18.04, or related Linux distributions, you may
install all these dependencies using APT:

```
sudo apt install build-essential git m4 scons zlib1g zlib1g-dev \
    libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev \
    python3-dev python3-six python libboost-all-dev pkg-config
```

### Setup on Ubuntu 20.04

If compiling gem5 on Ubuntu 20.04, or related Linux distributions, you may
install all these dependencies using API:

```
sudo apt install build-essential git m4 scons zlib1g zlib1g-dev \
    libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev \
    python3-dev python3-six python-is-python3 libboost-all-dev pkg-config
```

### Docker

For users struggling to setup an environment to build and run gem5, we provide
the following Docker Images:

Ubuntu 18.04 with all optional dependencies:
[gcr.io/gem5-test/ubuntu-18.04_all-dependencies](
https://gcr.io/gem5-test/ubuntu-18.04_all-dependencies) ([source Dockerfile](
https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/util/dockerfiles/ubuntu-18.04_all-dependencies/Dockerfile)).

Ubuntu 18.04 with the minimum set of dependencies:
[gcr.io/gem5-test/ubuntu-18.04_min-dependencies](
https://gcr.io/gem5-test/ubuntu-18.04_min-dependencies) ([source Dockerfile](
https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/util/dockerfiles/ubuntu-18.04_min-dependencies/Dockerfile)).


Ubuntu 20.04 with all optional dependencies:
[gcr.io/gem5-test/ubuntu-20.04_all-dependencies](
https://gcr.io/gem5-test/ubuntu-20.04_all-dependencies) ([source Dockerfile](
https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/util/dockerfiles/ubuntu-20.04_all-dependencies/Dockerfile)).

To obtain a docker image:

```
docker pull <image>
```

E.g., for Ubuntu 18.04 with all optional dependencies:

```
docker pull gcr.io/gem5-test/ubuntu-18.04_all-dependencies
```

Then, to work within this enviornment, we suggest using the following:

```
docker run -u $UID:$GID --volume <gem5 directory>:/gem5 --rm -it <image>
```

Where `<gem5 directory>` is the full path of the gem5 in your file system, and
`<image>` is the image pulled (e.g.,
`gcr.io/gem5-test/ubuntu-18.04_all-dependencies`).

From this environment, you will be able to build and run gem5 from the `/gem5`
directory.

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
scons build/{ISA}/gem5.{variant} -j {cpus}
```

where `{ISA}` is the target (guest) Instruction Set Architecture, and
`{variant}` specifies the compilation settings. For most intents and purposes
`opt` is a good target for compilation. The `-j` flag is optional and allows
for parallelization of compilation with `{cpus}` specifying the number of
threads. A single-threaded compilation from scratch can take up to 2 hours on
some systems. We therefore strongly advise allocating more threads if possible.

The valid ISAs are:

* ARCH
* ARM
* NULL
* MIPS
* POWER
* RISCV
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

For example, to build gem5 on 4 threads with `opt` and targeting x86:

```
scons build/X86/gem5.opt -j 4
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
