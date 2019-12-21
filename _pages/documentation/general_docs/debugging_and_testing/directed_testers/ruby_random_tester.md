---
layout: documentation
title: Ruby Random Tester
doc: gem5 documentation
parent: directed_testers
permalink: /documentation/general_docs/debugging_and_testing/directed_testers/ruby_random_tester/
author: Bobby R. Bruce
---

# Ruby Random Tester

A cache coherence protocol usually has several different types of state
machines, with state machine having several different states. For example, the
`MESI CMP` directory protocol has four different state machines (`L1`, `L2`,
`directory`, `dma`). Testing such a protocol for functional correctness is a
challenging task. gem5 provides a random tester for testing coherence
protocols. It is called the Ruby Random Tester. The source files related to the
tester are present in the directory `src/cpu/testers/rubytest`. The file
`configs/examples/ruby_random_test.py` is used for configuration and execution
of the test. For example, the following command can be used for testing a
protocol:

```
./build/X86/gem5.fast ./configs/example/ruby_random_test.py
```

Though one can specify many different options to the random tester, some of
them are note worthy.

|Parameter         |Description                                                       |
|:-----------------|:-----------------------------------------------------------------|
|`-n`, `--num-cpus`|Number of cpus injecting load/store requests to the memory system.|
|`--num-dirs`      |Number of directory controllers in the system.                    |
|`-m`, `--maxtick` |Number of cycles to simulate.                                     |
|`-l`, `--checks`  |Number of loads to be performed.                                  |
|`--random_seed`   |Seed for initialization of the random number generator.           |


Testing a coherence protocol with the random tester is a tedious task and
requires patience. First, build gem5 with the protocol to be tested. Then, run
the ruby random tester as mentioned above. Initially one should run the tester
with a single processor, and few loads. It is likely that one would encounter
problems. Use the debug flags to get a trace of the events ocurring in the
system. You may find the flag `ProtocolTrace` particularly useful. As these are
rectified, keep on increasing the number of loads, say by a factor of 10 each
time till one can execute one to ten million loads. Once it starts working for
a single processor, a similar process now needs to be followed for a two
processor system, followed by larger systems.

Theoretical approaches exist for [verifying coherence protocols](
https://doi.org/10.1145/248621.248624), but gem5 currently does not include any
testers based on those.
