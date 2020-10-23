---
layout: documentation
title: ARM DVFS Support
doc: Learning gem5
parent: part2
permalink: /documentation/learning_gem5/part2/arm_dvfs_support/
author: Thomas E. Hansen
---

ARM DVFS modelling
==================

Like most modern CPUs, ARM CPUs support DVFS. It is possible to model this and,
for example, monitor the resulting power usage in gem5. DVFS modelling is done
through the use of two components of Clocked Objects: Voltage Domains and Clock
Domains. This chapter details the different components and shows different ways
to add them to an existing simulation.

Voltage Domains
---------------

Voltage Domains dictate the voltage values the CPUs can use. If no VD is
specified when running a Full System simulation in gem5, a default value of
1.0 Volts is used. This is to avoid forcing users to consider voltage when they
are not interested in simulating this.

Voltage Domains can be constructed from either a single value or a list of
values, passed to the `VoltageDomain` constructor using the `voltage` kwarg. If
a single value and multiple frequencies are specified, the voltage is used for
all the frequencies in the Clock Domain. If a list of voltage values is
specified, its number of entries must match the number of entries in the
corresponding Clock Domain and the entries must be arranged in _descending_
order. As with real hardware, a Voltage Domain applies to the entire processor
socket. This means that if you want to have different VDs for the different
processors (e.g. for a big.LITTLE setup) you need to make sure the big and the
LITTLE cluster are on different sockets (check the `socket_id` value associated
with the clusters).

There are 2 ways to add a VD to an existing CPU/simulation, one is more
flexible, the other is more straightforward. The first method adds command-line
flags to the provided `configs/example/arm/fs_bigLITTLE.py` file, while the
second method adds custom classes.

1. The most flexible way to add Voltage Domains to a simulation is to use
   command-line flags. To add a command-line flag, find the `addOptions`
   function in the file and add the flag there, optionally with some help
   text.  
   An example supporting both a single and multiple voltages:

   ```python
   def addOptions(parser):
       [...]
       parser.add_argument("--big-cpu-voltage", nargs="+", default="1.0V",
                           help="Big CPU voltage(s).")
       return parser
   ```

   The voltage domain value(s) could then be specified with

   ```
   --big-cpu-voltage <val1>V [<val2>V [<val3>V [...]]]
   ```

   This would then be accessed in the `build` function using
   `options.big_cpu_voltage`.  The `nargs="+"` ensures that at least one
   argument is required.
   Example usage in `build`:

   ```python
   def build(options):
       [...]
       # big cluster
       if options.big_cpus > 0:
           system.bigCluster = big_model(system, options.big_cpus,
                                         options.big_cpu_clock,
                                         options.big_cpu_voltage)
       [...]
   ```

   A similar flag and additions to the `build` function could be added to
   support specifying voltage values for the LITTLE CPU. This approach allows
   for very easy specification and modification of the voltages. The only
   downside to this method is that the multiple command line arguments, some
   being in list form, could clutter up the command used to invoke the
   simulator.

2. The less flexible way to specify Voltage Domains is by creating sub-classes
   of the `CpuCluster`. Similar to the existing `BigCluster` and
   `LittleCluster` sub-classes, these will extend the `CpuCluster` class.
   In the constructor of the subclass, in addition to specifying a CPU-type, we
   also define a lists of values for the Voltage Domain and pass this to the
   call to the `super` constructor using the kwarg `cpu_voltage`.
   Here is an example, for adding voltage to a `BigCluster`:

   ```python
   class VDBigCluster(devices.CpuCluster):
       def __init__(self, system, num_cpus, cpu_clock=None, cpu_voltage=None):
           # use the same CPU as the stock BigCluster
           abstract_cpu = ObjectList.cpu_list.get("O3_ARM_v7a_3")
           # voltage value(s)
           my_voltages = [ '1.0V', '0.75V', '0.51V']

           super(VDBigCluster, self).__init__(
               cpu_voltage=my_voltages,
               system=system,
               num_cpus=num_cpus,
               cpu_type=abstract_cpu,
               l1i_type=devices.L1I,
               l1d_type=devices.L1D,
               wcache_type=devices.WalkCache,
               l2_type=devices.L2
           )
   ```

   Adding voltages to the `LittleCluster` could then be done by defining a
   similar `VDLittleCluster` class.

   With the subclass(es) defined, we still need to add an entry to the
   `cpu_types` dictionary in the file, specifying a string name as the key and
   a pair of classes as the value, e.g:

   ```python
   cpu_types = {
       [...]
       "vd-timing" : (VDBigCluster, VDLittleCluster)
   }
   ```

   The CPUs with VDs could then be used by passing

   ```
   --cpu-type vd-timing
   ```

   to the command invoking the simulation.

   Since any modifications to the voltage values have to be done by finding the
   right subclass and modifying its code, or adding more subclasses and
   `cpu_types` entries, this approach is a lot less flexible than the
   flag-based approach.

Clock Domains
-------------

Voltage Domains are used in conjunction with Clock Domains. As previously
mentioned, if no custom voltage values have been specified, a default value of
1.0V is used for all values in the Clock Domain.

Types of Clock Domain
In contrast to Voltage Domains, there are 3 types of Clock Domains (from
`src/sim/clock_domain.hh`):

- `ClockDomain` -- provides a clock to a group of Clocked Objects bundled under
  the same Clock Domain. The CDs are in turn grouped into Voltage Domains. The
  CDs provide support for a hierarchical structure with "Source" and "Derived"
  Clock Domains.
- `SrcClockDomain` -- provides the notion of a CD that is connected to a
  tunable clock source. It maintains the clock period and provides the methods
  for setting/getting the clock, as well as the configuration parameters for
  the CD that a handler is going to manage. This includes frequency values at
  various performance levels, a Domain ID, and the current performance level.
  Note that a performance level as requested by the software corresponds to one
  of the frequency operation points the CD can operate at.
- `DerivedClockDomain` -- provides the notion of a CD that is connected to a
  parent CD which can either be a `SrcClockDomain` or a `DerivedClockDomain`.
  It maintains the clock divider and provides methods for getting the clock.

Adding Clock Domains to an existing simulation
----------------------------------------------

This example will use the same provided files as the VD examples, i.e.
`configs/example/arm/fs_bigLITTLE.py` and `configs/example/arm/devices.py`.

Like VDs, CDs can be a single value or a list of values. If a list of clock
speeds is given, the same rules apply as for a list of voltages given to a VD,
i.e. the number of values in the CD must match the number of values in the VD;
and the clock speeds must be given in _descending_ order. The provided files
come with support for specifying the clock as a single value (through the
`--{big,little}-cpu-clock` flags), but not as a list of values.
Extending/Modifying the behaviour of the provided flags is the simplest and
most flexible way to add support for multi-value CDs, but it is also possible
to do it by adding subclasses.

1. To add multi-value support to the existing `--{big,little}-cpu-clock` flags,
   locate the `addOptions` function in the
   `configs/example/arm/fs_bigLITTLE.py` file. Amongst the various
   `parser.add_argument` calls, find the ones that add the CPU-clock flags and
   replace the kwarg `type=str` with `nargs="+"`:
   ```python
   def addOptions(parser):
       [...]
       parser.add_argument("--big-cpu-clock", nargs="+", default="2GHz",
                           help="Big CPU clock frequency.")
       parser.add_argument("--little-cpu-clock", nargs="+", default="1GHz",
                           help="Little CPU clock frequency.")
       [...]
   ```
   With this, multiple frequencies can be specified similarly to the flag used
   for VDs:
   ```
   --{big,little}-cpu-clock <val1>GHz [<val2>MHz [<val3>MHz [...]]]
   ```

   Since this modifies existing flags, the flags' values are already wired up
   to the relevant constructors and kwargs in the `build` function, so there is
   nothing to be modified there.

2. To add CDs in a subclass, the process is very similar to the process of
   adding VDs as a subclass. The difference is that instead of specifying
   voltages and using the `cpu_voltage` kwarg, we specify clock values and use
   the `cpu_clock` kwarg in the `super` call:
   ```python
   class CDBigCluster(devices.CpuCluster):
       def __init__(self, system, num_cpus, cpu_clock=None, cpu_voltage=None):
           # use the same CPU as the stock BigCluster
           abstract_cpu = ObjectList.cpu_list.get("O3_ARM_v7a_3")
           # clock value(s)
           my_freqs = [ '1510MHz', '1000MHz', '667MHz']

           super(VDBigCluster, self).__init__(
               cpu_clock=my_freqs,
               system=system,
               num_cpus=num_cpus,
               cpu_type=abstract_cpu,
               l1i_type=devices.L1I,
               l1d_type=devices.L1D,
               wcache_type=devices.WalkCache,
               l2_type=devices.L2
           )
   ```
   This could be combined with the VD example so as to specify both VDs and CDs
   for the cluster.

   As with adding VDs using this approach, you would need to define a class for
   each of the CPU-types you wanted to use and specify their name-cpuPair value
   in the `cpu_types` dictionary. This method also has the same limitations and
   is a lot less flexible than the flag-based approach.

Making sure CDs have a valid DomainID
-------------------------------------

Regardless of which of the previous methods are used, there are some additional
modifications required. These concern the provided
`configs/example/arm/devices.py` file.

In the file, locate the `CpuClusters` class and find the place where
`self.clk_domain` is initialised to a `SrcClockDomain`. As noted in the comment
concerning `SrcClockDomain` above, these have a Domain ID. If this is not set,
as is the case in the provided setup, then the default ID of `-1` will be used.
Instead of this, change the code to make sure the Domain ID is set:

```python
[...]
self.clk_domain = SrcClockDomain(clock=cpu_clock,
                                 voltage_domain=self.voltage_domain,
                                 domain_id=system.numCpuClusters())
[...]
```

The `system.numCpuClusters()` is used here since the CD applies to the entire
cluster, i.e. it will be 0 for the first cluster, 1 for the second cluster,
etc.

If you don't set the Domain ID, you will get the following error when trying to
run a DVFS-capable simulation as some internal checks catch the default Domain
ID:

```
fatal: fatal condition domain_id == SrcClockDomain::emptyDomainID occurred:
DVFS: Controlled domain system.bigCluster.clk_domain needs to have a properly
assigned ID.
```

The DVFS Handler
----------------

If you specify VDs and CDs and then try to run your simulation, it will most
likely run, but you might notice the following warning in the output:

```
warn: Existing EnergyCtrl, but no enabled DVFSHandler found.
```

The VDs and CDs have been added, but there is no `DVFSHandler` which the system
can interface with to adjust the values. The simplest way to fix this is to add
another command-line flag, in the `configs/example/arm/fs_bigLITTLE.py` file.

As in the VD and CD examples, locate the `addOptions` function and append the
following code to it:

```python
def addOptions(parser):
    [...]
    parser.add_argument("--dvfs", action="store_true",
                        help="Enable the DVFS Handler.")
    return parser
```

Then, locate the `build` function and append this code to it:

```python
def build(options):
    [...]
    if options.dvfs:
        system.dvfs_handler.domains = [system.bigCluster.clk_domain,
                                       system.littleCluster.clk_domain]
        system.dvfs_handler.enable = options.dvfs

    return root
```

With this in place, you should now be able to run a DVFS-capable simulation by
using the `--dvfs` flag when invoking the simulation, with the option to
specify the voltage and frequency operating points of both the big and the
LITTLE cluster as necessary.

