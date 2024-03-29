---
layout: documentation
title: Declaring a state machine
doc: Learning gem5
parent: part3
permalink: /documentation/learning_gem5/part3/cache-declarations/
author: Jason Lowe-Power
---


Let's start on our first state machine file! First, we will create the
L1 cache controller for our MSI protocol.

Create a file called `MSI-cache.sm` and the following code declares the
state machine.

```cpp
machine(MachineType:L1Cache, "MSI cache")
    : <parameters>
{
    <All state machine code>
}
```

The first thing you'll notice about the state machine code is that is
looks very C++-like. The state machine file is like creating a C++
object in a header file, if you included all of the code there as well.
When in doubt, C++ syntax with *probably* work in SLICC. However, there
are many cases where C++ syntax is incorrect syntax for SLICC as well as
cases where SLICC extends the syntax.

With `MachineType:L1Cache`, we are naming this state machine `L1Cache`.
SLICC will generate many different objects for us from the state machine
using that name. For instance, once this file is compiled, there will be
a new SimObject: `L1Cache_Controller` that is the cache controller. Also
included in this declaration is a description of this state machine:
"MSI cache".

There are many cases in SLICC where you must include a description to go
along with the variable. The reason for this is that SLICC was
originally designed to just describe, not implement, coherence
protocols. Today, these extra descriptions serve two purposes. First,
they act as comments on what the author intended each variable, or
state, or event, to be used for. Second, many of them are still exported
into HTML when building the HTML tables for the SLICC protocol. Thus,
while browsing the HTML table, you can see the more detailed comments
from the author of the protocol. It is important to be clear with these
descriptions since coherence protocols can get quite complicated.

## State machine parameters

Proceeding the `machine()` declaration is a colon, after which all of
the parameters to the state machine are declared. These parameters are
directly exported to the SimObject that is generated by the state
machine.

For our MSI L1 cache, we have the following parameters:

```cpp
machine(MachineType:L1Cache, "MSI cache")
: Sequencer *sequencer;
  CacheMemory *cacheMemory;
  bool send_evictions;

  <Message buffer declarations>

  {

  }
```

First, we have a `Sequencer`. This is a special class that is
implemented in Ruby to interface with the rest of gem5. The Sequencer is
a gem5 `MemObject` with a slave port so it can accept memory requests
from other objects. The sequencer accepts requests from a CPU (or other
master port) and converts the gem5 the packet into a `RubyRequest`.
Finally, the `RubyRequest` is pushed onto the `mandatoryQueue` of the
state machine. We will revisit the `mandatoryQueue` in
the [in-port section](../cache-in-ports).

Next, there is a `CacheMemory` object. This is what holds the cache data
(i.e., cache entries). The exact implementation, size, etc. is
configurable at runtime.

Finally, we can specify any other parameters we would like, similar to a
general `SimObject`. In this case, we have a boolean variable
`send_evictions`. This is used for out-of-order core models to notify
the load-store queue if an address is evicted after a load to squash a
load if it is speculative.

Next, also in the parameter block (i.e., before the first open bracket),
we need to declare all of the message buffers that this state machine
will use. Message buffers are the interface between the state machine
and the Ruby network. Messages are sent and received via the message
buffers. Thus, for each virtual channel in our protocol we need a
separate message buffer.

The MSI protocol needs three different virtual networks. Virtual
networks are needed to prevent deadlock (e.g., it is bad if a response
gets stuck behind a stalled request). In this protocol, the highest
priority is responses (virtual network 2), followed by forwarded
requests (virtual network 1), then requests have the lowest priority
(virtual network 0). See Sorin et al. for details on why these three
virtual networks are needed.

The following code declares all of the needed message buffers.

```cpp
machine(MachineType:L1Cache, "MSI cache")
: Sequencer *sequencer;
  CacheMemory *cacheMemory;
  bool send_evictions;

  MessageBuffer * requestToDir, network="To", virtual_network="0", vnet_type="request";
  MessageBuffer * responseToDirOrSibling, network="To", virtual_network="2", vnet_type="response";

  MessageBuffer * forwardFromDir, network="From", virtual_network="1", vnet_type="forward";
  MessageBuffer * responseFromDirOrSibling, network="From", virtual_network="2", vnet_type="response";

  MessageBuffer * mandatoryQueue;

{

}
```

We have five different message buffers: two "To", two "From", and one
special message buffer. The "To" message buffers are similar to slave
ports in gem5. These are the message buffers that this controller uses
to send messages to other controllers in the system. The "From" message
buffers are like slave ports. This controller receives messages on
"From" buffers from other controllers in the system.

We have two different "To" buffers, one for low priority requests, and
one for high priority responses. The priority for the networks are not
inherent. The priority is based on the order that other controllers look
at the message buffers. It is a good idea to number the virtual networks
so that higher numbers mean higher priority, but the virtual network
number is ignored by Ruby except that messages on network 2 can only go
to other message buffers on network 2 (i.e., messages can't jump from
one network to another).

Similarly, there is two different ways this cache can receive messages,
either as a forwarded request from the directory (e.g., another cache
requests a writable block and we have a readable copy) or as a response
to a request this controller made. The response is higher priority than
the forwarded requests.

Finally, there is a special message buffer, the `mandatoryQueue`. This
message buffer is used by the `Sequencer` to convert gem5 packets into
Ruby requests. Unlike the other message buffers, `mandatoryQueue` does
not connect to the Ruby network. Note: the name of this message buffer
is hard-coded and must be exactly "mandatoryQueue".

As previously mentioned, this parameter block is converted into the
SimObject description file. Any parameters you put in this block will be
SimObject parameters that are accessible from the Python configuration
files. If you look at the generated file L1Cache\_Controller.py, it will
look very familiar. Note: This is a generated file and you should never
modify generated files directly!

```python
from m5.params import *
from m5.SimObject import SimObject
from Controller import RubyController

class L1Cache_Controller(RubyController):
    type = 'L1Cache_Controller'
    cxx_header = 'mem/protocol/L1Cache_Controller.hh'
    sequencer = Param.RubySequencer("")
    cacheMemory = Param.RubyCache("")
    send_evictions = Param.Bool("")
    requestToDir = Param.MessageBuffer("")
    responseToDirOrSibling = Param.MessageBuffer("")
    forwardFromDir = Param.MessageBuffer("")
    responseFromDirOrSibling = Param.MessageBuffer("")
    mandatoryQueue = Param.MessageBuffer("")
```

## State declarations

The next part of the state machine is the state declaration. Here, we
are going to declare all of the stable and transient states for the
state machine. We will follow the naming convention in Sorin et al. For
instance, the transient state "IM\_AD" corresponds to moving from
Invalid to Modified waiting on acks and data. These states come directly
from the left column of Table 8.3 in Sorin et al.

```cpp
state_declaration(State, desc="Cache states") {
    I,      AccessPermission:Invalid,
                desc="Not present/Invalid";

    // States moving out of I
    IS_D,   AccessPermission:Invalid,
                desc="Invalid, moving to S, waiting for data";
    IM_AD,  AccessPermission:Invalid,
                desc="Invalid, moving to M, waiting for acks and data";
    IM_A,   AccessPermission:Busy,
                desc="Invalid, moving to M, waiting for acks";

    S,      AccessPermission:Read_Only,
                desc="Shared. Read-only, other caches may have the block";

    // States moving out of S
    SM_AD,  AccessPermission:Read_Only,
                desc="Shared, moving to M, waiting for acks and 'data'";
    SM_A,   AccessPermission:Read_Only,
                desc="Shared, moving to M, waiting for acks";

    M,      AccessPermission:Read_Write,
                desc="Modified. Read & write permissions. Owner of block";

    // States moving to Invalid
    MI_A,   AccessPermission:Busy,
                desc="Was modified, moving to I, waiting for put ack";
    SI_A,   AccessPermission:Busy,
                desc="Was shared, moving to I, waiting for put ack";
    II_A,   AccessPermission:Invalid,
                desc="Sent valid data before receiving put ack. "Waiting for put ack.";
}
```

Each state has an associated access permission: "Invalid", "NotPresent",
"Busy", "Read\_Only", or "Read\_Write". The access permission is used
for *functional* accesses to the cache. Functional accesses are
debug-like accesses when the simulator wants to read or update the data
immediately. One example of this is reading in files in SE mode which
are directly loaded into memory.

For functional accesses all caches are checked to see if they have a
corresponding block with matching address. For functional reads, *all*
of the blocks with a matching address that have read-only or read-write
permission are accessed (they should all have the same data). For
functional writes, all blocks are updated with new data if they have
busy, read-only, or read-write permission.

## Event declarations

Next, we need to declare all of the events that are triggered by
incoming messages for this cache controller. These events come directly
from the first row in Table 8.3 in Sorin et al.

```cpp
enumeration(Event, desc="Cache events") {
    // From the processor/sequencer/mandatory queue
    Load,           desc="Load from processor";
    Store,          desc="Store from processor";

    // Internal event (only triggered from processor requests)
    Replacement,    desc="Triggered when block is chosen as victim";

    // Forwarded request from other cache via dir on the forward network
    FwdGetS,        desc="Directory sent us a request to satisfy GetS. We must have the block in M to respond to this.";
    FwdGetM,        desc="Directory sent us a request to satisfy GetM. We must have the block in M to respond to this.";
    Inv,            desc="Invalidate from the directory.";
    PutAck,         desc="Response from directory after we issue a put. This must be on the fwd network to avoid deadlock.";

    // Responses from directory
    DataDirNoAcks,  desc="Data from directory (acks = 0)";
    DataDirAcks,    desc="Data from directory (acks > 0)";

    // Responses from other caches
    DataOwner,      desc="Data from owner";
    InvAck,         desc="Invalidation ack from other cache after Inv";

    // Special event to simplify implementation
    LastInvAck,     desc="Triggered after the last ack is received";
}
```

## User-defined structures

Next, we need to define some structures that we will use in other places
in this controller. The first one we will define is `Entry`. This is the
structure that is stored in the `CacheMemory`. It only needs to contain
data and a state, but it may contain any other data you want. Note: The
state that this structure is storing is the `State` type that was
defined above, not a hardcoded state type.

You can find the abstract version of this class (`AbstractCacheEntry`)
in `src/mem/ruby/slicc_interface/AbstractCacheEntry.hh`. If you want to
use any of the member functions of `AbstractCacheEntry`, you need to
declare them here (this isn't used in this protocol).

```cpp
structure(Entry, desc="Cache entry", interface="AbstractCacheEntry") {
    State CacheState,        desc="cache state";
    DataBlock DataBlk,       desc="Data in the block";
}
```

Another structure we will need is a TBE. TBE is the "transaction buffer
entry". This stores information needed during transient states. This is
*like* an MSHR. It functions as an MSHR in this protocol, but the entry
is also allocated for other uses. In this protocol, it will store the
state (usually needed), data (also usually needed), and the number of
acks that this block is currently waiting for. The `AcksOutstanding` is
used for the transitions where other controllers send acks instead of
the data.

```cpp
structure(TBE, desc="Entry for transient requests") {
    State TBEState,         desc="State of block";
    DataBlock DataBlk,      desc="Data for the block. Needed for MI_A";
    int AcksOutstanding, default=0, desc="Number of acks left to receive.";
}
```

Next, we need a place to store all of the TBEs. This is an externally
defined class; it is defined in C++ outside of SLICC. Therefore, we need
to declare that we are going to use it, and also declare any of the
functions that we will call on it. You can find the code for the
`TBETable` in src/mem/ruby/structures/TBETable.hh. It is templatized on
the TBE structure defined above, which gets a little confusing, as we
will see.

```cpp
structure(TBETable, external="yes") {
  TBE lookup(Addr);
  void allocate(Addr);
  void deallocate(Addr);
  bool isPresent(Addr);
}
```

The `external="yes"` tells SLICC to not look for the definition of this
structure. This is similar to declaring a variable `extern` in C/C++.

## Other declarations and definitions required

Finally, we are going to go through some boilerplate of declaring
variables, declaring functions in `AbstractController` that we will use
in this controller, and defining abstract functions in
`AbstractController`.

First, we need to have a variable that stores a TBE table. We have to do
this in SLICC because it is not until this time that we know the true
type of the TBE table since the TBE type was defined above. This is some
particularly tricky (or nasty) code to get SLICC to generate the right
C++ code. The difficulty is that we want templatize `TBETable` based on
the `TBE` type above. The key is that SLICC mangles the names of all
types declared in the machine with the machine's name. For instance,
`TBE` is actually L1Cache\_TBE in C++.

We also want to pass a parameter to the constructor of the `TBETable`.
This is a parameter that is actually part of the `AbstractController`,
thus we need to use the C++ name for the variable since it doesn't have
a SLICC name.

```cpp
TBETable TBEs, template="<L1Cache_TBE>", constructor="m_number_of_TBEs";
```

If you can understand the above code, then you are an official SLICC
ninja!

Next, any functions that are part of AbstractController need to be
declared, if we are going to use them in the rest of the file. In this
case, we are only going to use `clockEdge()`:

```cpp
Tick clockEdge();
```

There are a few other functions we're going to use in actions. These
functions are used in actions to set and unset implicit variables
available in action code-blocks. Action code blocks will be explained in
detail in the action section \<MSI-actions-section\>. These may be
needed when a transition has many actions.

```cpp
void set_cache_entry(AbstractCacheEntry a);
void unset_cache_entry();
void set_tbe(TBE b);
void unset_tbe();
```

Another useful function is `mapAddressToMachine`. This allows us to
change the address mappings for banked directories or caches at runtime
so we don't have to hardcode them in the SLICC file.

```cpp
MachineID mapAddressToMachine(Addr addr, MachineType mtype);
```

Finally, you can also add any functions you may want to use in the file
and implement them here. For instance, it is convenient to access cache
blocks by address with a single function. Again, in this function there
is some SLICC trickery. We need to access "by pointer" since the cache
block is something that we need to be mutable later ("by reference"
would have been a better name). The cast is also necessary since we
defined a specific `Entry` type in the file, but the `CacheMemory` holds
the abstract type.

```cpp
// Convenience function to look up the cache entry.
// Needs a pointer so it will be a reference and can be updated in actions
Entry getCacheEntry(Addr address), return_by_pointer="yes" {
    return static_cast(Entry, "pointer", cacheMemory.lookup(address));
}
```

The next set of boilerplate code rarely changes between different
protocols. There's a set of functions that are pure-virtual in
`AbstractController` that we must implement.

`getState`
:   Given a TBE, cache entry, and address return the state of the block.
    This is called on the block to decide which transition to execute
    when an event is triggered. Usually, you return the state in the TBE
    or cache entry, whichever is valid.

`setState`
:   Given a TBE, cache entry, and address make sure the state is set
    correctly on the block. This is called at the end of the transition
    to set the final state on the block.

`getAccessPermission`
:   Get the access permission of a block. This is used during functional
    access to decide whether or not to functionally access the block. It
    is similar to `getState`, get the information from the TBE if valid,
    cache entry, if valid, or the block is not present.

`setAccessPermission`
:   Like `getAccessPermission`, but sets the permission.

`functionalRead`
:   Functionally read the data. It is possible the TBE has more
    up-to-date information, so check that first. Note: testAndRead/Write
    defined in src/mem/ruby/slicc\_interface/Util.hh

`functionalWrite`
:   Functionally write the data. Similarly, you may need to update the
    data in both the TBE and the cache entry.

```cpp
State getState(TBE tbe, Entry cache_entry, Addr addr) {
    // The TBE state will override the state in cache memory, if valid
    if (is_valid(tbe)) { return tbe.TBEState; }
    // Next, if the cache entry is valid, it holds the state
    else if (is_valid(cache_entry)) { return cache_entry.CacheState; }
    // If the block isn't present, then it's state must be I.
    else { return State:I; }
}

void setState(TBE tbe, Entry cache_entry, Addr addr, State state) {
  if (is_valid(tbe)) { tbe.TBEState := state; }
  if (is_valid(cache_entry)) { cache_entry.CacheState := state; }
}

AccessPermission getAccessPermission(Addr addr) {
    TBE tbe := TBEs[addr];
    if(is_valid(tbe)) {
        return L1Cache_State_to_permission(tbe.TBEState);
    }

    Entry cache_entry := getCacheEntry(addr);
    if(is_valid(cache_entry)) {
        return L1Cache_State_to_permission(cache_entry.CacheState);
    }

    return AccessPermission:NotPresent;
}

void setAccessPermission(Entry cache_entry, Addr addr, State state) {
    if (is_valid(cache_entry)) {
        cache_entry.changePermission(L1Cache_State_to_permission(state));
    }
}

void functionalRead(Addr addr, Packet *pkt) {
    TBE tbe := TBEs[addr];
    if(is_valid(tbe)) {
        testAndRead(addr, tbe.DataBlk, pkt);
    } else {
        testAndRead(addr, getCacheEntry(addr).DataBlk, pkt);
    }
}

int functionalWrite(Addr addr, Packet *pkt) {
    int num_functional_writes := 0;

    TBE tbe := TBEs[addr];
    if(is_valid(tbe)) {
        num_functional_writes := num_functional_writes +
            testAndWrite(addr, tbe.DataBlk, pkt);
        return num_functional_writes;
    }

    num_functional_writes := num_functional_writes +
            testAndWrite(addr, getCacheEntry(addr).DataBlk, pkt);
    return num_functional_writes;
}
```
