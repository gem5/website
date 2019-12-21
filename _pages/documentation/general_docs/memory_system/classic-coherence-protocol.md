---
layout: documentation
title: "Classic memory system coherence"
doc: gem5 documentation
parent: memory_system
permalink: /documentation/general_docs/memory_system/classic-coherence-protocol/
author: Jason Lowe-Power
---

# Classic Memory System coherence

M5 2.0b4 introduced a substantially rewritten and streamlined cache
model, including a new coherence protocol. (The old pre-2.0 cache model
had been patched up to work with the new [Memory
System](/documentation/general_docs/memory_system/) introduced in 2.0beta, but not
rewritten to take advantage of the new memory system's features.)

The key feature of the new coherence protocol is that it is designed to
work with more-or-less arbitrary cache hierarchies (multiple caches each
on multiple levels). In contrast, the old protocol restricted sharing to
a single bus.

In the real world, a system architecture will have limits on the number
or configuration of caches that the protocol can be designed to
accommodate. It's not practical to design a protocol that's fully
realistic and yet efficient for arbitrary configurations. In order to
enable our protocol to work on (nearly) arbitrary configurations, we
currently sacrifice a little bit of realism and a little bit of
configurability. Our intent is that this protocol is adequate for
researchers studying aspects of system behavior other than coherence
mechanisms. Researchers studying coherence specifically will probably
want to replace the default coherence mechanism with implementations of
the specific protocols under investigation.

The protocol is a MOESI snooping protocol. Inclusion is **not**
enforced; in a CMP configuration where you have several L1s whose total
capacity is a significant fraction of the capacity of the common L2 they
share, inclusion can be very inefficient.

Requests from upper-level caches (those closer to the CPUs) propagate
toward memory in the expected fashion: an L1 miss is broadcast on the
local L1/L2 bus, where it is snooped by the other L1s on that bus and
(if none respond) serviced by the L2. If the request misses in the L2,
then after some delay (currently set equal to the L2 hit latency), the
L2 will issue the request on its memory-side bus, where it will possibly
be snooped by other L2s and then be issued to an L3 or memory.

Unfortunately, propagating snoop requests incrementally back up the
hierarchy in a similar fashion is a source of myriad nearly intractable
race conditions. Real systems don't typically do this anyway; in general
you want a single snoop operation at the L2 bus to tell you the state of
the block in the whole L1/L2 hierarchy. There are a handful of methods
for this:

1.  just snoop the L2, but enforce inclusion so that the L2 has all the
    info you need about the L1s as well---an idea we've already rejected
    above
2.  keep an extra set of tags for all the L1s at the L2 so those can be
    snooped at the same time (see the Compaq Piranha)---reasonable, if
    you're hierarchy's not too deep, but now you've got to size the tags
    in the lower-level caches based on the number, size, and
    configuration of the upper-level caches, which is a configuration
    pain
3.  snoop the L1s in parallel with the L2, something that's not hard if
    they're all on the same die (I believe Intel started doing this with
    the Pentium Pro; not sure if they still do with the Core2 chips or
    not, or if AMD does this as well, but I suspect so)---also
    reasonable, but adding explicit paths for these snoops would also
    make for a very cumbersome configuration process

We solve this dilemma by introducing "express snoops", which are special
snoop requests that get propagated up the hierarchy instantaneously and
atomically (much like the atomic-mode accesses described on the [Memory
System](/documentation/general_docs/memory_system) page), even when the system is running
in timing mode. Functionally this behaves very much like options 2 or 3
above, but because the snoops propagate along the regular bus
interconnects, there's no additional configuration overhead. There is
some timing inaccuracy introduced, but if we assume that there are
dedicated paths in the real hardware for these snoops (or for
maintaining the additional copies of the upper-level tags at the
lower-level caches) then the differences are probably minor.

(More to come: how does a cache know when its request is completed? and
other fascinating questions...)

Note: there are still some bugs in this protocol as of 2.0b4,
particularly if you have multiple L2s each with multiple L1s behind it,
but I believe it works for any configuration that worked in 2.0b3.

