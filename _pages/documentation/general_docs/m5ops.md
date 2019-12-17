---
layout: documentation
title: M5ops
doc: gem5 documentation
parent: m5ops
permalink: /documentation/general_docs/m5ops/
---

# M5ops
This page explains the special opcodes that can be used in M5 to do checkpoints etc. The m5 utility program (on our disk image and in util/m5/*) provides some of this functionality on the command line. In many cases it is best to insert the operation directly in the source code of your application of interest. You should be able to link with the appropriate m5op_ARCH.o file and the m5op.h header file has prototypes for all the functions.
#  The m5 Utility (FS mode)
he m5 utility (see util/m5/) can be used in FS mode to issue special instructions to trigger simulation specific functionality. It currently offers the following options:

* ivlb: Deprecated, present only for old binary compatibility
* ivle: Deprecated, present only for old binary compatibility
* initparam: Deprecated, present only for old binary compatibility
* sw99param: Deprecated, present only for old binary compatibility
* exit [delay]: Stop the simulation in delay nanoseconds.
* resetstats [delay [period]]: Reset simulation statistics in delay nanoseconds; repeat this every period nanoseconds.
* dumpstats [delay [period]]: Save simulation statistics to a file in delay nanoseconds; repeat this every period nanoseconds.
* dumpresetstats [delay [period]]: same as dumpstats; resetstats
* checkpoint [delay [period]]: Create a checkpoint in delay nanoseconds; repeat this every period nanoseconds.
* readfile: Print the file specified by the config parameter system.readfile. This is how the the rcS files are copied into the simulation environment.
* debugbreak: Call debug_break() in the simulator (causes simulator to get SIGTRAP signal, useful if debugging with GDB).
* switchcpu: Cause an exit event of type, "switch cpu," allowing the Python to switch to a different CPU model if desired.

# Other M5 ops
These are other M5 ops that aren't useful in command line form.
* quiesce: De-schedule the CPUs tick() call until an some asynchronous event wakes it (an interrupt)
* quiesceNS: Same as above, but automatically wakes after a number of nanoseconds if it's not woken up prior
* quiesceCycles: Same as above but with CPU cycles instead of nanoseconds
* quisceTIme: The amount of time the CPU was quiesced for
* addsymbol: Add a symbol to the simulators symbol table. For example when a kernel module is loaded

# Using gem5 ops in Java code
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
When building you need to make sure classpath include gem5OpJni.jar:

```javascript
javac -classpath $CLASSPATH:/path/to/gem5OpJni.jar HelloWorld.java
```
and when running you need to make sure both the java and library path are set:
```javascript
java -classpath $CLASSPATH:/path/to/gem5OpJni.jar -Djava.library.path=/path/to/libgem5OpJni.so HelloWorld
```

# Using gem5 ops with Fortran code
gem5's special opcodes (psuedo instructions) can be used with Fortran programs. In the Fortran code, one can add calls to C functions that invoke the special opcode. While creating the final binary, compile the object files for the Fortran program and the C program (for opcodes) together. I found the documentation provided [here](https://gcc.gnu.org/wiki/GFortranGettingStarted) useful. Read the section **-****- Compiling a mixed C-Fortran program**.
