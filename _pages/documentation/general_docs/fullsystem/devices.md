---
layout: documentation
title: Devices
parent: fullsystem
doc: gem5 documentation
permalink: documentation/general_docs/fullsystem/devices
---

# Devices in full system mode

## I/O Device Base Classes

The base classes in src/dev/\*_device.\* allow devices to be created with reasonable ease.
The classes and virtual functions that must be implemented are listed below.
Before reading the following it will help to be familiar with the [Memory_System](../memory_system).

### PioPort

The PioPort class is a programmed I/O port that all devices that are sensitive to an address range use.
The port takes all the memory access types and roles them into one `read()` and `write()` call that the device must respond to.
The device must also provide the `addressRanges()` function with which it returns the address ranges it is interested in.
If desired a device could have more than one PIO port.
However in the normal case it would only have one port and return multiple ranges when the `addressRange()` function is called. The only time multiple PIO ports would be desirable is if your device wanted to have separate connection to two memory objects.

### PioDevice

This is the base class which all devices senstive to an address range inherit from.
There are three pure virtual functions which all devices must implement `addressRanges()`, `read()`, and `write()`.
The magic to choose which mode we are in, etc is handled by the PioPort so the device doesn't have to bother.

Parameters for each device should be in a Params struct derived from `PioDevice::Params`.

### BasicPioDevice

Since most PioDevices only respond to one address range `BasicPioDevice` provides an `addressRanges()` and parameters for the normal pio delay and the address to which the device responds to.
Since the size of the device normally isn't configurable a parameter is not used for this and anything that inherits from this class is expected to write it's size into pioSize in its constructor.

### DmaPort

The DmaPort (in dma_device.hh) is used only for device mastered accesses.
The `recvTimingResp()` method must be available to responses (nacked or not) to requests it makes.
The port has two public methods `dmaPending()` which returns if the dma port is busy (e.g. It is still trying to send out all the pieces of the last request).
All the code to break requests up into suitably sized chunks, collect the potentially multiple responses and respond to the device is accessed through `dmaAction()`.
A command, start address, size, completion event, and possibly data is handed to the function which will then execute the completion events `process()` method when the request has been completed.
Internally the code uses `DmaReqState` to manage what blocks it has received and to know when to execute the completion event.

### DmaDevice

This is the base class from which a DMA non-pci device would inherit from, however none of those exist currently within M5. The class does have some methods `dmaWrite()`, `dmaRead()` that select the appropriate command from a DMA read or write operation.

### NIC Devices

The gem5 simulator has two different Network Interface Cards (NICs) devices that can be used to connect together two simulation instances over a simulated ethernet link.

#### Getting a list of packets on the ethernet link

You can get a list of the packet on the ethernet link by creating a Etherdump object, setting it's file parameter, and setting the dump parameter on the EtherLink to it.
This is easily accomplished with our fs.py example configuration by adding the command line option \-\-etherdump=\<filename\>. The resulting file will be named \<file\> and be in a standard pcap format.
This file can be read with [wireshark](https://www.wireshark.org/) or anything else that understands the pcap format.


### PCI devices
```
To do: Explanation of platforms and systems, how they’re related, and what they’re each for
```
