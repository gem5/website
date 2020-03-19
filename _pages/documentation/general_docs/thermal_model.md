---
layout: documentation
title: Power and Thermal Model
doc: gem5 documentation
parent: thermal_model
permalink: /documentation/general_docs/thermal_model
---

# Power and Thermal Model

This document gives an overview of the power and thermal modelling
infrastructure in Gem5.

The purpose is to give a high level view of all the pieces involved and how
they interact with each other and the simulator.

## Class overview

Classes involved in the power model are:

* [PowerModel](http://doxygen.gem5.org/release/current/classPowerModel.html):
Represents a power model for a hardware component.
* [PowerModelState](
http://doxygen.gem5.org/release/current/classPowerModelState.html): Represents a
power model for a hardware component in a certain power state. It is an
abstract class that defines an interface that must be implemented for each
model.
* [MathExprPowerModel](
http://doxygen.gem5.org/release/current/classMathExprPowerModel.html): Simple
implementation of [PowerModelState](
http://doxygen.gem5.org/release/current/classPowerModelState.html) that assumes
that power can be modeled using a simple power.

Classes involved in the thermal model are:

* [ThermalModel](http://doxygen.gem5.org/release/current/classThermalModel.html):
Contains the system thermal model logic and state. It performs the power query
and temperature update. It also enables gem5 to query for temperature (for OS
reporting).
* [ThermalDomain](http://doxygen.gem5.org/release/current/classThermalDomain.html):
Represents an entity that generates heat. It's essentially a group of
[SimObjects](http://doxygen.gem5.org/release/current/classSubSystem.html) grouped
under a SubSystem component that have its own thermal behaviour.
* [ThermalNode](http://doxygen.gem5.org/release/current/classThermalNode.html):
Represents a node in the thermal circuital equivalent. The node has a
temperature and interacts with other nodes through connections (thermal
resistors and capacitors).
* [ThermalReference](
http://doxygen.gem5.org/release/current/classThermalReference.html): Temperature
reference for the thermal model (essentially a thermal node with a fixed
temperature), can be used to model air or any other constant temperature
domains.
* [ThermalEntity](http://doxygen.gem5.org/release/current/classThermalEntity.html):
A thermal component that connects two thermal nodes and models a thermal
impedance between them. This class is just an abstract interface.
* [ThermalResistor](
http://doxygen.gem5.org/release/current/classThermalResistor.html): Implements
[ThermalEntity](http://doxygen.gem5.org/release/current/classThermalEntity.html) to
model a thermal resistance between the two nodes it connects. Thermal
resistances model the capacity of a material to transfer heat (units in K/W).
* [ThermalCapacitor](
http://doxygen.gem5.org/release/current/classThermalCapacitor.html): Implements
[ThermalEntity](http://doxygen.gem5.org/release/current/classThermalEntity.html) to
model a thermal capacitance. Thermal capacitors are used to model material's
thermal capacitance, this is, the ability to change a certain material
temperature (units in J/K).

## Thermal model

The thermal model works by creating a circuital equivalent of the simulated
platform. Each node in the circuit has a temperature (as voltage equivalent)
and power flows between nodes (as current in a circuit).

To build this equivalent temperature model the platform is required to group
the power actors (any component that has a power model) under SubSystems and
attach ThermalDomains to those subsystems. Other components might also be
created (like ThermalReferences) and connected all together by creating thermal
entities (capacitors and resistors).

Last step to conclude the thermal model is to create the [ThermalModel](
http://doxygen.gem5.org/release/current/classThermalModel.html) instance itself and
attach all the instances used to it, so it can properly update them at runtime.
Only one thermal model instance is supported right now and it will
automatically report temperature when appropriate (ie. platform sensor
devices).

## Power model

Every [ClockedObject](
http://doxygen.gem5.org/release/current/classClockedObject.html) has a power model
associated. If this power model is non-null power will be calculated at every
stats dump (although it might be possible to force power evaluation at any
other point, if the power model uses the stats, it is a good idea to keep both
events in sync). The definition of a power model is quite vague in the sense
that it is as flexible as users want it to be. The only enforced contraints so
far is the fact that a power model has several power state models, one for each
possible power state for that hardware block. When it comes to compute power
consumption the power is just the weighted average of each power model.

A power state model is essentially an interface that allows us to define two
power functions for dynamic and static. As an example implementation a class
called [MathExprPowerModel](
http://doxygen.gem5.org/release/current/classMathExprPowerModel.html) has been
provided. This implementation allows the user to define a power model as an
equation involving several statistics. There's also some automatic (or "magic")
variables such as "temp", which reports temperature.
