---
layout: documentation
title: M5ops
doc: gem5 documentation
parent: m5ops
permalink: /documentation/general_docs/m5ops/
---

# M5ops

This page explains the special opcodes that can be used in M5 to do checkpoints etc. The m5 utility program (on our disk image and in util/m5/*) provides some of this functionality on the command line. In many cases it is best to insert the operation directly in the source code of your application of interest. You should be able to link with the appropriate libm5.a file and the m5ops.h header file has prototypes for all the functions.

## Building M5 and libm5

In order to build m5 and libm5.a for your target ISA, run the following command in the util/m5/ directory.

```bash
scons build/{TARGET_ISA}/out/m5
```

The list of target ISAs is shown below.

* x86
* arm (arm-linux-gnueabihf-gcc)
* thumb (arm-linux-gnueabihf-gcc)
* sparc (sparc64-linux-gnu-gcc)
* arm64 (aarch64-linux-gnu-gcc)
* riscv (riscv64-linux-gnu-gcc)

Note if you are using a x86 system for other ISAs you need to have the cross-compiler installed. The name of the cross-compiler is shown inside the parentheses in the list above.

See util/m5/README.md for more details.

## The m5 Utility (FS mode)

The m5 utility (see util/m5/) can be used in FS mode to issue special instructions to trigger simulation specific functionality. It currently offers the following options:

* initparam: Deprecated, present only for old binary compatibility
* exit [delay]: Stop the simulation in delay nanoseconds.
* resetstats [delay [period]]: Reset simulation statistics in delay nanoseconds; repeat this every period nanoseconds.
* dumpstats [delay [period]]: Save simulation statistics to a file in delay nanoseconds; repeat this every period nanoseconds.
* dumpresetstats [delay [period]]: same as dumpstats; resetstats
* checkpoint [delay [period]]: Create a checkpoint in delay nanoseconds; repeat this every period nanoseconds.
* readfile: Print the file specified by the config parameter system.readfile. This is how the the rcS files are copied into the simulation environment.
* debugbreak: Call debug_break() in the simulator (causes simulator to get SIGTRAP signal, useful if debugging with GDB).
* switchcpu: Cause an exit event of type, "switch cpu," allowing the Python to switch to a different CPU model if desired.
* workbegin: Cause an exit evet of type, "workbegin", that could be used to mark the begining of an ROI.
* workend: Cause an exit event of type, "workend", that could be used to mark the termination of an ROI.

## Other M5 ops

These are other M5 ops that aren't useful in command line form.

* quiesce: De-schedule the CPUs tick() call until some asynchronous event wakes it (an interrupt)
* quiesceNS: Same as above, but automatically wakes after a number of nanoseconds if it's not woken up prior
* quiesceCycles: Same as above but with CPU cycles instead of nanoseconds
* quisceTIme: The amount of time the CPU was quiesced for
* addsymbol: Add a symbol to the simulators symbol table. For example when a kernel module is loaded

## Using gem5 ops in Java code

These ops can also be used in Java code. These ops allow gem5 ops to be called from within java programs like the following:

```python
import jni.gem5Op;

public  class HelloWorld {

   public static void main(String[] args) {
       gem5Op gem5 = new gem5Op();
       System.out.println("Rpns0:" + gem5.rpns());
       System.out.println("Rpns1:" + gem5.rpns());
   }

   static {
       System.loadLibrary("gem5OpJni");
   }
}
```

When building you need to make sure classpath includes gem5OpJni.jar:

```javascript
javac -classpath $CLASSPATH:/path/to/gem5OpJni.jar HelloWorld.java
```

and when running you need to make sure both the java and library path are set:

```javascript
java -classpath $CLASSPATH:/path/to/gem5OpJni.jar -Djava.library.path=/path/to/libgem5OpJni.so HelloWorld
```

## Using gem5 ops with Fortran code

gem5's special opcodes (psuedo instructions) can be used with Fortran programs. In the Fortran code, one can add calls to C functions that invoke the special opcode. While creating the final binary, compile the object files for the Fortran program and the C program (for opcodes) together. I found the documentation provided [here](https://gcc.gnu.org/wiki/GFortranGettingStarted) useful. Read the section **-****- Compiling a mixed C-Fortran program**.

## Linking M5 to your C/C++ code

In order to link m5 to your code, first build `libm5.a` as described in the section above.

Then

* Include `gem5/m5ops.h` in your source file(s)
* Add `gem5/include` to your compiler's include search path
* Add `gem5/util/m5/build/{TARGET_ISA}/out` to the linker search path
* Link against `libm5.a`

For example, this could be achieved by adding the following to your Makefile:

```
CFLAGS += -I$(GEM5_PATH)/include
LDFLAGS += -L$(GEM5_PATH)/util/m5/build/$(TARGET_ISA)/out -lm5
```
