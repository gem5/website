---
layout: documentation
title: Using local Data sources in gem5
parent: gem5-standard-library
doc: gem5 documentation
permalink: /documentation/gem5-stdlib/using-local-resources
author: Harshil Patel
---

gem5 supports using local data sources in the form of a MongoDB Atlas and JSON datasource. To utilize data sources other than the main gem5 resources database, you will need to override the gem5-resources-config.

MongoDB Atlas Config Format:
```json
{
    "sources":{
        "example-atlas-config": {
            "dataSource": "datasource name",
            "database": "database name",
            "collection": "collection name",
            "url": "Atlas data API URL",
            "authUrl": "Atlas authentication URL",
            "apiKey": "API key for data API for MongoDB Atlas",
            "isMongo": true
        }       
    }
}
```
JSON Config Format:

```json
{
    "sources":{
        "example-json-config": {
            "url": "local path to JSON file or URL to a JSON file",
            "isMongo": false
        }
    }
}
```
### Updating gem5 Resources Config

You can update the gem5 resources config in the following ways:

 - Set the GEM5_CONFIG environment variable to point to a new config file. This will override the default config.

- Have a file named gem5-config.json in the current working directory. This will also override the default config.

- If the above two methods are not used, then the default resources config will be used.

You can also override the resources config with a JSON file or add a JSON file to the config as follows:

- Use the GEM5_RESOURCE_JSON environment variable to override the default config to use a JSON file.

- GEM5_RESOURCE_JSON_APPEND environment variable to add a JSON file to the current config. 

If the gem5 resources config was updated by the GEM5_CONFIG environment variable or having a gem5-config.json in current working directory, then these flags will override or add to those configs.

Note: Overriding or appending does not modify the actual config files.

### Using Multiple Data Sources

gem5 supports the use of more than one data source. The structure of the resource configuration is as follows:

```json
{
    "sources": {
        "data-source-1": { ... },
        "data-source-2": { ... },
        // Add more data sources as needed
    }
}
```

The data sources can be a combination of MongoDB Atlas and JSON. By default, gem5 will search through all the data sources to find a resource and return the latest version of the resource compatible with the gem5 version if the `resource_version` is not given. If a resource with the same `id` and `resource_version` exists in multiple data sources, an error will be thrown. You can also specify a subset of data sources to obtain resources from:

```python
resource = obtain_resource("id", clients=["data-source-1"])
```

### Using Custom Resource Configuration and Local Resources

In this example, we will walk through how to set up your custom configuration and utilize your own local resources. For this illustration, we'll employ a JSON file as our resource data source.

#### Creating a Custom Resource Data Source

Let's begin by downloading the resource we'll use as our local source. I'm selecting the `riscv-hello` resource from gem5 resources.

```bash
wget https://storage.googleapis.com/dist.gem5.org/dist/develop/test-progs/hello/bin/riscv/linux/hello-20220728
```

Next, let's create the JSON data source. I'll name the file `my-resources.json`. The contents should look like this:

```json
[
    {
        "category": "binary",
        "id": "riscv-hello",
        "description": "A 'Hello World!' binary, compiled to RISCV.",
        "architecture": "RISCV",
        "size": 4674040,
        "tags": [
            "hello"
        ],
        "is_zipped": false,
        "md5sum": "6d9494d22b90d817e826b0d762fda973",
        "source": "src/simple",
        "url": "file://<path/to/the/above/downloaded/file>",
        "code_examples": [
            {
                "example": "https://github.com/gem5/gem5/tree/develop/configs/example/gem5_library/checkpoints/riscv-hello-restore-checkpoint.py",
                "tested": true
            },
            {
                "example": "https://github.com/gem5/gem5/tree/develop/configs/example/gem5_library/checkpoints/riscv-hello-save-checkpoint.py",
                "tested": true
            },
            {
                "example": "https://github.com/gem5/gem5/tree/develop/configs/example/gem5_library/riscvmatched-hello.py",
                "tested": true
            }
        ],
        "license": "",
        "author": [],
        "source_url": "https://github.com/gem5/gem5-resources/tree/develop/src/simple",
        "resource_version": "1.0.0",
        "gem5_versions": [
            "23.0"
        ],
        "example_usage": "obtain_resource(resource_id=\"riscv-hello\")"
    }
]
```

The JSON object of a resource should adhere to the [gem5 resources schema](https://resources.gem5.org/gem5-resources-schema.json). 

**Note**: While the `url` field can be a link, in this case, I'm using a local download.

#### Creating Your Custom Resource Configuration

Create a file named `gem5-config.json` with the following content:

```json
{
    "sources": {
        "my-json-data-source": {
            "url": "path/to/my-resources.json",
            "isMongo": false
        }
    }
}
```

#### Running gem5 with a Local Data Source

First, build gem5 with RISC-V:

```bash
scons build/RISCV/gem5.opt -j`nproc`
```

Next, run the `riscvmatched-hello.py` example using our local `riscv-hello` resource:

```bash
GEM5_CONFIG=path/to/gem5-config.json ./build/RISCV/gem5.opt configs/example/gem5_library/riscvmatched-hello.py
```

This command will execute the `riscvmatched-hello.py` script using our locally downloaded resource.