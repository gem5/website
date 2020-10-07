---
layout: documentation
title: Learning gem5
doc: Learning gem5
parent: learning_gem5
permalink: /documentation/learning_gem5/introduction/
author: Jason Lowe-Power
---

# Introduction

The goal of this document is to give you a thorough
introduction on how to use gem5 and the gem5 codebase. The purpose of
this document is not to provide a detailed description of every feature
in gem5. After reading this document, you should feel comfortable using
gem5 in the classroom and for computer architecture research.
Additionally, you should be able to modify and extend gem5 and then
contribute your improvements to the main gem5 repository.

This document is colored by my personal experiences with gem5 over the
past six years as a graduate student at the University of
Wisconsin-Madison. The examples presented are just one way to do it.
Unlike Python, whose mantra is "There should be one-- and preferably
only one --obvious way to do it." (from The Zen of Python. See
[The Zen of Python](https://www.python.org/dev/peps/pep-0020/#the-zen-of-python){:target="_blank"}), in gem5 there are a number of different ways to
accomplish the same thing. Thus, many of the examples presented in this
book are my opinion of the best way to do things.

One important lesson I have learned (the hard way) is when using complex
tools like gem5, it is important to actually understand how it works
before using it.

You can find the source for this book at
<https://gem5.googlesource.com/public/gem5-website/+/refs/heads/stable/_pages/documentation/learning_gem5/>.

## What is gem5?

gem5 is a modular discrete event driven computer system simulator platform. That means that:

1. gem5's components can be rearranged, parameterized, extended or replaced easily to suit your needs.
2. It simulates the passing of time as a series of discrete events.
3. Its intended use is to simulate one or more computer systems in various ways.
4. It's more than just a simulator; it's a simulator platform that lets you use as many of its premade components as you want to build up your own simulation system.

gem5 is written primarily in C++ and python and most components are provided under a BSD style license.
It can simulate a complete system with devices and an operating system in full system mode (FS mode), or user space only programs where system services are provided directly by the simulator in syscall emulation mode (SE mode).
There are varying levels of support for executing Alpha, ARM, MIPS, Power, SPARC, RISC-V, and 64 bit x86 binaries on CPU models including two simple single CPI models, an out of order model, and an in order pipelined model.
A memory system can be flexibly built out of caches and crossbars or the Ruby simulator which provides even more flexible memory system modeling.

There are many components and features not mentioned here, but from just this partial list it should be obvious that gem5 is a sophisticated and capable simulation platform.
Even with all gem5 can do today, active development continues through the support of individuals and some companies, and new features are added and existing features improved on a regular basis.

## Capabilities out of the box
gem5 is designed for use in computer architecture research, but if you're trying to research something new and novel it probably won't be able to evaluate your idea out of the box. If it could, that probably means someone has already evaluated a similar idea and published about it.

To get the most out of gem5, you'll most likely need to add new capabilities specific to your project's goals. gem5's modular design should help you make modifications without having to understand every part of the simulator.

As you add the new features you need, please consider contributing your changes back to gem5. That way others can take advantage of your hard work, and gem5 can become an even better simulator.

## Asking for help
gem5 has two main mailing lists where you can ask for help or advice.
gem5-dev is for developers who are working on the main version of gem5.
This is the version that's distributed from the website and most likely what you'll base your own work off of.
gem5-users is a larger mailing list and is for people working on their own projects which are not, at least initially, going to be distributed as part of the official version of gem5.

Most of the time, gem5-users is the right mailing list to use.
Most of the people on gem5-dev are also on gem5-users including all the main developers, and in addition many other members of the gem5 community will see your post.
That helps you because they might be able to answer your question, and it also helps them because they'll be able to see the answers people send you.
To find more information about the mailing lists, to sign up, or to look through archived posts visit [Mailing Lists](/mailing_lists).

Before reporting a problem on the mailing list, please read [Reporting Problems](/documentation/reporting_problems).
