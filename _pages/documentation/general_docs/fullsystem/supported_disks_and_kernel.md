---
layout: documentation
title: "Supported Kernels and Disk Images for gem5 stable"
doc: gem5 documentation
parent: fullsystem
permalink: /documentation/general_docs/fullsystem/supported_disks_and_kernels
---

# Supported Kernels and Disk Images for gem5 v25.0

This document outlines the kernel and disk image combinations used in gem5 v25.0, the level of support for each configuration, and additional components included in the kernels.

## Supported Architectures

* X86
* ARM
* RISC-V

## Kernel and Disk Image Pairings

The following kernel versions are used with each base disk image:

* **Ubuntu 22.04 disk images** use **kernel 5.15**
* **Ubuntu 24.04 disk images** (including `npb` and `gapbs` variants) use **kernel 6.8.12**

This pairing is consistent across all three ISAs: X86, ARM, and RISC-V.

Each disk image includes the kernel modules corresponding to its kernel version (e.g., the 24.04 images contain modules for kernel 6.8.12).

## How Kernels Were Chosen

The kernel versions used in gem5 v25.0 match the default versions shipped with Ubuntu 22.04 (5.15) and 24.04 (6.8.12). These were chosen to maintain compatibility with a wide variety of tools while minimizing custom maintenance overhead. Aligning with Ubuntu’s LTS distributions ensures we use stable, well-tested kernels without requiring custom patches.

## Included Kernel Module

All images include the `gem5-bridge` kernel module, which enables use of m5 annotations (e.g., `m5_exit`, `m5_reset_stats`) without requiring root access in the simulated system. This module is pre-installed within the disk image and matches the included kernel.

## Disk Images Overview

| Disk Image Name      | Ubuntu Version | Benchmarks Included |
| -------------------- | -------------- | ------------------- |
| `ubuntu-22.04`       | 22.04          | No                  |
| `ubuntu-24.04`       | 24.04          | No                  |
| `ubuntu-24.04-npb`   | 24.04          | Yes (NPB)           |
| `ubuntu-24.04-gapbs` | 24.04          | Yes (GAPBS)         |

These disk images are available for X86, ARM, and RISC-V.

## Support Status

* Only the combinations listed above (Ubuntu 22.04 with 5.15 and Ubuntu 24.04 with 6.8.12) are **regularly tested** and supported in gem5 v25.0.
* Other kernel versions or pairings **may not work** and are not guaranteed to be compatible with gem5 v25.0.
