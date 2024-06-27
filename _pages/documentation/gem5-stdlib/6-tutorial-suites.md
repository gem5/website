---
layout: documentation
title: Suites in gem5
parent: gem5-standard-library
doc: gem5 documentation
permalink: /documentation/gem5-stdlib/suites
author: Kunal Pai, Harshil Patel
---

## Introduction

Suite is a new category of resource introduced in gem5 version 23.1, which allows users to group workloads.
SuiteResource class is added to the resource specialization.
Pre-made suites on the gem5 resources can be obtained using `obtain_resource()` like all other resources. 

SuiteResource class has `__iter__` and `__len__` functions.
A SuiteResource will behave as an iterator that returns a generator of the workload objects. 

### How to Get a Suite

To get a suite already in gem5 resources, we can use the `obtain_resource` function present in the `[resource.py](http://resource.py)`.

To get a suite with ID “riscv-vertical-microbenchmarks” and version “1.0.0”

```python
suite_obj = obtain_resource(id = "riscv-vertical-microbenchmarks", resource_version="1.0.0")
```

Not specifying the resource_version will return the latest compatible version of the resource.

**NOTE**: The Suite used for the rest of the tutorial is the “riscv-vertical-microbenchmarks”, which exists in gem5 resources, but is only compatible with gem5 version 23.1 and above and with the RISC-V ISA.

### How to Filter a Workload in the Suite by Input Groups

Each suite had a workloads field which is an array containing the ID, version, and input groups of all the workloads in the suite.

The workload field would look like the following:

```python
[
	{
		'id': 'riscv-cca-run',
		'resource_version': '1.0.0',
		'input_group': ['cca']
	},
	{
		'id': 'riscv-cce-run',
		'resource_version': '1.0.0',
		'input_group': ['cce']
	},
	{
		'id': 'riscv-ccm-run',
		'resource_version': '1.0.0',
		'input_group': ['ccm']
	},
	...
]
```

The SuiteResource class has functions that allow users to filter workloads by input groups.
The function `get_input_groups()`  returns a set of all the input groups present in the suite.
The function `with_input_group(str)` returns a SuiteResource object which only has the workloads with the input group passed in as a parameter.
For example, our suite has the workloads field as defined above then, `get_input_groups()` will return the following:

```python
set(['cca','cce','ccm',...])
```

We can use the `with_input_group()` like this:

```python
suite_obj = obtain_resource('riscv-vertical-microbenchmarks')
filtered_suite = suite_obj.with_input_group('cca')
```

This will return a `SuiteResource` with all the workloads that fulfill the case of having input group “cca”, which in this case is the `WorkloadResource` with ID “riscv-cca-run”.

We can also use the `with_input_group()` function along with a for loop and a generator.

```python
for workload in suite_obj.with_input_group('cca')
	board.set_workload(workload)
	simulator = Simulator(board=board)
	simulator.run()
```

### Make a Custom Suite

Custom suites can also be made by directly using the `SuiteResource` class from `[resource.py](http://resource.py)`.
To create a custom suite we will also need `WorkloadResource` objects.

```python
workload1= obtain_resource('workload-1', resource_version='1.0.0')
workload2= obtain_resource('workload-2', resource_version='1.0.0')

suite_obj = SuiteResource(workloads=[workload1, workload2])
```

The above code snippet will create a suite object with two workloads.
We have not defined the `workloads` field in the above suite so the `get_input_group()` and `with_input_group()` functions will throw a warning and return an empty set and a suite object with no workloads respectively.

If the `workloads` field is added then the custom suite will function the same as a suite created by using `obtain_resource`.

```python
workload1= obtain_resource('workload-1', resource_version='1.0.0')
workload2= obtain_resource('workload-2', resource_version='1.0.0')
workloads = [
	{
		'id': 'workload-1',
		'resource_version': '1.0.0',
		'input_group': ['input_group_1', 'input_group_2']
	},
	{
		'id': 'workload-2',
		'resource_version': '1.0.0',
		'input_group': ['input_group_1', 'input_group_3']
	}]
suite_obj = SuiteResource(workloads=[workload1, workload2], worklaods= workloads)
```
