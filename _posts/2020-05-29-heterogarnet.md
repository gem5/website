---
layout: post
title:  "HeteroGarnet - A Detailed Simulator for Diverse Interconnect Systems"
author: Srikant Bharadwaj, Jieming Ying, Bradford Beckmann, and Tushar Krishna
date:   2020-05-27
---

Networks-on-Chips (NoCs) have become inevitably more complex with the increased heterogeneity of Systems-On-Chip (SoCs). Recent advances in die-stacking and 2.5D chip integration introduce in-package network heterogeneities that can complicate the interconnect design. Detailed modeling of such complex systems necessitates accurate modeling of their characteristics. Unfortunately, NoC simulators today lack the flexibility and features required to model these diverse interconnects.

We present HeteroGarnet, that improves upon the widely-popular Garnet 2.0 network model by enabling accurate simulation of emerging interconnect systems. Specifically, HeteroGarnet adds support for clock-domain islands, network crossings supporting multiple frequency domains, and network interface controllers capable of attaching to multiple physical links. It also supports variable bandwidth links and routers by introducing a new configurable Serializer-Deserializer component. Our recent work using HeteroGarnet [1] shows how accurate interconnect modeling can lead to better network designs. In this presentation, we will introduce HeteroGarnet and its benefits for modeling modern heterogeneous systems. HeteroGarnet is planned to be integrated into the gem5 repository and will be identified as Garnet 3.0.

# Workshop Presentation

<iframe width="960" height="540" src="https://www.youtube.com/embed/AH9r44r2lHA"
frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope;
picture-in-picture" allowfullscreen style="max-width: 960px";></iframe>
