---
layout: documentation
title: Common errors within gem5
doc: gem5 documentation
parent: common-errors
permalink: /documentation/general_docs/common-errors/
---

Here are some common issues that users run into when using gem5, and information on how to fix them on how to fix them.

## Build errors

If your gem5 compilation fails with the following message:

```txt
[    LINK]  -> ALL/gem5.opt
collect2: fatal error: ld terminated with signal 9 [Killed]
compilation terminated.
scons: *** [build/ALL/gem5.opt] Error 1
scons: building terminated because of errors.
```

This indicates that your machine has run out of memory while trying to build
gem5 and has killed the process as a result.
If this occurs, try compiling gem5 with fewer threads, as this will consume
less memory.
If there are other processes using large amounts of memory on your system, try
building gem5 when more memory is available.

## Segmentation Fault

A segfault error can occur and will output to the terminal like the following:

```bash
gem5 has encountered a segmentation fault!

— BEGIN LIBC BACKTRACE —
gem5/build/X86/gem5.opt(_Z15print_backtracev+0x2c)[0x55ead536d5bc]
gem5/build/X86/gem5.opt(+0x1030b8f)[0x55ead537fb8f]
/lib/x86_64-linux-gnu/libpthread.so.0(+0x128a0)[0x7f50fb78b8a0]
/lib/x86_64-linux-gnu/libgcc_s.so.1(_Unwind_Resume+0xcf)[0x7f50fa12ad9f]
gem5/build/X86/gem5.opt(_ZN6X86ISA7Decoder10decodeInstENS_11ExtMachInstE+0x5d19e)[0x55ead4e5ea8e]
gem5/build/X86/gem5.opt(_ZN6X86ISA7Decoder6decodeENS_11ExtMachInstEm+0x244)[0x55ead4dc74a4]
gem5/build/X86/gem5.opt(_ZN6X86ISA7Decoder6decodeERNS_7PCStateE+0x22b)[0x55ead4dc779b]
gem5/build/X86/gem5.opt(_ZN12DefaultFetchI9O3CPUImplE5fetchERb+0x942)[0x55ead54695f2]
gem5/build/X86/gem5.opt(_ZN12DefaultFetchI9O3CPUImplE4tickEv+0xd3)[0x55ead546a7b3]
gem5/build/X86/gem5.opt(_ZN9FullO3CPUI9O3CPUImplE4tickEv+0x12b)[0x55ead5448e3b]
gem5/build/X86/gem5.opt(_ZN10EventQueue10serviceOneEv+0xa5)[0x55ead5375a95]
gem5/build/X86/gem5.opt(_Z9doSimLoopP10EventQueue+0x87)[0x55ead539a7b7]
gem5/build/X86/gem5.opt(_Z8simulatem+0xcba)[0x55ead539b80a]
gem5/build/X86/gem5.opt(+0x11d3431)[0x55ead5522431]
gem5/build/X86/gem5.opt(+0x6df0b4)[0x55ead4a2e0b4]
/usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0(PyEval_EvalFrameEx+0x64d7)[0x7f50fba38c47]
/usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0(PyEval_EvalCodeEx+0x7d8)[0x7f50fbb77908]
/usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0(PyEval_EvalFrameEx+0x5bf6)[0x7f50fba38366]
/usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0(PyEval_EvalCodeEx+0x7d8)[0x7f50fbb77908]
/usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0(PyEval_EvalCode+0x19)[0x7f50fba325d9]
/usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0(PyEval_EvalFrameEx+0x6ac0)[0x7f50fba39230]
/usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0(PyEval_EvalCodeEx+0x7d8)[0x7f50fbb77908]
/usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0(PyEval_EvalFrameEx+0x5bf6)[0x7f50fba38366]
/usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0(PyEval_EvalCodeEx+0x7d8)[0x7f50fbb77908]
/usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0(PyEval_EvalCode+0x19)[0x7f50fba325d9]
/usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0(PyRun_StringFlags+0x76)[0x7f50fbae26f6]
gem5/build/X86/gem5.opt(_Z6m5MainiPPc+0x83)[0x55ead537e823]
gem5/build/X86/gem5.opt(main+0x38)[0x55ead48d5068]
/lib/x86_64-linux-gnu/libc.so.6(__libc_start_main+0xe7)[0x7f50f9d4ab97]
gem5/build/X86/gem5.opt(_start+0x2a)[0x55ead48fd37a]
— END LIBC BACKTRACE —
```

It is important to note that in order to verify that you're encountering a segfault error, scroll above the back trace output and verify the line `gem5 has encountered a segmentation fault!` has outputted.
The cause of such error is usually the result of an error within your C++ files causing an incorrect address access.
The best way to debug segfaults within gem5 is to use gdb, to which we provide documentation [here](https://www.gem5.org/documentation/general_docs/debugging_and_testing/debugging/debugger_based_debugging).

## Fatal

A fatal error typically occurs when a simulation configuration is invalid and cannot be processed by the gem5 simulator.
The fatal error is preceded by the file that this error came from, which is usually a good indicator of where to look for what went wrong.
For example, in the error below, `gem5/src/cpu/base.cc` would be a good starting point to debug this error.

```bash
build/ALL/cpu/base.cc:186: fatal: Number of processes (cpu.workload) (0) assigned to the CPU does not equal number of threads (1).
```

This type of error can cover situations such as wrong file types or invalid values being passed to gem5, or unconnected ports, just to name a couple examples.
This should give you more information on the issue at hand, but if there still isn't enough information, using some of the [debugging techniques](https://www.gem5.org/documentation/general_docs/debugging_and_testing/debugging/trace_based_debugging) within gem5, such as gdb or debug flags may help.


## Panic

If you encounter a panic error, that usually indicates that something is wrong with gem5 itself.
Some of the more common panic errors within gem5 are unrecognized values or unimplemented functions being used.
To debug these errors, you can start by looking into the file this error was generated by, which is indicated right before the panic error in your terminal.
For example, in the error below, it would be best to start looking at `gem5/src/sim/mem_pool.cc`

```bash
build/ARM/sim/mem_pool.cc:45: panic: assert(_totalPages > 0) failed
```

This should give you more information on the issue at hand, though similar to fatal errors above, if there still isn't enough information, using some of the [debugging techniques](https://www.gem5.org/documentation/general_docs/debugging_and_testing/debugging/trace_based_debugging) within gem5 may help.

## Python Script Errors

For any type of Python error, such as an AttributeError or OSError, it is best to start out by looking below the error message, where you should see a trace output.
The first file and line number should indicate where the error occurred.
For example, with the error below, you should start by looking to `build/ARM/python/m5/SimObject.py(908)`, and if that doesn't give enough information, move onto `configs/example/gem5_library/arm-ubuntu-run.py(70)`.

```bash
AttributeError: Class PrivateL1PrivateL2CacheHierarchy has no parameter l1_size

At:
  build/ARM/python/m5/SimObject.py(908): __setattr__
  configs/example/gem5_library/arm-ubuntu-run.py(70): <module>
  build/ARM/python/m5/main.py(597): main
```

Similarly, if you receive a trace back error as shown below, you'll also want to refer to the very bottom of the output to get an idea as to where to start debugging.  In this IOError example, you'd first want to look towards `gem5/configs/common/SysPaths.py`

```bash
Traceback (most recent call last):
File "<string>", line 1, in <module>
File "/opt/gem5/src/python/m5/main.py", line 389, in main
exec filecode in scope
File "./configs/example/fs.py", line 327, in <module>
test_sys = build_test_system(np)
File "./configs/example/fs.py", line 96, in build_test_system
options.ruby, cmdline=cmdline)
File "/opt/gem5/configs/common/FSConfig.py", line 580, in
makeLinuxX86System
makeX86System(mem_mode, numCPUs, mdesc, self, Ruby)
File "/opt/gem5/configs/common/FSConfig.py", line 506, in makeX86System
disk2.childImage(disk('linux-bigswap2.img'))
File "/opt/gem5/configs/common/SysPaths.py", line 45, in disk
return searchpath(disk.path, filename)
File "/opt/gem5/configs/common/SysPaths.py", line 41, in searchpath
raise IOError, "Can't find file '%s' on path." % filename
IOError: Can't find file 'linux-bigswap2.img' on path.
```

Looking within this file should give you more information to help debug, though if this isn't enough, you can look [here](https://www.gem5.org/documentation/general_docs/debugging_and_testing/debugging/trace_based_debugging) to enable trace based debugging for further information.

## PreCommit

If you're running into errors when pushing code to the develop branch, one potential issue is that you may not be passing the precommit checks that gem5 requires before any changes are submitted.
If you see within Gerrit that you have the following error on your verified check, you can navigate to the logs that were output by the tests.

```bash
Kokoro presubmit build finished with status: FAILURE
```

If the output in these logs contains anything like the line below, you need to verify that your changes match the coding style within gem5.

```bash
trim trailing whitespace.................................................Failed
```

In order to ensure your code passes these checks, you should install and run precommit on your changes.
You can install it by running the lines below.

```bash
pip install pre-commit
pre-commit install
```

Additionally, you could instead run `util/pre-commit-install.sh` to set it up.
From here, pre-commit will always run whenever you use `git commit`.
However, if you've already committed these files, you can manually check that pre-commit still passes by running `pre-commit run --files <files to format>` to check specific files, `pre-commit run --all-files` for testing the entire directory, or `pre-commit run <hook_id>` for individual hooks.
When running these commands, pre-commit will both detect any style issues, and automatically reformat the files for you.

## Change-ID

If you're running into issues getting you continuous integration tests to pass on GitHub, you may be forgetting to add a Change-Id to your commit message.
Though we have migrated away from using Gerrit, we still require the addition of a Change-Id.
In order to amend your commit and have all our checks pass, you must install the commit message hook from Gerrit.
You can install and update your commit by running the following commands below.

```bash
n f=.git/hooks/commit-msg ; mkdir -p  ;  curl -Lo  https://gerrit-review.googlesource.com/tools/hooks/commit-msg ; chmod +x
git commit --amend --no-edit
```

If you want more information on the commit message hook, read [here](https://gerrit-review.googlesource.com/Documentation/cmd-hook-commit-msg.html), and if you want to know more about Change-Ids, look [here](https://gerrit-review.googlesource.com/Documentation/user-changeid.html)

## Further Issues

If you continue to run into errors using gem5, feel free to [ask for help](/ask-a-question).
In addition, you can find information on how to report errors that may potentially need fixes [here](https://www.gem5.org/documentation/reporting_problems/) if other channels don't cover all the information you need.
