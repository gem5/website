---
layout: documentation
title: "Replacement Policies"
doc: gem5 documentation
parent: memory_system
permalink: /documentation/general_docs/memory_system/replacement_policies/
author: Jason Lowe-Power
---

# Replacement Policies

Gem5 has multiple implemented replacement policies. Each one uses its
specific replacement data to determine a replacement victim on
evictions.

All of the replacement policies prioritize victimizing invalid blocks.

A replacement policy consists of a reset(), touch(), invalidate() and
getVictim() methods. Each of which handles the replacement data
differently.

-   reset() is used to initialize a replacement data (i.e., validate).
    It should be called only on entry insertion, and must not be called
    again until invalidation. The first touch to an entry must always be
    a reset().
-   touch() is used on accesses to the replacement data, and as such
    should be called on entry accesses. It updates the replacement data.
-   invalidate() is called whenever an entry is invalidated, possibly
    due to coherence handling. It makes the entry as likely to be
    evicted as possible on the next victim search. An entry does not
    need to be invalidated before a reset() is done. When the simulation
    starts all entries are invalid.
-   getVictim() is called when there is a miss, and an eviction must be
    done. It searches among all replacement candidates for an entry with
    the worst replacement data, generally prioritizing the eviction of
    invalid entries.

We briefly describe the replacement policies implemented in Gem5. If
further information is required, the [Cache Replacement Policies
Wikipedia page](https://en.wikipedia.org/wiki/Cache_replacement_policies), or the respective papers can be studied.

Random
------

The simplest replacement policy; it does not need replacement data, as
it randomly selects a victim among the candidates.

Least Recently Used (LRU) {#least_recently_used_lru}
-------------------------

Its replacement data consists of a last touch timestamp, and the victim
is chosen based on it: the oldest it is, the more likely its respective
entry is to be victimized.

Tree Pseudo Least Recently Used (TreePLRU) {#tree_pseudo_least_recently_used_treeplru}
------------------------------------------

A variation of the LRU that uses a binary tree to keep track of the
recency of use of the entries through 1-bit pointers.

Bimodal Insertion Policy (BIP) {#bimodal_insertion_policy_bip}
------------------------------

The [Bimodal Insertion Policy] is similar to the LRU, however, blocks
have a probability of being inserted as the MRU, according to a bimodal
throttle parameter (btp). The highest btp is, the highest is the
likelihood of a new block being inserted as MRU.

LRU Insertion Policy (LIP) {#lru_insertion_policy_lip}
--------------------------

The [LRU Insertion Policy][Bimodal Insertion Policy] consists of a LRU
replacement policy that instead of inserting blocks with the most recent
last touch timestamp, it inserts them as the LRU entry. On subsequent
touches to the block, its timestamp is updated to be the MRU, as in LRU.
It can also be seen as a BIP where the likelihood of inserting a new
block as the most recently used is 0%.

Most Recently Used (MRU) {#most_recently_used_mru}
------------------------

The Most Recently Used policy chooses replacement victims by their
recency, however, as opposed to LRU, the newest the entry is, the more
likely it is to be victimized.

Least Frequently Used (LFU) {#least_frequently_used_lfu}
---------------------------

The victim is chosen using the reference frequency. The least referenced
entry is chosen to be evicted, regardless of the amount of times it has
been touched, or how long has passed since its last touch.

First-In, First-Out (FIFO) {#first_in_first_out_fifo}
--------------------------

The victim is chosen using the insertion timestamp. If no invalid
entries exist, the oldest one is victimized, regardless of the amount of
times it has been touched.

Second-Chance {#second_chance}
-------------

The [Second-Chance] replacement policy is similar to FIFO, however
entries are given a second chance before being victimized. If an entry
would have been the next to be victimized, but its second chance bit is
set, this bit is cleared, and the entry is re-inserted at the end of the
FIFO. Following a miss, an entry is inserted with its second chance bit
cleared.

Not Recently Used (NRU) {#not_recently_used_nru}
-----------------------

Not Recently Used (NRU) is an approximation of LRU that uses a single
bit to determine if a block is going to be re-referenced in the near or
distant future. If the bit is 1, it is likely to not be referenced soon,
so it is chosen as the replacement victim. When a block is victimized,
all its co-replacement candidates have their re-reference bit
incremented.

Re-Reference Interval Prediction (RRIP) {#re_reference_interval_prediction_rrip}
---------------------------------------

[Re-Reference Interval Prediction (RRIP)] is an extension of NRU that
uses a re-reference prediction value to determine if blocks are going to
be re-used in the near future or not. The higher the value of the RRPV,
the more distant the block is from its next access. From the original
paper, this implementation of RRIP is also called Static RRIP (SRRIP),
as it always inserts blocks with the same RRPV.

Bimodal Re-Reference Interval Prediction (BRRIP) {#bimodal_re_reference_interval_prediction_brrip}
------------------------------------------------

[Bimodal Re-Reference Interval Prediction
(BRRIP)][Re-Reference Interval Prediction (RRIP)] is an extension of
RRIP that has a probability of not inserting blocks as the LRU, as in
the Bimodal Insertion Policy. This probability is controlled by the
bimodal throtle parameter (btp).

  [Second-Chance]: https://apps.dtic.mil/docs/citations/AD0687552
  [Re-Reference Interval Prediction (RRIP)]: https://dl.acm.org/citation.cfm?id=1815971
  [Cache Replacement Policies Wikipedia page]: https://en.wikipedia.org/wiki/Cache_replacement_policies
  [Bimodal Insertion Policy]: https://dl.acm.org/citation.cfm?id=1250709

