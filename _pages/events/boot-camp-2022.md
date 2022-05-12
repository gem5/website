---
title: "gem5 Boot Camp 2022"
permalink: events/boot-camp-2022
---

We are happy to announce the first gem5 Boot Camp, to be held at UC Davis from July 11th to July 15th 2022.
The purpose of the gem5 Boot Camp is for junior computer architecture researchers, particularly PhD. students, to learn how to use gem5 in their projects.
The Boot Camp, held over 5 days, will take attendees through setting up basic system simulations, creating bespoke components, learning to interpret gem5 stats, and up to running and modifying simulations comparable to real-world systems.

**This event is free for all accepted attendees**. There is no cost for registration.
Accommodation and meals will be provided, and travel grants will be available.

## Key Dates

* Boot camp: **July 11th to July 15th 2022**
* Application deadline: **May 18th 2022** (Apply [here](https://forms.gle/3wWPsMDfXyaChmQ68))

## When and where is the Boot Camp?

The Boot Camp will be held from July 11th to July 15th 2022 at UC Davis in Davis, California.
Attendees will attend workshop sessions each day, typically from 9AM to 5PM.
Accommodation will be sponsored by NSF from July 10th to July 16th (6 nights).

## What should attendees expect?

There will be 5 full days of workshop activities centered around learning gem5.
The workshop will start with the assumption of no prior experience using gem5 and aims to go give attendees a solid and broad foundation of knowledge of gem5 in carrying out computer architecture research.

The workshop will give attendees the opportunity to:

* Learn how to create SimObjects.
* Learn how to use the gem5 Standard Library to create simulations.
* Get to grips with gem5art.
* Understand the gem5 statistics module and how to use it in your experiments.
* Create full system simulations capable of running real-world operating systems and software benchmarks.
* Network with others in the computer architecture research community.

And much, much more!

Breakfast, lunch, and dinner will be provided, as well as afternoon snacks.
Attendees will be hosted on campus with evening social events planned.

## Who can apply?

Anyone can apply though, as spaces are limited, preference will be given to early career researchers (e.g., first or second year PhD and masters students planning on applying for a PhD).
We especially encourage those from non-research universities, minority serving institutions, and universities without PhD programs to apply.

## How can I apply?

Those wishing to attend can fill out the following Google Form by **May 18th**: <https://forms.gle/3wWPsMDfXyaChmQ68>

If your application was successful you will be contacted, via the email address provided, by June 1st.

## What does it cost?

This event is sponsored by the NSF.
There will be no cost to attend.
Accommodation on the UC Davis campus, meals, and social events will be provided as part of the event.

We will be offering travel grants which can be applied for to cover transport expenses after the event.

## Tentative schedule

|Session| Topic | Objectives|
| :---  | :---  | :--- |
| Monday Morning | Welcome and Introduction | |
| | Building gem5 |- Learn about the gem5 dependencies <br> - Be introduced to SCons <br> - Understand the different gem5 binary types (opt, debug, fast)|
| | Python basics | - A recap of basic Python skills needed to use gem5 <br> - Object-oriented programming reminder <br> - Run a simple python script in gem5 |
| | Using gem5 basics | - Understand gem5 configuration scripts and its python interpreter <br> - Understand what the `m5` and `gem5` libraries are <br> - Get a general architecture outline of gem5 <br> - Obtain and understand the stats output <br> - Understand the `config.ini` file |
| | About simulation | - Learn about common gem5 terminology: "host", "guest", etc. <br> - Learn about the difference between Full-System and Syscall emulation mode |
| Monday Afternoon | The gem5 standard library | - Use the stdlib components to build a simulated system <br> - Use the stdlib `resource` class to automatically obtain gem5-resources to use in their experiment <br> - Create a gem5 resource custom resource <br> - Set workloads for a simulated system via the `set_workload` functions <br> - Create functions to run on specific exit events <br> - Create an stdlib component|
| | **Welcome dinner** | |
|Tuesday Morning | Using gem5 models | - Use different gem5 CPU models (Timing Simple, Atomic, O3, Minor, Trace, etc.) <br> - Use classic caches in a simulation <br> - Use Ruby caches in a simulation (understand the different coherence protocols, how to compile them and how to create a cache hierarchy via a simple network) |
| | Using gem5 to run things | - Use traffic generators to test memory systems <br> - Incorporate the m5 utility into workloads <br> - Learn to use cross-compilers for non-host ISA workloads <br> - Learn how to output and parse stats|
| Tuesday Afternoon| Full system simulation | - Create a disk image for FS simulations <br> - Create and add and modify gem5 resources <br> - Learn how to use the `m5 readfile` interface|
| | Accelerating Simulation | - Create checkpoints <br> - Load from checkpoints <br> - Fastforward a simulation <br> - Employ sampling techniques <br> - Learn about KVM |
| Wednesday Morning| Creating your own SimObjects| - Understand how a request travels through the system <br> - Implement a SimObject <br> - Learn how to model real-world hardware timing <br> - Learn how to add SimStats and how it maps to real-world hardware <br> - Debug a gem5 SimObject |
| Wednesday Afternoon| Adding your own instructions| - Understand the details of the ISA sub-system <br> - Extend gem5 to simulate an unsupported instruction <br> - Understand the differences between modeling a user-mode and supervisor mode instruction <br> - Understand gem5 debug traces for a particular execution |
| Thursday Morning | Advanced topics in memory systems | - Learn how to extend a packet with a new MemCmd <br> - Learn how to use Garnet (How to create different network topologies with specific characteristics; using the Garnet synthetic traffic; and understanding the output statistics) <br> -  Create and extend cache coherence protocols (create a classic coherence protocol; design a Ruby coherence protocol)|
| Thursday Afternoon | The gem5 GPU Model | [TBD] |
| | **Group Social Event** | |
| Friday Morning | Writing tests and contributing to gem5 | - Write a GTest to test a piece of CPP code <br> - Write a PyUnit test to test a python function <br> - Use testlib to test a gem5 simulation condition <br> - Run Testlib/PyUnit/GUnit tests for gem5 <br> - Understand gem5's quick/Kokoro, long/Nightly, very-long/Weekly test structure <br> - Understand gem5's code-formatting guidelines <br> - Use git to add code to the repo <br> - Review patches on Gerrit <br> - Respond to feedback on Gerrit |
| Friday Afternoon | gem5 extensions and other simulators | - Incorporate SST into a simulation <br> - Incorporate DRAMSim into a simulation <br> - Use SystemC in gem5 and gem5 in SystemC |
| | Wrapping things up | |
