---
layout: page
title: Setting Up and Using KVM on your machine
permalink: /documentation/general_docs/using_kvm/
author: Mahyar Samani and Bobby R. Bruce
---

In order to use gem5's `KVMCPU` to fast-forward your simulation, you must have a KVM compatible processor and have KVM installed on your machine.
This page will guide you through the process of enabling KVM on your machine and using it with gem5.

Note: The following tutorial assumes an X86 Linux host machine.
Various parts of this tutorial may not be applicable to other architectures or different operating systems.
At present KVM support is only available for X86 and ARM simulations (with respective X86 and ARM hosts).

## Ensuring system compatibility

In order to see if your processor supports hardware virtualization, run the following command:

```console
egrep -c '(vmx|svm)' /proc/cpuinfo
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

## Enablinbg KVM

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
./build/X86/gem5.opt configs/example/gem5_library/x86-ubuntu-run.py
```

If the simulation runs successfully, you have successfully installed KVM and can use it with gem5.
