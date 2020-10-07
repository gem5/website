---
layout: documentation
title: gem5-resources
doc: gem5 documentation
parent: gem5-apis
permalink: /documentation/general_docs/gem5-apis/
authors: Bobby R. Bruce
---

For complete documentation of all methods and variables tagged as APIs, please
see our [Doxygen Module page](
http://doxygen.gem5.org/release/v20-1-0-0/modules.html).

# The gem5 API

In efforts to improve product stability, the gem5 development team is gradually
tagging methods and variables within gem5 as APIs which developers will need to
undergo specific procedures to change. Our goal with the gem5 API is to provide
a stable interface for users to build gem5 models, and extend the gem5
code-base, with guarantees these APIs will not change in a dramatic sudden
manner between gem5 releases.

## How is the gem5 API documented?

We document the gem5 APIs using the [Doxygen documentation generation tool](
https://www.doxygen.nl/index.html). This means you may see the API tagged
at the level of source-code and via our [web-based documentation](
http://doxygen.gem5.org). We use Doxygen's `@ingroup` tag, to specify a
method/variables as part of the gem5 API. We break the API down into
sub-domains such as `api_simobject` or `api_ports`, though all the gem5 APIs
are tagged with the prefix `api_`. For example, we tag SimObject's `params()`
function as follows:

```cpp
/**
* @return This function returns the cached copy of the object parameters.
*
* @ingroup api_simobject
*/
const Params *params() const { return _params; }
```

Via Doxygen automatic generation, the list of gem5 APIs can be found on the
[Doxygen module page](http://doxygen.gem5.org/release/current/modules.html).
In this example, the entire list of SimObject APIs are noted in the
[SimObject API page](
http://doxygen.gem5.org/release/current/group__api__simobject.html). The
definitions of different API groups can be found in
[`src/doxygen/group_definitions.hh`](
https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/src/doxygen/group_definitions.hh).

### Notes for developers

If a developer wishes to tag a new method/variable as part of the gem5 API,
the gem5 community should be consulted. APIs are intended to stay unaltered for
some time. To avoid the gem5 project becoming encumbered with "too many APIs",
we strongly advise those wishing to extend the API to communicate to the
gem5 development team as to why the API will be of value. The
[gem5-dev mailing list](/mailing_lists/) is a good communication channel for
this.

## How can the API change?

We do not guarantee the gem5 API will never change over time. gem5 is a
product under continual development which must adapt to the needs of the
computer architecture research community. However, we guarantee that API
changes will follow strict guidelines outlined below.

1. When an API method or variable is altered, it will be done so in a way in
which the new API will exist alongside the old, with the old API tagged as
deprecated and still functional.

2. The old, deprecated API will exist for two gem5 major cycles before being
removed entirely from code-base, though gem5 developers may choose to keep a
deprecated API in the code-base for longer. For example, if an API is tagged as
deprecated in gem5 21.0, it will also still exist (still tagged as deprecated)
in gem5 21.1. It may be removed entirely in gem5 21.2, though this will be left
to the discretion of the gem5 developers.

3. The gem5 deprecated C++ APIs will be tagged with the C++ deprecated
attribute (`[[deprecated(<msg>)]]`). When utilizing a deprecated C++ API, a
warning will be given at compilation time specifying which API to transition
to. The gem5 deprecated Python parameter APIs are wrapped with our [bespoke
`DeprecatedParam` class](
https://gem5.googlesource.com/public/gem5/+/bd13e8e206e6c86581cf9afa904ef1060351a4b0/src/python/m5/params.py#2166).
Python parameters wrapped in this class will throw an warning when used and
specify which API to transition to.

### Notes for Developers

Prior to making any changes to the gem5 API the [gem5-dev mailing list](
/mailing_lists/) should be consulted. Changing the API, for whatever reason,
**will** be subject to higher scrutiny than other changes. Developers should
be prepared to provide compelling arguments as to why the API needs changed. We
strongly recommend API changes are discussed or they may be rejected during the
Gerrit Code review.

When creating a new API the old API must be tagged as deprecated and the new
API created to exist alongside the old. **It is of upmost importance that the
old, deprecated API is maintained and not deleted**.

As an example, take the following code:

```cpp
/**
 * @ingroup api_bitfield
 */
inline uint64_t
mask(int first, int last)
{
    return mbits((uint64_t)-1LL, first, last);
}
```

This function is part of the gem5 bitfield API. It is a basic mask function
that takes the MSB (first) and the LSB (last) for the generation of a 64-bit.
Let us assume there is a good argument that this function should be replaced
with one that takes the MSB (first), and the length of the mask instead.

To start, the old API needs maintained (i.e., not changed) and tagged with the
`[[deprecated(<msg>)]]` tag. The message (`<msg>`) Should state the new API
to use, and the API tagging should be removed. The new API should then be
created and tagged. So, using our example:

```cpp
[[deprecated("Use mask_length instead.")]]
inline uint64_t
mask(int first, int last)
{
    return mbits((uint64_t)-1LL, first, last);
}

/**
 * @ingroup api_bitfield
 */
inline uint64_t
mask_length(int first, int length)
{
    return mbits((uint64_t)-1LL, first, first + length);
}
```

Here a new function, `mask_length`, has been created. It has been tagged
correctly via Doxygen. The old API, `mask` exists but has the
`[[deprecated]]` annotation added. The message provided states which API
replaces it.

The developer then needs to replace all usage of `mask` in the code-base with
`mask_length`. A warning will be given at compile time if `mask` is used,
stating that it is deprecated and to "Use mask\_length instead.".

Occasionally there may be need to change the python API interface, which
relates to tagged APIs. For example, let's take the below code:

```python
class TLBCoalescer(ClockedObject):
    type = 'TLBCoalescer'
    cxx_class = 'TLBCoalescer'
    cxx_header = 'gpu-compute/tlb_coalescer.hh'

    ...

    slave    = VectorResponsePort("Port on side closer to CPU/CU")
    master   = VectorRequestPort("Port on side closer to memory")

   ...
```

[In recent revisions](
https://gem5.googlesource.com/public/gem5/+/392c1ced53827198652f5eda58e1874246b024f4)
the terms `master` and `slave` have been replaced. Though, the `slave` and
`master` terminology are widely used, so much so we consider them part of the
old API. We therefore wish to deprecate this API is a safe manner while
changing `master` and `slave` with `cpu_side_ports` and `mem_side_ports`. To
do so we would maintain the `master` and `slave` variables but utilize our
[`DeprecatedParam` Class](
https://gem5.googlesource.com/public/gem5/+/bd13e8e206e6c86581cf9afa904ef1060351a4b0/src/python/m5/params.py#2166)
to produce warnings when and if these deprecated variables are used. Working on
our example, we would produce the following:

```python
class TLBCoalescer(ClockedObject):
    type = 'TLBCoalescer'
    cxx_class = 'TLBCoalescer'
    cxx_header = 'gpu-compute/tlb_coalescer.hh'

    ...

    cpu_side_ports = VectorResponsePort("Port on side closer to CPU/CU")
    slave    = DeprecatedParam(cpu_side_ports,
                        '`slave` is now called `cpu_side_ports`')
    mem_side_ports = VectorRequestPort("Port on side closer to memory")
    master   = DeprecatedParam(mem_side_ports,
                        '`master` is now called `mem_side_ports`')

   ...
```

Note the use of `DeprecatedParam` that both ensures `master` and `slave` still
function by redirecting to `mem_side_ports` and `cpu_side_ports` respectively,
as well as providing a comment explaining why this API was deprecated. This
will be displayed to the user as a warning if `master` or `slave` are ever
used.

As with all changes to the gem5 source, these changes will have to go through
our Gerrit code review system before being merged into the `develop` branch,
and eventually making its way to our `stable` branch as part of a gem5 release.
In line with our API policy, these deprecated APIs must exist in a
marked-as-deprecated state for two gem5 major release cycles. After this they
may be removed though developers are under no requirement to do so.
