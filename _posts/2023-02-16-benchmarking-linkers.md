---
layout: post
title:  "Benchmarking Linkers within gem5"
author: Melissa Jost
date:   2023-02-16
categories: project
---
**tl;dr**: Use the [mold linker](<https://github.com/rui314/mold>) for the fastest linking times when building gem5

People familiar with gem5 are aware of its lengthy compilation time, especially during the linking stage.
This can become frustrating when even a minor edit necessitates re-linking previously compiled files.
This can add several minutes to the process.
Keeping this in mind, we evaluated a range of currently supported linkers with gem5 to determine which one is the most efficient.

To conduct these tests, we closely examined each of the linkers that gem5 currently supports including the current default linker, "ld".
The four additional supported linkers evaluated are "lld", "bfd", "gold", and "mold".

Our method for comparing these linkers was as follows: we first built gem5 normally by executing `scons build/ALL/gem5.opt`.
Once the `gem5.opt` binary was compiled, we deleted it.
Thus we were left with the compiled object files but no linked binary.
Then, we compared runs of rebuilding/linking gem5 with each of the linkers using `/usr/bin/time scons build/ALL/gem5.opt -j12 --linker=[linker-option]`, where `/usr/bin/time` measured the duration.
We ran these tests on a system using an AMD EPYC 7402P 24-Core processor with a 3.35 GHz frequency.

During these tests, we observed that using a linker other than the default "ld" in our experimental setup forced a recompilation of all of the m5 files.
However, if we deleted `gem5.opt` binary after this and ran the compilation again, only `gem5.opt` was rebuilt/linked, resulting in two distinct times.
To compare the times, we needed to take into account the time it took for the first run to build all the m5 files, as well as the time it took for the second run to re-link gem5.opt.
These are labeled below as "all m5" versus "last few".
In addition to these two runs, we also compared each run on a networked file system (NFS) and a local SSD to see if the storage type of the files had any impact on the run times.
Finally, we performed one last run on the local SSD using the 48 available cores on our system to assess if it made any difference.
Below, we present the elapsed time for each of these runs.

We found that among the four linkers we tested, "bfd" was the slowest, and "mold" was the fastest.
Additionally, the difference between using `-j12` and `-j48` appeared to be insignificant.

Based on our results, we suggest using "mold" as the linker when working with gem5.
It's worth noting that using a particular linker had a more significant impact on the time taken than the storage location.

|           | NFS + all m5  | NFS + last few    | Local SSD + all m5 | Local SSD + last few   | Local SSD + -j48 + last few    |
| :---:     | :---:         | :---:             | :---:              | :---:                  | :---:                          |
| ld        | ---           | 3:29.19           | ---                | 3:08.31                | 3:00.15                        |
| bfd       | 4:15.82       | 3:32.13           | 3:39.70            | 3:02.15                | 3:02.35                        |
| lld       | 2:16.22       | 1:54.25           | 1:52.94            | 1:13.12                | 1:13.16                        |
| gold      | 2:30.98       | 1:43.59           | 1:59.41            | 1:19.86                | 1:19.48                        |
| mold      | 1:48.62       | 1:07.08           | 1:08.18            | 0:28.23                | 0:27.89                        |

In addition to just comparing the build times, we executed 100000000 ticks for each linked compilation to ensure that using these linkers wouldn't cause any issues when actually using gem5, such as increased execution time or functional problems.

We achieved this by performing an x86 linux boot with an O3 CPU and a Ruby cache. The command to do so is provided below.

Command:

```sh
/usr/bin/time build/ALL/gem5.opt -re tests/gem5/configs/x86_boot_exit_run.py --cpu o3 --num-cpus 2 --mem-system mesi_two_level --dram-class DualChannelDDR4_2400 --boot-type init --resource-directory tests/gem5/resources --tick-exit 100000000
```

We found none of the linkers had a significant impact on the runtime of any tests and all tests completed successfully.
This indicates that using linkers should not have any detrimental effects on experiments conducted within gem5.

Based on our findings, we can confidently recommend using the [mold linker](<https://github.com/rui314/mold>) to speed up linking times when building gem5.
If you're interested in using mold, you can follow the instructions [here](<https://github.com/rui314/mold#how-to-build>) to compile it.
Once it's properly installed, you can use it by passing `--linker=mold` while building gem5.

Here's an example command: `scons build/ALL/gem5.opt -j12 --linker=mold`.
