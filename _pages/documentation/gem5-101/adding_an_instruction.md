---
layout: documentation
title: Adding An Instruction
doc: gem5 101
permalink: /adding_an_instruction/
author: Jason Lowe-Power
date: 2018-05-12T23:00:45-04:00
---

## Part 2 Adding An Instruction
For part II, we had used gem5 capabilities straight out of the box. Now,
we will witness the flexibility and usefulness of gem5 by extending the
simulator functionality. We walk you through the implementation of an
x86 instruction (FSUBR), which is currently missing from gem5. This will
introduce you to gem5's language for describing instruction sets, and
illustrate how instructions are decoded and broken down into micro-ops
which are ultimately executed by the processor.
