---
layout: post
title: “Moving to full system simulation of GPU applications”
author: Matthew Poremba
date:   2023-02-13
---

For over a decade gem5 has supported two modes of simulation: full system (FS) mode where the simulator uses a disk image and a kernel to boot an instance of Linux and run applications on the disk image and System-emulation (SE) mode where the simulator runs applications on the host machine and intercepts system calls and provides emulation for them.
Up until a few years ago, binaries run in SE mode were required to be statically linked to be run.
Dynamically linked binaries can now be run assuming the dynamic libraries are available on the host machine.
For increasingly more complicated and specialized applications, such as GPU applications, the dynamic libraries may not be available on the host system or may be a different version than what is needed for the simulated application.
In these cases, using FS mode is preferred.

This issue of unavailable or different version libraries also occurs with the GPU model in gem5.
The GPU model currently runs in SE mode and requires an older version of [AMD’s ROCm™ stack](https://www.amd.com/en/graphics/servers-solutions-rocm).
This is problematic for a few reasons: (1) the user may not have a GPU and therefore does not need the ROCm™ stack installed locally (2) the user may not be on a system compatible with the ROCm™ installer to install the libraries or (3) the user has ROCm™ installed but does not have the specific version required for gem5.
These issues are currently solved by running building and running gem5 using a docker image.
This is not necessary when using FS mode, making GPUFS easier to run along with regular simulation.

Over the past two years, work has been being done to implement a simulated GPU device with all of the necessary components to communicate with the upstream GPU driver.
With this work in place, it is now possible to use FS mode to simulate GPU applications.
With the 22.1 release of gem5, we are announcing GPU FS mode (GPUFS) as the preferred method to simulate GPU applications and will eventually replace SE mode entirely.
Based on our most recent testing, nearly all applications which worked in SE mode will work in FS mode.
The remainder of this blog post discusses the use cases of FS mode along with additional benefits and known issues.

# Use cases
The use cases for GPUFS are the same as SE mode GPU simulation.
That is, we simulate a single GPU application, collect stats, and exit the simulation.
Although GPUFS in theory provides the ability to do more advanced simulations such as simulating concurrent GPU applications or simulating multiple GPU devices, these are *not* supported in the current model.


# Benefits of Full System
The primary benefit of GPUFS is avoiding issues with dynamic libraries.
Currently SE mode GPU simulations need to be run within a docker image.
This itself has many user facing complexities, such as environments (e.g., universities) which do not allow docker to be run and potentially different build directories for GPU simulation and non-GPU simulation, and many developer complexities including testing and keeping up with download locations of older out-of-date libraries.

With a simulated GPU device users will be able to fast-forward through memory copies in GPU applications.
A basic GPU application has three main GPU-related library calls: (1) copy data to the GPU, (2) launch a kernel on the GPU, and (3) copy data to the host.
On a real system data can be copied using a GPU kernel which reads from host memory and writes to device memory or by using the help of a DMA engine.
With GPUFS, system DMA engines are implemented to copy data to/from GPU memory.
These engines can be simulated functionally within gem5 to speed up simulation.
As a result, users can copy several GBs of data to GPU memory in minutes of simulation time by avoiding the detailed simulation of copy kernels.

GPUFS also more easily allows users and developers to update the ROCm™ stack to the latest version with each gem5 release.
This allows users to be able to use features of the latest ROCm™ stack which can mean less time spent backporting applications to older ROCm™ versions.
GPUFS has currently been tested on ROCm 4.2, 4.3, 5.0, and 5.4 but any version above 4.0 should work.
This testing was done on the core ROCm package only, so 1st party libraries (rocBLAS, rocFFT, rocSPARSE, etc.) have not been thoroughly tested.

Full system mode uses the full ROCm stack, including the kernel driver, rather than using the emulated driver developed for SE mode.
This means users can modify the Linux kernel driver to research areas that are difficult to do in SE mode.
Examples include virtual memory research such as utilizing flexible page sizes and exploring page fault handling, implementing new packet types for the new SDMA and PM4 processors, or using virtualization features.

# Using full system
Like FS mode in general, users need a disk image and a kernel to run GPUFS.
A packer script is provided in the gem5-resources repository under `src/gpu-fs/disk-image`.
Additionally, the kernel is available for download or can be transferred out of the disk image.
This disk image and kernel consist of an operating system and kernel version compatible with the official ROCm™ release notes.
A prebuilt [GPUFS disk image](http://dist.gem5.org/dist/v22-1/images/x86/ubuntu-18-04/x86-gpu-fs-20220512.img.gz) and [GPUFS kernel](http://dist.gem5.org/dist/v22-1/kernels/x86/static/vmlinux-5.4.0-105-generic) are available for download.

Scripts are provided for the user which can take a GPU application as an argument and copy it into the disk image upon simulation start to run a GPU application without needing to modify or mount the disk image.
The traditional “rcS” script approach can also be used to run applications which exist on the binary already, applications which may need further input files, or applications the user wishes to build from source files in the disk image.
Applications can be built using a docker image provided at gcr.io/gem5-test/gpu-fs:v22-1 or building a local docker image using `util/dockerfiles/gpu-fs/` in the gem5 repository.
Using this docker allows users to build GPU applications without needing to install ROCm™ on their host machine and without wasting simulation time building source files on the disk image.
If desired, users may also install the required ROCm™ version locally, even without an AMD GPU, and build applications on their host machine.

More information on how to setup GPUFS is provided in the README.md file in the gem5-resources repository at `src/gpu-fs/README.md`.

# Known issues
There are some known issues that are actively being addressed which will not be completed until a future release after gem5 22.1.
These issues are below.
If you are using GPUFS and run into an issue that is not listed here, we encourage you to report the issue to gem5-users, JIRA, or the gem5 slack channel.
A useful bug report will include both terminal output and gem5 output preferably with the following debug flags: `--debug-flags=AMDGPUDevice,SDMAEngine,PM4PacketProcessor,HSAPacketProcessor,GPUCommandProc`.

* Currently KVM and X86 are required to run full system.  Atomic and Timing CPUs are not yet compatible with the disconnected Ruby network required for GPUFS and is a work in progress.
* Some memory accesses generate incorrect addresses causing hard page faults leading to simulation panics.  This is currently being investigated with high priority.
* The `printf` function does not work within GPU kernels.  As a workaround, a gem5-specific print function is being developed.

# Recap
Full system GPU simulation (GPUFS) is now the preferred method to run GPU applications in gem5 22.1+.
GPUFS is intended to be used for the same use cases are SE mode GPU simulation.
It has the benefits of avoiding simulation within docker, improved simulation speed by functionally simulating memory copies, and an easier update path for gem5 developers.

As users move to GPUFS, we expect there will be some bug reports.
Users are encouraged to submit reports to the gem5-users mailing list, JIRA, or gem5 slack channel.
