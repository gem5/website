---
layout: documentation
title: Full System AMD GPU model
doc: gem5 documentation
parent: gpu_models
permalink: /documentation/general_docs/gpu_models/gpufs
---

# **Full System AMD GPU model**

The Full System AMD GPU model simulates a GPU at the "gfx9" ISA level, as opposed to the intermediate language level. This page will give you a general overview of how to use this model, the software stack the model uses, and provide resources that detail the model and how it is implemented. **It is recommended to use Full System instead of System Emulation as Full System supports the latest versions of the GPU software stack.**

## Requirements

The Full System GPU model is primarily designed to simulate discrete GPUs using a native software stack without modification. This means that the CPU portion of simulation is not configured for detailed simulation -- only the GPU is detailed. The [ROCm software stack](https://rocm.docs.amd.com/en/latest/) limits usage to officially supported gfx9 devices listed in the [ROCm documentation](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html). Currently gem5 provides configurations for Vega10 (gfx900), MI210/MI250X (gfx90a), and MI300X (gfx942).

*Note:* Previously supported "gfx9" devices in older versions of ROCm still work in most cases (gfx900, gfx906). As mentioned in the ROCm documentation, these may result in runtime errors for prebuilt ROCm libraries.

The CPU portion of code is ideally fast-forwarded using the KVM CPU model. Since the software stack is x86 you will need an x86 Linux host with KVM enabled to run Full System efficiently. The atomic CPU can also be used to run on non-x86 hosts or where KVM is not usable. See the [Running without KVM](#Running-without-kvm) section for details.

## **Using the model**

Several places in this guide assume that gem5 and gem5-resources are located in the same base directory.

The [gem5 repository](https://github.com/gem5/gem5) contains the base code of the GPU model.
The [gem5-resources repository](https://github.com/gem5/gem5-resources/) contains files needed to create a disk image for Full System and comes with a number of sample applications that can be used to get started with the model. We recommend users start with [square](https://resources.gem5.org/resources/square), as it is a simple, heavily tested application that should run relatively quickly.

#### Building gem5

The GPU model requires the GPU_VIPER cache coherence protocol which is implemented in Ruby and the Full System software stack is only supported in a simulated X86 environment. The VEGA_X86 build option uses the GPU_VIPER protocol and x86. Therefore, gem5 must be built using the VEGA_X86 build option:

```
scons build/VEGA_X86/gem5.opt
```

The Full System GPU model is built similarly to a CPU only version of gem5. Refer to the [building gem5](https://www.gem5.org/documentation/general_docs/building) documentation for how to build gem5, including number of build threads, linker options, and gem5 binary targets.

#### Building Disk Image and Kernel

Just like a CPU only version of gem5, the Full System GPU model requires a disk image and kernel to run. The [gem5-resources repository](https://github.com/gem5/gem5-resources/) provides a one-step disk image builder to create a disk image for the GPU model with all of the software requirements installed.

From your base directory with gem5 and gem5-resources cloned, navigate to [gem5-resources/src/x86-ubuntu-gpu-ml](https://github.com/gem5/gem5-resources/tree/stable/src/x86-ubuntu-gpu-ml). This directory contains a file `./build.sh` to create the disk image in one step. Building the disk depends on the [packer](https://www.packer.io/) tool which uses [QEMU](https://www.qemu.org/) as a backend. See the [BUILDING.md](https://github.com/gem5/gem5-resources/blob/stable/src/x86-ubuntu-gpu-ml/BUILDING.md) guide for troubleshooting. Generally, the disk image can be created in one step using the following command:

```
./build.sh
```

This process takes approximately 15-20 minutes and is mostly bound by download speed as a majority of the time is spent downloading Ubuntu packages.

Building the disk image will also extract the Linux kernel. The extracted Linux kernel *must* be used with the disk image. In other words, you cannot input an arbitrary kernel to gem5 otherwise the GPU driver may not load successfully.

After this process your environment should contain:
* Disk image: `gem5-resources/src/x86-ubuntu-gpu-ml/disk-image/x86-ubuntu-gpu-ml`
* Kernel: `gem5-resources/src/x86-ubuntu-gpu-ml/vmlinux-gpu-ml`

#### Building GPU applications

The GPU model is designed to run unmodified GPU binaries. If you have an application which runs on AMD GPU hardware and that hardware is supported in gem5, you can run the same binary in gem5. Note that as this is simulation, the application will need to be scaled down to a reasonable size to simulate in a realistic amount of time.

Building applications for the GPU model is similar to [cross compiling](https://www.gem5.org/documentation/general_docs/compiling_workloads/) when the simulated ISA does not match the host. Either you must have the development tools installed locally or containerization like Docker can be used. Docker images to build GPU applications are provided with gem5 in [util/dockerfiles/gpu-fs](https://github.com/gem5/gem5/tree/stable/util/dockerfiles/gpu-fs). You may either build this image or use the gem5 provided image at `ghcr.io/gem5/gpu-fs`. This docker image provides a specific version of ROCm. The ROCm version in the Dockerfile must match the ROCm version on the disk image being used to simulate gem5. The docker and disk image versions are synced upon gem5 releases. The instructions below show an example using the pre-built gem5 docker on GitHub container registry (ghcr.io).

[Square](https://github.com/gem5/gem5-resources/tree/stable/src/gpu/square) is a simple application provided in gem5-resources which can be used to get started with the model. Generally, the `src/gpu` directory of gem5-resources contains a `Makefile.default` which is used to build a native application and `Makefile.gpufs` which contains application annotated with [m5ops](https://www.gem5.org/documentation/general_docs/m5ops/) that will only run within gem5.

To build square using the gem5 provided docker image, navigate to the square directory and use the `Makefile.default` Makefile:

```
cd gem5-resources/src/gpu/square
docker run --rm -u $UID:$GID -v $PWD:$PWD -w $PWD ghcr.io/gem5/gpu-fs make -f Makefile.default
```

The square binary should then be located at `gem5-resources/src/gpu/square/bin.default/square.default`

#### Testing GPU application

The GPU model provides multiple gfx9 configurations to simulate GPU applications. The configurations specify the ISA (e.g., gfx942, gfx90a) and generally a minimally sized device. *They are not intended to be indicative of real hardware measurements*. In the gem5 repository, these are:
* MI300X: `configs/example/gpufs/mi300.py`
* MI210 / MI250: `configs/example/gpufs/mi200.py`

The GPU model uses config script based configuration (i.e., not [standard library](https://www.gem5.org/documentation/gem5-stdlib/overview)) which uses command line arguments as the primary way to modify simulation parameters. However, most common configuration options are set by the top-level scripts (e.g., `configs/example/gpufs/mi300.py`). The main required arguments are disk image, kernel, and application.

Using the disk image and kernel created above and the square binary built above, square can be run with the following command:

```
build/VEGA_X86/gem5.opt configs/example/gpufs/mi300.py --disk-image gem5-resources/src/x86-ubuntu-gpu-ml/disk-image/x86-ubuntu-gpu-ml --kernel gem5-resources/src/x86-ubuntu-gpu-ml/vmlinux-gpu-ml --app gem5-resources/src/gpu/square/bin.default/square.default
```

In Full System the output of the simulator and the output of the simulated system are shown in two separate locations. By default, the gem5 output prints to the terminal where gem5 is run. The simulated terminal output is located in the gem5 output directory which is `m5out` by default.

Once gem5 completes (or while running) the output of the Full System simulation can be seen in `m5out/system.pc.com_1.device`. For the square example, the application will print "PASSED!" to the simulated terminal output upon successful completion.

#### Using Python or shell scripts

Python scripts such as PyTorch, TensorFlow, etc. and shell scripts can be passed directly as the value of the `--app` command line. For example, the following minimal PyTorch application can be run directly when saved as `pytorch_test.py`:

```
#!/usr/bin/env python3

import torch

x = torch.rand(5, 3).to('cuda')
y = torch.rand(3, 5).to('cuda')

z = x @ y
```

For example:

```
build/VEGA_X86/gem5.opt configs/example/gpufs/mi300.py --disk-image gem5-resources/src/x86-ubuntu-gpu-ml/disk-image/x86-ubuntu-gpu-ml --kernel gem5-resources/src/x86-ubuntu-gpu-ml/vmlinux-gpu-ml --app ./pytorch_test.py
```

#### Input files

The GPU model configuration files are designed to copy the file provided to the `--app` option into the simulator. **Full System gem5 cannot read files from your host system!** If your application requires input files, they must be copied into the disk image. See instructions for [extending the disk image](https://github.com/gem5/gem5-resources/blob/stable/src/x86-ubuntu-gpu-ml/BUILDING.md) for ways to do this.

If your application requires input files, it is recommended to create a shell script and pass the shell script to the `--app` option. The shell script should be written with paths relative to the disk image paths as it will run within gem5. For example, if your application requires `foo.dat`, create a shell script such as:

```
#!/bin/bash

# We have previously copied foo.dat to /data outside of simulation.
cd /data
my_gpu_app -i foo.dat
```

## Advanced Usage

#### Running without KVM

The AtomicSimpleCPU can also be used in situations where the host is not x86 or KVM is not available. To enable the Atomic CPU, you will need to modify your config (e.g., `configs/example/gpufs/mi300.py`) and replace `args.cpu_type = "X86KvmCPU"` with `args.cpu_type = "AtomicSimpleCPU"`.

Note that this will slow down the CPU portion of your simulation potentially by 100x. It is possible to speed this up using [checkpoints](https://www.gem5.org/documentation/general_docs/checkpoints/).

#### Checkpoints

The config scripts provided allow for checkpointing after Linux boots out of the box. It is recommended to use this when using the atomic CPU. To create a checkpoint after boot, simply add a `--checkpoint-dir` to the command line with a directory to place the checkpoint. For example:

```
build/VEGA_X86/gem5.opt configs/example/gpufs/mi300.py --disk-image gem5-resources/src/x86-ubuntu-gpu-ml/disk-image/x86-ubuntu-gpu-ml --kernel gem5-resources/src/x86-ubuntu-gpu-ml/vmlinux-gpu-ml --app gem5-resources/src/gpu/square/bin.default/square.default --checkpoint-dir square-cpt
```

The checkpoint can then be restored and re-simulating the application will take significantly less time. To restore a checkpoint, replace the `--checkpoint-dir` option with `--restore-dir`:

```
build/VEGA_X86/gem5.opt configs/example/gpufs/mi300.py --disk-image gem5-resources/src/x86-ubuntu-gpu-ml/disk-image/x86-ubuntu-gpu-ml --kernel gem5-resources/src/x86-ubuntu-gpu-ml/vmlinux-gpu-ml --app gem5-resources/src/gpu/square/bin.default/square.default --restore-dir square-cpt
```

Checkpoints can also be taken using the `m5_checkpoint(..)` [pseudo instruction]() or by checkpointing in the python configs after an exit event. For example, kernel exit events can be enabled using `--exit-at-gpu-task=-1` and the config can be modified to create a checkpoint at the *Nth* kernel by checking the current task number in `configs/example/gpufs/runfs.py`.

Note that checkpoints are currently not supported within a GPU kernel. Thus, checkpoints must be taken when no GPU kernels are running.

#### Build GPU custom applications

If you want to build an application that is not part of gem5-resources, you will want to build the GPU application targeting either `gfx90a` (MI210 and MI250), `gfx942` (MI300X), or both. For example:

```
hipcc my_gpu_app.cpp -o my_gpu_app --offload-arch=gfx90a,gfx942
```

You can build without a docker image on an x86 Linux host by installing the rocm-dev package after setting up a package manager following the steps in the [ROCm Linux documentation](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/).

#### Modifying GPU configuration

The configurations in `configs/example/gpufs/` are helper configurations that interface with `configs/example/gpufs/runfs.py` and set meaningful default values for a specific device. Some parameters of interest in this file are the number of compute units, the GPU topology, the system memory size, and the CPU type.

Some of these parameters *only* modify the value in gem5 and do not change the simulated device. In particular the dgpu_mem_size parameter does not change the amount of memory seen by the device driver and is hardcoded to 16GB in C++. Changing this value will result in a gem5 fatal.

The supported cpu_types are X86KvmCPU and AtomicSimpleCPU as timing CPUs do not support the disjointed Ruby network required to simulate a discrete GPU.

Other parameters related to GPU can be found in `configs/example/gpufs/system/amdgpu.py` which creates the compute units for the GPU. See the ComputeUnit class in `src/gpu-compute/GPU.py` for all available options. Note that not all possible combinations of options can be tested. Options such as queue sizes and latencies are generally safe to modify.
