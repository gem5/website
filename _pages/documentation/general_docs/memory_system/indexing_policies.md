---
layout: documentation
title: "Indexing Policies"
doc: gem5 documentation
parent: memory_system
permalink: /documentation/general_docs/memory_system/indexing_policies/
author: Jason Lowe-Power
---

# Indexing Policies

Indexing policies determine the locations to which a block is mapped
based on its address.

The most important methods of indexing policies are getPossibleEntries()
and regenerateAddr():

-   getPossibleEntries() determines the list of entries a given address
    can be mapped to.
-   regenerateAddr() uses the address information stored in an entry to
    determine its full original address.

For further information on Cache Indexing Policies, please refer to the
wikipedia articles on [Placement Policies](https://en.wikipedia.org/wiki/Cache_Placement_Policies) and
[Associativity](https://en.wikipedia.org/wiki/CPU_cache#Associativity%7C).

Set Associative {#set_associative}
---------------

The set associative indexing policy is the standard for table-like
structures, and can be further divided into Direct-Mapped (or 1-way
set-associative), Set-Associative and Full-Associative (N-way
set-associative, where N is the number of table entries).

A set associative cache can be seen as a skewed associative cache whose
skewing function maps to the same value for every way.

Skewed Associative {#skewed_associative}
------------------

The skewed associative indexing policy has a variable mapping based on a
hash function, so a value x can be mapped to different sets, based on
the way being used. Gem5 implements skewed caches as described in
["Skewed-Associative
Caches", from Seznec et al](https://www.researchgate.net/publication/220758754_Skewed-associative_Caches).

Note that there are only a limited number of implemented hashing
functions, so if the number of ways is higher than that number then a
sub-optimal automatically generated hash function is used.
