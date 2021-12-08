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

### From gem5 v21.2

The best way to get a synced version of Arm architectural features is to have a look at the [ArmExtension](https://gem5.googlesource.com/public/gem5/+/refs/heads/develop/src/arch/arm/ArmSystem.py) enum
used by the release object and the available example releases provided within the same file.

A user can choose one of the following options:

* Use the default release
* Use another example release (e.g. Armv82)
* Generate a custom release from the available ArmExtension enum values

### Before gem5 v21.2

The best way to get a synced version of Arm architectural features is to have a look at Arm ID registers and boolean values:

* [src/arch/arm/ArmISA.py](https://gem5.googlesource.com/public/gem5/+/refs/tags/v21.1.0.2/src/arch/arm/ArmISA.py)
* [src/arch/arm/ArmSystem.py](https://gem5.googlesource.com/public/gem5/+/refs/tags/v21.1.0.2/src/arch/arm/ArmSystem.py)
