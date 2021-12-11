---
layout: documentation
title: GCN3 GPU model
doc: gem5 documentation
parent: gpu_models
permalink: /documentation/general_docs/gpu_models/GCN3
---

# **GCN3**

Table of Contents

1. [Using the model](##Using-the-model)
2. [ROCm](##ROCm)
3. [Documentation and Tutorials](##Documentation-and-Tutorials)

The GCN3 GPU is a model that simulates a GPU at the ISA level, as opposed to the intermediate language level. This page will give you a general overview of how to use this model, the software stack the model uses, and provide resources that detail the model and how it is implemented.

## **Using the model**

Currently, the GCN3 GPU model in gem5 is supported on the stable and develop branch.

The [gem5 repository](https://gem5.goooglesource.com/public/gem5) comes with a dockerfile located in `util/dockerfiles/gcn-gpu/`. This dockerfile contains the drivers and libraries needed to run the GPU model. A pre-built version of the docker image is hosted at `gcr.io/gem5-test/gcn-gpu`.

The [gem5-resources repository](https://gem5.googlesource.com/public/gem5-resources/) also comes with a number of sample applications that can be used to verify that the model runs correctly.  We recommend users start with [square](https://resources.gem5.org/resources/square), as it is a simple, heavily tested application that should run relatively quickly.

#### Using the image
The docker image can either be built or pulled from gcr.io

To build the docker image from source:
```
# Working directory: gem5/util/dockerfiles/gcn-gpu
docker build -t <image_name> .
```

To pull the pre-built docker image:
```
docker pull gcr.io/gem5-test/gcn-gpu
```
You can also put `gcr.io/gem5-test/gcn-gpu` as the image in the docker run command without pulling beforehand and it will be pulled automatically.

#### Building gem5 using the image
See square in [gem5 resources](https://resources.gem5.org/resources/square) for an example of how to build gem5 in the docker.  Note: these directions assume you are pulling the latest image automatically.

#### Building & running a GPU application using the image
See [gem5 resources](https://resources.gem5.org/) for examples of how to build and run GPU applications in the docker.

## **ROCm**

The GCN3 model was designed with enough fidelity to not require an emulated runtime. Instead, the GCN3 model uses the Radeon Open Compute platform (ROCm). ROCm is an open platform from AMD that implements [Heterogeneous Systems Architecture (HSA)](http://www.hsafoundation.com/) principles. More information about the HSA standard can be found on the HSA Foundation's website. More information about ROCm can be found on the [ROCm website](https://rocmdocs.amd.com/en/latest/)

#### Simulation support for ROCm
The model currently only works with system-call emulation (SE) mode, therefore all kernel level driver functionality is modeled entirely within the SE mode layer of gem5. In particular, the emulated GPU driver supports the necessary `ioctl()` commands it receives from the userspace code. The source for the emulated GPU driver can be found in:

* The GPU compute driver: `src/gpu-compute/gpu_compute_driver.[hh|cc]`

* The HSA device driver: `src/dev/hsa/hsa_driver.[hh|cc]`

The HSA driver code models the basic functionality for an HSA agent, which is any device that can be targeted by the HSA runtime and accepts Architected Query Language (AQL) packets. AQL packets are a standard format for all HSA agents, and are used primarily to initiate kernel launches on the GPU. The base `HSADriver` class holds a pointer to the HSA packet processor for the device, and defines the interface for any HSA device. An HSA agent does not have to be a GPU, it could be a generic accelerator, CPU, NIC, etc.

The `GPUComputeDriver` derives from `HSADriver` and is a device-specific implementation of an `HSADriver`. It provides the implementation for GPU-specific `ioctl()` calls.

The `src/dev/hsa/kfd_ioctl.h` header must match the `kfd_ioctl.h` header that comes with ROCt. The emulated driver relies on that file to interpret the `ioctl()` codes the thunk uses.

#### ROCm toolchain and software stack
The GCN3 model supports ROCm version 4.0.

The following ROCm components are required:
* [Heterogeneous Compute Compiler (HCC)](https://github.com/RadeonOpenCompute/hcc)
* [Radeon Open Compute runtime (ROCr)](https://github.com/RadeonOpenCompute/ROCR-Runtime)
* [Radeon Open Compute thunk (ROCt)](https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface)
* [HIP](https://github.com/ROCm-Developer-Tools/HIP)

The following additional components are used to build and run machine learning programs:
* [hipBLAS](https://github.com/ROCmSoftwarePlatform/hipBLAS/)
* [rocBLAS](https://github.com/ROCmSoftwarePlatform/rocBLAS/)
* [MIOpen](https://github.com/ROCmSoftwarePlatform/MIOpen/)
* [rocm-cmake](https://github.com/RadeonOpenCompute/rocm-cmake/)

For information about installing these components locally, the commands in the GCN3 dockerfile (`util/dockerfiles/gcn-gpu/`) can be followed on an Ubuntu 16 machine.

## **Documentation and Tutorials**

#### GCN3 Model
Describes the GCN3 model
* [HPCA 2018](https://ieeexplore.ieee.org/document/8327041)

#### gem5 GCN3 ISCA tutorial
Covers information about the GPU architecture, GCN3 ISA and HW-SW interfaces in gem5. Also provides an introduction to ROCm.
* [gem5 GCN3 ISCA webpage](http://www.gem5.org/events/isca-2018)
* [gem5 GCN3 ISCA slides](http://old.gem5.org/wiki/images/1/19/AMD_gem5_APU_simulator_isca_2018_gem5_wiki.pdf)

#### GCN3 ISA
* [GCN3 ISA](https://gpuopen.com/documentation/amd-isa-documentation/)

#### ROCm Documentation
Contains further documentation about the ROCm stack, as well as programming guides for using ROCm.
* [ROCm webpage](https://rocmdocs.amd.com/en/latest/)

#### AMDGPU LLVM Information
* [LLVM AMDGPU](https://llvm.org/docs/AMDGPUUsage.html)
