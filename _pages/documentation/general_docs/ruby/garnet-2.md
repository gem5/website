---
layout: documentation
title: "Garnet 2.0"
doc: gem5 documentation
parent: ruby
permalink: /documentation/general_docs/ruby/garnet-2/
author: Jason Lowe-Power
---

**More details of the gem5 Ruby Interconnection Network are
[here](interconnection-network "wikilink").**

### Garnet2.0: An On-Chip Network Model for Heterogeneous SoCs

Garnet2.0 is a detailed interconnection network model inside gem5. It is
in active development, and patches with more features will be
periodically pushed into gem5. **Additional garnet-related patches and
tool support under development (not part of the repo) can be found at
the** [Garnet page at Georgia
Tech](http://synergy.ece.gatech.edu/tools/garnet).

Garnet2.0 builds upon the original Garnet model which was published in
[2009](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=4919636%7CISPASS).

If your use of Garnet contributes to a published paper, please cite the
following paper:

```
    @inproceedings{garnet,
      title={GARNET: A detailed on-chip network model inside a full-system simulator},
      author={Agarwal, Niket and Krishna, Tushar and Peh, Li-Shiuan and Jha, Niraj K},
      booktitle={Performance Analysis of Systems and Software, 2009. ISPASS 2009. IEEE International Symposium on},
      pages={33--42},
      year={2009},
      organization={IEEE}
    }
```

Garnet2.0 provides a cycle-accurate micro-architectural implementation
of an on-chip network router. It leverages the [Topology](
/documentation/general_docs/ruby/interconnection-network#Topology) and [Routing](
/documentation/general_docs/ruby/interconnection-network#Routing) frastructure
provided by gem5's ruby memory system model. The default router is a
state-of-the-art 1-cycle pipeline. There is support to add additional
delay of any number of cycles in any router, by specifying it within the
topology.

Garnet2.0 can also be used to model an off-chip interconnection network
by setting appropriate delays in the routers and links.

- **Related Files**:
  - **src/mem/ruby/network/Network.py**
  - **src/mem/ruby/network/garnet2.0/GarnetNetwork.py**
  - **src/mem/ruby/network/Topology.cc**

## Invocation

The garnet networks can be enabled by adding **--network=garnet2.0**.

## Configuration

Garnet2.0 uses the generic network parameters in Network.py:

- **number_of_virtual_networks**: This is the maximum number of
  virtual networks. The actual number of active virtual networks
  is determined by the protocol.
- **control_msg_size**: The size of control messages in bytes.
  Default is 8. **m_data_msg_size** in Network.cc is set to the
  block size in bytes + control_msg_size.

Additional parameters are specified in garnet2.0/GarnetNetwork.py:

- **ni_flit_size**: flit size in bytes. Flits are the
  granularity at which information is sent from one router to the
  other. Default is 16 (=\> 128 bits). \[This default value of 16
  results in control messages fitting within 1 flit, and data
  messages fitting within 5 flits\]. Garnet requires the
  ni_flit_size to be the same as the bandwidth_factor (in
  network/BasicLink.py) as it does not model variable bandwidth
  within the network. This can also be set from the command line
  with **--link-width-bits**.
- **vcs_per_vnet**: number of virtual channels (VC) per virtual
  network. Default is 4. This can also be set from the command
  line with **--vcs-per-vnet**.
- **buffers_per_data_vc**: number of flit-buffers per VC in the
  data message class. Since data messages occupy 5 flits, this
  value can lie between 1-5. Default is 4.
- **buffers_per_ctrl_vc**: number of flit-buffers per VC in the
  control message class. Since control messages occupy 1 flit, and
  a VC can only hold one message at a time, this value has to be
  1. Default is 1.
- **routing_algorithm**: 0: Weight-based table (default), 1: XY,
  2: Custom. More details below.

## Topology

Garnet2.0 leverages the
[Topology](/documentation/general_docs/ruby/interconnection-network#Topology)
infrastructure
provided by gem5's ruby memory system model. Any heterogeneous topology
can be modeled. Each router in the topology file can be given an
independent latency, which overrides the default. In addition, each link
has 2 optional parameters: src_outport and dst_inport, which are
strings with names of the output and input ports of the source and
destination routers for each link. These can be used inside garnet2.0 to
implement custom routing algorithms, as described next. For instance, in
a Mesh, the west to east links have src_outport set to "west" and
dst_inport" set to "east".

- **Network Components**:
    - **GarnetNetwork**: This is the top level object that
      instantiates all network interfaces, routers, and links.
      Topology.cc calls the methods to add "external links" between
      NIs and routers, and "internal links" between routers.
    - **NetworkInterface**: Each NI connects to one coherence
      controller via MsgBuffer interfaces on one side. It has a link
      to a router on the other. Every protocol message is put into a
      one-flit control or multi (default=5)-flit data (depending on
      its vnet), and injected into the router. Multiple NIs can
      connect to the same router (for e.g., in the Mesh topology,
      cache and dir controllers connect via individual NIs to the same
      router).
    - **Router**: The router manages arbitration for output links, and
      flow control between routers.
    - **NetworkLink**: Network links carry flits. They can be of one
      of 3 types: EXT_OUT_ (router to NI), EXT_IN_ (NI to router),
      and INT_ (internal router to router)
    - **CreditLink**: Credit links carry VC/buffer credits between
      routers for flow control.

## Routing

Garnet2.0 leverages the
[Routing](/documentation/general_docs/ruby/interconnection-network#Routing) infrastructure
provided by gem5's ruby memory system model. The default routing
algorithm is a deterministic table-based routing algorithm with shortest
paths. Link weights can be used to prioritize certain links over others.
See src/mem/ruby/network/Topology.cc for details about how the routing
table is populated.

**Custom Routing**: To model custom routing algorithms, say adaptive, we
provide a framework to name each link with a src_outport and
dst_inport direction, and use these inside garnet to implement routing
algorithms. For instance, in a Mesh, West-first can be implemented by
sending a flit along the "west" outport link till the flit no longer has
any X- hops remaining, and then randomly (or based on next router VC
availability) choosing one of the remaining links. See how
outportComputeXY() is implemented in
src/mem/ruby/network/garnet2.0/RoutingUnit.cc. Similarly,
outportComputeCustom() can be implemented, and invoked by adding
--routing-algorithm=2 in the command line.

**Multicast messages**: The network modeled does not have hardware
multi-cast support within the network. A multi-cast message gets broken
into multiple uni-cast messages at the Network Interface.

## Flow Control

Virtual Channel Flow Control is used in the design. Each VC can hold one
packet. There are two kinds of VCs in the design - control and data. The
buffer depth in each can be independently controlled from
GarnetNetwork.py. The default values are 1-flit deep control VCs, and
4-flit deep data VCs. Default size of control packets is 1-flit, and
data packets is 5-flit.

## Router Microarchitecture

The garnet2.0 router performs the following actions:

1.  **Buffer Write (BW)**: The incoming flit gets buffered in its VC.
2.  **Route Compute (RC)** The buffered flit computes its output port,
    and this information is stored in its VC.
3.  **Switch Allocation (SA)**: All buffered flits try to reserve the
    switch ports for the next cycle. \[The allocation occurs in a
    *separable* manner: First, each input chooses one input VC, using
    input arbiters, which places a switch request. Then, each output
    port breaks conflicts via output arbiters\]. All arbiters in ordered
    virtual networks are *queueing* to maintain point-to-point ordering.
    All other arbiters are *round-robin*.
4.  **VC Selection (VS)**: The winner of SA selects a free VC (if
    HEAD/HEAD_TAIL flit) from its output port.
5.  **Switch Traversal (ST)**: Flits that won SA traverse the crossbar
    switch.
6.  **Link Traversal (LT)**: Flits from the crossbar traverse links to
    reach the next routers.

In the default design, BW, RC, SA, VS, and ST all happen in 1-cycle. LT
happens in the next cycle.

**Multi-cycle Router**: Multi-cycle routers can be modeled by specifying
a per-router latency in the topology file, or changing the default
router latency in src/mem/ruby/network/BasicRouter.py. This is
implemented by making a buffered flit wait in the router for (latency-1)
cycles before becoming eligible for SA.

## Buffer Management

Each router input port has number_of_virtual_networks Vnets, each
with vcs_per_vnet VCs. VCs in control Vnets have a depth of
buffers_per_ctrl_vc (default = 1) and VCs in data Vnets have a depth
of buffers_per_data_vc (default = 4). **Credits are used to relay
information about free VCs, and number of buffers within each VC.**

## Lifecycle of a Network Traversal

  - NetworkInterface.cc::wakeup()
      - Every NI connected to one coherence protocol controller on one
        end, and one router on the other.
      - receives messages from coherence protocol buffer in appropriate
        vnet and converts them into network packets and sends them into
        the network.
          - garnet2.0 adds the ability to capture a network trace at
            this point \[under development\].
      - receives flits from the network, extracts the protocol message
        and sends it to the coherence protocol buffer in appropriate
        vnet.
      - manages flow-control (i.e., credits) with its attached router.
      - The consuming flit/credit output link of the NI is put in the
        global event queue with a timestamp set to next cycle. The
        eventqueue calls the wakeup function in the consumer.

<!-- end list -->

  - NetworkLink.cc::wakeup()
      - receives flits from NI/router and sends it to NI/router after
        m_latency cycles delay
      - Default latency value for every link can be set from command
        line (see configs/network/Network.py)
      - Per link latency can be overwritten in the topology file
      - The consumer of the link (NI/router) is put in the global event
        queue with a timestamp set after m_latency cycles. The
        eventqueue calls the wakeup function in the consumer.

<!-- end list -->

  - Router.cc::wakeup()
      - Loop through all InputUnits and call their wakeup()
      - Loop through all OutputUnits and call their wakeup()
      - Call SwitchAllocator's wakeup()
      - Call CrossbarSwitch's wakeup()
      - The router's wakeup function is called whenever any of its
        modules (InputUnit, OutputUnit, SwitchAllocator, CrossbarSwitch)
        have a ready flit/credit to act upon this cycle.

<!-- end list -->

  - InputUnit.cc::wakeup()
      - Read input flit from upstream router if it is ready for this
        cycle
      - For HEAD/HEAD_TAIL flits, perform route computation, and update
        route in the VC.
      - Buffer the flit for (m_latency - 1) cycles and mark it valid
        for SwitchAllocation starting that cycle.
          - Default latency for every router can be set from command
            line (see configs/network/Network.py)
          - Per router latency (i.e., num pipeline stages) can be set in
            the topology file.

<!-- end list -->

  - OutputUnit.cc::wakeup()
      - Read input credit from downstream router if it is ready for this
        cycle
      - Increment the credit in the appropriate output VC state.
      - Mark output VC as free if the credit carries is_free_signal as
        true

<!-- end list -->

  - SwitchAllocator.cc::wakeup()
      - Note: SwitchAllocator performs VC arbitration and selection
        within it.
      - SA-I (or SA-i): Loop through all input VCs at every input port,
        and select one in a round robin manner.
          - For HEAD/HEAD_TAIL flits only select an input VC whose
            output port has at least one free output VC.
          - For BODY/TAIL flits, only select an input VC that has
            credits in its output VC.
      - Place a request for the output port from this VC.
      - SA-II (or SA-o): Loop through all output ports, and select one
        input VC (that placed a request during SA-I) as the winner for
        this output port in a round robin manner.
          - For HEAD/HEAD_TAIL flits, perform outvc allocation (i.e.,
            select a free VC from the output port.
          - For BODY/TAIL flits, decrement a credit in the output vc.
      - Read the flit out from the input VC, and send it to the
        CrossbarSwitch
      - Send a increment_credit signal to the upstream router for this
        input VC.
          - for HEAD_TAIL/TAIL flits, mark is_free_signal as true in
            the credit.
          - The input unit sends the credit out on the credit link to
            the upstream router.
      - Reschedule the Router to wakeup next cycle for any flits ready
        for SA next cycle.

<!-- end list -->

  - CrossbarSwitch.cc::wakeup()
      - Loop through all input ports, and send the winning flit out of
        its output port onto the output link.
      - The consuming flit output link of the router is put in the
        global event queue with a timestamp set to next cycle. The
        eventqueue calls the wakeup function in the consumer.

<!-- end list -->

  - NetworkLink.cc::wakeup()
      - receives flits from NI/router and sends it to NI/router after
        m_latency cycles delay
      - Default latency value for every link can be set from command
        line (see configs/network/Network.py)
      - Per link latency can be overwritten in the topology file
      - The consumer of the link (NI/router) is put in the global event
        queue with a timestamp set after m_latency cycles. The
        eventqueue calls the wakeup function in the consumer.

## Running Garnet2.0 with Synthetic Traffic

Garnet2.0 can be run in a standalone manner and fed with synthetic
traffic. The details are described here: **[Garnet Synthetic
Traffic](/documentation/general_docs/ruby/garnet_synthetic_traffic)**
