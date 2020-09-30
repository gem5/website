---
layout: post
title:  "A Modular and Secure System Architecture for the IoT"
author: Nils Asmussen, Hermann Härtig, and Gerhard Fettweis
date:   2020-05-29
---

Introduction
------------

The "Internet of Things (IoT)" is already pervasive in industrial production and it is expected to become ubiquitous in many other sectors, too. For example, such connected devices have great potential to better automate and optimize critical infrastructure such as electrical grids and transportation networks and are also promising for health care applications. However, a one-size-fits-all solution for the compute hardware and system software of all these devices is infeasible, primarily due to cost pressure and energy constraints, but also because each domain requires different compute capacity, sensors, and actuators. Instead, customized solutions are needed for both the hardware and the software that drives it. System designers should be able to easily assemble these specialized computers and their operating systems (OSes) from reusable building blocks, requiring modularity at both the hardware and the OS level.

Besides modularity, security is essential due to the interaction of IoT devices with the physical world and their attachment to the Internet, enabling attackers to cause harm to the environment or humans. For that reason, using encypted communication is not sufficient, but the IoT devices themselves need to be secured as well. At the software level, the high complexity and missing isolation between subsystems in monolithic OSes render them an inappropriate choice for this security-critical use case. Instead, microkernel-based systems such as L4 [1] are a promising candidate due to their modular architecture and strong isolation between subsystems. In fact, it has been shown that a microkernel-based system could have at least reduced the severity of 96% of Linux's critical CVEs by restricting the impact to a single subsystem and could have completely eliminated 40% of the CVEs [2].

We argue that the ideas of microkernel-based systems to split up the system into multiple isolated components can and should also be applied to hardware. For example, system-on-a-chip designers often buy hardware components (IP blocks) from third-party vendors. However, IP blocks such as modems or accelerators can be complex and should therefore not be trusted. Furthermore, the recently found side-channel attacks on modern general-purpose cores such as Meltdown [3], Spectre [4], and ZombieLoad [5] have raised the question whether we should still trust these complex cores to properly enforce isolation boundaries between different software components. Thus, we believe that hardware components such as modems, accelerators, and cores should be strongly separated just as software components are in microkernel-based systems.

System Architecture
-------------------
<p align="center">
  <img src="{{site.url}}/assets/img/blog/modular-and-secure/modular-and-secure-fig-1.png"/>
</p>



Our system architecture [6], depicted in Figure 1a, builds upon tiled architectures, which already allow to integrate hardware components in a modular way into separate tiles. However, although the tiles are physically separate, typically they still have unrestricted access to the network-on-chip (NoC) that connects the tiles. We are proposing to add a new and simple hardware component between each tile and the NoC that restricts the tile's access to the NoC. This hardware component is called trusted communication unit (TCU). Besides isolating the tiles from each other, the TCU allows to establish and use communication channels between tiles.

The operating system, called M³ and shown in Figure 1b, is designed as a microkernel-based system and leverages the TCU to isolate hardware and software components, while selectively allowing their communication. The kernel of M³ runs exclusively on a dedicated *kernel tile*, whereas services and applications run on the *user tiles*. The kernel as the only privileged component in the system is the only one that can establish communication channels between tiles. User tiles can afterwards use the established channels to directly communicate with other user tiles without involving the kernel. However, user tiles cannot change or add new channels. Due to the physical separation between tiles, M³ has no specific requirements on the tiles such as user/kernel mode or memory management units. For that reason, not only compute cores, but arbitrary hardware components such as modems, accelerators, or devices can be integrated as a user tile and the kernel can control their communication permissions in a uniform way.

Simulation with gem5
--------------------

Besides working on a FPGA-based implementation, we are prototyping the system architecture in gem5 to evaluate its feasibility. To simulate the system architecture we represent each tile as a `System` object and connect the tiles with a `NoncoherentXBar`. The `System` object implements a custom loader for M³ to load the kernel and other components onto the individual tiles. In our simulation we use x86, ARMv7, and RISC-V. However, our hardware implementation will use RISC-V cores due to their simplicity and openness. Since gem5 had only support for system emulation with RISC-V, we contributed full-system support for RISC-V to gem5, which enables us to run our OS and make use of virtual memory.

Conclusion
----------

IoT devices that interface with the physical world and the Internet require both security and modularity. We are investigating a new system architecture that takes the ideas from microkernel-based systems for software and apply them to hardware as well. The key idea is to build upon tiled architectures and add a new and simple hardware component called trusted communication unit to each tile for isolation and communication. The microkernel-based OS called M³ builds on top of this hardware platform and establishes communication channels between otherwise isolated tiles. We believe that modularity at both the hardware and software level and the strong isolation between components enables us to deliver a suitable foundation for future IoT devices.

Bibliography
------------

[1] Hermann Hartig, Michael Hohmuth, Norman Feske, Christian Helmuth, Adam Lackorzynski, Frank Mehnert, and Michael Peter. The nizza secure-system architecture. In 2005 International Conference on Collaborative Computing: Networking, Applications and Worksharing, pages 10–pp. IEEE, 2005.

[2] Simon Biggs, Damon Lee, and Gernot Heiser. The Jury Is In: Monolithic OS Design Is Flawed: Microkernel-based Designs Improve Security. Proceedings of the 9th Asia-Pacific Workshop on Systems. 2018.

[3] Moritz Lipp, Michael Schwarz, Daniel Gruss, Thomas Prescher, Werner Haas, Stefan Mangard, Paul Kocher, Daniel Genkin, Yuval Yarom, and Mike Hamburg. Meltdown. CoRR, abs/1801.01207, 2018.

[4] Paul Kocher, Daniel Genkin, Daniel Gruss, Werner Haas, Mike Hamburg, Moritz Lipp, Stefan Mangard, Thomas Prescher, Michael Schwarz, and Yuval Yarom. Spectre attacks: Exploiting speculative execution. CoRR, abs/1801.01203, 2018.

[5] Schwarz, Michael, Moritz Lipp, Daniel Moghimi, Jo Van Bulck, Julian Stecklina, Thomas Prescher, and Daniel Gruss. ZombieLoad: Cross-privilege-boundary data sampling. In Proceedings of the 2019 ACM SIGSAC Conference on Computer and Communications Security, pp. 753-768. 2019.

[6] Nils Asmussen, Marcus Völp, Benedikt Nöthen, Hermann Härtig, and Gerhard Fettweis. M³: A hardware/operating-system co-design to tame heterogeneous manycores. In Proceedings of the wenty-First International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS'16, pages 189–203. ACM, 2016.

Workshop Presentation
---------------------

<iframe width="960" height="540"
src="https://www.youtube.com/embed/2jPiXOhboko" frameborder="0"
allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
allowfullscreen style="max-width: 960px;"></iframe>
