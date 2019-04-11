---
title: "ARM research summit 2017"
date: 2018-05-13T18:51:37-04:00
draft: false
weight: 1000
---

The [ARM Research Summit](https://developer.arm.com/research/summit) is
an academic summit to discuss future trends and disruptive technologies
across all sectors of computing. On the first day of the Summit, ARM
Research will host a gem5 workshop to give a brief overview of gem5 for
computer engineers who are new to gem5 and dive deeper into some of
gem5's more advanced capabilities. The attendees will learn what gem5
can and cannot do, how to use and extend gem5, as well as how to
contribute back to gem5.

The ARM Research Summit will take place in Cambridge (UK) over the days
of 11-13 September 2017. The gem5 workshop will be a full day event on
the 11th September.

# Streaming & Offline viewing

The workshop is being streamed live and all talks will be available on
YouTube after the workshop. See the [main summit
page](https://developer.arm.com/research/summit/summit-live) for
details.

# Target Audience

The primary audience is researchers who are using, or planning to use,
gem5 for architecture research.

**Prerequisites**: Attendees are expected to have a working knowledge of
C++, Python, and computer systems.

# Registration

See the main [ARM Research Summit
website](https://developer.arm.com/research/summit) for details about
registration.

# Schedule

The workshop will take place on Monday the 11th September 2017 at
Robinson College in Cambridge (UK). The workshop starts at 9.00 and runs
in parallel with the main Summit program until 16.30 when it joins the
main
program.

| Time        | Topic                                                                                                                                                                             |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 09.00-09.30 | Welcome and introduction to gem5 — [slides](Media:Summit2017_Intro_to_gem5.pdf "wikilink")                                                                                        |
| 09.30-09.45 | [Interacting with gem5 using workload-automation & devlib](#WA "wikilink") — [slides](Media:Summit2017_wa_devlib.pdf "wikilink")                                                  |
| 09.45-10.00 | [ARM Research Starter Kit: System Modeling using gem5](#StarterKit "wikilink") — [slides](Media:Summit2017_starterkit.pdf "wikilink")                                             |
| 10.00-10.15 | Break                                                                                                                                                                             |
| 10.15-10.30 | [Debugging a target-agnostic JIT compiler with GEM5](#JIT_Debugging "wikilink")                                                                                                   |
| 10.30-11.00 | [Learning gem5: Modeling Cache Coherence with gem5](#Ruby "wikilink") — [slides](Media:Summit2017_learning_gem5_ruby.pdf "wikilink")                                              |
| 11.00-11.15 | Break (overlaps with main program break)                                                                                                                                          |
| 11.15-11.45 | [A Detailed On-Chip Network Model inside a Full-System Simulator](#Garnet2 "wikilink") — [slides](Media:Summit2017_garnet2.0_tutorial.pdf "wikilink")                             |
| 11.45-12.00 | [Integrating and quantifying the impact of low power modes in the DRAM controller in gem5](#DRAMPower "wikilink") — [slides](Media:Summit2017_drampower.pdf "wikilink")           |
| 12.00-12.15 | Break                                                                                                                                                                             |
| 12.15-12.45 | [CPU power estimation using PMCs and its application in gem5](#PowMon "wikilink") — [slides](Media:Summit2017_powmon.pdf "wikilink")                                              |
| 12.45-13.00 | [gem5: empowering the masses](#PowerFramework "wikilink") — [slides](Media:Summit2017_powerframework.pdf "wikilink")                                                              |
| 13.00-14.15 | Lunch                                                                                                                                                                             |
| 14.15-14.45 | [Trace-driven simulation of multithreaded applications in gem5](#ElasticSimMATE "wikilink") — [slides](Media:Summit2017_elasticsimmate.pdf "wikilink")                            |
| 14.45-15.00 | [Generating Synthetic Traffic for Heterogeneous Architectures](#TraceGeneration "wikilink") — [slides](Media:Summit2017_trace_generation.pdf "wikilink")                          |
| 15:00-15:15 | Break                                                                                                                                                                             |
| 15:15-16:45 | [System Simulation with gem5, SystemC and other Tools](#SystemC "wikilink") — [slides](Media:Summit2017_systemc.pdf "wikilink")                                                   |
| 15:45-16:00 | [COSSIM: An Integrated Solution to Address the Simulator Gap for Parallel Heterogeneous Systems](#COSSIM "wikilink") — [slides](Media:Summit2017_COSSIM.pdf "wikilink")           |
| 16:00-16:15 | [Simulation of Complex Systems Incorporating Hardware Accelerators](#ComplexSystems "wikilink") — [slides](Media:Summit2017_complex_fs_incorporating_accelerators.pdf "wikilink") |
| 16:15-16:30 | Break                                                                                                                                                                             |
| 16:30-18:15 | Introduction to ARM Research                                                                                                                                                      |
| 18:20-20.00 | Poster Session & Pre-Dinner Drinks                                                                                                                                                |
| 20.00-21.30 | Buffet Dinner                                                                                                                                                                     |

# Talks

<span id="ElasticSimMATE">

## Trace-driven simulation of multithreaded applications in gem5

The gem5 modular simulator provides a rich set of CPU models which
permits balancing simulation speed and accuracy. The growing interest in
using gem5 for design-space exploration however requires higher
simulation speeds so as to enable scalability analysis with systems
comprising tens to hundreds of cores. One relevant approach for enabling
significant speedups lies in using trace-driven simulation, in which CPU
cores are abstracted away thereby enabling to refocus simulation effort
on memory/interconnect subsystems which play a key role on performance.
This talk describes some of the work carried out on the Mont-Blanc
european projects on trace-driven simulation and discusses the related
challenges for multicore architectures in which trace injection requires
to account for the API synchronization of the underlying running
application. The ElasticSimMATE tool is presented as an initiative
towards combining Elastic Traces and SimMATE so as to enable fast and
accurate simulation of multithreaded applications on ARM multicore
systems.

> **Dr Gilles Sassatelli** is a CNRS senior scientist at LIRMM, a
> CNRS-University of Montpellier academic research unit with a staff of
> over 400. He is vice-head of the microelectronics department and leads
> a group of 20 researchers working in the area of smart embedded
> digital systems. He has authored over 200 peer-reviewed papers and has
> occupied key roles in a number of international conferences. Most of
> his research is conducted in the frame of international EU-funded
> projects such as the DreamCloud and Mont-Blanc projects.

> **Alejandro Nocua** received the Ph.D. degree in Microelectronics from
> the University of Montpellier, France, in 2016. Currently, he is a
> postdoctoral researcher at the French National Center for Scientific
> Research (CNRS). His research interests include the analysis of
> high-performance and energy-efficiency design methodologies. He
> received his Master degree in Science from the National Institute of
> Astrophysics, Optics and Electronics (INAOE), Mexico, in 2013.
> Alejandro was awarded his BS degree in Electronics Engineering from
> Industrial University of Santander (UIS), Colombia in 2011.

> **Florent Bruguier** received the M.S. and Ph.D. degrees in
> microelectronics from the University of Montpellier, France, in 2009
> and 2012, respectively. From 2012 to 2015, he was a Scientific
> Assistant with the Montpellier Laboratory of Informatics, Robotics,
> and Microelectronics, University of Montpellier. Since 2015, he is a
> Permanent Associate Professor. He has co-authored over 30
> publications. His research interests are focused on self-adaptive and
> secure approaches for embedded systems.

> **Anastasiia Butko**, Ph.D. is a Postdoctoral Fellow in the
> Computational Research Division at Lawrence Berkeley National
> Laboratory (LBNL), CA. Her research interests lie in the general area
> of computer architecture, with particular emphasis on high-performance
> computing, emerging and heterogeneous technologies, associated
> parallel programming and architectural simulation techniques. Broadly,
> her reasearch addresses the question of how alternative technologies
> can provide continuing performance scaling in the approaching
> Post-Moore’s Law era. Her primary research projects include
> development of the EDA tools for fast superconducting logic design,
> development of the classical ISA for quantum processor control,
> development of the fast and flexible System-on-Chip generators using
> Chisel DSL. Dr. Butko co-leads Open Source Supercomputing project and
> is a technical committee member of the RISC-V foundation.
>
> Dr. Butko received her Ph.D. in Microelectronics from the University
> of Montpellier, France (2015). Her doctoral thesis developed fast and
> accurate simulation techniques for many-core architectures
> exploration. Her graduate work has been conducted within the European
> project MontBlanc, which aims to design a new supercomputer
> architecture using low-power embedded technologies.
>
> Dr. Butko received her MSc. Degree in Microelectronics from UM2,
> France and MSc and BSc Degrees in Digital Electronics from NTUU "KPI",
> Ukraine. During her Master she participated on the international
> program of double diploma between Montpellier and Kiev universities.

</span>

<span id="Ruby">

## Modeling Cache Coherence with gem5

Correctly implementing cache coherence protocols is hard and these
implementation details can affect the system's performance. Therefore,
it is important to robustly model the detailed cache coherence
implementation. The popular computer architecture simulator gem5 uses
Ruby as its cache coherence model providing higher fidelity cache
coherence modeling than many other simulators.

In this talk, I will give a brief overview of Ruby, including SLICC: the
domain-specific language Ruby uses to specify cache protocols. I will
show the extreme flexibility of this model and details of a simple cache
coherence protocol. After this talk, you will be able to dive in and
begin writing your own coherence protocols\!

> **Jason Lowe-Power** is an Assistant Professor at University of
> California, Davis in the Computer Science department. Jason's research
> focuses on increasing the energy efficiency and performance of
> end-to-end applications like analytic database operations used by
> Amazon, Google, Target, etc. One important aspect of this research is
> adding hardware mechanisms to systems that enable all programmers to
> use emerging hardware accelerators like GPUs. Additionally, Jason is a
> leader of the open-source architectural simulator, gem5, used by over
> 1500 academic papers. Jason received his PhD from University of
> Wisconsin-Madison in Summer 2017. He was awarded the Wisconsin
> Distinguished Graduate Fellowship Cisco Computer Sciences Award in
> 2014 and 2015.

</span>

<span id="Garnet2">

## A Detailed On-Chip Network Model inside a Full-System Simulator

Compute systems are ubiquitous, with form factors ranging from
smartphones at the edge to datacenters in the cloud. Chips in all these
systems today comprise 10s to 100s of homogeneous/heterogeneous cores or
processing elements. The growing emphasis on parallelism, distributed
computing, heterogeneity, and energy-efficiency across all these systems
makes the design of the Network-on-Chip (NoC) fabric connecting the
cores critical to both high-performance and low power consumption.

It is imperative to model the details of the NoC when architecting and
exploring the design-space of a complex many-core system. If ignored, an
inaccurate NoC model could lead to over-design or under-design due to
incorrect trade-off choices, causing performance losses at runtime. To
this end, we have designed and integrated a detailed on-chip network
model called Garnet inside the gem5 (www.gem5.org) full-system
architectural simulator which is being used extensively by both industry
and academia. Together with Garnet, gem5 provides plug-and-play models
of cores, caches, cache coherence protocols, NoC, memory controller, and
DRAM, with varying levels of details, enabling computer architects and
designers to trade-off simulation speed and accuracy.

In this talk, we will first introduce the basic building blocks of NoCs
and present the state-of-the-art used in chips today. We will then
present Garnet, and demonstrate how it faithfully models the
state-of-the-art, while also offering immense flexibility in modifying
various parts of the microarchitecture to serve the needs of both
homogeneous many-cores and heterogeneous accelerator-based systems of
the future via case studies and code-snippets. Finally, we will
demonstrate how Garnet works within the entire gem5 ecosystem.

> **Tushar Krishna** is an Assistant Professor in the Schools of ECE and
> CS at Georgia Tech. He received a Ph.D. in Electrical Engineering and
> Computer Science from the Massachusetts Institute of Technology in
> 2014. Prior to that he received a M.S.E from Princeton University in
> 2009, and a B.Tech from the Indian Institute of Technology (IIT) Delhi
> in 2007, both in Electrical Engineering.
>
> Before joining Georgia Tech in 2015, Dr. Krishna was a post-doctoral
> researcher in the VSSAD Group at Intel, Massachusetts, and then at the
> Singapore-MIT Alliance for Research and Technology at MIT.
>
> Dr. Krishna's research interests are in computer architecture,
> interconnection networks, networks-on-chip, deep learning
> accelerators, and FPGAs.

</span>

<span id="SystemC">

## System Simulation with gem5, SystemC and other Tools

SystemC TLM based virtual prototypes have become the main tool in
industry and research for concurrent hardware and software development,
as well as hardware design space exploration. However, there exists a
lack of accurate, free, changeable and realistic SystemC models of
modern CPUs. Therefore, many researchers use the cycle accurate open
source system simulator gem5, which has been developed in parallel to
the SystemC standard. In this tutorial we present the coupling of gem5
with SystemC that offers full interoperability between both simulation
frameworks, and therefore enables a huge set of possibilities for system
level design space exploration. Furthermore, we show several examples
for coupling gem5 with SystemC and other tools.

> **Matthias Jung** received his PhD degree in Electrical Engineering
> from the University of Kaiserslautern Germany in 2017. His research
> interest are SystemC based virtual prototypes, especially with the
> focus on the modeling of memory systems and memory controller design.
> Since may 2017 he is a researcher at Fraunhofer IESE, Kaiserslautern,
> Germany.

> **Christian Menard** received a Diploma degree in Information Systems
> Technology from TU Dresden in Germany in 2016 and joined the chair for
> compiler construction as a Ph.D. student within the excellence cluster
> cfaed in TU Dresden. His current research includes system-level
> modeling of widely heterogeneous hardware as well dataflow compilers
> for heterogeneous MPSoC platforms.

</span>

<span id="PowMon">

## CPU power estimation using PMCs and its application in gem5

Fast and accurate estimation of CPU power consumption is necessary to
inform run-time power management approaches and allow effective design
space exploration. Power simulators, combined with a full-system
architectural simulator such as gem5, enable power-performance
trade-offs to be investigated early in the design of a system. However,
the accuracy of existing power simulators is known to be low, and this
can lead to incorrect conclusions being made. In this talk, I will
present our statistically rigorous methodology for building accurate
run-time power models using Performance Monitoring Counters (PMCs) for
mobile and embedded devices, and demonstrate how our models make more
efficient use of limited training data and better adapt to unseen
scenarios by uniquely considering stability. Models built using the
methodology for both ARM Cortex-A7 and Cortex-A15 CPUs exhibit a 3.8%
and 2.8% average error respectively. I will also present online
resources that we have made available from the work, including software
tools, documentation, raw data and further results. I will also present
results from an investigation into the correlation between gem5 activity
statistics and hardware PMCs. Based on this, a gem5 power model for a
simulated quadcore ARM Cortex-A15 has been created, built using the
above methodology, and its accuracy compared against experimental
results obtained from hardware.

> **Geoff Merrett** is an Associate Professor in the Department of
> Electronics and Computer Science at the University of Southampton. He
> received the BEng (1st, Hons) and PhD degrees in Electronic
> Engineering from Southampton in 2004 and 2009 respectively. His
> research interests are in energy-aware and self-powered computing
> systems, with application across the spectrum from highly constrained
> IoT devices to many-core mobile and embedded systems. He has published
> over 100 peer-reviewed articles in these areas, and given invited
> talks at a number of international events. Dr Merrett is a
> Co-Investigator on the EPSRC-funded £5.6M PRiME Programme Grant (where
> he leads the applications and cross-layer interaction theme),
> "Continuous on-line adaptation in many-core systems: From graceful
> degradation to graceful amelioration", and deputy-lead on the
> "Wearable and Autonomous Computing for Future Smart Cities" Platform
> Grant. He is technical manager of Southampton’s ARM-ECS Research
> Centre, an award-winning industry-academia collaboration between the
> University of Southampton and ARM. He coordinates IoT research at the
> University, and leads the wireless sensing theme of its Pervasive
> Systems Centre. He is an Associate Editor for the IET CDS journal,
> serves as a reviewer for a number of leading journals, and on TPCs for
> a range of conferences. He co-manages the UK’s Energy Harvesting
> Network, was General Chair of the ACM Workshop on Energy-Harvesting
> and Energy-Neutral Sensing Systems in 2013, 2014, and 2015, and was
> the General Chair of the European Workshop on Microelectronics
> Education 2016. He is a member of the IEEE, IET and Fellow of the HEA.

</span>

# Short Talks

<span id="JIT_Debugging">

## Debugging a target-agnostic JIT compiler with GEM5

**Author:** Boris Shingarov - LabWare

We explain how GEM5 enabled us to develop a target-agnostic JIT
compiler, in which no knowledge about the target ISA is coded by the
human programmer; instead, the backend is inferred, using logic
programming, from a formal machine description written in a Processor
Description Language. Debugging such a JIT presents some challenges
which can not be addressed using traditional approaches. One such
challenge is the impedance mismatch between the high-level abstractions
in the PDL and the low-level inferred implementation. In this talk, we
present a new debugger based on simulating the execution of the target
runtime VM in GEM5; the debugger frontend connects to this simulation
using the RSP wire protocol.
</span>

<span id="COSSIM">

## COSSIM: An Integrated Solution to Address the Simulator Gap for Parallel Heterogeneous Systems

In an era of complex networked heterogeneous systems, simulating
independently only parts, components or attributes of a
system-under-design is not a viable, accurate or efficient option. The
interactions are too many and too complicated to produce meaningful
results and the optimization opportunities are severely limited when
considering each part of a system in an isolated manner. COSSIM offers a
framework that can handle the simulation of a complete system-of-systems
including processors, peripherals and networks that can appeal to
Parallel (Heterogeneous) Systems designers and application developers in
an integrated way.

The framework is based on gem5 as the main simulation engine for
processor-based systems and extends its capabilities by integrating it
with the OMNET++ network simulator. This integration allows independent
gem5 instances to be networked with all network protocols and
hierarchies that can be supported by OMNET++, thus creating a very
flexible solution. The integration of the two main simulation tools is
realized through the IEEE 1516 High-Level Architecture standard (HLA),
through which all communication tasks are performed. Through HLA and
custom libraries, a two-level (per node and global) synchronization
scheme is also implemented to ensure a coherent notion of time between
all nodes.

Since HLA is IP-based all gem5 instances and OMNET++ can be executed on
the same physical machine or on any distributed system (or any
combination in between). The overall framework – the set of gem5 nodes,
the OMNET++ simulator and the CERTI HLA – are integrated in a unified
Eclipse-based GUI that has been developed to provide easy simulation
set-up, execution and visualization of results. McPAT is also integrated
in a semi-automated way through the GUI in order to provide power and
energy estimations for each node, while OMNET++ provides power
estimations for networking-related components (NICs and network
devices).

> **Andreas Brokalakis** is a senior hardware engineer at Synelixis
> Solutions Ltd. At the same time he is pursuing a PhD degree at the
> Technical University of Crete, Greece. He holds a Bachelor degree in
> Computer Engineering from University of Patras, Greece and a Master’s
> Degree on Hardware/Software Co-design from the same university.
> Current work and research interests involve computer architecture and
> arithmetic, as well as design of ASIC and FPGA systems and
> accelerators.

> **Nikolaos Tampouratzis** is a PhD student at Technical University of
> Crete, working on simulation tools for computing systems. He has
> joined Telecommunication Systems Institute, Technical University of
> Crete since October 2012 as a research associate, providing research
> and development services to several EU-funded research projects. He
> received his Computer Science diploma from the University of Crete
> (UOC, Greece), with specialization in Hardware Design and FPGAs. He
> continued his studies in the Technical University of Crete (TUC
> Greece) where he received his Master Diploma in Electronic and
> Computer Engineering in which he specialized in Computer Architecture
> and Hardware Design.

</span>

<span id="ComplexSystems">

## Simulation of Complex Systems Incorporating Hardware Accelerators

The breakdown of Dennard scaling coupled with the persistently growing
transistor counts increased the importance of application-specific
hardware acceleration; such an approach offers significant performance
and energy benefits compared to general-purpose solutions. In order to
thoroughly evaluate such architectures, the designer should perform a
quite extensive design space exploration so as to evaluate the
trade-offs across the entire system. The design, until recently, has
been predominantly done using Register Transfer Level languages such as
Verilog and VHDL, which, however, lead to a prohibitively long and
costly design effort. In order to reduce the design time a wide range of
both commercial and academic High-Level Synthesis (HLS) tools have
emerged; most of these tools, handle hardware accelerators that are
described in synthesizable SystemC. The problem today, however, is that
most simulators used for evaluating the complete user applications (i.e.
full-system CPU/Mem/Peripheral simulators) lack any type of SystemC
accelerator support.

Within this context, we extend gem5 to support the simulation of generic
SystemC accelerators. We introduce a novel flow that enables us to
rapidly prototype synthesisable SystemC hardware accelerators in
conjunction with gem5. The proposed solution handles automatically all
communication and synchronisation issues.

Compared to a standard gem5 system, several changes at different levels
are required, from the OS and device drivers level down to the
implementation of a device model in the gem5 simulator. Instead of using
files to write data for an external accelerator, perform the simulation
and then read back the results, our approach communicates with the
SystemC simulator through programmed I/Os and DMA engines, supporting
full global synchronisation. Apart from the apparent benefits concerning
the implementation and simulation accuracy, the proposed solution is
also orders of magnitude faster.

> **Nikolaos Tampouratzis** is a PhD student at Technical University of
> Crete, working on simulation tools for computing systems. He has
> joined Telecommunication Systems Institute, Technical University of
> Crete since October 2012 as a research associate, providing research
> and development services to several EU-funded research projects. He
> received his Computer Science diploma from the University of Crete
> (UOC, Greece), with specialization in Hardware Design and FPGAs. He
> continued his studies in the Technical University of Crete (TUC
> Greece) where he received his Master Diploma in Electronic and
> Computer Engineering in which he specialized in Computer Architecture
> and Hardware Design.

</span>

<span id="TraceGeneration">

## Generating Synthetic Traffic for Heterogeneous Architectures

Modern system-on-chip architectures consist of many heterogeneous
processing elements. The communication fabric and memory hierarchy
supporting these processing elements heavily influence the system’s
overall performance. Exploring the design space of these heterogeneous
architectures with detailed models of each processing element can be
time-consuming. Statistical simulation has been shown to be an effective
tool for quickly evaluating architectures by abstracting away
complexity.

This talk describes work done on modelling the spatial and temporal
behaviour of a processing element’s address stream. We present a
methodology that can automatically characterize a processing element by
observing its reads and writes. Using these characteristics we can
stimulate a communication fabric connecting many different processing
elements by synthetically recreating their addresses. These addresses
arrive at their destination in the memory hierarchy, spawning new
messages and responses to read and write requests. Architects can now
combine ynthetic processing elements that represent various different
components on current and future systems-on-chip to evaluate the impact
of changes at the interconnection network and memory hierarchy.

> **Mario Badr** is a PhD Candidate at the University of Toronto working
> under the supervision of Dr. Natalie Enright Jerger. He received his
> B.A.Sc. and M.A.Sc from the University of Toronto in Electrical
> Engineering and Computer Engineering, respectively. He has interned
> with Qualcomm Research Silicon Valley and received the Roberto
> Padovani Scholarship for his outstanding technical contributions. In
> addition, he has been recognized at the university and departmental
> levels for excellence as a teaching assistant. His research interests
> include performance evaluation in computer architecture, heterogeneous
> architectures, and multi-threaded workloads.

</span>

<span id="StarterKit">

## ARM Research Starter Kit: System Modeling using gem5

ARM Research Enablement aims to enhance computing research by enabling
researchers worldwide to easily access ARM-based IP and technologies,
and helping them to increase their research impact. As a part of our
research enablement activities, we provide a System Modeling Research
Starter Kit using gem5. We have released a High Performance In-order
(HPI) CPU timing model based on ARMv8-A in gem5. I will present a
high-level overview of the released system, its documentation and
benchmark scripts. This talk will target those who are new to gem5 as
well as those who would like to promote gem5 in research.

> **Ashkan Tousi** is a Senior Research Engineer at ARM Cambridge and an
> Honorary Lecturer at the University of Glasgow. He received his PhD in
> computing science (parallel computing) in 2015. He currently leads
> research enablement activities at ARM, which cover a range of
> different research areas from SoC design to IoT and data science.

</span>

<span id="WA">

## Interacting with gem5 using workload-automation & devlib

Running workloads on gem5 is often not straightforward. This talk will
discuss workload-automation and devlib, 2 new open-source tools to
interact with gem5. These frameworks, written to interact with various
hardware platforms, have recently been extended to include gem5 as a
platform. We will discuss use cases and advantages/disadvantages of each
tool and show how they can make your gem5 work easier.

> **Anouk Van Laer** is a Modelling Engineer in Architecture: Systems &
> Technology group at ARM. She obtained her PhD at University College
> London, where she investigated the effects of optical interconnects on
> the performance of chip multiprocessors, using gem5.

</span>

<span id="PowerFramework">

## gem5: empowering the masses

This talk will give an overview of the state of power modelling in gem5.
After discussing the basic power modelling infrastructure, it will cover
the state of CPU DVFS as well as recent improvements in how CPU power
states are controlled for the ARM architecture in gem5. The talk will
cover these improvements in power modelling, highlighting the way in
which the accuracy and versatility of the simulator have been improved.

> **Sascha Bischoff** is a Senior Software Engineer in the Architecture:
> Systems & Technology group at ARM in Cambridge. Whilst completing his
> PhD with the University of Southampton, he spent 3.5 years based in
> ARM Research in Cambridge. He has spent a large part of the last 6
> years working with gem5, typically with a focus on power management,
> ideally without impacting the delivered
performance.

</span>

<span id="DRAMPower">

## Integrating and quantifying the impact of low power modes in the DRAM controller in gem5

Across applications, DRAM is a significant contributor to the overall
system power, with the DRAM access energy per bit up to three orders of
magnitude higher compared to on-chip memory accesses. To improve the
power efficiency, DRAM technology incorporates multiple low power modes,
each with different trade-offs between achievable power savings and
performance impact due to entry and exit delay requirements. Accurate
modeling of these low power modes and entry and exit control is crucial
to analyze the trade-offs across controller configurations and workloads
with varied memory access characteristics.

In this talk, we will give an overview of the decision making logic we
added to the DRAM controller in gem5 that triggers transitions to/from
the power-down modes. Integrating this functionality makes gem5 the
first publicly available DRAM low power full-system simulator, providing
the research community a tool for DRAM power analysis for a breadth of
use cases. We will conclude with simulation data that characterises the
low power behaviour and shows energy and performance trade-offs for
realistic workloads.

**Note:** This talk is based on a paper accepted at MEMSYS 17. Authors
from ARM: Radhika Jagtap, Wendy Elsasser and Andreas Hansson. Authors
from University of Kaiserslautern: Matthias Jung and Norbert Wehn.

> **Radhika Jagtap** is a Senior Research Engineer working in the Memory
> & Systems research group. She has plenty of experience with gem5
> (elastic traces, interconnect, memory controller) and is involved in
> several collaborative research projects, especially with academics.
> Currently she is exploring the problem of energy efficient data
> movement for sparse data workloads.

</span>

