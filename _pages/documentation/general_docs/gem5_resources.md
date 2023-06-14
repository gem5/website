---
layout: documentation
title: gem5-resources
doc: gem5 documentation
parent: gem5_resources
permalink: /documentation/general_docs/gem5_resources/
authors: Bobby R. Bruce, Kunal Pai, Parth Shah
---

# gem5 Resources

gem5 Resources is a repository providing sources for artifacts known and
proven compatible with the gem5 architecture simulator. These resources
are not necessary for the compilation or running of gem5, but may aid users
in producing certain simulations.

## Why gem5 Resources?

gem5 has been designed with flexibility in mind. Users may simulate a wide
variety of hardware, with an equally wide variety of workloads. However,
requiring users to find and configure workloads for gem5 (their own disk
images, their own OS boots, their own tests, etc.) is a significant
investment, and a hurdle to many.

The purpose of gem5 Resources is therefore __to provide a stable set of
commonly used resources, with proven and documented compatibility with gem5__.
In addition to this, gem5 resources also puts emphasis on __reproducibility
of experiments__ by providing citable, stable resources, tied to a particular
release of gem5.

## Where can I obtain the gem5 Resources?

To find a specific resource with the gem5 Resources, we recommend using the [gem5 Resources Website](https://resources.gem5.org). Detailed information on how searching, filtering and sorting works on this website is on this [help page](https://resources.gem5.org/help).

The gem5 Resources are hosted on our Google Cloud Bucket. Links to the
resources can be found [gem5 resources README.md file](
https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/README.md).
The resource metadata is stored in a MongoDB database hosted on MongoDB Atlas.
To request updates to gem5 resources, create an issue or mail gem5-dev.

## Using a Resource from the gem5 Resources Website in gem5

When you find the Resource that you want to use in your simulation, navigate to the 'Usage' tab of that Resource.

For the purpose of this tutorial, let's assume that the Resource you are looking for is `riscv-hello`, found [here](https://resources.gem5.org/resources/riscv-hello).In the ['Usage'](https://resources.gem5.org/resources/riscv-hello/usage) tab of this Resource, you will find the code that can be pasted in a gem5 simulation to use this Resource.

In this case, the code is `obtain_resource(resource_id="riscv-hello")`.

To use the `obtain_resource` function, you require the following import statement:

```
from gem5.resources.resource import obtain_resource
```

The `obtain_resource` function accepts the following parameters:

- `resource_id`: The ID of the Resource you want to use.
- `resource_version`: An optional parameter that specifies the version of the Resource you want to use. If not specified, the latest version of the Resource compatible with the version of gem5 being used will be used.
- `clients`: An optional parameter that specifies the list of clients that gem5 would search for the Resource in. If not specified, gem5 will search for the Resource in all clients specified in the `src/python/gem5_default_config.py` file. By default, gem5 will use the public MongoDB metadata database to find resources. This can be overridden to specify your own local resource metadata.

## Using a Workload from the gem5 Resources Website in gem5

When you find the Workload that you want to use in your simulation, navigate to the 'Usage' tab of that Workload.

For the purpose of this tutorial, let's assume that the Workload you are looking for is `riscv-ubuntu-20.04-boot`, found [here](https://resources.gem5.org/resources/riscv-ubuntu-20.04-boot). In the ['Usage'](https://resources.gem5.org/resources/riscv-ubuntu-20.04-boot/usage) tab of this Workload, you will find the code that can be pasted in a gem5 simulation to use this Workload.

In this case, the code is `Workload("riscv-ubuntu-20.04-boot")`.

To use the `Workload` class, you require the following import statement:

```
from gem5.resources.workload import Workload
```

The `Workload` class accepts the following parameters:

- `workload_name`: The name of the Workload you want to use.
- `resource_directory`: An optional parameter that specifies where any resources should be download and accessed from.
- `resource_version`: An optional parameter that specifies the version of the Resource that should be used. If not specified, the latest version of the Resource compatible with the version of gem5 being used will be used.
- `clients`: An optional parameter that specifies a list of clients that gem5 would search for the Resource in. If not specified, gem5 will search for the Resource in all clients specified in the `src/python/gem5_default_config.py` file.

## Using a Custom Resource in gem5

To use a Custom Resource in gem5, we recommend using one of the supported data sources formats in gem5. Currently, we support MongoDB Atlas, local JSON files and remote JSON files.

You can use your own config file by overriding the `GEM5_DEFAULT_CONFIG` variable while running a file.

NOTE: Any Custom Resource you add must be compliant with the [gem5 Resources Schema](https://resources.gem5.org/gem5-resources-schema.json).

There is a utility in `utils/gem5-resources-manager` which provides a GUI for updating and creating resources for both the public resources (only modifiable by gem5 admins) and local resource metadata.
You can find more information on the gem5 Resources Manager in the README file.

## How do I obtain the gem5 Resource sources?

gem5 resources sources may be obtained from
<https://github.com/gem5/gem5-resources>:

```bash
git clone https://github.com/gem5/gem5-resources
```

The HEAD of the `stable` branch will point towards a set of resource sources
compatible with the latest release of gem5 (which can be obtained via
`git clone https://github.com/gem5/gem5.git`).

Please consult the [README.md](
https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/README.md)
file for information on compiling individual gem5 resources. Where license
permits, the [README.md](
https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/README.md)
file will provide a link to download the compiled resource from our
dist.gem5.org Google Cloud Bucket.

## How is gem5 Resources repository constructed?

The structure of this repository is as follows:

* **README.md** : This README will outline each resources, their origin,
how they have been modified to work with gem5 (if applicable), relevant
licensing information, and compilation instructions. This should be the first
port-of-call for those looking to use a gem5 resource.
* **src** : The resource sources. The gem5 resources can be found in this
directory. Each sub-directory outlines a resource. Each resource contains its
own README.md file documenting relevant information -- compilation
instructions, usage notes, etc.
* **CHANGELOG.md** : This CHANGELOG will outline the changes in a particular resource across its versions.

### Versioning

Each resource can have multiple versions. A version is in the form of
`<major>.<minor>.<patch>`. The versioning scheme is based on [Semantic
Versioning](https://semver.org/). Each version of a resource is linked to one
or more gem5 versions (e.g., v20.0, v20.1, v20.2, etc.).

By default, gem5 uses the latest version of a resource compatible with the
version of gem5 being used. However, users may specify a particular version
of a resource to use. If a user specifies a version of a resource that is not
compatible with the version of gem5 being used, gem5 will throw a warning.
You may still use the resource at your own risk.

### Citing a Resource

We strongly recommend gem5 Resources are cited in publications to aid in
replication of experiments, tutorials, etc.

To cite as a URL, please use the following formats:

```
# For the git repository at a particular revision:
https://github.com/gem5/gem5-resources/<revision>/src/<resource>

# For the git repository at a particular tag:
https://github.com/gem5/gem5-resources/tree/<branch>/src/<resource>
```

Alternatively, as BibTex:

```
@misc{gem5-resources,
  title = {gem5 Resources. Resource: <resource>},
  howpublished = {\url{https://github.com/gem5/gem5-resources/<revision>/src/<resource>}},
  note = {Git repository at revision '<revision>'}
}

@misc{gem5-resources,
  title = {gem5 Resources. Resource: <resource>},
  howpublished = {\url{https://github.com/gem5/gem5-resources/tree/<branch>/src/<resource>}},
  note = {Git repository at tag '<tag>'}
}
```

## How to I contribute to gem5 Resources?

Changes to the gem5 Resources repository are made to the develop branch via our
Gerrit code review system. Therefore, to make changes, first clone the
repository:

```
git clone https://github.com/gem5/gem5-resources.git
```

Then make changes and commit. When ready, push to Gerrit with:

```
git push origin HEAD:refs/for/stable
```

This will add resources to be used in the latest release of gem5.

To contribute resources to the next release of gem5,
```
git clone https://github.com/gem5/gem5-resources.git
git checkout --track origin/develop
```

Then make changes, commit, and push with:

```
git push origin HEAD:refs/for/develop
```

Commit message heads should not exceed 65 characters and start with the tag
`resources:`. The description after the header must not exceed 72 characters.

E.g.:

```
resources: Adding a new resources X

This is where the description of this commit will occur taking into
note the 72 character line limit.
```

We strongly advise contributors follow our [Style Guide](
/documentation/general_docs/development/coding_style/) where
possible and appropriate.

Any change will then be reviewed via our [Gerrit code review system](
https://gem5-review.googlesource.com). Once fully accepted and merged into
the gem5 resources repository, please contact Bobby R. Bruce
([bbruce@ucdavis.edu](mailto:bbruce@ucdavis.edu)) to have any compiled sources
uploaded to the gem5 resources bucket.
