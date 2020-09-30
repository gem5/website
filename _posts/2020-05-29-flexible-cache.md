---
layout: post
title:  "A flexible cache coherency protocol for the Ruby memory system"
author: Tiago Mück
date:   2020-05-29
---

Gem5's Ruby memory subsystem provides flexible on-chip network models and
multiple cache coherency protocols modeled in detail. However, simple
experiments are sometimes difficult to pull off. For instance, modifying an
existing configuration by just adding another shared cache level requires
either:

1. switching to an entirely new protocol that models the desired cache hierarchy;
2. or modify an existing protocol;

While (1) is not always an option, (2) is a non-trivial task since Ruby
protocols can be very complex and hard to debug. This creates a major
flexibility gap between gem5 "classic" memory sub-system and Ruby.

# New protocol implementation

We are working on a new protocol implementation that aims at addressing this
configurability limitation. Our new protocol provides a single cache controller
that can be reused at multiple levels of the cache hierarchy and configured to
model multiple instances of MESI and MOESI cache coherency protocols. This
implementation is based of [Arm's AMBA 5 CHI specification](
https://static.docs.arm.com/ihi0050/d/IHI0050D_amba_5_chi_architecture_spec.pdf)
and provides a scalable framework for the design space exploration of large SoC
designs.

# Presentation

To known more please take a look at our workshop presentation:

<iframe width="960" height="540" src="https://www.youtube.com/embed/OOEqCZekJbA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="max-width: 960px;"></iframe>
