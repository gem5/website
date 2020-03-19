---
layout: documentation
title: gem5 documentation
doc: gem5 documentation
parent: gem5_documentation
permalink: /documentation/
author: Jason Lowe-Power
---

# gem5 Documentation

## Learning gem5

[Learning gem5](learning_gem5/introduction/) gives a prose-heavy introduction to using gem5 for computer architecture research written by Jason Lowe-Power.
This is a great resource for junior researchers who plan on using gem5 heavily for a research project.

It covers details of how gem5 works starting with [how to create configuration scripts](learning_gem5/part1/simple_config).
It then goes on to describe [how to modify and extend](learning_gem5/part2/environment) gem5 for your research including [creating `SimObjects`](learning_gem5/part2/helloobject), [using gem5's event-driven simulation infrastructure](learning_gem5/part2/events), and [adding memory system objects](learning_gem5/part2/memoryobject).
In [Learning gem5 Part 3](learning_gem5/part3/MSIintro) the [Ruby cache coherence model](/documentation/general_docs/ruby) is discussed in detail including a full implementation of an MSI cache coherence protocol.

More Learning gem5 parts are coming soon including:
* CPU models and ISAs
* Debugging gem5
* **Your idea here!**

Note: this has been migrated from learning.gem5.org and there are minor problems due to this migration (e.g., missing links, bad formatting).
Please contact Jason (jason@lowepower.com) or create a PR if you find any errors!

## gem5 101

[gem5 101](learning_gem5/gem5_101) is a set of assignments mostly from Wisconsin's graduate computer architecture classes (CS 752, CS 757, and CS 758) which will help you learn to use gem5 for research.

## gem5 API documentation

You can find the doxygen-based documentation here: <http://doxygen.gem5.org/release/current/index.html>

## Other general gem5 documentation

See the navigation on the left side of the page!
