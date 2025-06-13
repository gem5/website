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
on **Ubuntu 20.04**, **Ubuntu 22.04** and **Ubuntu 24.04** to ensure gem5 functions well in
these environments. Though **any Linux based OS should function if the correct
dependencies are installed**. We ensure that gem5 is compilable with both gcc
and clang (see [Dependencies](#dependencies)  below for compiler version
information).

As of gem5 21.0, **we support building and running gem5 with Python 3.6+
only**. gem5 20.0 was our last version of gem5 to provide support for Python
2.

If running gem5 in a suitable OS/environment is not possible, we have provided
pre-prepared [Docker](https://www.docker.com/) images which may be used to
compile and run gem5. Please see our [Docker](#docker) section below for more
information on this.

## Dependencies

* **git** : gem5 uses git for version control.
* **gcc**: gcc is used to compiled gem5. **Version >=10 must be used**. We
support up to gcc Version 13.
* **Clang**: Clang can also be used. At present, we support Clang 7 to
Clang 16 (inclusive).
* **SCons** : gem5 uses SCons as its build environment. SCons 3.0 or greater
must be used.
* **Python 3.6+** : gem5 relies on Python development libraries. gem5 can be
compiled and run in environments using Python 3.6+.
* **protobuf 2.1+** (Optional): The protobuf library is used for trace
generation and playback.
* **Boost** (Optional): The Boost library is a set of general purpose C++
libraries. It is a necessary dependency if you wish to use the SystemC
implementation.

### Setup on Ubuntu 24.04 (gem5 >= v24.0)

If compiling gem5 on Ubuntu 24.04, or related Linux distributions, you may
install all these dependencies using APT:

```
sudo apt install build-essential scons python3-dev git pre-commit zlib1g zlib1g-dev \
    libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev \
    libboost-all-dev  libhdf5-serial-dev python3-pydot python3-venv python3-tk mypy \
    m4 libcapstone-dev libpng-dev libelf-dev pkg-config wget cmake doxygen
```

### Setup on Ubuntu 22.04 (gem5 >= v21.1)

If compiling gem5 on Ubuntu 22.04, or related Linux distributions, you may
install all these dependencies using APT:

```
sudo apt install build-essential git m4 scons zlib1g zlib1g-dev \
    libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev \
    python3-dev libboost-all-dev pkg-config python3-tk
```

### Setup on Ubuntu 20.04 (gem5 >= v21.0)

If compiling gem5 on Ubuntu 20.04, or related Linux distributions, you may
install all these dependencies using APT:

```
sudo apt install build-essential git m4 scons zlib1g zlib1g-dev \
    libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev \
    python3-dev python-is-python3 libboost-all-dev pkg-config gcc-10 g++-10 \
    python3-tk
```


### Docker

For users struggling to setup an environment to build and run gem5, we provide
the following Docker Images:

Ubuntu 24.04 with all optional dependencies:
[ghcr.io/gem5/ubuntu-24.04_all-dependencies:v24-0](
https://ghcr.io/gem5/ubuntu-24.04_all-dependencies:v24-0)
([source Dockerfile](https://github.com/gem5/gem5/blob/v24.0.0.0/util/dockerfiles/ubuntu-24.04_all-dependencies/Dockerfile)).

Ubuntu 24.04 with minimum dependencies:
[ghcr.io/gem5/ubuntu-24.04_min-dependencies:v24-0](
https://ghcr.io/gem5/ubuntu-24.04_min-dependencies:v24-0)
([source Dockerfile](https://github.com/gem5/gem5/blob/v24.0.0.0/util/dockerfiles/ubuntu-24.04_min-dependencies/Dockerfile)).

Ubuntu 22.04 with all optional dependencies:
[ghcr.io/gem5/ubuntu-22.04_all-dependencies:v23-0](
https://ghcr.io/gem5/ubuntu-22.04_all-dependencies:v23-0) ([source Dockerfile](
https://github.com/gem5/gem5/blob/v23.0.1.0/util/dockerfiles/ubuntu-22.04_all-dependencies/Dockerfile)).

Ubuntu 20.04 with all optional dependencies:
[ghcr.io/gem5/ubuntu-20.04_all-dependencies:v23-0](
https://ghcr.io/gem5/ubuntu-20.04_all-dependencies:v23-0) ([source Dockerfile](
https://github.com/gem5/gem5/blob/v23.0.1.0/util/dockerfiles/ubuntu-20.04_all-dependencies/Dockerfile)).

Ubuntu 18.04 with all optional dependencies:
[ghcr.io/gem5/ubuntu-18.04_all-dependencies:v23-0](
https://ghcr.io/gem5/ubuntu-18.04_all-dependencies:v23-0) ([source Dockerfile](
https://github.com/gem5/gem5/blob/v23.0.1.0/util/dockerfiles/ubuntu-18.04_all-dependencies/Dockerfile)).

To obtain a docker image:

```
docker pull <image>
```

E.g., for Ubuntu 20.04 with all optional dependencies:

```
docker pull ghcr.io/gem5/ubuntu-20.04_all-dependencies:v23-0
```

Then, to work within this environment, we suggest using the following:

```
docker run -u $UID:$GID --volume <gem5 directory>:/gem5 --rm -it <image>
```

Where `<gem5 directory>` is the full path of the gem5 in your file system, and
`<image>` is the image pulled (e.g.,
ghcr.io/gem5/ubuntu-22.04_all-dependencies:v23-0`).

From this environment, you will be able to build and run gem5 from the `/gem5`
directory.

## Getting the code

```
git clone https://github.com/gem5/gem5
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
However, compilation of gem5 is compute and memory intensive and increasing the
number of threads also increases memory usage. If using a machine with less
memory, it is recommended to use fewer threads (e.g. `-j 1` or `-j 2`).

The valid ISAs are:

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

These versions are summarized in the following table.

|Build variant|Optimizations|Run time debugging support|
|-------------|-------------|--------------------------|
|**debug**    |             |X                         |
|**opt**      |X            |X                         |
|**fast**     |X            |                          |

For example, to build gem5 on 4 threads with `opt` and targeting x86:

```
scons build/X86/gem5.opt -j 4
```

In addition, users may make use of the "gprof" and "pperf" build options to
enable profiling:

* **gprof** allows gem5 to be used with the gprof profiling tool. It can be
enabled by compiling with the `--gprof` flag. E.g.,
`scons build/ARM/gem5.debug --gprof`.
* **pprof** allows gem5 to be used with the pprof profiling tool. It can be
enabled by compiling with the `--pprof` flag. E.g.,
`scons build/X86/gem5.debug --pprof`.

## Build with Kconfig

Please see [here](https://www.gem5.org/documentation/general_docs/kconfig_build_system/)

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
--help, -h              show this help message and exit
--build-info, -B        Show build information
--copyright, -C         Show full copyright information
--readme, -R            Show the readme
--outdir=DIR, -d DIR    Set the output directory to DIR [Default: m5out]
--redirect-stdout, -r   Redirect stdout (& stderr, without -e) to file
--redirect-stderr, -e   Redirect stderr to file
--silent-redirect       Suppress printing a message when redirecting stdout or
                        stderr
--stdout-file=FILE      Filename for -r redirection [Default: simout.txt]
--stderr-file=FILE      Filename for -e redirection [Default: simerr.txt]
--listener-mode={on,off,auto}
                        Port (e.g., gdb) listener mode (auto: Enable if
                        running interactively) [Default: auto]
--allow-remote-connections
                        Port listeners will accept connections from anywhere
                        (0.0.0.0). Default is only localhost.
--interactive, -i       Invoke the interactive interpreter after running the
                        script
--pdb                   Invoke the python debugger before running the script
--path=PATH[:PATH], -p PATH[:PATH]
                        Prepend PATH to the system path when invoking the
                        script
--quiet, -q             Reduce verbosity
--verbose, -v           Increase verbosity
-m mod                  run library module as a script (terminates option
                        list)
-c cmd                  program passed in as string (terminates option list)
-P                      Don't prepend the script directory to the system path.
                        Mimics Python 3's `-P` option.
-s                      IGNORED, only for compatibility with python. don'tadd
                        user site directory to sys.path; also PYTHONNOUSERSITE

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
--debug-file=FILE       Sets the output file for debug. Append '.gz' to the
                        name for it to be compressed automatically [Default:
                        cout]
--debug-activate=EXPR[,EXPR]
                        Activate EXPR sim objects
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
