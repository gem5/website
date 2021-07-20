---
layout: documentation
title: gem5-resources
doc: gem5 documentation
parent: gem5_resources
permalink: /documentation/general_docs/gem5_resources/
authors: Bobby R. Bruce
---

# gem5 Resources

gem5 resources is a repository providing sources for artifacts known and
proven compatible with the gem5 architecture simulator. These resources
are not necessary for the compilation or running of gem5, but may aid users
in producing certain simulations.

## Why gem5 Resources?

gem5 has been designed with flexibility in mind. Users may simulate a wide
variety of hardware, with an equally wide variety of workloads. However,
requiring users to find and configure workloads for gem5 (their own disk
images, their own OS boots, their own tests, etc.) is a significant
investment, and a hurdle to many.

The purpose of gem5 resources is therefore __to provide a stable set of
commonly used resources, with proven and documented compatibility with gem5__.
In addition to this, gem5 resources also puts emphasis on __reproducibility
of experiments__ by providing citable, stable resources, tied to a particular
release of gem5.

## Where can I obtain the gem5 resources?

The gem5 resources are hosted on our Google Cloud Bucket. Listed below are the
compiled resources presently available, as well as links to their sources in
the gem5 resources repository. **These are resources sources for gem5 20.1**.

|Resource |Compiled/Built Resource |Source |
|:--------|:-----------------------|:------|
|asmtest | 351 test binaries, downloadable with `https://dist.gem5.org/dist/v21-1/test-progs/asmtest/bin/<binary>` | [here](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/asmtest) |
|riscv-tests | [dhryston.riscv](http://dist.gem5.org/dist/v21-1/test-progs/riscv-tests/dhrystone.riscv), [median.riscv](http://dist.gem5.org/dist/v21-1/test-progs/riscv-tests/median.riscv), [mm.riscv](http://dist.gem5.org/dist/v21-1/test-progs/riscv-tests/mm.riscv), [mt-matmul.riscv](http://dist.gem5.org/dist/v21-1/test-progs/riscv-tests/mt-matmul.riscv), [mt-vvadd.riscv](http://dist.gem5.org/dist/v21-1/test-progs/riscv-tests/mt-vvadd.riscv), [multiply.riscv](http://dist.gem5.org/dist/v21-1/test-progs/riscv-tests/multiply.riscv), [pmp.riscv](http://dist.gem5.org/dist/v21-1/test-progs/riscv-tests/pmp.riscv), [qsort.riscv](http://dist.gem5.org/dist/v21-1/test-progs/riscv-tests/qsort.riscv), [rsort.riscv](http://dist.gem5.org/dist/v21-1/test-progs/riscv-tests/rsort.riscv), [spmv.riscv](http://dist.gem5.org/dist/v21-1/test-progs/riscv-tests/spmv.riscv), [towers.riscv](http://dist.gem5.org/dist/v21-1/test-progs/riscv-tests/towers.riscv), [vvadd.riscv](http://dist.gem5.org/dist/v21-1/test-progs/riscv-tests/vvadd.riscv) |[here](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/riscv-tests) |
|insttests | [insttest-rv64a](http://dist.gem5.org/dist/v21-1/test-progs/insttest/bin/riscv/linux/insttest-rv64a), [insttest-rv64c](http://dist.gem5.org/dist/v21-1/test-progs/insttest/bin/riscv/linux/insttest-rv64c), [insttest-rv64d](http://dist.gem5.org/dist/v21-1/test-progs/insttest/bin/riscv/linux/insttest-rv64d), [insttest-rv64f](http://dist.gem5.org/dist/v21-1/test-progs/insttest/bin/riscv/linux/insttest-rv64f), [insttest-rv64i](http://dist.gem5.org/dist/v21-1/test-progs/insttest/bin/riscv/linux/insttest-rv64i), [insttest-rv64m](http://dist.gem5.org/dist/v21-1/test-progs/insttest/bin/riscv/linux/insttest-rv64m) | [here](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/insttest) |
|simple/pthread (x86) | [test_pthread_create_seq](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/x86/test_pthread_create_seq), [test_pthread_create_para](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/x86/test_pthread_create_para), [test_pthread_mutex](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/x86/test_pthread_mutex), [test_atomic](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/x86/test_atomic), [test_pthread_cond](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/x86/test_pthread_cond), [test_std_thread](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/x86/test_std_thread), [test_std_mutex](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/x86/test_std_mutex), [test_std_condition_variable](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/x86/test_std_condition_variable) | [here (Along with other 'simple' executables)](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/simple) |
|simple/pthread (aarch32) | [test_pthread_create_seq](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/aarch32/test_pthread_create_seq), [test_pthread_create_para](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/aarch32/test_pthread_create_para), [test_pthread_mutex](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/aarch32/test_pthread_mutex), [test_atomic](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/aarch32/test_atomic), [test_pthread_cond](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/aarch32/test_pthread_cond), [test_std_thread](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/aarch32/test_std_thread), [test_std_mutex](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/aarch32/test_std_mutex), [test_std_condition_variable](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/aarch32/test_std_condition_variable) | [here (Along with other 'simple' executables)](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/simple) |
|simple/pthread (aarch64) | [test_pthread_create_seq](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/aarch64/test_pthread_create_seq), [test_pthread_create_para](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/aarch64/test_pthread_create_para), [test_pthread_mutex](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/aarch64/test_pthread_mutex), [test_atomic](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/aarch64/test_atomic), [test_pthread_cond](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/aarch64/test_pthread_cond), [test_std_thread](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/aarch64/test_std_thread), [test_std_mutex](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/aarch64/test_std_mutex), [test_std_condition_variable](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/aarch64/test_std_condition_variable) | [here (Along with other 'simple' executables)](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/simple) |
|simple/pthread (riscv64) | [test_pthread_create_seq](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/riscv64/test_pthread_create_seq), [test_pthread_create_para](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/riscv64/test_pthread_create_para), [test_pthread_mutex](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/riscv64/test_pthread_mutex), [test_atomic](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/riscv64/test_atomic), [test_pthread_cond](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/riscv64/test_pthread_cond), [test_std_thread](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/riscv64/test_std_thread), [test_std_mutex](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/riscv64/test_std_mutex), [test_std_condition_variable](http://dist.gem5.org/dist/v21-1/test-progs/pthreads/riscv64/test_std_condition_variable) | [here (Along with other 'simple' executables)](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/simple) |
|simple/hello| [x86 executable](https://dist.gem5.org/dist/v21-1/test-progs/hello/bin/x86/linux/hello), [arm executable](https://dist.gem5.org/dist/v21-1/test-progs/hello/bin/arm/linux/hello), [mips executable](https://dist.gem5.org/dist/v21-1/test-progs/hello/bin/mips/linux/hello), [power executable](https://dist.gem5.org/dist/v21-1/test-progs/hello/bin/power/linux/hello), [riscv executable](https://dist.gem5.org/dist/v21-1/test-progs/hello/bin/riscv/linux/hello), [sparc executable](https://dist.gem5.org/dist/v21-1/test-progs/hello/bin/sparc/linux/hello) | [here (Along with other 'simple' executables)](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/simple) |
|simple/m5_exit | [x86 executable](https://dist.gem5.org/dist/v21-1/test-progs/m5-exit/bin/x86/linux/m5_exit) | [here (Along with other 'simple' executables)](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/simple) |
|insttest | [insttest](https://dist.gem5.org/dist/v21-1/test-progs/insttest/bin/sparc/linux/insttest)| [here](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/insttest) |
|square | [square.o](https://dist.gem5.org/dist/v21-1/test-progs/square/square.o) | [here](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/square) |
|spec-2006 | --- | [here](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/spec-2006) |
|spec-2017 | --- | [here](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/spec-2017) |
|gapbs | [Disk Image (GZIPPED)](http://dist.gem5.org/dist/v21-1/images/x86/ubuntu-18-04/gapbs.img.gz) | [here](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/gapbs) |
|parsec | [Disk Image (GZIPPED)](http://dist.gem5.org/dist/v21-1/images/x86/ubuntu-18-04/parsec.img.gz) | [here](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/parsec) |
|npb | [Disk Image (GZIPPED)](http://dist.gem5.org/dist/v21-1/images/x86/ubuntu-18-04/npb.img.gz) | [here](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/npb) |
|Linux boot-exit | [Disk Image (GZIPPED)](http://dist.gem5.org/dist/v21-1/images/x86/ubuntu-18-04/boot-exit.img.gz) |[here](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/boot-exit) |
|hack-back| --- | [here](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/hack-back) |
|linux kernels | [v4.4.186](http://dist.gem5.org/dist/v21-1/kernels/x86/static/vmlinux-4.4.186), [v4.9.186](http://dist.gem5.org/dist/v21-1/kernels/x86/static/vmlinux-4.9.186), [v4.14.134](http://dist.gem5.org/dist/v21-1/kernels/x86/static/vmlinux-4.14.134), [v4.19.83](http://dist.gem5.org/dist/v21-1/kernels/x86/static/vmlinux-4.19.83), [v5.4.49](http://dist.gem5.org/dist/v21-1/kernels/x86/static/vmlinux-5.4.49) | [here](https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/linux-kernel/) |

## How do I obtain the gem5 resource sources?

gem5 resources sources may be obtained from
<https://gem5.googlesource.com/public/gem5-resources>:

```
git clone https://gem5.googlesource.com/public/gem5-resources
```

The HEAD of the `stable` branch will point towards a set of resource sources
compatible with the latest release of gem5 (which can be obtained via
`git clone https://gem5.googlesource.com/public/gem5`).

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

### Versioning

The HEAD of the stable branch will contain resources that can be built and run
with the latest release of gem5 (that at the HEAD of the stable branch on
<https://gem5.googlesource.com/public/gem5>).

If you wish to use resources for an older release of gem5, then you must
checkout the version of gem5 resources for that release. We tag the repository
at specific versions. E.g., for gem5 20.0, there will be a tag for gem5 20.0.
Checking out the gem5 resources at that tag will give the resources confirmed
to work for that version.

To list all the tags in the repository: `git tag`.

To checkout a specific tag: `git checkout <tag name>`.

It should noted that there will be no tag for the most recent release of gem5,
as the most recent resources for the latest release are found at the HEAD
of the stable branch. The reason for this is resources may be added continually
during the course of a gem5 release. Upon the next release of a gem5 version,
gem5 resources is tagged.

For example, assuming the current version of gem5 is v20.2. The gem5 resources
will contain tags for v20.0 and v20.1. The current HEAD of the stable branch
will contain resources for gem5 v20.2. If new resources are added, they will
be added as commits on top of the stable branch. During this time, the next
major version of gem5 will be under develop on the gem5 develop branch. The
gem5 resources repository also has a develop branch for resources developed,
expanded, and/or modified for the upcoming gem5 release. Upon the release of
this new major version of gem5 (v20.3), the stable branch is tagged (in this
case, as v20.2) and the develop branch is merged into the stable.

### Citing a resource

We strongly recommend gem5 resources are cited in publications to aid in
replication of experiments, tutorials, etc.

To cite as a URL, please use the following formats:

```
# For the git repository at a particular revision:
https://gem5.googlesource.com/public/gem5-resources/+/<revision>/src/<resource>

# For the git repository at a particular tag:
https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/<tag>/src/<resource>
```

Alternatively, as BibTex:

```
@misc{gem5-resources,
  title = {gem5 Resources. Resource: <resource>},
  howpublished = {\url{https://gem5.googlesource.com/public/gem5-resources/+/<revision>/src/<resource>}},
  note = {Git repository at revision '<revision>'}
}

@misc{gem5-resources,
  title = {gem5 Resources. Resource: <resource>},
  howpublished = {\url{https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/<tag>/src/<resource>}},
  note = {Git repository at tag '<tag>'}
}
```

## How to I contribute to gem5 Resources?

Changes to the gem5 resources repository are made to the develop branch via our
Gerrit code review system. Therefore, to make changes, first clone the
repository:

```
git clone https://gem5.googlesource.com/public/gem5-resources
```

Then make changes and commit. When ready, push to Gerrit with:

```
git push origin HEAD:refs/for/stable
```

This will add resources to be used in the latest release of gem5.

To contribute resources to the next release of gem5,
```
git clone https://gem5.googlesource.com/public/gem5-resources
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
