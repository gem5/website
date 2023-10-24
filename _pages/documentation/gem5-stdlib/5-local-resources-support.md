---
layout: documentation
title: Local Resources Support in gem5
parent: gem5-standard-library
doc: gem5 documentation
permalink: /documentation/gem5-stdlib/local-resources-support
author: Kunal Pai, Harshil Patel
---

This tutorial will walk you through the process of creating a WorkloadResource in gem5 and testing it, through the new gem5 Resources infrastructure introduced in gem5 v23.0.

A workload is set to a board in gem5 through the following line:

``` python
board.set_workload(obtain_resource(<ID_OF_WORKLOAD>))
```

The following image shows what a Resource ID is, as viewed on the [gem5 Resources website](https://resources.gem5.org/):
![gem5 resource ID example](/assets/img/stdlib/gem5-resource-id-example.png)

Therefore, the WorkloadResource with ID '<ID_OF_WORKLOAD>' will be parsed and it will be used to construct the function call it defines. 

The function call specified in the `"function"` field of the Workload JSON is then executed on the board, along with any parameters it has defined in the `"additional_parameters"` field.

## Introduction

The gem5 Resources infrastructure allows adding a local JSON data source that can be added to the main gem5 Resources MongoDB database.

We will use the local JSON data source to add a new WorkloadResource to gem5.

## Prerequisites

This tutorial assumes that you already have a pre-compiled Resource that you want to make into a WorkloadResource.

## Defining the Workload

### Defining the Resource JSON

The first step is to define the Resource that is used in a WorkloadResource.
In case the Resource already exists in gem5, you may skip this step.
Let's assume that the Resource we want to wrap in a WorkloadResource is compiled for `RISC-V`, categorized as a `binary`, and has the name `my-benchmark`.

We can define this Resource in a JSON object as follows:

``` json
{
    "category": "binary",
    "id": "my-benchmark",
    "description": "A RISCV binary used to test a specific RISCV instruction.",
    "architecture": "RISCV",
    "is_zipped": false,
    "resource_version": "1.0.0",
    "gem5_versions": [
        "23.0"
    ],
}
```

It is important to initialize all the fields here correctly, as they are used by gem5 to initialize and run the Resource.

To see more about the fields required and not required by the Resources, see the [gem5 Resources JSON Schema](https://github.com/gem5/gem5-resources-website/blob/main/public/gem5-resources-schema.json).

### Defining the Workload JSON

Assuming that the binary of the Resource is uploaded to gem5 Resources cloud, its source code is available on the [gem5-resources GitHub repository](https://github.com/gem5/gem5-resources/) and the Resource is viewable on the [gem5 Resources website](https://resources.gem5.org) , you can now define the Workload JSON.
Let's assume that the WorkloadResource we are building wraps `my-benchmark`, and is called `binary-workload`.

We can define this WorkloadResource in a local JSON file as follows:

``` json
{
    "id": "binary-workload",
    "category": "workload",
    "description": "A RISCV binary used to test a specific RISCV instruction.",
    "architecture": "RISCV",
    "function": "set_se_binary_workload",
    "resource_version": "1.0.0",
    "gem5_versions": [
        "23.0"
    ],
    "resources": {
        "binary": "my-benchmark"
    },
    "additional_parameters": {
        "arguments": ["arg1", "arg2"]
    }
}
```

The `"function"` field defines the function that will be called on the board.
The `"resources"` field defines the Resources that will be passed into the Workload.
The `"additional_parameters"` field defines the additional parameters that will be passed into the WorkloadResource.
So, the WorkloadResource defined above is equivalent to the following line of code:

``` python
board.set_se_binary_workload(binary = obtain_resource("binary_resource"), arguments = ["arg1", "arg2"])
```

To see more about the fields required and not required by the workloads, see the [gem5 Resources JSON Schema](https://github.com/gem5/gem5-resources-website/blob/main/public/gem5-resources-schema.json)

## Testing the Workload

To test the WorkloadResource, we first have to add the local JSON file as a data source for gem5.

This can be done by creating a new JSON file with the following format:

``` json
{
    "sources": {
        "my-resources": {
            "url": "<PATH_TO_JSON_FILE>",
            "isMongo": false,
        }
    }
}
```
On running gem5, if the new JSON config file you have created is present in the current working directory, it will be used as the data source for gem5.
If the JSON file is not present in the current working directory, you can specify the path to the JSON file using the `GEM5_CONFIG` flag while building gem5.

You should now be able to use the WorkloadResource in your simulations through its name, `binary-workload`.

**NOTE**: In order to check if the Resources you specified as part of a WorkloadResource are being passed into the WorkloadResource correctly, you can use the `get_parameters()` function in the WorkloadResource class.
This function returns a dictionary of the Resources passed into the WorkloadResource.
Its implementation can be found in [`src/python/gem5/resources/resource.py`](https://github.com/gem5/gem5/blob/6f5d877b1aacd551749dafa87da26600a4f01155/src/python/gem5/resources/resource.py#L673).

From gem5 v23.1, there are a couple additional ways to define your local `resources.json` file.
Both these ways are through environment variables and are defined through the command line while running a gem5 simulation.

1. `GEM5_RESOURCE_JSON` variable: This variable substitutes all the current data sources used by gem5 with the JSON file present at the path passed in through this variable. 
This is equivalent to a gem5 data source configuration file as follows:

    ``` json
    {
        "sources": {
            "my-resources": {
                "url": $GEM5_RESOURCE_JSON,
                "isMongo": false,
            }
        }
    }
    ```

2. `GEM5_RESOURCE_JSON_APPEND` variable: This variable adds the JSON file present at the path passed in through this variable to all the current data sources used by gem5.
This is equivalent to a gem5 data source configuration file as follows:

    ``` json
    {
        "sources": {
            "my-resources-1": {
                "url": '/local/local.json',
                "isMongo": false,
            },
                    "my-resources-2": {
                "url": $GEM5_RESOURCE_JSON_APPEND,
                "isMongo": false,
            },
        }
    }
    ```

## Support for Local Path to Resources

From gem5 v23.1, support has been added to make a workload of local resources through the method mentioned above.

This method involves making the same JSON object as mentioned in [Defining the Resource JSON](#defining-the-resource-json), with the addition of the "url" field.
This field is used in the gem5 Resources database to indicate where the file for a Resource is.
From gem5 v23.1, this field also accepts the _file_ URI scheme.
You can specify a path on your localhost and gem5 would be able to run it.

With these changes, a JSON object for a local instance of `my-benchmark` would look like:

``` json
{
    "category": "binary",
    "id": "my-benchmark",
    "description": "A RISCV binary used to test a specific RISCV instruction.",
		"url": "file:/<PATH_TO_LOCAL_FILE>",
    "architecture": "RISCV",
    "is_zipped": false,
    "resource_version": "1.1.0",
    "gem5_versions": [
        "23.0"
    ],
}
```

**NOTE**: If you are creating a local version of a Resource with an ID that exists in gem5 Resources, be sure to change the `"resource_version"` field to a resource version that does not exist in the gem5 Resources database to avoid receiving an error while running a gem5 simulation. 
