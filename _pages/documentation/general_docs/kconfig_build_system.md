---
layout: documentation
title: Kconfig Build System
doc: gem5 documentation
parent: kconfig_build_system
permalink: /documentation/general_docs/kconfig_build_system/
---

This guide is intended for advanced users who need to build gem5 (>=23.1) with
multiple ISAs or customize the build options, such as the Ruby memory protocol.
Familiarity with the Kconfig system is required.

## Build gem5 with the Kconfig Build System

```bash
scons [OPTIONS] Kconfig_command TARGET
```

Supported Kconfig commands include:

- `defconfig`
- `setconfig`
- `menuconfig`
- `guiconfig`
- `listnewconfig`
- `oldconfig`
- `olddefconfig`
- `savedefconfig`

The most common options are `defconfig`, `setconfig` and `menuconfig`.
Use can use `scons --help` to list these commands with additional information.

To build gem5 with Kconfig, there are now two steps.
The first is the initial configuration, which sets up a build directory with
the desired configuration. The second is building the target.
this is done with the `defconfig` command.
For example:

```bash
scons defconfig gem5_build build_opts/ALL
```

This will create a configuration in  `gem5_build` build directory based on
that specified in`build_opts/ALL`. The exact path of this configuration is
stored in `gem5_build/gem5.build/config`.

The second step is to build the target in the configured build directory.
This is done with `scons` as usual.
For example:


```bash
scons -j$(nproc) gem5_build/gem5.opt
```

Note: In order to maintain backward compatibility with the old build scheme,
users need to avoid using the "build" directory for Kconfig builds.

To build gem5 Kconfig with customized Kconfig options, an additional step
is required between **initial configuration** and **building the target**.

This step is to set up the Kconfig options in the configured build directory.
There are two ways to set up the Kconfig options.
The first is to directly set the Kconfig options in the command line with the
`setconfig` command. For example:

```bash
scons setconfig gem5_build USE_KVM=y
```

This will set the `USE_KVM` option to `y` in the configuration, thus enabling
KVM support.

The second way is to use the `menuconfig` command to open the menuconfig
editor.
The menuconfig editor allows you to view and edit config values and view help.
For example:

```bash

```bash
scons menuconfig gem5_build
```

## Details of Kconfig Commands

### defconfig

The `defconfig` command sets up a config using values specified in a defconfig file, or if no value is
given, uses the default values. The second argument specifies the defconfig file. All
default gem5 defconfig files are located in the build_opts directory. Users
can also use their own defconfig files.

For example:

```bash
scons defconfig gem5_build build_opts/RISCV
```

To use your own defconfig file:

```bash
scons defconfig gem5_build $HOME/foo/bar/myconfig
```

### setconfig

The `setconfig` command sets values in an existing config directory as specified on the command line.

The users or developers can get the Kconfig options via `menuconfig` or
`guiconfig`.

For example, to enable gem5 is built in systemc kernel:

```bash
scons setconfig gem5_build USE_SYSTEMC=y
```

### menuconfig

The `menuconfig` command opens the menuconfig editor.
This editor allows you to view and edit config values
and view help text. `menuconfig` runs in the CLI.

```bash
scons menuconfig gem5_build
```

If is successful, the CLI will look like this:

![](/assets/img/kconfig/menuconfig.png)

The user can use the arrow keys to navigate the menu, and the enter key to
select a menu item. The user can also use the space bar to select or deselect
an option. The user can also use the search function to find a specific
option. The user can also use the `?` key to view help text for a specific
option.
Below is a screenshot of the help text for the `USE_ARM_ISA` option:

![](/assets/img/kconfig/menuconfig_details.png)

If the `gem5_build` directory does not exist, SCons will set up a build
directory at the path `gem5_build` with default options and then invoke
menuconfig so you can set up its configuration.

### guiconfig

The `guiconfig` command opens the guiconfig editor.
This editor will let you view and edit config values,
and view help text. guiconfig runs as a graphical application. The command
requires `python3-tk` package be installed in the system.

```bash
scons guiconfig gem5_build
```

If is successful, it will create new windows to show up like:

![](/assets/img/kconfig/guiconfig.png)


### savedefconfig

Te=he `savedefconfig` command saves the current configuration to a defconfig.
You can use menuconfig to set up a
configuration with the options you care about, and then use `savedefconfig` to
create a minimal configuration file. These files are suitable for use in the
build_opts directory. The second argument specifies the filename for the new
defconfig file.

A saved defconfig is a good way to see what
options have been set to something interesting, and an easier way to
pass a config to someone else to use, to put in bug reports, etc.

```bash
scons savedefconfig gem5_build new_def_config
```

### listnewconfig

The `listnewconfig` command lists which option settings are new in the Kconfig and which are not currently
set in the existing config file.

```bash
scons listnewconfig gem5_build
```

### oldconfig

The `oldconfig` command updates the existing config setting new values for the desired options. This is
similar to `olddefconfig` except it asks what values you want
for the new settings.

```bash
scons oldconfig gem5_build
```

### oldsaveconfig

The `oldsaveconfig` command updates an existing config by setting new values for the desired options. This is
similar to the `oldconfig` option, except it uses the default for any new
setting.

```bash
scons oldsaveconfig gem5_build
```

Users can get help by running `scons -h` to get details of Kconfig commands.

## Report a Bug

If an issue is encountered we recommend you report the issue by saving the
configuration used and distributing it.
To do so, the `savedefconfig` command can be used:

```bash
scons savedefconfig gem5_build new_config
```

Alternatively, the configuration can be found in the
`gem5_build/gem5.build/config` file.


# Reference

1. Kconfig website: https://www.kernel.org/doc/html/next/kbuild/kconfig-language.html
