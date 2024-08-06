---
layout: page
title: Setting Up and Using KVM on your machine
permalink: /documentation/general_docs/using_kvm/
author: Mahyar Samani and Bobby R. Bruce
---

Kernel-based Virtual Machine (KVM) is a Linux kernel module allowing creating a virtual machine managed by the kernel.
On recent x86 and ARM processors, KVM supports hardware-assisted virtualization, enabling running the virtual machine at close to native speed.
gem5's `KVMCPU` enables this feature in gem5, with the trade-offs being architectual statistics are not being recorded by gem5.
Some statistics can be optionally gathered via `perf` when using `KVMCPU`, but this option requires `root` permission.

In order to use gem5's `KVMCPU` to fast-forward your simulation, you must have a KVM compatible processor and have KVM installed on your machine.
This page will guide you through the process of enabling KVM on your machine and using it with gem5.

Note: The following tutorial assumes an X86 Linux host machine.
Various parts of this tutorial may not be applicable to other architectures or different operating systems.
At present KVM support is available for X86 and ARM simulations (with respective X86 and ARM hosts).

## Ensuring system compatibility

In order to see if your processor supports hardware virtualization, run the following command:

```console
grep -E -c '(vmx|svm)' /proc/cpuinfo
```

If the command returns 0, your processor does not support hardware virtualization.
If the command returns 1 or more, your processor does support hardware virtualization

You may still have to ensure it is enabled in your bios.
The processes for doing so varies from depending on manufacturer and model.
Please consult your motherboard's manual for more information on this.

Finally, it is recommended that you use a 64-bit kernel on your host machine.
The limitations of using a 32-bit kernel on your host machine are as follows:

* You can only allocate 2GB of memory for your VMs
* You can only create 32-bit VMs.

This can severely limit the usefulness of KVM in for gem5 simulations.

## Enabling KVM

For KVM to function directly with gem5, the following dependencies must be installed:

```console
sudo apt-get install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils
```

Next, you need to add your user to the `kvm` and `libvirt` groups.
Run the two commands below:

```console
sudo adduser `id -un` libvirt
sudo adduser `id -un` kvm
```

After this, you need to leave then re-connect to your account.
If you are using SSH, disconnect all your session and login again.
Now if you run the `groups` command below you should see `kvm` and `libvirt`.

## Proving KVM is working

The "configs/example/gem5_library/x86-ubuntu-run.py" file is a gem5 configuration that will create a simulation which boots a Ubuntu 18.04 image using KVM.
It can be executed with the following:

```console
scons build/X86/gem5.opt -j`nproc`
./build/X86/gem5.opt configs/example/gem5_library/x86-ubuntu-run-with-kvm.py
```

If the simulation runs successfully, you have successfully installed KVM and can use it with gem5.

## `KVMCPU`, fast-forwarding, and `perf`

`perf` is a feature in Linux allowing users to access performance counters.
By default, `perf` is enabled by `KVMCPU` to collect statistics, such as the number of executed instructions.
Typically, `perf` requires some system privileges to setup.
Otherwise, you'll see related permission issues, such as `kernel.perf_event_paranoid` value is too high.

However, if you'd like to fast-forward the simulation and do not intent to collect the statistics of the fast-forwarded phase, you can choose not to use `perf` when using `KVMCPU`.
The `KVMCPU` SimObject has a parameter called `usePerf`, which specifies if the `KVMCPU` should collect statistics using `perf`.
This option is enabled by default.

The following is an example of turning `perf` off,
[https://github.com/gem5/gem5/blob/stable/configs/example/gem5\_library/x86-ubuntu-run-with-kvm-no-perf.py](https://github.com/gem5/gem5/blob/stable/configs/example/gem5_library/x86-ubuntu-run-with-kvm-no-perf.py).
