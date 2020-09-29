---
layout: documentation
title: gem5-20 Working Status of Benchmarks
doc: Working Status of Benchmarks
parent: benchmark_status
permalink: /documentation/benchmark_status/gem5-20
---

# gem5-20 Working Status of Benchmarks

* TOC
{:toc}

This page provides information on the working status of some benchmark suites with gem5-20.
The resources needed to run these benchmarks with gem5 can be found in [gem5-resources repository](https://gem5.googlesource.com/public/gem5-resources/) or [gem5 resources web page](https://www.gem5.org/documentation/general_docs/gem5_resources/).

# Boot Tests

The Linux Kernel boot tests rely on 5 LTS kernel releases (4.4.186, 4.9.186, 4.14.134, 4.19.83, and 5.4), four CPU models (kvmCPU, AtomicSimpleCPU, TimingSimpleCPU, O3CPU), three memory systems (classic, MI_Example, MESI_Two_Level) and two boot types (init, systemd).

Following is the description of the possible status of these runs:

**timeout:** experiment did not finish in a reasonable amount of time (12 hours: this time was chosen as we found similar successful cases did not exceed this limit on the same host machine).

**not-supported:** cases which are not yet supported in gem5.

**success:** cases where Linux booted successfully.

**sim-crash:** cases where gem5 crashed.

**kernel-panic:** cases where kernel went into panic during simulation.

<img src="/assets/img/status-plots/gem5-20/boot_classic_init.png" alt="Boot Tests Status with Classic Memory and init Boot" width="100%">
<img src="/assets/img/status-plots/gem5-20/boot_classic_systemd.png" alt="Boot Tests Status with Classic Memory and systemd Boot" width="100%">
<img src="/assets/img/status-plots/gem5-20/boot_MI_example_init.png" alt="Boot Tests Status with MI_Example Memory and init Boot" width="100%">
<img src="/assets/img/status-plots/gem5-20/boot_MI_example_systemd.png" alt="Boot Tests Status with MI_Example Memory and systemd Boot" width="100%">
<img src="/assets/img/status-plots/gem5-20/boot_MESI_Two_Level_init.png" alt="[Boot Tests Status with MESI_Two_Level Memory and init Boot" width="100%">
<img src="/assets/img/status-plots/gem5-20/boot_MESI_Two_Level_systemd.png" alt="Boot Tests Status with MESI_Two_Level Memory and systemd Boot" width="100%">

**Summary:** kvmCPU works in all cases.
AtomicSimpleCPU works fine with Classic memory system, but it is not supported with any Ruby protocols.
TimingSimpleCPU always work for a single CPU core in case of Classic memory system, but fails to complete the booting process in the alloted time for more than one CPU cores.
TimingSimpleCPU mostly works for any number of CPU cores for Ruby memory protocols except one case with MI_example and seven cases with MESI_Two_Level protocols, where gem5 crashes.
However, all of these crashes show an error that the cache controller's packet queue has grown beyond 100 packets.
It is expected that recompiling gem5 after changing the default packet queue size to a bigger value will lead these simulations to work fine.
For O3CPU, the Classic memory system is considered to not support more than one CPU core and with a single CPU core it works successfully in less than half of the cases and either shows kernel panic or simulation times out in the rest of the cases.
For Ruby memory protocols as well, O3CPU simulations do not work in all the cases (except one), but either times out or show kernel panic or crash.
The O3CPU (with Ruby) cases where simulations crash, the errors point to possible deadlocks or segmentation faults.

# NPB Tests

These NPB tests use KVM CPU (1,8,16,32, and 64 cores) and TimingSimple CPU (1 and 8 cores) with MESI_Two_Level memory system.

<img src="/assets/img/status-plots/gem5-20/npb_multicore_kvm.png" alt="NPB Status with KVM CPU" width="100%">

It is a known problem that if the number of simulated CPU cores increase, KVM simulations get stuck sometimes.
A work around is to use lower number of event queues than the CPU cores.
Although our scripts do that for more than 1 CPU core, the cases shown as `timeout` in the plot above
suffer from this problem of getting stuck.

<img src="/assets/img/status-plots/gem5-20/npb_multicore_timing.png" alt="NPB Status with TimingSimple CPU and MESI_Two_Level Memory System" width="100%">

There are three cases with TimingSimple CPU which did not finish in the alloted time.
There is no reason apparent in the generated results files (`simout`, `simerr`, `system.pc.com_1.device`).
Without further analysis, it is hard to tell if the simulation is stuck or is proceeding normally and just need more time to finish.

**Summary:** Most of the tested KVM and TimingSimple CPU simulations of NPB work successfully.
The rest of the cases could not result into success in the allocated simulation time (except one kernel panic case).

# PARSEC Tests

The PARSEC Experiments have been run with the following configurations:

* KVM CPU model: Ruby Memory System + MESI_Two_Level + [`simsmall`, `simlarge`, `native`] sizes + [`1`, `2`, `8`] cores.

* TimingSimple CPU model: Ruby System + MESI_Two_Level + [`simsmall`] size + [`1`, `2`] cores.

The result of experiments with gem5-20 is shown below:

<img src="/assets/img/status-plots/gem5-20/parsec_mesi_two_level_kvm.png" alt="PARSEC Status with KVM CPU" width="100%">
<img src="/assets/img/status-plots/gem5-20/parsec_mesi_two_level_timing.png" alt="PARSEC Status with TimingSimple CPU" width="100%">

The cases of unsuccessfull termination of simulation are shown below:

* Corrupted Input: When running experiments using `vips` workload, simulation does not start because the inputs to the workload are corrupted.
* Stack Smashing Detected: When running workload `x264` with TimingSimple CPU model, the simulation stops because a stack smashing attack is detected.

# SPEC 2006 Tests

The following plot represent the status of SPEC2006 workloads for different CPUs and data sizes with respect to gem5-20, linux kernel version 4.19.83 and gcc version 7.5.0.

<img src="/assets/img/status-plots/gem5-20/spec2006_gem5-20_status.png" alt="SPEC-2006 status for gem5-20" width="100%">

* **434.zeusmp** had crashed in gem5-19 and gem5-20 segmentation fault.
* **453.povray** needs a rerun and the test with gem5-19 was a success.

# SPEC 2017 Tests

The following plot represent the status of SPEC2017 workloads with respect to gem5-20, linux kernel version 4.19.83 and gcc version 7.5.0.

<img src="/assets/img/status-plots/gem5-20/spec2017_gem5-20_status.png" alt="SPEC-2017 status for gem5-20" width="100%">

* **600.perlbench_s** kernel panic while booting, couldn't find a reason.

# GAPBS Tests
The results of the GAPBS experiments with gem5-20 are shown below. For this experiment the input graphs for the workloads are synthetically generated.

<img src="/assets/img/status-plots/gem5-20/gapbs_kvm.png" alt="GAPBS status for gem5-20 kvm" width="100%">
<img src="/assets/img/status-plots/gem5-20/gapbs_atomic.png" alt="GAPBS status for gem5-20 atomic" width="100%">
<img src="/assets/img/status-plots/gem5-20/gapbs_simple.png" alt="GAPBS status for gem5-20 simple" width="100%">
<img src="/assets/img/status-plots/gem5-20/gapbs_o3.png" alt="GAPBS status for gem5-20 o3" width="100%">
