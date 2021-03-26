---
layout: documentation
title: "Interconnection network"
doc: gem5 documentation
parent: ruby
permalink: /documentation/general_docs/ruby/interconnection-network/
author: Jason Lowe-Power
---

# Interconnection Network

The various components of the interconnection network model inside
gem5's ruby memory system are described here.

## How to invoke the network

**Simple Network**:

```
./build/<ISA>/gem5.debug \
                      configs/example/ruby_random_test.py \
                      --num-cpus=16  \
                      --num-dirs=16  \
                      --network=simple
                      --topology=Mesh_XY  \
                      --mesh-rows=4
```

The default network is simple, and the default topology is crossbar.

**Garnet network**:

```
./build/<ISA>/gem5.debug \
                      configs/example/ruby_random_test.py  \
                      --num-cpus=16 \
                      --num-dirs=16  \
                      --network=garnet2.0 \
                      --topology=Mesh_XY \
                      --mesh-rows=4
```

## Topology

The connection between the various controllers are specified via python
files. All external links (between the controllers and routers) are
bi-directional. All internal links (between routers) are uni-directional
-- this allows a per-direction weight on each link to bias routing
decisions.

- **Related Files**:
    - **src/mem/ruby/network/topologies/Crossbar.py**
    - **src/mem/ruby/network/topologies/CrossbarGarnet.py**
    - **src/mem/ruby/network/topologies/Mesh_XY.py**
    - **src/mem/ruby/network/topologies/Mesh_westfirst.py**
    - **src/mem/ruby/network/topologies/MeshDirCorners_XY.py**
    - **src/mem/ruby/network/topologies/Pt2Pt.py**
    - **src/mem/ruby/network/Network.py**
    - **src/mem/ruby/network/BasicLink.py**
    - **src/mem/ruby/network/BasicRouter.py**



- **Topology Descriptions**:
  - **Crossbar**: Each controller (L1/L2/Directory) is connected to
    a simple switch. Each switch is connected to a central switch
    (modeling the crossbar). This can be invoked from command line
    by **--topology=Crossbar**.
  - **CrossbarGarnet**: Each controller (L1/L2/Directory) is
    connected to every other controller via one garnet router (which
    internally models the crossbar and allocator). This can be
    invoked from command line by **--topology=CrossbarGarnet**.
  - **Mesh_\***: This topology requires the number of directories
    to be equal to the number of cpus. The number of
    routers/switches is equal to the number of cpus in the system.
    Each router/switch is connected to one L1, one L2 (if present),
    and one Directory. The number of rows in the mesh **has to be
    specified** by **--mesh-rows**. This parameter enables the
    creation of non-symmetrical meshes too.
      - **Mesh_XY**: Mesh with XY routing. All x-directional links
        are biased with a weight of 1, while all y-directional links
        are biased with a weight of 2. This forces all messages to
        use X-links first, before using Y-links. It can be invoked
        from command line by **--topology=Mesh_XY**
      - **Mesh_westfirst**: Mesh with west-first routing. All
        west-directional links are biased with a weight of 1, al
        other links are biased with a weight of 2. This forces all
        messages to use west-directional links first, before using
        other links. It can be invoked from command line by
        **--topology=Mesh_westfirst**
  - **MeshDirCorners_XY**: This topology requires the number of
    directories to be equal to 4. number of routers/switches is
    equal to the number of cpus in the system. Each router/switch is
    connected to one L1, one L2 (if present). Each corner
    router/switch is connected to one Directory. It can be invoked
    from command line by **--topology=MeshDirCorners_XY**. The
    number of rows in the mesh **has to be specified** by
    **--mesh-rows**. The XY routing algorithm is used.
  - **Pt2Pt**: Each controller (L1/L2/Directory) is connected to
    every other controller via a direct link. This can be invoked
    from command line by
  - **Pt2Pt**: All to all point-to-point connection

![](http://pwp.gatech.edu/ece-synergy/wp-content/uploads/sites/332/2016/10/topologies.jpg)

**In each topology, each link and each router can independently be
passed a parameter that overrides the defaults (in BasicLink.py and
BasicRouter.py)**:

  - **Link Parameters:**
      - **latency**: latency of traversal within the link.
      - **weight**: weight associated with this link. This parameter is
        used by the routing table while deciding routes, as explained
        next in [Routing](Interconnection_Network#Routing "wikilink").
      - **bandwidth_factor**: Only used by simple network to specify
        width of the link in bytes. This translates to a bandwidth
        multiplier (simple/SimpleLink.cc) and the individual link
        bandwidth becomes bandwidth multiplier x endpoint_bandwidth
        (specified in SimpleNetwork.py). In garnet, the bandwidth is
        specified by ni_flit_size in GarnetNetwork.py)


  - **Internal Link Parameters:**
      - **src_outport**: String with name for output port from source
        router.
      - **dst_inport**: String with name for input port at destination
        router.

These two parameters can be used by routers to implement custom routing
algorithms in garnet2.0

  - **Router Parameters:**
      - **latency**: latency of each router. Only supported by
        garnet2.0.

## Routing

**Table-based Routing (Default):** Based on the topology, shortest
path graph traversals are used to populate *routing tables* at each
router/switch. This is done in src/mem/ruby/network/Topology.cc The
default routing algorithm is table-based and tries to choose the route
with minimum number of link traversals. Links can be given weights in
the topology files to model different routing algorithms. For example,
in Mesh_XY.py and MeshDirCorners_XY.py Y-direction links are given
weights of 2, while X-direction links are given weights of 1, resulting
in XY traversals. In Mesh_westfirst.py, the west-links are given
weights of 1, and all other links are given weights of 2. In garnet2.0,
the routing algorithm randomly chooses between links with equal weights.
In simple network, it statically chooses between links with equal
weights.

**Custom Routing algorithms:** In garnet2.0, we provide additional
support to implement custom (including adaptive) routing algorithms (See
outportComputeXY() in src/mem/ruby/network/garnet2.0/RoutingUnit.cc).
The src_outport and dst_inport fields of the links can be used to give
custom names to each link (e.g., directions if a mesh), and these can be
used inside garnet to implement any routing algorithm. A custom routing
algorithm can be selected from the command line by setting
--routing-algorithm=2. See configs/network/Network.py and
src/mem/ruby/network/garnet2.0/GarnetNetwork.py

## Flow-Control and Router Microarchitecture

Ruby supports two network models, Simple and Garnet, which trade-off
detailed modeling versus simulation speed respectively.

### Simple Network

The default network model in Ruby is the simple network.

- **Related Files**:
    - **src/mem/ruby/network/Network.py**
    - **src/mem/ruby/network/simple**
    - **src/mem/ruby/network/simple/SimpleNetwork.py**

## Configuration

Simple network uses the generic network parameters in Network.py:

- **number_of_virtual_networks**: This is the maximum number of
      virtual networks. The actual number of active virtual networks
      is determined by the protocol.
- **control_msg_size**: The size of control messages in bytes.
      Default is 8. **m_data_msg_size** in Network.cc is set to the
      block size in bytes + control_msg_size.

Additional parameters are specified in simple/SimpleNetwork.py:

- **buffer_size**: Size of buffers at each switch input and
  output ports. A value of 0 implies infinite buffering.
- **endpoint_bandwidth**: Bandwidth at the end points of the
  network in 1000th of byte.
- **adaptive_routing**: This enables adaptive routing based on
  occupancy of output buffers.

## Switch Model

The simple network models hop-by-hop network traversal, but abstracts
out detailed modeling within the switches. The switches are modeled in
simple/PerfectSwitch.cc while the links are modeled in
simple/Throttle.cc. The flow-control is implemented by monitoring the
available buffers and available bandwidth in output links before
sending.

![Simple_network.jpg](/assets/img/Simple_network.jpg "Simple_network.jpg")


### Garnet2.0

Details of the new (2016) Garnet2.0 network are
**[here](garnet-2)**.

## Running the Network with Synthetic Traffic

The interconnection networks can be run in a standalone manner and fed
with synthetic traffic. We recommend doing this with garnet2.0.

**[Running Garnet Standalone with Synthetic Traffic](/documentation/general_docs/ruby/garnet_synthetic_traffic)**
