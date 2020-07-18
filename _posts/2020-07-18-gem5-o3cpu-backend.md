---
layout: post
title:  "gem5 O3CPU Backend Documentation Update"
author: Zhengrong Wang
date:   2020-07-18
categories: project
---

The documentation about gem5 O3CPU is a little bit abstract and not
closely related to the code. Therefore, this post extracts
key function chains to show how an instruction is handled by the backend,
with some basic description to ease the learning curve of the O3CPU
backend (IEW and Commit stage).

Hopefully this could help more people. Reader should already be
familiar with gem5. This post has also been added to the
[documentation]({{site.url}}/documentation/general_docs/cpu_models/O3CPU#backend-pipeline).

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
