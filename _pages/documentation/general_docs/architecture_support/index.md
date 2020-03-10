---
layout: documentation
title: "Architecture Support"
doc: gem5 documentation
parent: architecture_support
permalink: /documentation/general_docs/architecture_support/
---

# Architecture Support

{: .outdated-notice}
The information and hyperlinks in this page may not be accurate.

## Alpha

Gem5 models a DEC Tsunami based system. 
In addition to the normal Tsunami system that support 4 cores, we have an extension which supports 64 cores (a custom PALcode and patched Linux kernel is required). 
The simulated system looks like an Alpha 21264 including the BWX, MVI, FIX, and CIX to user level code. 
For historical reasons the processor executes EV5 based PALcode.

It can boot unmodified Linux 2.4/2.6, FreeBSD, or L4Ka::Pistachio as well as applications in syscall emulation mode. 
Many years ago it was possible to boot HP/Compaq's Tru64 5.1 operating system. 
We no longer actively maintain that capability, however, and it does not currently work.

## ARM

The ARM Architecture models within gem5 support an [ARMv8-A](https://developer.arm.com/docs/den0024/latest/armv8-a-architecture-and-processors/armv8-a) profile of the ARM® architecture with multi-processor extensions. 
This includes both AArch32 and AArch64 state. 
In AArch32, this include support for [Thumb®](https://www.embedded.com/introduction-to-arm-thumb/), Thumb-2, VFPv3 (32 double register variant) and [NEON™](https://developer.arm.com/architectures/instruction-sets/simd-isas/neon), and Large Physical Address Extensions (LPAE). 
Optional features of the architecture that are not currently supported are [TrustZone®](https://developer.arm.com/ip-products/security-ip/trustzone), ThumbEE, [Jazelle®](https://en.wikipedia.org/wiki/Jazelle), and [Virtualization](https://developer.arm.com/docs/100942/0100/aarch64-virtualization).

In full system mode gem5 is able to boot uni- or multi-processor Linux and bare metal applications built with ARM's compilers. 
Newer Linux versions work out of the box (if used with gem5's DTBs) we also provide gem5-specific Linux kernels with custom configurations and custom drivers Additionally, statically linked Linux binaries can be run in ARM's syscall emulation mode.

## POWER

Support for the POWER ISA within gem5 is currently limited to syscall emulation only and is based on the [POWER ISA v2.06 B Book](http://kib.kiev.ua/x86docs/POWER/PowerISA_V2.06B_V2_PUBLIC.pdf).
A big-endian, 32-bit processor is modeled. 
Most common instructions are available (enough to run all the SPEC CPU2000 integer benchmarks). 
Floating point instructions are available but support may be patchy. 
In particular, the Floating-Point Status and Control Register (FPSCR) is generally not updated at all. 
There is no support for vector instructions.

Full system support for POWER would require a significant amount of effort and is not currently being developed. 
However, if there is interest in pursuing this, a set of patches-in-progress that make a start towards this can be obtained from [Tim](mailto:timothy.jones@cl.cam.ac.uk).

## SPARC

The gem5 simulator models a single core of a UltraSPARC T1 processor (UltraSPARC Architecture 2005).

It can boot Solaris like the Sun T1 Architecture simulator tools do (building the hypervisor with specific defines and using the HSMID virtual disk driver). 
Multiprocessor support was never completed for full-system SPARC. 
With syscall emulation gem5 supports running Linux or Solaris binaries. 
New versions of Solaris no longer support generating statically compiled binaries which gem5 requires.

## x86

X86 support within the gem5 simulator includes a generic x86 CPU with 64 bit extensions, more similar to AMD's version of the architecture than Intel's but not strictly like either. 
Unmodified versions of the Linux kernel can be booted in UP and SMP configurations, and patches are available for speeding up boot. 
SSE and 3dnow are implemented, but the majority of x87 floating point is not. 
Most effort has been focused on 64 bit mode, but compatibility mode and legacy modes have some support as well. 
Real mode works enough to bootstrap an AP, but hasn't been extensively tested. 
The features of the architecture that are exercised by Linux and standard Linux binaries are implemented and should work, but other areas may not. 
64 and 32 bit Linux binaries are supported in syscall emulation mode.

## MIPS 


## RISC-V

