---
layout: documentation
title: Compiling a SLICC protocol
doc: Learning gem5
parent: part3
permalink: /documentation/learning_gem5/part3/MSIbuilding/
author: Jason Lowe-Power
---


## Building the MSI protocol

### The SLICC file

Now that we have finished implementing the protocol, we need to compile
it. You can download the complete SLICC files below:

- [MSI-cache.sm](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/src/learning_gem5/part3/MSI-cache.sm)
- [MSI-dir.sm](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/src/learning_gem5/part3/MSI-dir.sm)
- [MSI-msg.sm](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/src/learning_gem5/part3/MSI-msg.sm)

Before building the protocol, we need to create one more file:
`MSI.slicc`. This file tells the SLICC compiler which state machine
files to compile for this protocol. The first line contains the name of
our protocol. Then, the file has a number of `include` statements. Each
`include` statement has a file name. This filename can come from any of
the env variable `PROTOCOL_DIRS` directories. We declared the current
directory as part of the `PROTOCOL_DIRS` in the SConsopts file
(`main.Append(PROTOCOL_DIRS=[Dir('.')])`). The other directory is
`src/mem/protocol/`. These files are included like C++ header files.
Effectively, all of the files are processed as one large SLICC file.
Thus, any files that declare types that are used in other files must
come before the files they are used in (e.g., `MSI-msg.sm` must come
before `MSI-cache.sm` since `MSI-cache.sm` uses the `RequestMsg` type).

```cpp
protocol "MSI";
include "RubySlicc_interfaces.slicc";
include "MSI-msg.sm";
include "MSI-cache.sm";
include "MSI-dir.sm";
```

You can download the fill file
[here](https://github.com/gem5/gem5/blob/stable/src/learning_gem5/part3/MSI.slicc).

### Add new config options RUBY_PROTOCOL_MSI (gem5 >= 23.1)

Note: If users use the gem5 version newer than 23.0, they need to do some additional
steps to set up the Kconfig file. Otherwise, users can skip the steps to
`Compiling a protocol with SCons` section.

Then You need to added the MSI protocol in the `learning_gem5/part3/Kconfig`
file to let scons enable build gem5 with MSI protocol.

```
# Set the PROTOCOL="MSI" if the RUBY_PROTOCOL_MSI=y
config PROTOCOL
    default "MSI" if RUBY_PROTOCOL_MSI

# Add the new choice RUBY_PROTOCOL_MSI
cont_choice "Ruby protocol"
    config RUBY_PROTOCOL_MSI
        bool "MSI"
endchoice
```

In the `src/Kconfig`

```
rsource "base/Kconfig"
rsource "mem/ruby/Kconfig"
rsource "learning_gem5/part3/Kconfig"
```

Please add the `learning_gem5/part3/Kconfig` below the `mem/ruby/Kconfig`.

### Compiling a protocol with SCons

#### In the older gem5 version (gem5 <= 23.0)

Most SCons defaults (found in `build_opts/`) specify the protocol as
`MI_example`, an example, but poor performing protocol. Therefore, we
cannot simply use a default build name (e.g., `X86` or `ARM`). We have
to specify the SCons options on the command line. The command line below
will build our new protocol with the X86 ISA.

```sh
scons build/X86_MSI/gem5.opt --default=X86 PROTOCOL=MSI SLICC_HTML=True
```

This command will build `gem5.opt` in the directory `build/X86_MSI`. You
can specify *any* directory here. This command line has two new
parameters: `--default` and `PROTOCOL`. First, `--default` specifies
which file to use in `build_opts` for defaults for all of the SCons
variables (e.g., `ISA`, `CPU_MODELS`). Next, `PROTOCOL` *overrides* any
default for the `PROTOCOL` SCons variable in the default specified.
Thus, we are telling SCons to specifically compile our new protocol, not
whichever protocol was specified in `build_opts/X86`.

There is one more variable on this command line to build gem5:
`SLICC_HTML=True`. When you specify this on the building command line,
SLICC will generate the HTML tables for your protocol. You can find the
HTML tables in `<build directory>/mem/protocol/html`. By default, the
SLICC compiler skips building the HTML tables because it impacts the
performance of compiling gem5, especially when compiling on a network
file system.

After gem5 finishes compiling, you will have a gem5 binary with your new
protocol! If you want to build another protocol into gem5, you have to
change the `PROTOCOL` SCons variable. Thus, it is a good idea to use a
different build directory for each protocol, especially if you will be
comparing protocols.

When building your protocol, you will likely encounter errors in your
SLICC code reported by the SLICC compiler. Most errors include the file
and line number of the error. Sometimes, this line number is the line
*after* the error occurs. In fact, the line number can be far below the
actual error. For instance, if the curly brackets do not match
correctly, the error will report the last line in the file as the
location.

#### In the newer gem5 version (gem5 >= 23.1)

Most Kconfig defaults (found in `build_opts/`) specify the protocol as
`MI_example`, an example, but poor performing protocol. Therefore, we
cannot simply use a default build name (e.g., `X86` or `ARM`). We have
to specify the Kconfig options through `menuconfig`, `setconfig`, etc.
The command lines below will build our new protocol with the X86 ISA.

```sh
scons defconfig build/X86_MSI build_opts/X86
scons setconfig build/X86_MSI RUBY_PROTOCOL_MSI=y SLICC_HTML=y
scons build/X86_MSI/gem5.opt
```

This command will build `gem5.opt` in the directory `build/X86_MSI`. You
can specify *any* directory here. The first command tells SCons to create a
new build directory, and use the defaults in `build_opts/X86` to configure it.
The second command uses the `setconfig` kconfig tool use `RUBY_PROTOCOL_MSI=y`
to update the `PROTOCOL` and `SLICC_HTML` options in the `build/X86_MSI`
directory's configuration. You can also use other tools like `menuconfig` to
update these settings interactively. Finally, the last command tells SCons to
build in our build directory using this new configuration.

There is one more kconfig setting we're changing: `SLICC_HTML=y`. When
you specify this, SLICC will generate the HTML tables for your protocol.
You can find the HTML tables in `<build directory>/mem/protocol/html`. By
default, the SLICC compiler skips building the HTML tables because it impacts
the performance of compiling gem5, especially when compiling on a network
file system.

After gem5 finishes compiling, you will have a gem5 binary with your new
protocol! If you want to build another protocol into gem5, you have to
set the `RUBY_PROTOCOL_{NAME}=y` in setconfig step to change the `PROTOCOL`
kconfig variable. Thus, it is a good idea to use a different build directory
for each protocol, especially if you will be comparing protocols.

When building your protocol, you will likely encounter errors in your
SLICC code reported by the SLICC compiler. Most errors include the file
and line number of the error. Sometimes, this line number is the line
*after* the error occurs. In fact, the line number can be far below the
actual error. For instance, if the curly brackets do not match
correctly, the error will report the last line in the file as the
location.

For gem5 kconfig document, see
[here](https://www.gem5.org/documentation/general_docs/kconfig_build_system/)
