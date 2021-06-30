---
layout: documentation
title: Building EXTRAS
doc: gem5 documentation
parent: building_extras
permalink: /documentation/general_docs/building/EXTRAS
authors: Jason Lowe-Power
---

# Building EXTRAS
The `EXTRAS` SCons option is a way to add functionality in gem5 without adding your files to the gem5 source tree. Specifically, it allows you to identify one or more directories that will get compiled in with gem5 as if they appeared under the 'src' part of the gem5 tree, without requiring the code to be actually located under 'src'. It's present to allow user to compile in additional functionality (typically additional SimObject classes) that isn't or can't be distributed with gem5. This is useful for maintaining local code that isn't suitable for incorporating into the gem5 source tree, or third-party code that can't be incorporated due to an incompatible license. Because the EXTRAS location is completely independent of the gem5 repository, you can keep the code under a different version control system as well.

The main drawback of the EXTRAS feature is that, by itself, it only supports adding code to gem5, not modifying any of the base gem5 code. 

One use of the EXTRAS feature is to support EIO traces. The trace reader for EIO is licensed under the SimpleScalar license, and due to the incompatibility of that license with gem5's BSD license, the code to read these traces is not included in the gem5 distribution. Instead, the EIO code is distributed via a separate "encumbered" [repository](https://gem5.googlesource.com/public/gem5).

The following examples show how to compile the EIO code. By adding to or modifying the extras path, any other suitable extra could be compiled in. To compile in code using EXTRAS simply execute the following

```js
 scons EXTRAS=/path/to/encumbered build/<ISA>/gem5.opt
```

In the root of this directory you should have a SConscript that uses the ```Source()``` and ```SimObject()``` scons functions that are used in the rest of M5 to compile the appropriate sources and add any SimObjects of interest. If you want to add more than one directory, you can set EXTRAS to a colon-separated list of paths.

Note that EXTRAS is a "sticky" parameter, so after a value is provided to scons once, the value will be reused for future scons invocations targeting the same build directory (```build/<ISA>``` in this case) as long as it is not overridden. Thus you only need to specify EXTRAS the first time you build a particular configuration or if you want to override a previously specified value.
To run a regression with EXTRAS use a command line similar to the following:
```js
 ./util/regress --scons-opts = "EXTRAS=/path/to/encumbered" -j 2 quick
```
