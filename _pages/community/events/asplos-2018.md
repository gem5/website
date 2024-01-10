---
title: "ASPLOS 2018"
date: 2020-02-04T14:54:41-07:00
draft: false
permalink: events/asplos-2018
---

# Learning gem5 Tutorial at ASPLOS 2018

Thanks to all of those who attended the tutorial! Links to the slides and videos are below.

 - Part 1: [Slides](/_pages/static/events/learning gem5 - part 1.pdf) and [Video](https://www.youtube.com/watch?v=wo4b9FPEiHk)
 - Part 2: [Slides](/_pages/static/events/learning gem5 - part 2.pdf) and [Video 1](https://www.youtube.com/watch?v=SEiOsMmG5qo) [Video 2](https://www.youtube.com/watch?v=eiliJz_YsG4)
 - Part 3: [Slides](/_pages/static/events/learning gem5 - part 3.pdf) and [Video](https://www.youtube.com/watch?v=XTIrVBb86aM)
 - Part 4: [Slides](/_pages/static/events/learning gem5 - part 4.pdf) and [Video](https://www.youtube.com/watch?v=JFC0km8zPbw)
 - Part N: [Slides](/_pages/static/events/learning gem5 - other.pdf)

We will be hosting a Learning gem5 tutorial at [ASPLOS 2018](http://asplos2018.org/) in Williamsburg, VA on March 24th.

gem5 is used by an incredible number of architecture researchers. The gem5 paper has been cited over 2000 times according to Google Scholar. However, gem5 is a unique software infrastructure; as a user, you also have to be a developer. Currently, there are few resources for young computer architects to learn how to productively use gem5.

This tutorial builds off of the [Learning gem5 book](/documentation/learning_gem5/introduction) and will introduce junior architecture students to the inner workings of gem5 so they can be more productive in their future research. The goal of the "tutorial" section of this tutorial is not to introduce attendees to every feature of gem5, but to give them a framework to succeed when using gem5 in their future research.

After spending the morning learning about the basics of how gem5 works, the afternoon will be a series of invited talks from users who have experience using gem5 on "gem5 best practices". This will cover a variety of topics including the basics of computer architecture research, software development practices, and how to contribute to the gem5 open source project.

This tutorial is perfect for beginning graduate students or other computer architecture researchers to get started using one of the architecture communities most popular too.

This page is under development. It will be updated often leading up to the day of the tutorial. Hope to see you there!
### Preparing for the tutorial

To get the most out of this tutorial, you are encouraged to bring a laptop to work along. This will be an interactive tutorial, with many coding examples. Additionally, by bringing a laptop, you will be able to easily participate in the afternoon coding sprint.

While this tutorial is appropriate for you even if you've never used gem5 before, you'll get more out of it if you familiarize yourself with gem5 before coming. Specifically, by downloading gem5 and making sure it builds on your system you will save yourself a lot of time. Reading and completing the [first chapter from the the Learning gem5 book](http://www.gem5.org/documentation/learning_gem5/part1/building/) before coming to the tutorial is strongly encouraged.
### Audience

The primary audience is junior computer architecture researchers (e.g., first or second year graduate students) who are planning on using gem5 for future architecture research. We also invite others who want a high-level idea of how gem5 works and its applicability to architecture research.
# Schedule

## Morning Schedule: Learning gem5 8:30 – 10:00

 - Breakfast 7:00 – 8:30
 - What is gem5 and history
 - Getting started with gem5
    - Overall (software) architecture of gem5
    - Compiling gem5
    - Simple introduction script
    - First time running gem5
    - Interpreting gem5's output
    - Simple assembly example to show debug trace of everything
 - Extending gem5
    - Structure of C++ code
    - Writing a simple SimObject
 - BREAK 10:00 – 10:30
    - Discrete event simulation programming
    - SimObject parameters
    - gem5 memory system
    - Overview of simple cache implementation

## Lunch (Provided) 12:00 – 1:30
## Advanced Learning gem5 topics 1:30 – 3:30

 - Building a CPU model in gem5
    - ISAs and CPU model ISA relation
    - Overview of different CPU models
    - Building a simple CPU model
 - Coherence protocols with Ruby
    - Intro to Ruby
    - Simple MSI protocol
    - Configuring Ruby
    - Debugging Ruby protocols
 - Quick overview of other gem5 topics
    - Overview of full system simulation
    - Briefly gem5's other features
    - gem5 limitations
 - BREAK 3:30 – 4:00

## gem5 Best Practices 4:00 – 5:00

 - Developing and contributing to gem5

   This will cover an quick introduction to [git](https://git-scm.com/), best practices for contributing, how to test gem5, and how to use [gem5's code review site](https://gem5-review.googlesource.com/).
 - Ryota Shioya: Visualizing the out-of-order CPU model

   Konata is a new CPU pipeline viewer and has many useful features not in the previous text-based viewer. This talk will explain how to use the new viewer and best practices in gem5. [https://github.com/shioyadan/Konata/releases]

   [Link to presentation](http://learning.gem5.org/tutorial/presentations/vis-o3-gem5.pdf)
 - Éder F. Zulian: Using gem5 for Memory Research

   This talk provides an overview of our experiences with the gem5 simulator at the Microelectronic System Design Research Group of the TU Kaiserslautern. It begins with our motivation and use cases for applying gem5. Then we jump ahead to a brief description of innovations introduced by our research group and partners.

   The span of topics covers the DRAM power model used by gem5 (DRAMPower), which is being currently extended and maintained by our group. Furthermore, we show how a simple HMC memory model can be built from native objects provided by gem5, the configuration parameters are generated by our DRAMSpec tool.

   Moreover, we present how gem5 can be coupled to SystemC/TLM2.0 based modules, an interesting approach for industry to reuse in-house and third-party SystemC modules together with gem5. Finally, we close the session showing a bunch of useful scripts, called gem5 Tips and Tricks, for setting up and breaking the ice with gem5.

   [Link to presentation](http://learning.gem5.org/tutorial/presentations/gem5_mem_research.pdf)

Open forum for questions and feedback 5:00 – 5:30
