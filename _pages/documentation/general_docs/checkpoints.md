---
layout: documentation
title: Checkpoints
doc: gem5 documentation
parent: checkpoints
permalink: /documentation/general_docs/checkpoints/
---

# Checkpoints #
Checkpoints are essentially snapshops of a simulation. You would want to use a checkpoint when your simulation takes an extremely long time (which is almost always the case) so you can resume from that checkpoint at a later time with the DerivO3CPU.
## Creation ##
First of all, you need to create a checkpoint. Each checkpoint as saved in a new directory named 'cpt.TICKNUMBER', where TICKNUMBER refers to the tick value at which this checkpoint was created. There are several ways in which a checkpoint can be created: 
* After booting the gem5 simulator, execute the command m5 checkpoint. One can execute the command manually using m5term, or include it in a run script to do this automatically after the Linux kernel has booted up.
* There is a pseudo instruction that can be used for creating checkpoints. For example, one may include this pseduo instruction in an application program, so that the checkpoint is created when the application has reached a certain state.
* The option **-****-take-checkpoints** can be provided to the python scripts (fs.py, ruby_fs.py) so that checkpoints are dumped periodically. The option **-****-checkpoint-at-end** can be used for creating the checkpoint at the end of the simulation. Take a look at the file **configs/common/Options.py** for these options.

While creating checkpoints with Ruby memory model, it is necessary to use the MOESI hammer protocol. This is because checkpointing the correct memory state requires that the caches are flushed to the memory. This flushing operation is currently supported only with the MOESI hammer protocol.

## Restoring ##
Restoring from a checkpoint can usually be easily done from the command line, e.g.:

```
  build/<ISA>/gem5.debug configs/example/fs.py -r N
  OR
  build/<ISA>/gem5.debug configs/example/fs.py --checkpoint-restore=N
```

The number N is integer that represents checkpoint number which usually starts from 1 then increases incrementally to 2,3,4...

By default, gem5 assumes that the checkpoint is to be restored using Atomic CPUs. This may not work if the checkpoint was recorded using Timing / Detailed / Inorder CPU. One can mention the option <br /> **-****-restore-with-cpu \<CPU Type\>** on the command line. The cpu type supplied with this option is then used for restoring from the checkpoint.

## Detailed example: Parsec ##
In the following section we would describe how checkpoints are created for workloads PARSEC benchmark suite. However similar procedure can be followed to create checkpoint for other workloads beyond PARSEC suite. Following are the high level steps of creating checkpoint:

1. Annotate each workload with start and end of Region of Interest and with start and end of work units in the program.
2. Take a checkpoint at the start of the Region of Interest.
3. Simulate the whole program in the Region of Interest and periodically take checkpoints.
4. Analyse the statistics corresponding to periodic checkpoints and select the most interesting section of the program execution.
5. Take warm up cache trace for Ruby before reaching most interesting portion of the program and take the final checkpoint.
In each of the following sections we explain each of the above steps in more details.

### Annotating workloads ###
Annotation is required for two purposes: for defining region of program beyond the initialization section of a program and for defining logical units of work in each of the workloads.

Workloads in PARSEC benchmark suite, already has annotating demarcating start and end of portion of program without program initialization section and program finalization section. We just use gem5 specific annotation for start of Region of Interest. The start of the Region of Interest (ROI) is marked by **m5_roi_begin()** and the end of ROI is demarcated by **m5_roi_end()**.

Due to large simulation time its not always possible to simulate whole program. Moreover, unlike single threaded programs, simulating for a given number instructions in multi-threaded workloads is not a correct way to simulate portion of a program due to possible presence of instructions spinning on synchronization variable. Thus it is important define semantically meaningful logical units of work in each workload. Simulating for a given number of workuints in a multi-threaded workloads gives a reasonable way of simulating portion of workloads as the problem of instructions spinning on synchronization variables.

# Switchover/Fastforwarding
## Sampling
Sampling (switching between functional and detailed models) can be implemented via your Python script. In your script you can direct the simulator to switch between two sets of CPUs. To do this, in your script setup a list of tuples of (oldCPU, newCPU). If there are multiple CPUs you wish to switch simultaneously, they can all be added to that list. For example:
```python
run_cpu1 = SimpleCPU()
switch_cpu1 = DetailedCPU(switched_out=True)
run_cpu2 = SimpleCPU()
switch_cpu2 = FooCPU(switched_out=True)
switch_cpu_list = [(run_cpu1,switch_cpu1),(run_cpu2,switch_cpu2)]
```
Note that the CPU that does not immediately run should have the parameter "switched_out=True". This keeps those CPUs from adding themselves to the list of CPUs to run; they will instead get added when you switch them in.

In order for gem5 to instantiate all of your CPUs, you must make the CPUs that will be switched in a child of something that is in the configuration hierarchy. Unfortunately at the moment some configuration limitations force the switch CPU to be placed outside of the System object. The Root object is the next most convenient place to place the CPU, as shown below:
```python
m5.simulate(500)  # simulate for 500 cycles
m5.switchCpus(switch_cpu_list)
m5.simulate(500)  # simulate another 500 cycles after switching
```
Note that gem5 may have to simulate for a few cycles prior to switching CPUs due to any outstanding state that may be present in the CPUs being switched out.
