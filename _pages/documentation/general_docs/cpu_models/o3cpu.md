---
layout: documentation
title: Out of order CPU model
doc: gem5 documentation
parent: cpu_models
permalink: /documentation//general_docs/cpu_models/O3CPU
---

<!-- This page was last updated 5 years ago. It might be out of date at this point -->

# **O3CPU**

Table of Contents

 1. [Pipeline stages](##Pipeline-stages)
 2. [Execute-in-execute model](##Execute-in-execute-model)
 3. [Template Policies](##Template-Policies)
 4. [ISA independence](##ISA-independence)
 5. [Interaction with ThreadContext](##Interaction-with-ThreadContext**)

The O3CPU is <!--our new detailed model for the v2.0 release. It is--> an out of order CPU model loosely based on the Alpha 21264. This page will give you a general overview of the O3CPU model, the pipeline stages and the pipeline resources. <!--We have made efforts to keep the code well documented, so please browse the code for exact details on how each part of the O3CPU works.-->


## **Pipeline stages**
* Fetch
  
     Fetches instructions each cycle, selecting which thread to fetch from based on the policy selected. This stage is where the DynInst is first created. Also handles branch prediction.
    
* Decode
  
  Decodes instructions each cycle. Also handles early resolution of PC-relative unconditional branches.

* Rename
  
  Renames instructions using a physical register file with a free list. Will stall if there are not enough registers to rename to, or if back-end resources have filled up. Also handles any serializing instructions at this point by stalling them in rename until the back-end drains.

* Issue/Execute/Writeback
  
  Our simulator model handles both execute and writeback when the execute() function is called on an instruction, so we have combined these three stages into one stage. This stage (IEW) handles dispatching instructions to the instruction queue, telling the instruction queue to issue instruction, and executing and writing back instructions.

* Commit
  
   Commits instructions each cycle, handling any faults that the instructions may have caused. Also handles redirecting the front-end in the case of a branch misprediction.


## **Execute-in-execute model**

For the O3CPU, we've made efforts to make it highly timing accurate. In order to do this, we use a model that actually executes instructions at the execute stage of the pipeline. Most simulator models will execute instructions either at the beginning or end of the pipeline; SimpleScalar and our old detailed CPU model both execute instructions at the beginning of the pipeline and then pass it to a timing backend. This presents two potential problems: first, there is the potential for error in the timing backend that would not show up in program results. Second, by executing at the beginning of the pipeline, the instructions are all executed in order and out-of-order load interaction is lost. Our model is able to avoid these deficiencies and provide an accurate timing model.

## **Template Policies**

The O3CPU makes heavy use of template policies to obtain a level of polymorphism without having to use virtual functions. It uses template policies to pass in an "Impl" to almost all of the classes used within the O3CPU. This Impl has defined within it all of the important classes for the pipeline, such as the specific Fetch class, Decode class, specific DynInst types, the CPU class, etc. It allows any class that uses it as a template parameter to be able to obtain full type information of any of the classes defined within the Impl. By obtaining full type information, there is no need for the traditional virtual functions/base classes which are normally used to provide polymorphism. The main drawback is that the CPU must be entirely defined at compile time, and that the templated classes require manual instantiation. See `src/cpu/o3/impl.hh ` and `src/cpu/o3/cpu_policy.hh` for example Impl classes.

## **ISA independence**

The O3CPU has been designed to try to separate code that is ISA dependent and code that is ISA independent. The pipeline stages and resources are all mainly ISA independent, as well as the lower level CPU code. The ISA dependent code implements ISA-specific functions. For example, the AlphaO3CPU implements Alpha-specific functions, such as hardware return from error interrupt (hwrei()) or reading the interrupt flags. The lower level CPU, the FullO3CPU, handles orchestrating all of the pipeline stages and handling other ISA-independent actions. We hope this separation makes it easier to implement future ISAs, as hopefully only the high level classes will have to be redefined.

## **Interaction with ThreadContext**

The [ThreadContext](/documentation/general_docs/cpu_models/execution_basics) provides interface for external objects to access thread state within the CPU. However, this is slightly complicated by the fact that the O3CPU is an out-of-order CPU. While it is well defined what the architectural state is at any given cycle, it is not well defined what happens if that architectural state is changed. Thus it is feasible to do reads to the ThreadContext without much effort, but doing writes to the ThreadContext and altering register state requires the CPU to flush the entire pipeline. This is because there may be in flight instructions that depend on the register that has been changed, and it is unclear if they should or should not view the register update. Thus accesses to the ThreadContext have the potential to cause slowdown in the CPU simulation.

## **Backend Pipeline**
### Compute Instructions
Compute instructions are simpler as they do not access memory and
do not interact with the LSQ. Included below is a high-level calling chain
(only important functions) with a description about the functionality of each.

```cpp
Rename::tick()->Rename::RenameInsts()
IEW::tick()->IEW::dispatchInsts()
IEW::tick()->InstructionQueue::scheduleReadyInsts()
IEW::tick()->IEW::executeInsts()
IEW::tick()->IEW::writebackInsts()
Commit::tick()->Commit::commitInsts()->Commit::commitHead()
```

- Rename (`Rename::renameInsts()`).
As suggested by the name, registers are renamed and the instruction
is pushed to the IEW stage. It checks that the IQ/LSQ can hold the new
instruction.
- Dispatch (`IEW::dispatchInsts()`).
This function inserts the renamed instruction into the IQ and LSQ.
- Schedule (`InstructionQueue::scheduleReadyInsts()`)
The IQ manages the ready instructions (operands ready) in a ready list,
and schedules them to an available FU. The latency of the FU is set here,
and instructions are sent to execution when the FU done.
- Execute (`IEW::executeInsts()`).
Here `execute()` function of the compute instruction is invoked and
sent to commit. Please note `execute()` will write results to the destiniation
register.
- Writeback (`IEW::writebackInsts()`).
Here `InstructionQueue::wakeDependents()` is invoked. Dependent
instructions will be added to the ready list for scheduling.
- Commit (`Commit::commitInsts()`).
Once the instruction reaches the head of ROB, it will be committed and
released from ROB.

### Load Instruction
Load instructions share the same path as compute instructions until
execution.

```cpp
IEW::tick()->IEW::executeInsts()
  ->LSQUnit::executeLoad()
    ->StaticInst::initiateAcc()
      ->LSQ::pushRequest()
        ->LSQUnit::read()
          ->LSQRequest::buildPackets()
          ->LSQRequest::sendPacketToCache()
    ->LSQUnit::checkViolation()
DcachePort::recvTimingResp()->LSQRequest::recvTimingResp()
  ->LSQUnit::completeDataAccess()
    ->LSQUnit::writeback()
      ->StaticInst::completeAcc()
      ->IEW::instToCommit()
IEW::tick()->IEW::writebackInsts()
```

- `LSQUnit::executeLoad()` will initiate the access by invoking the
instruction's `initiateAcc()` function. Through the execution context interface,
`initiateAcc()` will call `initiateMemRead()` and eventually be directed
to `LSQ::pushRequest()`.
- `LSQ::pushRequest()` will allocate a `LSQRequest` to track all states, and
start translation. When the translation completes, it will
record the virtual address and invoke `LSQUnit::read()`.
- `LSQUnit::read()` will check if the load is aliased with any previous
store.
  - If can it can forward, then it will schedule `WritebackEvent` for the next
cycle.
  - If it is aliased but cannot forward, it calls
  `InstructionQueue::rescheduleMemInst()` and `LSQReuqest::discard()`.
  - Otherwise, it send packets to the cache.
- `LSQUnit::writeback()` will invoke `StaticInst::completeAcc()`, which
will write a loaded value to the destination register. The
instruction is then pushed to the commit queue. `IEW::writebackInsts()`
will then mark it done and wake up its dependents. Starting from here it
shares same path as compute instructions.

### Store Instruction
Store instructions are similar to load instructions, but only writeback
to cache after committed.

```cpp
IEW::tick()->IEW::executeInsts()
  ->LSQUnit::executeStore()
    ->StaticInst::initiateAcc()
      ->LSQ::pushRequest()
        ->LSQUnit::write()
    ->LSQUnit::checkViolation()
Commit::tick()->Commit::commitInsts()->Commit::commitHead()
IEW::tick()->LSQUnit::commitStores()
IEW::tick()->LSQUnit::writebackStores()
  ->LSQRequest::buildPackets()
  ->LSQRequest::sendPacketToCache()
  ->LSQUnit::storePostSend()
DcachePort::recvTimingResp()->LSQRequest::recvTimingResp()
  ->LSQUnit::completeDataAccess()
    ->LSQUnit::completeStore()
```

- Unlike `LSQUnit::read()`, `LSQUnit::write()` will only copy the store
data, but not send the packet to cache, as the store is not committed yet.
- After the store is committed, `LSQUnit::commitStores()` will mark the SQ
entry as `canWB` so that `LSQUnit::writebackStores()` will send
the store request to cache.
- Finally, when the response comes back, `LSQUnit::completeStore()` will
release the SQ entries.

### Branch Misspeculation

Branch misspeculation is handled in `IEW::executeInsts()`. It will
notify the commit stage to start squashing all instructions in the ROB
on the misspeculated branch.

```cpp
IEW::tick()->IEW::executeInsts()->IEW::squashDueToBranch()
```

### Memory Order Misspeculation

The `InstructionQueue` has a `MemDepUnit` to track memory order dependence.
The IQ will not schedule an instruction if MemDepUnit states there is
dependency.

In `LSQUnit::read()`, the LSQ will search for possible aliasing store and
forward if possible. Otherwise, the load is blocked and rescheduled for when
the blocking store completes by notifying the MemDepUnit.

Both `LSQUnit::executeLoad/Store()` will call `LSQUnit::checkViolation()`
to search the LQ for possible misspeculation. If found, it will set
`LSQUnit::memDepViolator` and `IEW::executeInsts()` will start later to
squash the misspeculated instructions.

```cpp
IEW::tick()->IEW::executeInsts()
  ->LSQUnit::executeLoad()
    ->StaticInst::initiateAcc()
    ->LSQUnit::checkViolation()
  ->IEW::squashDueToMemOrder()
```
