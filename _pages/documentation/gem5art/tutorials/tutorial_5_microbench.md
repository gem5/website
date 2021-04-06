---
layout: documentation
title: Microbench Tutorial
doc: gem5art
parent: tutorial
permalink: /documentation/gem5art/tutorials/microbench-tutorial
Authors:
  - Ayaz Akram
  - Nadia Etemadi
---

# Tutorial: Run Microbenchmarks with gem5

## Introduction
In this tutorial, we will learn how to run some simple microbenchmarks using gem5art.
Microbenchmarks are small benchmarks designed to test a component of a larger system.
The particular microbenchmarks we are using in this tutorial were originally developed at the
[University of Wisconsin-Madison](https://github.com/VerticalResearchGroup/microbench).
This microbenchmark suite is divided into different control, execution and memory benchmarks.
We will use system emulation (SE) mode of gem5 to run these microbenchmarks with gem5.


This tutorial follows the following directory structure:

- configs-micro-tests: the base gem5 configuration to be used to run SE mode simulations
- gem5: gem5 [source code](https://gem5.googlesource.com/public/gem5) and the compiled binary

- results: directory to store the results of the experiments (generated once gem5 jobs are executed)
- launch_micro_tests.py: gem5 jobs launch script (creates all of the needed artifacts as well)


## Setting up the environment
First, we need to create the main directory named micro-tests (from where we will run everything) and turn it into a git repository like we did in the previous tutorials.
Next, add a git remote to this repo pointing to a remote location where we want this repo to be hosted.

```sh
mkdir micro-tests
cd micro-tests
git init
git remote add origin https://your-remote-add/micro-tests.git
```

We also need to add a .gitignore file in our git repo to leave unnecessary files untracked:

```
*.pyc
m5out
.vscode
results
gem5
venv
```

Next, we will create a virtual python3 environment before using gem5art.

```sh
virtualenv -p python3 venv
source venv/bin/activate
```
This virtual environment needs to be running in order to run experiments with gem5art.
You can deactivate the environment at any time with the command `deactivate`.

gem5art can be installed (if not already) using pip:

```sh
pip install gem5art-artifact gem5art-run gem5art-tasks
```

## Build gem5

First clone gem5 in your micro-tests repo:

```sh
git clone https://gem5.googlesource.com/public/gem5
cd gem5
```

Before building gem5, we need to apply a [patch](https://github.com/darchr/gem5/commit/38d07ab0251ea8f5181abc97a534bb60157b2b5d) to the source repo.
As you will later see, we will run gem5 with various memory configs.
**Inf** (SimpleMemory with 0ns latency) and **SingleCycle** (SimpleMemory with 1ns latency) do not use any caches.
Therefore, to implement cacheless SimpleMemory, we need to add support of vector ports in SimpleMemory by applying this patch.
This becomes necessary as we need to connect cpu's icache and dcache ports to the mem_ctrl port (a vector port).
You can download and apply the patch as follows:

```sh
wget https://github.com/darchr/gem5/commit/f0a358ee08aba1563c7b5277866095b4cbb7c36d.patch
git am f0a358ee08aba1563c7b5277866095b4cbb7c36d.patch --reject
```

Now, build gem5:

```sh
scons build/X86/gem5.opt -j8
```

## Download and compile the microbenchmarks
Download the microbenchmarks:

```sh
git clone https://github.com/darchr/microbench.git
```

Commit the source of microbenchmarks to the micro-tests repo, so that the current version of the microbenchmarks repo becomes a part of the micro-tests repository.

```sh
git add microbench/
git commit -m "Add microbenchmarks"
```

Compile the benchmarks:

```sh
cd microbench
make
```

By default, these microbenchmarks are compiled for the x86 ISA, which will be our focus in this tutorial.
You can use the following commands to compile these benchmarks for ARM and RISC-V ISAs if you wish to work with them.

```sh
make ARM

make RISCV
```

## gem5 run scripts

Now, we will add the gem5 run and configuration scripts to a new folder named `configs-micro-tests`.
Get the run script named run_micro.py from [here](https://github.com/darchr/gem5art/blob/master/docs/gem5-configs/configs-micro-tests/run_micro.py), and other system configuration file from
[here](https://github.com/darchr/gem5art/blob/master/docs/gem5-configs/configs-micro-tests/system.py).
The run script (run_micro.py) takes the following arguments:
- **cpu:** cpu type [**TimingSimple:** timing simple cpu model, **DerivO3:** O3 cpu model]
- **memory:** memory type [**Inf:** 0ns latency memory, **SingleCycle:** 1ns latency memory, **SlowMemory:** 100ns latency memory. All types have infinite bandwidth. Caches are only enabled for SlowMemory.]
- **benchmark:** benchmark binary to run with gem5



## Database and Celery Server

If not already running or created, you can create a database using:

```sh
docker run -p 27017:27017 -v <absolute path to the created directory>:/data/db --name mongo-<some tag> -d mongo
```
in a newly created directory.

If not already installed, install `RabbitMQ` on your system (before running celery) using:

```sh
apt-get install rabbitmq-server
```

Now, run the celery server using:

```sh
celery -E -A gem5art.tasks.celery worker --autoscale=[number of workers],0
```

## Creating a launch script
Next, we will create a launch script with the name `launch_micro_tests.py`, which will register the artifacts to be used and will start gem5 jobs.

Like we did in previous tutorials, the first step is to import the required modules and classes:

```python
import os
import sys
from uuid import UUID

from gem5art.artifact import Artifact
from gem5art.run import gem5Run
from gem5art.tasks.tasks import run_gem5_instance
```

Next, we will register the artifacts:

```python
experiments_repo = Artifact.registerArtifact(
    command = 'git clone https://your-remote-add/micro-tests.git',
    typ = 'git repo',
    name = 'micro-tests',
    path =  './',
    cwd = '../',
    documentation = 'main experiments repo to run microbenchmarks with gem5'
)

gem5_repo = Artifact.registerArtifact(
    command = '''git clone https://gem5.googlesource.com/public/gem5;
    cd gem5;
    wget https://github.com/darchr/gem5/commit/38d07ab0251ea8f5181abc97a534bb60157b2b5d.patch;
    git am 38d07ab0251ea8f5181abc97a534bb60157b2b5d.patch --reject;
    ''',
    typ = 'git repo',
    name = 'gem5',
    path =  'gem5/',
    cwd = './',
    documentation = 'git repo with gem5 cloned on Nov 22 from googlesource (patch applied to support mem vector port)'
)

gem5_binary = Artifact.registerArtifact(
    command = 'scons build/X86/gem5.opt',
    typ = 'gem5 binary',
    name = 'gem5',
    cwd = 'gem5/',
    path =  'gem5/build/X86/gem5.opt',
    inputs = [gem5_repo,],
    documentation = 'default gem5 x86'
)
```

The number of artifacts is less than what we had to use in previous (full-system) tutorials ([boot](boot-tutorial.md), [npb](npb-tutorial.md)), as expected.

Now to run the benchmarks, we will iterate through possible cpu types, memory types and all of the microbenchmarks from the microbench repository.
We will also register an artifact for each microbenchmark. If you want to run certain benchmarks, you can indicate which ones in the `bm_list` array.

```python

if __name__ == "__main__":

    cpu_types = ['TimingSimple', 'DerivO3']
    mem_types = ['Inf', 'SingleCycle', 'Slow']

    bm_list = []

    # iterate through files in microbench dir to
    # create a list of all microbenchmarks

    for filename in os.listdir('microbench'):
        if os.path.isdir(f'microbench/{filename}') and filename != '.git':
            bm_list.append(filename)

    # create an artifact for each single microbenchmark
    for bm in bm_list:
        bm = Artifact.registerArtifact(
        command = '''
        cd microbench/{};
        make X86;
        '''.format(bm),
        typ = 'binary',
        name = bm,
        cwd = 'microbench/{}'.format(bm),
        path =  'microbench/{}/bench.X86'.format(bm),
        inputs = [experiments_repo,],
        documentation = 'microbenchmark ({}) binary for X86 ISA'.format(bm)
        )

    for bm in bm_list:
        for cpu in cpu_types:
            for mem in mem_types:
                run = gem5Run.createSERun(
                    'microbench_tests',
                    'gem5/build/X86/gem5.opt',
                    'configs-micro-tests/run_micro.py',
                    'results/X86/run_micro/{}/{}/{}'.format(bm,cpu,mem),
                    gem5_binary,gem5_repo,experiments_repo,
                    cpu,mem,os.path.join('microbench',bm,'bench.X86'))
                run.run()

```

Note that, in contrast to previous tutorials ([boot](boot-tutorial), [npb](npb-tutorial)), we are using `createSERun()` this time, as we want to run gem5 in SE mode.
The full launch script is available [here](https://github.com/darchr/gem5art/blob/master/docs/launch-scripts/launch_micro_tests.py).

Once you run this launch script (as shown below), your microbenchmark experiments will start running, which will simulate execution of microbenchmarks on different cpu and memory types.

```python
python launch_micro_tests.py
```

Later, you can access the database to see the status of these jobs and further analyze the results of your microbenchmark experiments. Happy experimenting!
