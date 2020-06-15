---
layout: post
title:  "Town Hall Meeting notes"
author: Bobby R. Bruce
date:   15-06-2020
---

On Wednesday June 3rd the gem5 Workshop Town hall was held.

This session was recorded and is publicly available for viewing:

<iframe width="560" height="315"
src="https://www.youtube.com/embed/fvCXmMBblZY" frameborder="0"
allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
allowfullscreen></iframe>

Noted below are the highlights from the meeting:

* A question was raised about minor releases. While we are open to the idea of
releasing minor versions of gem5, we have no immediate plans to do so in the
near future. We will continue to focus efforts on the next major version of
gem5; to be released in the next few months.
* The project intends to provide "good known configurations" which are
tested against, and known to be realistic simulations of, real-world hardware.
* To produce a faster product, it was suggested that gem5 could be
paralleized. This is considered a task requiring significant engineering
effort. As such, we have no intention of doing so as part of any foreseeable
release.
* The stats package was discussed at length, particularly the fact that its
output is confusing.
    * Stats documentation is accepted to be lacking and should be improved.
    * A suggestion was raised to include a stats parser in the code-base. There
was general agreement this would be beneficial.
    * A JSON stats output format is now available, though not all SimObjects
have been converted for it to function correctly in all cases.
* Testing SimObjects was raised as a pain-point.
    * A test harness for SimObjects would be of benefit; one that would
permit the creation of unit tests for SimObjects.
    * Better SimObject testing plays into gem5's broader desire to improve
testing overall.
* Some complained about gem5's code format checking.
    * We could provide a clang format checker config as part of the gem5
code-base.
    * Some policies could be relaxed, particularly those regarding the C/C++
header files which are, in some cases, non-standard.
    * A general move towards more standardized C/C++ code-style standards would
be beneficial overall.
* It was noted that the clang address sanitizer should be run more frequently.
Though these were run prior to the release of gem5-20, regular checks could
catch bugs earlier in development.
* Many in the community are are interested in the simulated performance. Going
forward, this should be noted on the gem5 benchmark page. This data will enable
us to understand whether our performance is degrading or improving over time.
    * There were suggestions that simulated performance should be regularly,
and automatically, tested in order to flag changes that result in degraded
performance. However, it is unknown how this can be achieved.
* FlexCPU should be merged into the gem5 code-base.
* In a discussion regarding O3CPU; it was generally accepted that it is very
out-of-date and needs considerable improvements.
* PCI/PCIe support is desired by some but most agreed it should not be a top
priority.
* Multicore simulation is agreed to have problems and, generally, needs to be
better supported.
* A question was raised asking if SE mode will eventually be dropped. While we
will continue to improve FS mode, we wish to maintain SE mode as it can be
used to run faster simulations in cases where full-system simulation is not
required.
    * There is on-going engineering efforts to consolidate the SE and FS code
in order to lessen the maintenance burden associated with supporting both modes
of usage.
