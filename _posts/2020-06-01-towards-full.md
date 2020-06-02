---
layout: post
title:  "Towards full-system discrete GPU simulation"
author: Mattew Poremba, Alexandru Dutu, Gaurav Jain, Pouya Fotouhi, Michael Boyer, and Bradford M. Beckmann.
date:   2020-06-01
---

AMD Research is developing a full system GPU (Graphics Processing Unit) model capable of using the amdgpu Linux kernel driver and the most up to date software stacks. Previously AMD updated the gem5 [1] GPU compute timing model  to execute the GCN (Graphics Core Next) generation 3 machine ISA [2,3], but it still relied on system-call emulation. With full-system support, the model can run the most recent open-source Radeon Open Compute platform (ROCm) stack without modification. This allows users to run a wide variety of applications written in several high-level languages, including C++, HIP, OpenMP, and OpenCL. This provides researchers the ability to evaluate many different types of workloads, from traditional compute applications to emerging modern GPU workloads, such as task parallel and machine learning applications. The resulting AMD gem5 GPU simulator is a cycle-level, flexible research model that is capable of representing many different GPU configurations, on-chip cache hierarchies, and system designs. The model has been used in several top-tier computer architecture publications in the last several years.

In this presentation, we will describe the capabilities of the AMD gem5 GPU simulator that will be publicly released with a BSD license. We will detail the simulation changes and describe the new execution flow. The presentation will also highlight the new capabilities provided by full-system support. In particular, simulation will be more deterministic and allows the user to run host-side CPU code using KVM fast-forwarding. We will detail the additional support being added including multi-context virtual memory support, system DMA engines, and support for the software interface between them.

[1] Binkert, Nate L., et al. “The gem5 Simulator,” In SIGARCH Computer Arch. News, vol. 39, no. 2, pp. 1-7, Aug. 2011.

[2] AMD. “AMD GCN3 ISA Architecture Manual”, https://gpuopen.com/compute-product/amd-gcn3-isa-architecture-manual/

[3] Gutierrez, Anthony et al. “The Updated AMD gem5 APU Simulator: Modeling GPUs Using the Machine ISA” ISCA tutorial 2018.

## Workshop Presentation
<iframe width="560" height="315" src="https://www.youtube.com/embed/cpnoUgcGjuI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
