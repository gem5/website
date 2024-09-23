---
layout: documentation
title: Setting gem5 Resources data sources to support local resources
parent: gem5-standard-library
doc: gem5 documentation
permalink: /documentation/gem5-stdlib/using-local-resources
author: Harshil Patel
---

gem5 supports using local data sources in the form of a MongoDB Atlas and JSON datasource. gem5 has a default resources config in `src/python/gem5_default_config.py`. This resources config points to the MongoDB Atlas collection of gem5 resources. To utilize data sources other than the main gem5 resources database, you will need to override the gem5-resources-config.

There are several ways to update the gem5 resources configuration:

1. **Setting GEM5_CONFIG environment variable:** You can set the GEM5_CONFIG environment variable to specify a new configuration file. Doing this will replace the default resources configuration with the one you've specified.

2. **Using gem5-config.json:** If a file named gem5-config.json exists in the current working directory, it will take precedence over the default resources configuration.

3. **Fallback to default resources config:** If neither of the above methods is used, the system will resort to using the default resources configuration.

Additionally, if you wish to utilize or add a local resource JSON file to the currently selected config (as mentioned in the above methods), you have two additional methods available:

- **GEM5_RESOURCE_JSON environment variable:** This variable can be employed to override the current resources configuration and make use of a specified JSON file.

- **GEM5_RESOURCE_JSON_APPEND environment variable:** Use this variable to add a JSON file to the existing resources configuration without replacing it.

It's essential to note that overriding or appending doesn't modify the actual configuration files themselves. These methods allow you to temporarily specify or add resource configurations during runtime without altering the original configuration files.


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
### Setting up a MongoDB Atlas Database

You would need to set up an Atlas cluster, steps on setting up an Atlas cluster can be found here:
- https://www.mongodb.com/basics/mongodb-atlas-tutorial

You would also need to enable Atlas dataAPI, steps on enabling dataAPI can be found here:
- https://www.mongodb.com/docs/atlas/app-services/data-api/generated-endpoints/

### Using Multiple Data Sources

gem5 supports the use of more than one data source. The structure of the resource configuration is as follows:

```json
{
    "sources": {
         "gem5-resources": {
            "dataSource": "gem5-vision",
            "database": "gem5-vision",
            "collection": "resources",
            "url": "https://data.mongodb-api.com/app/data-ejhjf/endpoint/data/v1",
            "authUrl": "https://realm.mongodb.com/api/client/v2.0/app/data-ejhjf/auth/providers/api-key/login",
            "apiKey": "OIi5bAP7xxIGK782t8ZoiD2BkBGEzMdX3upChf9zdCxHSnMoiTnjI22Yw5kOSgy9",
            "isMongo": true,
        },
        "data-source-json-1": {
            "url": "path/to/json",
            "isMongo": false,
        },
        "data-source-json-2": {
            "url": "path/to/another/json",
            "isMongo": false,
        },
        // Add more data sources as needed
    }
}
```

The above example shows a gem5 resources config with a MongoDB Atlas data source and 2 JSON data sources. By default gem5 will create a union of all the resources present in all the specified data sources. If you ask to obtain a resource where multiple data sources have the same `id` and `resource_version` of the resource then an error will be thrown. You can also specify a subset of data sources to obtain resources from:

```python
resource = obtain_resource("id", clients=["data-source-json-1"])
```

### Understanding Local Resources

Local resources, in the context of gem5, pertain to resources that users possess and wish to integrate into gem5 but aren't pre-existing in the gem5 resources database.

For users, This offers the flexibility to employ their own resources seamlessly within gem5, bypassing the need to create dedicated resource objects using `BinaryResource(local_path=/path/to/binary)`. Instead, they can directly utilize these local resources through `obtain_resource()`, streamlining the integration process.

### Using Custom Resource Configuration and Local Resources

In this example, we will walk through how to set up your custom configuration and utilize your own local resources. For this illustration, we'll employ a JSON file as our resource data source.

#### Creating a Custom Resource Data Source

Let's begin by creating a local resource. This is a bare bones resource that will serve as an example. To use local resources with `obtain_resource()`, our bare bones resource need to have a binary file. Here we use an empty binary called `fake-binary`. 

**Note**: Make sure that Gem5 binary and `fake-binary` have same ISA target (RISCV here).

Next, let's create the JSON data source. I'll name the file `my-resources.json`. The contents should look like this:

```json
[
    {
        "category": "binary",
        "id": "test-binary",
        "description": "A test binary",
        "architecture": "RISCV",
        "size": 1,
        "tags": [
            "test"
        ],
        "is_zipped": false,
        "md5sum": "6d9494d22b90d817e826b0d762fda973",
        "source": "src/simple",
        "url": "file:// path to fake_binary",
        "license": "",
        "author": [],
        "source_url": "https://github.com/gem5/gem5-resources/tree/develop/src/simple",
        "resource_version": "1.0.0",
        "gem5_versions": [
            "23.0"
        ],
        "example_usage": "obtain_resource(resource_id=\"test-binary\")"
    }
]
```

The JSON file of a resource should adhere to the [gem5 resources schema](https://resources.gem5.org/gem5-resources-schema.json).

**Note**: While the `url` field can be a link, in this case, I'm using a local file.

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
**Note**: It is implied that isMongo = false means that the data source is a JSON data source as gem5 currently only supports 2 types of data sources.

#### Running gem5 with a Local Data Source

First, build gem5 with RISCV:

```bash
scons build/RISCV/gem5.opt -j`nproc`
```

Next, run the `local-resource-example.py` file using our local `test-binary` resource:

Using environment variable
```bash
GEM5_RESOURCE_JSON_APPEND=path/to/my-resources.json ./build/RISCV/gem5.opt configs/example/gem5_library/local-resource-example.py --resource test-binary
```
or you can overwrite the `gem5_default_config` with our own custom config:

```bash
GEM5_CONFIG=path/to/gem5-config.json ./build/RISCV/gem5.opt configs/example/gem5_library/local-resource-example.py --resource test-binary
```
This command will execute the `local-resource-example.py` script using our locally downloaded resource. This script just calls the obtain_resource function and prints the local path of the resource. This script indicates that local resources function similarly as resources on the gem5 resources database.
