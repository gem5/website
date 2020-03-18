---
layout: documentation
title: "ARM implementation"
doc: gem5 documentation
parent: architecture_support
permalink: /documentation/general_docs/architecture_support/arm_implementation/
---

# ARM Implementation

## Supported features and modes

The ARM Architecture models within gem5 support an [ARMv8.0-A](https://developer.arm.com/docs/den0024/latest/armv8-a-architecture-and-processors/armv8-a) profile of the ARM® architecture with multi-processor extensions.
This includes both AArch32 and AArch64 state at all ELs. This basically means supporting:

* [EL2: Virtualization](https://developer.arm.com/docs/100942/0100/aarch64-virtualization)
* [EL3: TrustZone®](https://developer.arm.com/ip-products/security-ip/trustzone)

The baseline model is ARMv8.0 compliant, we also support some mandatory/optional ARMv8.x features (with x > 0)
While the best way to get a synced version of Arm architectural features is to have a look at Arm ID registers:

* [src/arch/arm/ArmISA.py](https://github.com/gem5/gem5/blob/master/src/arch/arm/ArmISA.py)
* [src/arch/arm/ArmSystem.py](https://github.com/gem5/gem5/blob/master/src/arch/arm/ArmSystem.py)

Here you will find a summary of some (but not all) notable`architectural extensions supported in gem5:

* ARMv8.1-LSE, Armv8.1 Large System Extensions
* ARMv8.1-PAN, Privileged access never
* ARMv8.2-SVE, Scalable Vector Extension
* ARMv8.3-JSConv, Javascript conversion instructions
* ARMv8.3-PAuth, Pointer Authentication

