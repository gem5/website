---
layout: documentation
title: "Garnet standalone"
doc: gem5 documentation
parent: ruby
permalink: /documentation/general_docs/ruby/Garnet_standalone/
author: Jason Lowe-Power
---

# Garnet Standalone

This is a dummy cache coherence protocol that is used to operate Garnet
in a standalone manner. This protocol works in conjunction with the
[Garnet Synthetic Traffic](/documentation/general_docs/ruby/garnet_synthetic_traffic)
injector.

### Related Files

  - **src/mem/protocols**
      - **Garnet_standalone-cache.sm**: cache controller specification
      - **Garnet_standalone-dir.sm**: directory controller
        specification
      - **Garnet_standalone-msg.sm**: message type specification
      - **Garnet_standalone.slicc**: container file

### Cache Hierarchy

This protocol assumes a 1-level cache hierarchy. The role of the cache
is to simply send messages from the cpu to the appropriate directory
(based on the address), in the appropriate virtual network (based on the
message type). It does not track any state. Infact, no CacheMemory is
created unlike other protocols. The directory receives the messages from
the caches, but does not send any back. The goal of this protocol is to
enable simulation/testing of just the interconnection network.

### Stable States and Invariants

| States | Invariants                        |
| ------ | --------------------------------- |
| **I**  | Default state of all cache blocks |

### Cache controller

  - Requests, Responses, Triggers:
      - Load, Instruction fetch, Store from the core.

The network tester (in src/cpu/testers/networktest/networktest.cc)
generates packets of the type **ReadReq**, **INST_FETCH**, and
**WriteReq**, which are converted into **RubyRequestType:LD**,
**RubyRequestType:IFETCH**, and **RubyRequestType:ST**, respectively, by
the RubyPort (in src/mem/ruby/system/RubyPort.hh/cc). These messages
reach the cache controller via the Sequencer. The destination for these
messages is determined by the traffic type, and embedded in the address.
More details can be found [here](/documentation/general_docs/debugging_and_testing/directed_testers/ruby_random_tester).

  - Main Operation:
      - The goal of the cache is only to act as a source node in the
        underlying interconnection network. It does not track any
        states.
      - On a **LD** from the core:
          - it returns a hit, and
          - maps the address to a directory, and issues a message for it
            of type **MSG**, and size **Control** (8 bytes) in the
            request vnet (0).
          - Note: vnet 0 could also be made to broadcast, instead of
            sending a directed message to a particular directory, by
            uncommenting the appropriate line in the *a_issueRequest*
            action in Network_test-cache.sm
      - On a **IFETCH** from the core:
          - it returns a hit, and
          - maps the address to a directory, and issues a message for it
            of type **MSG**, and size **Control** (8 bytes) in the
            forward vnet (1).
      - On a **ST** from the core:
          - it returns a hit, and
          - maps the address to a directory, and issues a message for it
            of type **MSG**, and size **Data** (72 bytes) in the
            response vnet (2).
      - Note: request, forward and response are just used to
        differentiate the vnets, but do not have any physical
        significance in this protocol.

### Directory controller

  - Requests, Responses, Triggers:
      - **MSG** from the cores

  - Main Operation:
      - The goal of the directory is only to act as a destination node
        in the underlying interconnection network. It does not track any
        states.
      - The directory simply pops its incoming queue upon receiving the
        message.

### Other features

   This protocol assumes only 3 vnets.
  - It should only be used when running [Garnet Synthetic
        Traffic](/documentation/general_docs/ruby/garnet_synthetic_traffic).
