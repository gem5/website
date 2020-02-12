---
layout: documentation
title: "Building ARM Kernel"
doc: gem5 documentation
parent: fullsystem
permalink: /documentation/general_docs/fullsystem/building_arm_kernel
---

# Building ARM Kernel

This page contains instructions for building up-to-date kernels for gem5 running on ARM. 

## Prerequisites
These instructions are for running headless systems. That is a more "server" style system where there is no frame-buffer. The description has been created using the latest known-working tag in the repositories linked below, however the tables in each section list previous tags that are known to work. To built the kernels on an x86 host you'll need ARM cross compilers and the device tree compiler. If you're running a reasonably new version of Ubuntu or Debian you can get required software through apt:

```
apt-get install  gcc-arm-linux-gnueabihf gcc-aarch64-linux-gnu device-tree-compiler
```

If you can't use these pre-made compilers the next easiest way to obtain the required compilers from [Linaro](http://releases.linaro.org/latest/components/toolchain/binaries/). 

Depending on the exact source of your cross compilers, the compiler names used below will required small changes.

To actually run the kernel, you'll need to download or compile gem5's bootloader. See the (bootloaders)(#bootloaders) section in this documents for details.

## Linux 4.x
Newer gem5 kernels for ARM (v4.x and later) are based on the vanilla Linux kernel and typically have a small number of patches to make them work better with gem5. The patches are optional and you should be able to use a vanilla kernel as well. However, this requires you to configure the kernel yourself. Newer kernels all use the VExpress\_GEM5\_V1 gem5 platform for both AArch32 and AArch64. The required DTB files to describe the hardware to the OS ship with gem5. To build them, execute this command:

```
make -C system/arm/dt
```

## Kernel Checkout
To checkout the kernel, execute the following command:

```
git clone https://gem5.googlesource.com/arm/linux
```

The repository contains a tag per gem5 kernel releases and working branches for major Linux revisions. Check the [project page](https://gem5-review.googlesource.com/#/admin/projects/arm/linux project page) for a list of tags and branches. The clone command will, by default, check out the latest release branch. To checkout the v4.4 branch, execute the following in the repository:
```
git checkout -b gem5/v4.4
```

## AArch32
To compile the kernel, execute the following commands in the repository:

```
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- gem5_defconfig
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j `nproc`
```

Testing the just built kernel:

```
./build/ARM/gem5.opt configs/example/fs.py --kernel=/tmp/linux-arm-gem5/vmlinux --machine-type=VExpress_GEM5_V1 \
    --dtb-file=$PWD/system/arm/dt/armv7_gem5_v1_1cpu.dtb
```

## AArch64
To compile the kernel, execute the following commands in the repository:

```
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- gem5_defconfig
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- -j `nproc`
```

Testing the just built kernel:

```
./build/ARM/gem5.opt configs/example/fs.py --kernel=/tmp/linux-arm-gem5/vmlinux --machine-type=VExpress_GEM5_V1 \
    --dtb-file=$PWD/system/arm/dt/armv8_gem5_v1_1cpu.dtb --disk-image=linaro-minimal-aarch64.img
```

# Legacy kernels (pre v4.x)
Older gem5 kernels for ARM (pre v4.x) are based on Linaro's Linux kernel for ARM. These kernels use either the VExpress\_EMM (AArch32) or VExpress\_EMM64 (AArch64)  gem5 platform. Unlike the newer kernels, there is a separate AArch32 and AArch64 kernel repository and the device tree files are shipped with the kernel.

## 32 bit kernel (AArch32)
These are instructions to generate a 32-bit ARM Linux binary.

To checkout the aarch32 kernel, execute the following command:

```
git clone https://gem5.googlesource.com/arm/linux-arm-legacy
```

The repository contains a tag per gem5 kernel release. Check the [project page](https://gem5-review.googlesource.com/#/admin/projects/arm/linux-arm-legacy project page) for a list of branches and release tags. To checkout a tag, execute the following in the repository:

```
git checkout -b TAGNAME
```

To compile the kernel, execute the following commands in the repository:

```
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- vexpress_gem5_server_defconfig
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j `nproc`
```

Testing the just built kernel:

```
./build/ARM/gem5.opt configs/example/fs.py  --kernel=/tmp/linux-arm-gem5/vmlinux \
   --machine-type=VExpress_EMM --dtb-file=/tmp/linux-arm-gem5/arch/arm/boot/dts/vexpress-v2p-ca15-tc1-gem5.dtb 
```

## 64 bit kernel (AArch64)
These are instructions to generate a 64-bit ARM Linux binary. 

To checkout the aarch64 kernel, execute the following command:

```
git clone https://gem5.googlesource.com/arm/linux-arm64-legacy
```

The repository contains a tag per gem5 kernel release. Check the [project page](https://gem5-review.googlesource.com/#/admin/projects/arm/linux-arm64-legacy project page) for a list of branches and release tags. To checkout a tag, execute the following in the repository:

```
git checkout -b TAGNAME
```

To compile the kernel, execute the following commands in the repository:

```
make ARCH=arm64 CROSS_COMPILE=aarch64-none-elf- gem5_defconfig
make ARCH=arm64 CROSS_COMPILE=aarch64-none-elf- -j4
```

Testing the just built kernel:

```
./build/ARM/gem5.opt configs/example/fs.py --kernel=/tmp/linux-arm64-gem5/vmlinux --machine-type=VExpress_EMM64 \
    --dtb-file=/tmp/linux-arm64-gem5/arch/arm64/boot/dts/aarch64_gem5_server.dtb --disk-image=linaro-minimal-aarch64.img
```

# Bootloaders
There are two different bootloaders for gem5. One of 32-bit kernels and one for 64-bit kernels. They can be compiled using the following command:

```
make -C system/arm/simple_bootloader
make -C system/arm/aarch64_bootloader
```

Once you have compiled the binaries, put them in the binaries directory in your M5\_PATH.
