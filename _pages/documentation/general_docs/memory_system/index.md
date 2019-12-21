---
layout: documentation
title: "Memory system"
doc: gem5 documentation
parent: memory_system
permalink: /documentation/general_docs/memory_system/
author: Jason Lowe-Power
---

# Memory system

M5's new memory system (introduced in the first 2.0 beta release) was
designed with the following goals:

1.  Unify timing and functional accesses in timing mode. With the old
    memory system the timing accesses did not have data and just
    accounted for the time it would take to do an operation. Then a
    separate functional access actually made the operation visible to
    the system. This method was confusing, it allowed simulated
    components to accidentally cheat, and prevented the memory system
    from returning timing-dependent values, which isn't reasonable for
    an execute-in-execute CPU model.
2.  Simplify the memory system code -- remove the huge amount of
    templating and duplicate code.
3.  Make changes easier, specifically to allow other memory
    interconnects besides a shared bus.

For details on the new coherence protocol, introduced (along with a
substantial cache model rewrite) in 2.0b4, see [Coherence
Protocol](classic-coherence-protocol "wikilink").

### MemObjects

All objects that connect to the memory system inherit from `MemObject`.
This class adds the pure virtual functions `getMasterPort(const
std::string &name, PortID idx)` and `getSlavePort(const std::string
&name, PortID idx)` which returns a port corresponding to the given name
and index. This interface is used to structurally connect the MemObjects
together.

### Ports

The next large part of the memory system is the idea of ports. Ports are
used to interface memory objects to each other. They will always come in
pairs, with a MasterPort and a SlavePort, and we refer to the other port
object as the peer. These are used to make the design more modular. With
ports a specific interface between every type of object doesn't have to
be created. Every memory object has to have at least one port to be
useful. A master module, such as a CPU, has one or more MasterPort
instances. A slave module, such as a memory controller, has one or more
SlavePorts. An interconnect component, such as a cache, bridge or bus,
has both MasterPort and SlavePort instances.

There are two groups of functions in the port object. The `send*`
functions are called on the port by the object that owns that port. For
example to send a packet in the memory system a CPU would call
`myPort->sendTimingReq(pkt)` to send a packet. Each send function has a
corresponding recv function that is called on the ports peer. So the
implementation of the `sendTimingReq()` call above would simply be
`peer->recvTimingReq(pkt)` on the slave port. Using this method we only
have one virtual function call penalty but keep generic ports that can
connect together any memory system objects.

Master ports can send requests and receive responses, whereas slave
ports receive requests and send responses. Due to the coherence
protocol, a slave port can also send snoop requests and receive snoop
responses, with the master port having the mirrored interface.

### Connections

In Python, Ports are first-class attributes of simulation objects, much
like Params. Two objects can specify that their ports should be
connected using the assignment operator. Unlike a normal variable or
parameter assignment, port connections are symmetric: `A.port1 =
B.port2` has the same meaning as `B.port2 = A.port1`. The notion of
master and slave ports exists in the Python objects as well, and a check
is done when the ports are connected together.

Objects such as busses that have a potentially unlimited number of ports
use "vector ports". An assignment to a vector port appends the peer to a
list of connections rather than overwriting a previous connection.

In C++, memory ports are connected together by the python code after all
objects are instantiated.

### Request

A request object encapsulates the original request issued by a CPU or
I/O device. The parameters of this request are persistent throughout the
transaction, so a request object's fields are intended to be written at
most once for a given request. There are a handful of constructors and
update methods that allow subsets of the object's fields to be written
at different times (or not at all). Read access to all request fields is
provided via accessor methods which verify that the data in the field
being read is valid.

The fields in the request object are typically not available to devices
in a real system, so they should normally be used only for statistics or
debugging and not as architectural values.

Request object fields include:

- Virtual address. This field may be invalid if the request was issued
  directly on a physical address (e.g., by a DMA I/O device).
- Physical address.
- Data size.
- Time the request was created.
- The ID of the CPU/thread that caused this request. May be invalid if
  the request was not issued by a CPU (e.g., a device access or a
  cache writeback).
- The PC that caused this request. Also may be invalid if the request
  was not issued by a CPU.

### Packet

A Packet is used to encapsulate a transfer between two objects in the
memory system (e.g., the L1 and L2 cache). This is in contrast to a
Request where a single Request travels all the way from the requester to
the ultimate destination and back, possibly being conveyed by several
different Packets along the way.

Read access to many packet fields is provided via accessor methods which
verify that the data in the field being read is valid.

A packet contains the following all of which are accessed by accessors
to be certain the data is valid:

- The address. This is the address that will be used to route the
  packet to its target (if the destination is not explicitly set) and
  to process the packet at the target. It is typically derived from
  the request object's physical address, but may be derived from the
  virtual address in some situations (e.g., for accessing a fully
  virtual cache before address translation has been performed). It may
  not be identical to the original request address: for example, on a
  cache miss, the packet address may be the address of the block to
  fetch and not the request address.
- The size. Again, this size may not be the same as that of the
  original request, as in the cache miss scenario.
- A pointer to the data being manipulated.
    - Set by `dataStatic()`, `dataDynamic()`, and `dataDynamicArray()`
      which control if the data associated with the packet is freed
      when the packet is, not, with `delete`, and with `delete []`
      respectively.
    - Allocated if not set by one of the above methods `allocate()`
      and the data is freed when the packet is destroyed. (Always safe
      to call).
    - A pointer can be retrived by calling `getPtr()`
    - `get()` and `set()` can be used to manipulate the data in the
      packet. The get() method does a guest-to-host endian conversion
      and the set method does a host-to-guest endian conversion.
- A status indicating Success, BadAddress, Not Acknowleged, and
  Unknown.
- A list of command attributes associated with the packet
    - Note: There is some overlap in the data in the status field and
      the command attributes. This is largely so that a packet an be
      easily reinitialized when nacked or easily reused with atomic or
      functional accesses.
- A `SenderState` pointer which is a virtual base opaque structure
  used to hold state associated with the packet but specific to the
  sending device (e.g., an MSHR). A pointer to this state is returned
  in the packet's response so that the sender can quickly look up the
  state needed to process it. A specific subclass would be derived
  from this to carry state specific to a particular sending device.
- A `CoherenceState` pointer which is a virtual base opaque structure
  used to hold coherence-related state. A specific subclass would be
  derived from this to carry state specific to a particular coherence
  protocol.
- A pointer to the request.

### Access Types

There are three types of accesses supported by the ports.

1.  **Timing** - Timing accesses are the most detailed access. They
    reflect our best effort for realistic timing and include the
    modeling of queuing delay and resource contention. Once a timing
    request is successfully sent at some point in the future the device
    that sent the request will either get the response or a NACK if the
    request could not be completed (more below). Timing and Atomic
    accesses can not coexist in the memory system.
2.  **Atomic** - Atomic accesses are a faster than detailed access. They
    are used for fast forwarding and warming up caches and return an
    approximate time to complete the request without any resource
    contention or queuing delay. When a atomic access is sent the
    response is provided when the function returns. Atomic and timing
    accesses can not coexist in the memory system.
3.  **Functional** - Like atomic accesses functional accesses happen
    instantaneously, but unlike atomic accesses they can coexist in the
    memory system with atomic or timing accesses. Functional accesses
    are used for things such as loading binaries, examining/changing
    variables in the simulated system, and allowing a remote debugger to
    be attached to the simulator. The important note is when a
    functional access is received by a device, if it contains a queue of
    packets all the packets must be searched for requests or responses
    that the functional access is effecting and they must be updated as
    appropriate. The `Packet::intersect()` and `fixPacket()` methods can
    help with this.

### Packet allocation protocol

The protocol for allocation and deallocation of Packet objects varies
depending on the access type. (We're talking about low-level C++
`new`/`delete` issues here, not anything related to the coherence
protocol.)

- *Atomic* and *Functional* : The Packet object is owned by the
  requester. The responder must overwrite the request packet with the
  response (typically using the `Packet::makeResponse()` method).
  There is no provision for having multiple responders to a single
  request. Since the response is always generated before
  `sendAtomic()` or `sendFunctional()` returns, the requester can
  allocate the Packet object statically or on the stack.
- *Timing* : Timing transactions are composed of two one-way messages,
  a request and a response. In both cases, the Packet object must be
  dynamically allocated by the sender. Deallocation is the
  responsibility of the receiver (or, for broadcast coherence packets,
  the target device, typically memory). In the case where the receiver
  of a request is generating a response, it *may* choose to reuse the
  request packet for its response to save the overhead of calling
  `delete` and then `new` (and gain the convenience of using
  `makeResponse()`). However, this optimization is optional, and the
  requester must not rely on receiving the same Packet object back in
  response to a request. Note that when the responder is not the
  target device (as in a cache-to-cache transfer), then the target
  device will still delete the request packet, and thus the responding
  cache must allocate a new Packet object for its response. Also,
  because the target device may delete the request packet immediately
  on delivery, any other memory device wishing to reference a
  broadcast packet past point where the packet is delivered must make
  a copy of that packet, as the pointer to the packet that is
  delivered cannot be relied upon to stay valid.

### Timing Flow control

Timing requests simulate a real memory system, so unlike functional and
atomic accesses their response is not instantaneous. Because the timing
requests are not instantaneous, flow control is needed. When a timing
packet is sent via `sendTiming()` the packet may or may not be accepted,
which is signaled by returning true or false. If false is returned the
object should not attempt to sent anymore packets until it receives a
`recvRetry()` call. At this time it should again try to call
`sendTiming()`; however the packet may again be rejected. Note: The
original packet does not need to be resent, a higher priority packet can
be sent instead. Once `sendTiming()` returns true, the packet may still
not be able to make it to its destination. For packets that require a
response (i.e. `pkt->needsResponse()` is true), any memory object can
refuse to acknowledge the packet by changing its result to `Nacked` and
sending it back to its source. However, if it is a response packet, this
can not be done. The true/false return is intended to be used for local
flow control, while nacking is for global flow control. In both cases a
response can not be nacked.

### Response and Snoop ranges

Ranges in the memory system are handled by having devices that are
sensitive to an address range provide an implementation for
`getAddrRanges` in their slave port objects. This method returns an
`AddrRangeList` of addresses it responds to. When these ranges change
(e.g. from PCI configuration taking place) the device should call
`sendRangeChange()` on its slave port so that the new ranges are
propagated to the entire hierarchy. This is precisely what happens
during `init()`; all memory objects call `sendRangeChange()`, and a
flurry of range updates occur until everyones ranges have been
propagated to all busses in the system.
