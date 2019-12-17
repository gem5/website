---
layout: documentation
title: "ARM implementation"
doc: gem5 documentation
parent: architecture_support
permalink: /documentation/general_docs/architecture_support/arm_implementation
---

# ARM Implementation

**Note:** The information in this page is outdated, and so are the hyperlinks.  

## Supported features and modes

The ARM Architecture models within gem5 support an [ARMv8-A](https://developer.arm.com/docs/den0024/latest/armv8-a-architecture-and-processors/armv8-a) profile of the ARM® architecture with multi-processor extensions. 
This includes both AArch32 and AArch64 state.
In AArch32, this include support for [Thumb®](https://www.embedded.com/introduction-to-arm-thumb/), Thumb-2, VFPv3 (32 double register variant) and [NEON™](https://developer.arm.com/architectures/instruction-sets/simd-isas/neon), and Large Physical Address Extensions (LPAE). 
Optional features of the architecture that are not currently supported are [TrustZone®](https://developer.arm.com/ip-products/security-ip/trustzone), ThumbEE, [Jazelle®](https://en.wikipedia.org/wiki/Jazelle), and [Virtualization](https://developer.arm.com/docs/100942/0100/aarch64-virtualization).

## Pertinent Non-supported Features

Currently in ARMv8-A implementation in gem5, there isn't support for interworking between AArch32 and AArch64 execution. 
This limits the ability to run some OSes that expect to execute both 32-bit and 64-bit code, but is expected to be fixed in the short term. 
Additionally, there has been limited testing of EL2 and EL3 modes in the implementation.


## Conditional Execution Support

Many instructions within the ARM architecture are predicated. 
To handle the predication within the gem5 framework and not have to generate N varieties of each instruction for every condition code, the instructions constructors determine which, if any, conditional execution flags are set and then conditionally read the condition codes or a "zero register" which is always available and doesn't insert any dependencies in the dynamic execution of instructions.

## Special PC management

The PCState object used for ARM® encodes additional execution state information so facilitate the use of the generic gem5 CPU components. 
In addition to the standard program counter, the Thumb® vs. 
ARM® instruction state is included as well as the ITSTATE (predication within Thumb® instructions).

## Boot loader

A simple bootloader for ARM is in the source tree under `system/arm/`. 
Two boot loaders exist, one for AArch64 (`aarch64_bootloader`) and another for AArch32 (`simple_bootloader`).

For the AArch64 bootloader: The initial conditions of the boot loader are the same as those for Linux, `r0 = device tree blob address; r6 = kernel start address`. 
The boot loader starts the kernel with CPU 0 and places the other CPUs in a WFE spin-loop until the kernel starts them later.

For the AArch32 boot loader: The initial conditions of the bootloader running are the same as those ffor Linux, `r0 = 0; r1 = machine number; r2 = atags ptr;` and some special registers for the boot loader to use `r3 = start address of kernel; r4 = address of GIC; r5 = adderss of flags register`. 
The bootloader works by reading the MPIDR register to determine the CPU number. 
CPU0 jumps immediately to the kernel while CPUn enables their interrupt interface and and wait for an interrupt. 
When CPU0 generates an IPI, CPUn reads the flags register until it is non-zero and then jumps to that address. 

