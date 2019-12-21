---
layout: documentation
title: Garnet Synthetic Traffic
doc: gem5 documentation
parent: directed_testers
permalink: /documentation/general_docs/debugging_and_testing/directed_testers/garnet_synthetic_traffic/
author: Bobby R. Bruce
---

# Garnet Synthetic Traffic

The Garnet Synthetic Traffic provides a framework for simulating the Garnet
network with controlled inputs. This is useful for network testing/debugging,
or for network-only simulations with synthetic traffic.

**Note: The garnet synthetic traffic injector only works with Garnet_standalone
coherence protocol.**

## Related Files

* `configs/example/garnet_synth_traffic.py` : file to invoke the network tester
* `src/cpu/tester/garnet_sythetic_taffic/GarnetSyntheticTraffic.*` : files
implementing the tester

## How to run

First build gem5 with the Garnet_standalone coherence protocol. This protocol
is ISA-agnostic, and hence we build it with the NULL ISA.

```
scons build/NULL/gem5.debug PROTOCOL=Garnet_standalone
```

Example command:

```
./build/NULL/gem5.debug configs/example/garnet_synth_traffic.py  \
--num-cpus=16 \
--num-dirs=16 \
--network=garnet2.0 \
--topology=Mesh_XY \
--mesh-rows=4  \
--sim-cycles=1000 \
--synthetic=uniform_random \
--injectionrate=0.01
```

## Parameterized Options

|System Configuration &nbsp; &nbsp; &nbsp;         |Description                                                                              |
|:---------------------|:----------------------------------------------------------------------------------------|
|`--num-cpus`          |Number of cpus. This is the number of source (injection) nodes in the network.           |
|`--num-dirs`          |Number of directories. This is the number of destination (ejection) nodes in the network.|
|`--network`           |Network model: simple or garnet2.0. Use garnet2.0 for running synthetic traffic.         |
|`--topology`          |Topology for connecting the cpus and dirs to the network routers/switches.               |
|`--mesh-rows`         |The number of rows in the mesh. Only valid when --topology is Mesh* MeshDirCorners*      |

<br>
<br>

|Network Configuration &nbsp;       |Description                                                                                                                             |
|:---------------------|:---------------------------------------------------------------------------------------------------------------------------------------|
|`--router-latency`    | Default number of pipeline stages in the garnet router. Has to be >= 1. Can be over-ridden on a per router basis in the topology file. |
|`--link-latency`      | Default latency of each link in the network. Has to be >= 1. Can be over-ridden on a per link basis in the topology file.              |
|`--vcs-per-vnet`      | Number of VCs per Virtual Network.                                                                                                     |
|`--link-width-bits`   | Width in bits for all links inside the garnet network. Default = 128.                                                                  |

<br>
<br>

|Traffic Injection Configuration &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  |Description |
|:---------------------|:-----------|
|`--sim-cycles`        | Total number of cycles for which the simulation should run. |
|`--synthetic`         | The type of synthetic traffic to be injected. The following synthetic traffic patterns are currently supported: `uniform_random`, `tornado`, `bit_complement`, `bit_reverse`, `bit_rotation`, `neighbor`, `shuffle`, and `transpose` |
|`--injectionrate`     | Traffic Injection Rate in `packets/node/cycle`. It can take any decimal value between 0 and 1. The number of digits of precision after the decimal point can be controlled by `--precision` which is set to 3 as default in `garnet_synth_traffic.py`. |
|`--single-sender-id`  | Only inject from this sender. To send from all nodes, set to -1. |
|`--single-dest-id`    | Only send to this destination. To send to all destinations as specified by the synthetic traffic pattern, set to -1. |
|`--num-packets-max`   | Maximum number of packets to be injected by each cpu node. Default value is -1 (keep injecting till sim-cycles). |
|`--inj-vnet`          | Only inject in this vnet (0, 1 or 2). 0 and 1 are 1-flit, 2 is 5-flit. Set to -1 to inject randomly in all vnets. |

<br>
<br>

## Implementation of Garnet Synthetic Traffic

The synthetic traffic injector is implemente in `GarnetSnytheticTraffic.cc`.
The sequence of steps involved in generating and sending a packet are as
follows.

* Every cycle, each cpu performs a bernouli trial with probability equal to
--injectionrate to determine whether to generate a packet or not.
* If `--num-packets-max` is non negative, each cpu stops generating new packets
after generating `--num-packets-max` number of packets. The injector terminates
after `--sim-cycles`.
* If the cpu has to generate a new packet, it computes the destination for the
new packet based on the synthetic traffic type (`--synthetic`).
* This destination is embedded into the bits after block offset in the packet
address.
* The generated packet is randomly tagged as a `ReadReq`, or an `INST_FETCH`,
or a `WriteReq`, and sent to the Ruby Port
(`src/mem/ruby/system/RubyPort.hh/cc`).
* The Ruby Port converts the packet into a `RubyRequestType:LD`,
`RubyRequestType:IFETCH`, and `RubyRequestType:ST`, respectively, and sends it
to the Sequencer, which in turn sends it to the Garnet_standalone cache
controller.
* The cache controller extracts the destination directory from the packet
address.
* The cache controller injects the `LD`, `IFETCH` and `ST` into virtual
networks 0, 1 and 2 respectively.
* `LD` and `IFETCH` are injected as control packets (8 bytes), while `ST` is
injected as a data packet (72 bytes).
* The packet traverses the network and reaches the directory.
* The directory controller simply drops it.
