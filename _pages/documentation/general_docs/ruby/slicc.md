---
layout: documentation
title: "SLICC"
doc: gem5 documentation
parent: ruby
permalink: /documentation/general_docs/ruby/slicc/
author: Jason Lowe-Power
---

# SLICC

SLICC is a domain specific language for specifying cache coherence
protocols. The SLICC compiler generates C++ code for different
controllers, which can work in tandem with other parts of Ruby. The
compiler also generates an HTML specification of the protocol. HTML
generation is turned off by default. To enable HTML output, pass the
option "SLICC_HTML=True" to scons when compiling.

### Input To the Compiler

The SLICC compiler takes, as input, files that specify the controllers
involved in the protocol. The .slicc file specifies the different files
used by the particular protocol under consideration. For example, if
trying to specify the MI protocol using SLICC, then we may use MI.slicc
as the file that specifies all the files necessary for the protocol. The
files necessary for specifying a protocol include the definitions of the
state machines for different controllers, and of the network messages
that are passed on between these controllers.

The files have a syntax similar to that of C++. The compiler, written
using [PLY (Python Lex-Yacc)](http://www.dabeaz.com/ply/), parses these
files to create an Abstract Syntax Tree (AST). The AST is then traversed
to build some of the internal data structures. Finally the compiler
outputs the C++ code by traversing the tree again. The AST represents
the hierarchy of different structures present with in a state machine.
We describe these structures next.

### Protocol State Machines

In this section we take a closer look at what goes in to a file
containing specification of a state machine.

#### Specifying Data Members

Each state machine is described using SLICC's **machine** datatype. Each
machine has several different types of members. Machines for cache and
directory controllers include cache memory and directory memory data
members respectively. We will use the MI protocol available in
src/mem/protocol as our running example. So here is how you might want
to start writing a state machine

```
machine(MachineType:L1Cache, "MI Example L1 Cache")
  : Sequencer * sequencer,
    CacheMemory * cacheMemory,
    int cache_response_latency = 12,
    int issue_latency = 2 {
      // Add rest of the stuff
    }
```
In order to let the controller receive messages from different
entities in the system, the machine has a number of **Message
Buffers**. These act as input and output ports for the machine. Here
is an example specifying the output ports.

```
 MessageBuffer requestFromCache, network="To", virtual_network="2", ordered="true";
 MessageBuffer responseFromCache, network="To", virtual_network="4", ordered="true";
```

Note that Message Buffers have some attributes that need to be specified
correctly. Another example, this time for specifying the input
ports.

```
 MessageBuffer forwardToCache, network="From", virtual_network="3", ordered="true";
 MessageBuffer responseToCache, network="From", virtual_network="4", ordered="true";
```

Next the machine includes a declaration of the **states** that
machine can possibly reach. In cache coherence protocol, states can
be of two types -- stable and transient. A cache block is said to be
in a stable state if in the absence of any activity (in coming
request for the block from another controller, for example), the
cache block would remain in that state for ever. Transient states
are required for transitioning between stable states. They are
needed when ever the transition between two stable states can not be
done in an atomic fashion. Next is an example that shows how states
are declared. SLICC has a keyword **state_declaration** that has to
be used for declaring
states.

```
state_declaration(State, desc="Cache states") {
   I, AccessPermission:Invalid, desc="Not Present/Invalid";
   II, AccessPermission:Busy, desc="Not Present/Invalid, issued PUT";
   M, AccessPermission:Read_Write, desc="Modified";
   MI, AccessPermission:Busy, desc="Modified, issued PUT";
   MII, AccessPermission:Busy, desc="Modified, issued PUTX, received nack";
   IS, AccessPermission:Busy, desc="Issued request for LOAD/IFETCH";
   IM, AccessPermission:Busy, desc="Issued request for STORE/ATOMIC";
}
```

The states I and M are the only stable states in this example. Again
note that certain attributes have to be specified with the states.

The state machine needs to specify the **events** it can handle and
thus transition from one state to another. SLICC provides the
keyword **enumeration** which can be used for specifying the set of
possible events. An example to shed more light on this -

```
enumeration(Event, desc="Cache events") {
   // From processor
   Load,       desc="Load request from processor";
   Ifetch,     desc="Ifetch request from processor";
   Store,      desc="Store request from processor";
   Data,       desc="Data from network";
   Fwd_GETX,        desc="Forward from network";
   Inv,        desc="Invalidate request from dir";
   Replacement,  desc="Replace a block";
   Writeback_Ack,   desc="Ack from the directory for a writeback";
   Writeback_Nack,   desc="Nack from the directory for a writeback";
}
```

While developing a protocol machine, we may need to define
structures that represent different entities in a memory system.
SLICC provides the keyword **structure** for this purpose. An
example
follows

```
structure(Entry, desc="...", interface="AbstractCacheEntry") {
   State CacheState,        desc="cache state";
   bool Dirty,              desc="Is the data dirty (different than memory)?";
   DataBlock DataBlk,       desc="Data in the block";
}
```

The cool thing about using SLICC's structure is that it automatically
generates for you the get and set functions on different fields. It also
writes a nice print function and overloads the \<\< operator. But in
case you would prefer do everything on your own, you can make use of the
keyword **external** in the declaration of the structure. This would
prevent SLICC from generating C++ code for this structure.

```
structure(TBETable, external="yes") {
   TBE lookup(Address);
   void allocate(Address);
   void deallocate(Address);
   bool isPresent(Address);
}
```

In fact many predefined types exist in src/mem/protocol/RubySlicc_\*.sm
files. You can make use of them, or if you need new types, you can
define new ones as well. You can also use the keyword **interface** to
make use of inheritance features available in C++. Note that currently
SLICC supports public inheritance only.

We can also declare and define functions as we do in C++. There are
certain functions that the compiler expects would always be defined
by the controller. These include
- getState()
- setState()

#### Input for the Machine

Since protocol is state machine, we need to specify how to machine
transitions from one state to another on receiving inputs. As mentioned
before, each machine has several input and output ports. For each input
port, the **in_port** keyword is used for specifying the behavior of
the machine, when a message is received on that input port. An example
follows that shows the syntax for declaring an input
port.

```
in_port(mandatoryQueue_in, RubyRequest, mandatoryQueue, desc="...") {
  if (mandatoryQueue_in.isReady()) {
    peek(mandatoryQueue_in, RubyRequest, block_on="LineAddress") {
      Entry cache_entry := getCacheEntry(in_msg.LineAddress);
      if (is_invalid(cache_entry) &&
          cacheMemory.cacheAvail(in_msg.LineAddress) == false ) {
        // make room for the block
        trigger(Event:Replacement, cacheMemory.cacheProbe(in_msg.LineAddress),
                getCacheEntry(cacheMemory.cacheProbe(in_msg.LineAddress)),
                TBEs[cacheMemory.cacheProbe(in_msg.LineAddress)]);
      }
      else {
        trigger(mandatory_request_type_to_event(in_msg.Type), in_msg.LineAddress,
                cache_entry, TBEs[in_msg.LineAddress]);
      }
    }
  }
}
```

As you can see, in_port takes in multiple arguments. The first
argument, mandatoryQueue_in, is the identifier for the in_port
that is used in the file. The next argument, RubyRequest, is the
type of the messages that this input port receives. Each input port
uses a queue to store the messages, the name of the queue is the
third argument.

The keyword **peek** is used to extract messages from the queue of
the input port. The use of this keyword implicitly declares a
variable **in_msg** which is of the same type as specified in the
input port's declaration. This variable points to the message at the
head of the queue. It can be used for accessing the fields of the
message as shown in the code above.

Once the incoming message has been analyzed, it is time for using
this message for taking some appropriate action and changing the
state of the machine. This done using the keyword **trigger**. The
trigger function is actually used only in SLICC code and is not
present in the generated code. Instead this call is converted in to
a call to the **doTransition()** function which appears in the
generated code. The doTransition() function is automatically
generated by SLICC for each of the state machines. The number of
arguments to trigger depend on the machine itself. In general, the
input arguments for trigger are the type of the message that needs
to processed, the address for which this message is meant for, the
cache and the transaction buffer entries for that address.

**trigger** also increments a counter that is checked before a
transition is made. In one ruby cycle, there is a limit on the
number of transitions that can be carried out. This is done to
resemble more closely to a hardware based state machine. **@TODO:
What happens if there are no more transitions left? Does the wakeup
abort?**

#### Actions

In this section we will go over how the actions that a state machine can
carry out are defined. These actions will be called in to action when
the state machine receives some input message which is then used to make
a transition. Let's go over an example on how the key word **action**
can be made use of.

```
action(a_issueRequest, "a", desc="Issue a request") {
   enqueue(requestNetwork_out, RequestMsg, latency=issue_latency) {
   out_msg.Address := address;
     out_msg.Type := CoherenceRequestType:GETX;
     out_msg.Requestor := machineID;
     out_msg.Destination.add(map_Address_to_Directory(address));
     out_msg.MessageSize := MessageSizeType:Control;
   }
}
```

The first input argument is the name of the action, the next
argument is the abbreviation used for generating the documentation
and last one is the description of the action which used in the HTML
documentation and as a comment in the C++ code.

Each action is converted in to a C++ function of that name. The
generated C++ code implicitly includes up to three input parameters
in the function header, again depending on the machine. These
arguments are the memory address on which the action is being taken,
the cache and transaction buffer entries pertaining to this address.

Next useful thing to look at is the **enqueue** keyword. This
keyword is used for queuing a message, generated as a result of the
action, to an output port. The keyword takes three input arguments,
namely, the name of the output port, the type of the message to be
queued and the latency after which this message can be dequeued.
Note that in case randomization is enabled, the specified latency is
ignored. The use of the keyword implicitly declares a variable
out_msg which is populated by the follow on statements.

#### Transitions

A transition function is a mapping from the cross product of set of
states and set of events to the set of states. SLICC provides the
keyword **transition** for specifying the transition function for state
machines. An example follows --

```
transition(IM, Data, M) {
   u_writeDataToCache;
   sx_store_hit;
   w_deallocateTBE;
   n_popResponseQueue;
}
```

In this example, the initial state is *IM*. If an event of type *Data*
occurs in that state, then final state would be *M*. Before making the
transition, the state machine can perform certain actions on the
structures that it maintains. In the given example,
*u_writeDataToCache* is an action. All these operations are performed
in an atomic fashion, i.e. no other event can occur before the set of
actions specified with the transition has been completed.

For ease of use, sets of events and states can be provided as input
to transition. The cross product of these sets will map to the same
final state. Note that the final state cannot be a set. If for a
particular event, the final state is same as the initial state, then
the final state can be omitted.

```
transition({IS, IM, MI, II}, {Load, Ifetch, Store, Replacement}) {
   z_stall;
}
```

### Special Functions

#### Stalling/Recycling/Waiting input ports

One of the more complicated internal features of SLICC and the resulting
state machines is how the deal with the situation when events cannot be
process due to the cache block being in a transient state. There are
several possible ways to deal with this situation and each solution has
different tradeoffs. This sub-section attempts to explain the
differences. Please email the gem5-user list for further follow-up.

##### Stalling the input port

The simplest way to handle events that can't be processed is to simply
stall the input port. The correct way to do this is to include the
"z_stall" action within the transition statement:

```
transition({IS, IM, MI, II}, {Load, Ifetch, Store, Replacement}) {
   z_stall;
}
```

Internally SLICC will return a ProtocolStall for this transition and no
subsequent messages from the associated input port will be processed
until the stalled message is processed. However, the other input ports
will be analyzed for ready messages and processed in parallel. While
this is a relatively simple solution, one may notice that stalling
unrelated messages on the same input port will cause excessive and
unnecessary stalls.

One thing to note is **Do Not** leave the transition statement blank
like so:

```
transition({IS, IM, MI, II}, {Load, Ifetch, Store, Replacement}) {
   // stall the input port by simply not popping the message
}
```

This will cause SLICC to return success for this transition and SLICC
will continue to repeatedly analyze the same input port. The result is
eventual deadlock.

##### Recycling the input port

The better performance but more unrealistic solution is to recycle the
stalled message on the input port. The way to do this is to use the
"zz_recycleMandatoryQueue"
action:

```
action(zz_recycleMandatoryQueue, "\z", desc="Send the head of the mandatory queue to the back of the queue.") {
   mandatoryQueue_in.recycle();
}
```
```
transition({IS, IM, MI, II}, {Load, Ifetch, Store, Replacement}) {
   zz_recycleMandatoryQueue;
}
```

The result of this action is that the transition returns a Protocol
Stall and the offending message moved to the back of the FIFO input
port. Therefore, other unrelated messages on the same input port can be
processed. The problem with this solution is that recycled messages may
be analyzed and reanalyzed every cycle until an address changes state.

##### Stall and wait the input port

An even better, but more complicated solution is to "stall and wait" the
offending input message. The way to do this is to use the
"z_stallAndWaitMandatoryQueue"
action:

```
action(z_stallAndWaitMandatoryQueue, "\z", desc="recycle L1 request queue") {
   stall_and_wait(mandatoryQueue_in, address);
}
```
```
transition({IS, IM, IS_I, M_I, SM, SINK_WB_ACK}, {Load, Ifetch, Store, L1_Replacement}) {
   z_stallAndWaitMandatoryQueue;
}
```

The result of this action is that the transition returns success, which
is ok because stall_and_wait moves the offending message off the input
port and to a side table associated with the input port. The message
will not be analyzed again until it is woken up. In the meantime, other
unrelated messages will be processed.

The complicated part of stall and wait is that stalled messages must be
explicitly woken up by other messages/transitions. In particular,
transitions that move an address to a base state should wake up
potentially stalled messages waiting for that address:

```
action(kd_wakeUpDependents, "kd", desc="wake-up dependents") {
   wakeUpBuffers(address);
}
```

```
transition(M_I, WB_Ack, I) {
   s_deallocateTBE;
   o_popIncomingResponseQueue;
   kd_wakeUpDependents;
}
```

Replacements are particularly complicated since stalled addresses are
not associated with the same address they are actually waiting to
change. In those situations all waiting messages must be woken
up:

```
action(ka_wakeUpAllDependents, "ka", desc="wake-up all dependents") {
   wakeUpAllBuffers();
}
```

```
transition(I, L2_Replacement) {
   rr_deallocateL2CacheBlock;
   ka_wakeUpAllDependents;
}
```

### Other Compiler Features

- SLICC supports conditional statements in form of **if** and
**else**. Note that SLICC does not support **else if**.

- Each function has return type which can be void as well. Returned
values cannot be ignored.

- SLICC has limited support for pointer variables. is_valid() and
is_invalid() operations are supported for testing whether a given
pointer 'is not NULL' and 'is NULL' respectively. The keyword
**OOD**, which stands for Out of Domain, plays the role of keyword
NULL used in C++.

- SLICC does not support **\!** (the not operator).

- Static type casting is supported in SLICC. The keyword
**static_cast** has been provided for this purpose. For example, in
the following piece of code, a variable of type AbstractCacheEntry
is being casted in to a variable of type Entry.

```
   Entry L1Dcache_entry := static_cast(Entry, "pointer", L1DcacheMemory[addr]);
```

### SLICC Internals

**C++ to Slicc Interface - @note: What do each of these files
do/define???**

- src/mem/protocol/RubySlicc_interaces.sm
    - RubySlicc_Exports.sm
    - RubySlicc_Defines.sm
    - RubySlicc_Profiler.sm
    - RubySlicc_Types.sm
    - RubySlicc_MemControl.sm
    - RubySlicc_ComponentMapping.sm

**Variable Assignments**

- Use the `:=` operator to assign members in class (e.g. a member
defined in RubySlicc_Types.sm):
    - an automatic `m_` is added to the name mentioned in the SLICC
    file.
