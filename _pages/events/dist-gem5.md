---
title: "ISCA2017 - distributed gem5"
date: 2018-05-13T17:02:19-04:00
draft: false
weight: 10
---

<big>

<center>

**Title: dist-gem5: Modeling and Simulating a Distributed Computer
System Using Multiple Simulation**

**Sunday, June 25, 9:00 to 12:30**

**`44th`` ``International`` ``Symposium`` ``on`` ``Computer``
``Architecture,`` ``June`` ``24-28,`` ``2017,`` ``Toronto,`` ``ON,``
``Canada`**

</center>

</big>

-----

__TOC__

## List of organisers/presenters

  - Nam Sung Kim, University of Illinois, Urbana-Champaign
  - Mohammad Alian, University of Illinois, Urbana-Champaign
  - Nikos Nikoleris, ARM Ltd.
  - Radhika Jagtap, ARM Ltd.
  - Gabor Dozsa, ARM Ltd.
  - Stephan Diestelhorst, ARM Ltd.

## Abstract

The single-thread performance improvement of processors has been
sluggish for the past decade as Dennard’s scaling is approaching its
fundamental physical limit. Thus, the importance of efficiently running
applications on a **parallel/distributed computer system** has continued
to increase and diverse applications based on parallel/distributed
computing models such as MapReduce and MPI have thrived.

In a parallel/distributed computing system, the complex interplay
amongst processor, node, and network architectures strongly affects the
performance and power efficiency. In particular, we observe that all the
hardware and software aspects of the network, which encompasses
interface technology, switch/router capability, link bandwidth,
topology, traffic patterns, and protocols, significantly impact the
processor and node activities. Therefore, to maximize performance and
power efficiency, it is critical to develop various optimization
strategies cutting across processor, node, and network architectures, as
well as their software stacks, necessitating **full-system simulation**.
However, our community lacks a proper research infrastructure to study
the interplay of these subsystems. Facing such a challenge, we have
released a gem5-based simulation infrastructure dubbed **dist-gem5** to
support full-system simulation of a parallel/distributed computer system
using multiple simulation host. This tutorial will cover an introduction
to dist-gem5 including relevant background knowledge.

## Objectives

![Packet-forwarding-highlevel.png](Packet-forwarding-highlevel.png
"Packet-forwarding-highlevel.png")

More specifically, the tutorial will provide the following.

  - Introduction of parallel/distributed system architecture.
  - Details of enhanced gem5 components to enable simulation of a
    parallel/distributed computer system.
      - Network interface and switch models to connect multiple
        simulated nodes (as shown in the Figure).
      - Synchronization amongst multiple simulated nodes running across
        multiple simulation hosts.
      - Simulating a region of interest of a given benchmark using
        check-point creation/restoration enhanced for simulating
        multiple simulated nodes using multiple simulation hosts.
  - Examples of modeling parallel/distributed computer systems using a
    few network topologies.

|               |                              |
| ------------- | ---------------------------- |
| 09:00 – 10:00 | Introduction (60 min)        |
| 10:00 – 10:15 | Break (15 min)               |
| 10:15 – 11:15 | dist-gem5 deep dive (60 min) |
| 11:15 – 11:30 | Break (15 min)               |
| 11:30 – 12:00 | dist-gem5 examples (30 min)  |

Program for the tutorial

## Slides

  - The slides from the tutorial can be downloaded
    [here](:file:isca2017-dist-gem5.pdf "wikilink").

## Publications

  - Mohammad Alian, Gabor Dozsa, Umur Darbaz, Stephan Diestelhorst,
    Daehoon Kim, and Nam Sung Kim. *“dist-gem5: Distributed Simulation
    of Computer Clusters”*, IEEE International Symposium on Performance
    Analysis of Systems (ISPASS), April 2017 (Nominated for the Best
    Paper Award)

<!-- end list -->

  - Mohammad Alian, Daehoon Kim, and Nam Sung Kim. *“pd-gem5: Simulation
    Infrastructure for Parallel/Distributed Computer Systems”*, IEEE
    Computer Architecture Letters (CAL), Jan 2016
    [paper](http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7114236)

<!-- end list -->

  - [**dist-gem5 website**](https://publish.illinois.edu/icsl-pdgem5/)

## Pre-requisites

  - Basic knowledge of computer architecture
  - No prior experience with simulators is required

## Previous tutorials

  - [dist-gem5 tutorial at
    MICRO 2015](https://publish.illinois.edu/icsl-pdgem5/micro-48-tutorial/)
  - [gem5 tutorial at ASPLOS 2017](http://gem5.org/ASPLOS2017_tutorial)
