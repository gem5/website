---
layout: documentation
title: "Coding Style"
doc: gem5 documentation
parent: development
permalink: /documentation/general_docs/development/coding_style/
---
# Coding Style

We strive to maintain a consistent coding style in the M5 source code to make the source more readable and maintainable. This necessarily involves compromise among the multiple developers who work on this code. We feel that we have been successful in finding such a compromise, as each of the primary M5 developers is annoyed by at least one of the rules below. We ask that you abide by these guidelines as well if you develop code that you would like to contribute back to M5. An Emacs c++-mode style embodying the indentation rules is available in the source tree at util/emacs/m5-c-style.el.

## Indentation and Line Breaks

Indentation will be 4 spaces per level, though namespaces should not increase the indentation.

* Exception: labels followed by colons (case and goto labels and public/private/protected modifiers) are indented two spaces from the enclosing context.

Indentation should use spaces only (no tabs), as tab widths are not always set consistently, and tabs make output harder to read when used with tools such as diff.

Lines must be a maximum of 79 characters long.

## Braces

For control blocks (if, while, etc.), opening braces must be on the same line as the control keyword with a space between the closing parenthesis and the opening brace.

* Exception: for multi-line expressions, the opening brace may be placed on a separate line to distinguish the control block from the statements inside the block.

```c++
if (...) {
    ...
}

// exception case
for (...;
     ...;
     ...) // brace could be up here
{ // but this is optionally OK *only* when the 'for' spans multiple lines
    ...
}
```

'Else' keywords should follow the closing 'if' brace on the same line, as follows:

```c++
if (...) {
    ...
} else if (...) {
    ...
} else {
    ...
}
```

Blocks that consist of a single statement that fits on a single line may optionally omit the braces. Braces are still required if the single statement spans multiple lines, or if the block is part of an else/if chain where other blocks have braces.

```c++
// This is OK with or without braces
if (a > 0)
    --a;

// In the following cases, braces are still required
if (a > 0) {
    obnoxiously_named_function_with_lots_of_args(verbose_arg1,
                                                 verbose_arg2,
                                                 verbose_arg3);
}

if (a > 0) {
    --a;
} else {
    underflow = true;
    warn("underflow on a");
}
```

For function definitions or class declarations, the opening brace must be in the first column of the following line.

In function definitions, the return type should be on one line, followed by the function name, left-justified, on the next line. As mentioned above, the opening brace should also be on a separate line following the function name.

See examples below:

```c++
int
exampleFunc(...)
{
    ...
}

class ExampleClass
{
  public:
    ...
};
```

Functions should be preceded by a block comment describing the function.

Inline function declarations longer than one line should not be placed inside class declarations. Most functions longer than one line should not be inline anyway.

## Spacing

There should be:

* one space between keywords (if, for, while, etc.) and opening parentheses
* one space around binary operators (+, -, <, >, etc.) including assignment operators (=, +=, etc.)
* no space around '=' when used in parameter/argument lists, either to bind default parameter values (in Python or C++) or to bind keyword arguments (in Python)
* no space between function names and opening parentheses for arguments
* no space immediately inside parentheses, except for very complex expressions. Complex expressions are preferentially broken into multiple simpler expressions using temporary variables.


For pointer and reference argument declarations, either of the following are acceptable:

```c++
FooType *fooPtr;
FooType &fooRef;
```

or

```c++
FooType* fooPtr;
FooType& fooRef;
```
However, style should be kept consistent within a file. If you are editing an existing file, please keep consistent with the existing code. If you are writing new code in a new file, feel free to choose the style of your preference.

## Naming

Class and type names are mixed case, start with an uppercase letter, and do not contain underscores (e.g., ClassName). Exception: names that are acronyms should be all upper case (e.g., CPU). Class member names (method and variables, including const variables) are mixed case, start with a lowercase letter, and do not contain underscores (e.g., aMemberVariable). Class members that have accessor methods should have a leading underscore to indicate that the user should be using an accessor. The accessor functions themselves should have the same name as the variable without the leading underscore.

Local variables are lower case, with underscores separating words (e.g., local_variable). Function parameters should use underscores and be lower case.

C preprocessor symbols (constants and macros) should be all caps with underscores. However, these are deprecated, and should be replaced with const variables and inline functions, respectively, wherever possible.

```c++
class FooBarCPU
{
  private:
    static const int minLegalFoo = 100;  // consts are formatted just like other vars
    int _fooVariable;   // starts with '_' because it has public accessor functions
    int barVariable;    // no '_' since it's internal use only

  public:
    // short inline methods can go all on one line
    int fooVariable() const { return _fooVariable; }

    // longer inline methods should be formatted like regular functions,
    // but indented
    void
    fooVariable(int new_value)
    {
        assert(new_value >= minLegalFoo);
        _fooVariable = new_value;
    }
};
```

## #includes

Whenever possible favor C++ includes over C include. E.g. choose cstdio, not stdio.h.

The block of #includes at the top of the file should be organized. We keep several sorted groups. This makes it easy to find #include and to avoid duplicate #includes.

Always include Python.h first if you need that header. This is mandated by the integration guide. The next header file should be your main header file (e.g., for foo.cc you'd include foo.hh first). Having this header first ensures that it is independent and can be included in other places without missing dependencies.

```c++
// Include Python.h first if you need it.
#include <Python.h>

// Include your main header file before any other non-Python headers (i.e., the one with the same name as your cc source file)
#include "main_header.hh"

// C includes in sorted order
#include <fcntl.h>
#include <sys/time.h>

// C++ includes
#include <cerrno>
#include <cstdio>
#include <string>
#include <vector>

// Shared headers living in include/. These are used both in the simulator and utilities such as the m5 tool.
#include <gem5/asm/generic/m5ops.h>

// M5 includes
#include "base/misc.hh"
#include "cpu/base.hh"
#include "params/BaseCPU.hh"
#include "sim/system.hh"
```

## File structure and modularity

Source files (.cc files) should never contain extern declarations; instead, include the header file associated with the .cc file in which the object is defined. This header file should contain extern declarations for all objects exported from that .cc file. This header should also be included in the defining .cc file. The key here is that we have a single external declaration in the .hh file that the compiler will automatically check for consistency with the .cc file. (This isn't as important in C++ as it was in C, since linker name mangling will now catch these errors, but it's still a good idea.)

When sufficient (i.e., when declaring only pointers or references to a class), header files should use forward class declarations instead of including full header files.

Header files should never contain using namespace declarations at the top level. This forces all the names in that namespace into the global namespace of any source file including that header file, which basically completely defeats the point of using namespaces. It is OK to use using namespace declarations at the top level of a source (.cc) file since the effect is entirely local to that .cc file. It's also OK to use them in _impl.hh files, since for practical purposes these are source (not header) files despite their extension.

## Documenting the code

Each file/class/member should be documented using doxygen style comments.Doxygen allows users to quickly create documentation for our code by extracting the relavent information from the code and comments. It is able to document all the code structures including classes, namespaces, files, members, defines, etc. Most of these are quite simple to document, you only need to place a special documentation block before the declaration. The Doxygen documentation within gem5 is processed every night and the following web pages are generated: [Doxygen](http://doxygen.gem5.org/release/current/index.html)

### Using Doxygen

The special documentation blocks take the form of a javadoc style comment. A javadoc comment is a C style comment with 2 *'s at the start, like this:

```c++
/**
 * ...documentation...
 */
```

The intermediate asterisks are optional, but please use them to clearly delineate the documentation comments.

The documentation within these blocks is made up of at least a brief description of the documented structure, that can be followed by a more detailed description and other documentation. The brief description is the first sentence of the comment. It ends with a period followed by white space or a new line. For example:

```c++
/**
 * This is the brief description. This is the start of the detailed
 * description. Detailed Description continued.
 */
```

If you need to have a period in the brief description, follow it with a backslash followed by a space.

```c++
/**
 * e.g.\ This is a brief description with an internal period.
 */
```
Blank lines within these comments are interpreted as paragraph breaks to help you make the documentation more readble.

### Special commands

Placing these comments before the declaration works in most cases. For files however, you need to specify that you are documenting the file. To do this you use the @file special command. To document the file that you are currently in you just need to use the command followed by your comments. To comment a separate file (we shouldn't have to do this) you can supply the name directly after the file command. There are some other special commands we will be using quite often. To document functions we will use @param and @return or @retval to document the parameters and the return value. @param takes the name of the paramter and its description. @return just describes the return value, while @retval adds a name to it. To specify pre and post conditions you can use @pre and @post.

Some other useful commands are @todo and @sa. @todo allows you to place reminders of things to fix/implement and associate them with a specific class or member/function. @sa lets you place references to another piece of documentation (class, member, etc.). This can be useful to provide links to code that would be helpful in understanding the code being documented.

### Example of Simple Documentation

Here is a simple header file with doxygen comments added.

```c++
/**
 * @file
 * Contains an example of documentation style.
 */

#include <vector>

/**
 * Adds two numbers together.
 */
#define DUMMY(a,b) (a+b)

/**
 * A simple class description. This class does really great things in detail.
 *
 * @todo Update to new statistics model.
 */
class foo
{
  /** This variable stores blah, which does foo and has invariants x,y,z
         @warning never set this to 0
         @invariant foo
    */
   int myVar;

 /**
  * This function does something.
  * @param a The number of times to do it.
  * @param b The thing to do it to.
  * @return The number of times it was done.
  *
  * @sa DUMMY
  */
 int bar(int a, long b);


 /**
  * A function that does bar.
  * @retval true if there is a problem, false otherwise.
  */
 bool manchu();

};
```

### Grouping

Doxygen also allows for groups of classes and member (or other groups) to be declared. We can use these to create a listing of all statistics/global variables. Or just to comment about the memory hierarchy as a whole. You define a group using @defgroup and then add to it using @ingroup or @addgroup. For example:

```c++
/**
 * @defgroup statistics Statistics group
 */

/**
  * @defgroup substat1 Statistitics subgroup
  * @ingroup statistics
  */

/**
 *  A simple class.
 */
class foo
{
  /**
   * Collects data about blah.
   * @ingroup statistics
   */
  Stat stat1;

  /**
   * Collects data about the rate of blah.
   * @ingroup statistics
   */
  Stat stat2;

  /**
   * Collects data about flotsam.
   * @ingroup statistics
   */
  Stat stat3;

  /**
   * Collects data about jetsam.
   * @ingroup substat1
   */
  Stat stat4;

};
```

This places stat1-3 in the statistics group and stat4 in the subgroup. There is a shorthand method to place objects in groups. You can use @{ and @} to mark the start and end of group inclusion. The example above can be rewritten as:

```c++
/**
 * @defgroup statistics Statistics group
 */

/**
  * @defgroup substat1 Statistitics subgroup
  * @ingroup statistics
  */

/**
 *  A simple class.
 */
class foo
{
  /**
   * @ingroup statistics
   * @{
   */

  /** Collects data about blah.*/
  Stat stat1;
  /** Collects data about the rate of blah. */
  Stat stat2;
  /** Collects data about flotsam.*/
  Stat stat3;

  /** @} */

  /**
   * Collects data about jetsam.
   * @ingroup substat1
   */
  Stat stat4;

};
```

It remains to be seen what groups we can come up with.

### Other features

Not sure what other doxygen features we want to use.

## M5 Status Messages
### Fatal v. Panic

There are two error functions defined in `src/base/misc.hh:` `panic()` and `fatal()`. While these two functions have roughly similar effects (printing an error message and terminating the simulation process), they have distinct purposes and use cases. The distinction is documented in the comments in the header file, but is repeated here for convenience because people often get confused and use the wrong one.

* `panic()` should be called when something happens that should never ever happen regardless of what the user does (i.e., an actual m5 bug). `panic()` calls `abort()` which can dump core or enter the debugger.
* `fatal()` should be called when the simulation cannot continue due to some condition that is the user's fault (bad configuration, invalid arguments, etc.) and not a simulator bug. `fatal()` calls `exit(1)`, i.e., a "normal" exit with an error code.

The reasoning behind these definitions is that there's no need to panic if it's just a silly user error; we only panic if m5 itself is broken. On the other hand, it's not hard for users to make errors that are fatal, that is, errors that are serious enough that the m5 process cannot continue.
### Inform, Warn and Hack

The file `src/base/misc.hh` also houses 3 functions that alert the user to various conditions happening within the simulation: `inform()`, `warn()` and `hack()`. The purpose of these functions is strictly to provide simulation status to the user so none of these functions will stop the simulator from running.

* `inform()` and `inform_once()` should be called for informative messages that users should know, but not worry about. `inform_once()` will only display the status message generated by the `inform_once()` function the first time it is called.

* `warn()` and `warn_once()` should be called when some functionality isn't necessarily implemented correctly, but it might work well enough. The idea behind a `warn()` is to inform the user that if they see some strange behavior shortly after a `warn()` the description might be a good place to go looking for an error.

* `hack()` should be called when some functionality isn't implemented nearly as well as it could or should be but for expediency or history sake hasn't been fixed.
* `inform()` Provides status messages and normal operating messages to the console for the user to see, without any connotations of incorrect behavior.
