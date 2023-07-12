---
layout: documentation
title: Kconfig Build System
doc: gem5 documentation
parent: kconfig_build_system
permalink: /documentation/general_docs/kconfig_build_system/
---

This guide is intended for advanced users who need to build gem5(>= 23.1) with
multiple ISAs or customize the build options, such as the Ruby memory protocol.
Familiarity with the Kconfig system is required.

## Build GEM5 with Kconfig Build System

```bash
scons [OPTIONS] Kconfig_command TARGET
```

Supported Kconfig commands include

- defconfig
- setconfig
- menuconfig
- guiconfig
- listnewconfig
- oldconfig
- olddefconfig
- savedefconfig

The most common uses of options are `defconfig`, `setconfig` and `menuconfig`.

Use `scons --help` to list these commands, and for additional information.

To build gem5 with Kconfig, there are now two steps.

Initial configuration

```bash
scons defconfig gem5_build build_opts/ALL
```

This will create a configuration for the `gem5_build` build directory based on
`build_opts/ALL`. The configuration is stored in the
`gem5_build/gem5.build/config`.

To build a target in a configured build directory, run a scons command similar
to the one used before.

```bash
scons -j$(nproc) gem5_build/gem5.opt
```

Note: In order to maintain backward compatibility with the old build scheme,
users need to avoid using the "build" directory for Kconfig builds.

To build gem5 Kconfig with customized Kconfig options, an additional step
is required between **initial configuration** and **building the target**

- Directly set Kconfig options

```bash
scons setconfig gem5_build USE_KVM=y
```

- set Kconfig options by `menuconfig`

```bash
scons menuconfig gem5_build
```

## Details of Kconfig Commands

### defconfig

Set up a config using values specified in a defconfig file, or if no value is
given, use the default. The second argument specifies the defconfig file. All
default gem5 defconfig files are located in the build_opts directory. Users
can also use their own defconfig files.

```bash
scons defconfig gem5_build build_opts/RISCV
```

Use the own defconfig file

```bash
scons defconfig gem5_build $HOME/foo/bar/myconfig
```

### setconfig

Set values in an existing config directory as specified on the command line.

The users or developers can get the Kconfig options via `menuconfig` or
`guiconfig`

For example, to enable gem5's built in systemc kernel:

```bash
scons setconfig gem5_build USE_SYSTEMC=y
```

### menuconfig

Opens the menuconfig editor, which allows you to view and edit config values
and view help text. menuconfig runs in CLI.

```bash
scons menuconfig gem5_build
```

If is successful, the CLI will look like this

![](/assets/img/kconfig/menuconfig.png)

To view help text, for example, USE_ARM_ISA, will look like this

![](/assets/img/kconfig/menuconfig_details.png)

If the `gem5_build` directory does not exist, SCons will set up a build
directory at the path `gem5_build` with default options and then invoke
menuconfig so you can set up its configuration.

### guiconfig

Opens the guiconfig editor which will let you view and edit config values,
and view help text. guiconfig runs as a graphical application. The command
requires `python3-tk` package be installed in the system.

```bash
scons guiconfig gem5_build
```

If is successful, it will create new windows to show up like

![](/assets/img/kconfig/guiconfig.png)

Open guiconfig in Ubuntu 22.04 with python3-tk

### savedefconfig

This helper utility allows you to save the defconfig that corresponds to a
given configuration. For instance, you can use menuconfig to set up a
configuration with the options you care about, and then use savedefconfig to
create a minimal configuration file. These files are suitable for use in the
build_opts directory. The second argument specifies the filename for the new
defconfig file.

A saved defconfig like that can also be a good way to visually see what
options have been set to something interesting, and an easier way to
pass a config to someone else to use, to put in bug reports, etc.

```bash
scons savedefconfig gem5_build new_def_config
```

### listnewconfig

Lists config options which are new in the Kconfig and which are not currently
set in the existing config file.

```bash
scons listnewconfig gem5_build
```

### oldconfig

Update an existing config by adding settings for new options. This is
the same as the olddefconfig tool, except it asks what values you want
for the new settings.

```bash
scons oldconfig gem5_build
```

### oldsaveconfig

Update an existing config by adding settings for new options. This is
the same as the oldconfig tool, except it uses the default for any new
setting.

```bash
scons oldsaveconfig gem5_build
```

Users can get help by running `scons -h` to get details of Kconfig commands.

# Report the Bug

If the user encounter the issue in build or run gem5, he/she should report the
issue with `config` file so that anyone can reproduce it.

To get the `config` file, the user can either

by `savedefconfig`
```
scons savedefconfig gem5_build new_config
```

or by copy then in `<builddir>/gem5.config/config`

```
cp <builddir>/gem5.config/config new_config
```

# Reference

1. Kconfig website: https://www.kernel.org/doc/html/next/kbuild/kconfig-language.html
