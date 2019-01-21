---
layout: post
title: gem5 Horrors and what we can do about it
author: Jason Lowe-Power
date:   2015-6-9
---

![image](/assets/img/gem5-horrors.png)

This post is a post which mostly follows the talk that I am giving at
the [gem5 Users Workshop](http://gem5.org/User_workshop_2015). This post
contains some more details on problems that I skipped in my talk and
some references that I was not able to include in a presentation. You
can view my presentation on Google Drive
[here](https://docs.google.com/presentation/d/1QGA5UVaVJkkMITF2TXCY_KlwmfWef1KBzfDP6ocbj7I/pub?start=false&loop=false&delayms=3000).

I \<3 gem5
----------

Before I get into the negative aspects of [gem5](http://gem5.org), I
first want to point out that it is a great tool. gem5 is used by a large
number of computer architecture researchers, both in industry and in
academia. Here at Wisconsin, and at other universities, gem5 is used in
the classroom to teach students about computer architecture and how to
do computer architecture research.

gem5 is, without a doubt, the most full-featured architecture simulator.
It leverages execute-at-execute semantics for high-fidelity
cycle-by-cycle simulation. gem5 can boot a mostly unmodified Linux
image. It has multiple different CPU and memory models. gem5 has a
modular design which makes it simple to embed and extend. This has
allowed gem5 to be used a large number of projects (see
<http://gem5.org/Projects> and <http://gem5.org/Publications>).

However, as great as gem5 is, its growth has not been without pain. Now
that gem5 is nearing 15 years of development (if you include the
original m5 and GEMS project from which gem5 was born), I believe it's
time to look at some of its deficiencies and talk about what we can do
to mitigate them.

gem5 horrors
------------

Below, I discuss a few specific pain points with that I and others have
experienced with gem5. However, before I get to that, I'd like to talk
about what I think the root of these issues are. gem5 has two main
problems

1)  There is no formal governance model.
2)  The gem5 developers do not think of the user first.

Later, after I give some examples of specific problems, I will discuss
what I think can be done to fix these to issues.

Next I discuss four specific "gem5 horrors" that either I have
personally experienced or I have talked to others who have experienced
them. These issues are deeper that just bugs, even if sometimes they can
be solved with simple changes. After describing each issue, I will also
quickly discuss a possible way to mitigate the problem.

### Horror 1: Merges

There are a number of projects that build on top of gem5. In fact, I
would argue that this is the main use case for gem5. Everyone that I
know who uses gem5 for research, takes the mainline gem5 and builds
their own changes on top of it.

The problem with this model, where people build on top of gem5, is that
when new features are added or bugs are fixed in the mainline,
downstream users have to consume these changes. If the downstream users
do a good job managing their patch queues, this should be a
straightforward thing to do. However, I have found that even when
careful development practices are followed, merging gem5 changes is
incredibly difficult.

Below I discuss a few specific problems that I have run into when
merging new changes in gem5. I believe the problems can be summed up
with two high-level issued we currently have in gem5.

1)  There is no well-defined static API. The interface to different
    modules is constantly in a state of flux.
2)  The regression suite we have in gem5 has poor coverage. There are
    many features that users depend on that are not covered by the
    regression tester.

#### Merge headache \#1: Pointless code changes

Examples from Ruby and Slicc and packet.

#### Merge headache \#2: Features break between versions

Ruby backing store, checkpointing

#### Merge headache \#3: APIs are a moving target

Example with the minimal gem5 script.

#### How to mitigate

I believe that there are two things we can can do as the gem5
development community to make merging upstream changes much easier.
First, we need a stable set of APIs. Second, we need a robust testing
and regression structure. I discuss some specifics of these two
characteristics below.

#### Stable APIs

Today in gem5, it is just as easy to change widely used interfaces, like
the port interface, as it is to change the implementation of a rarely
used function. We need to change this. I think that we need to choose a
set of interfaces and make them stable. This is similar to how the Linux
kernel operates.

Once we have chosen a set of stable interfaces, I'm not suggesting that
they never change, only that it should be more onerous to change stable
APIs than other things. Additionally, this has the added benefit that
"gem5-stable" can actually mean something. We can now have a stable
version, which has non-changing APIs, and a dev version that we can't
necessarily count on to have constant APIs.

I personally do not know what the API should be. I would like to see the
community come together and talk about what they see as important
interfaces. Then, once we find these interfaces, we can architect these
interfaces and hopefully make gem5 easier to use.

#### Testing structure

I do not think that this is a very controversial issue, but gem5 needs a
better regression structure. If all of the features that we used in
gem5-gpu had been part of the regression suite, then we would have had
many less problems.

Again, I do not know exactly how to make the regression suite better,
but I do think a good idea would be to require new features, and bug
fixes, to include a unit-test or something like that. We really need a
softeare engineer to sit down and architect a new regression system.
This would be a great project for someone who is new to the gem5
codebase.

### Horror 2: Configuration files

gem5 has an incredibly flexible configuration system. But with
flexibility often come complexity. In fact, I ran SLOCcount on the
configs directory and found there was more than 4000 lines of Python
code. According to the SLOCcount tool, this means there was 16
person-months and a quarter of a million dollars worth of code here!

All of this complexity causes a number of issues. In my talk, I touched
on the fact that the defaults are confusing, and in some cases
inconsistent.

#### How to mitigate

Since the m5 and GEMS integration, I have noticed a trend that the
number of command line parameters has continued to grow significantly.
It seems that every time a new feature has been added, we have added
some new command line parameters as well. I think this is the wrong way
to do it.

There is an amazing C++-Python wrapper in gem5. We should be taking
advantage of the scripting capabilities of Python.

I have created a simple script that is under 30 lines of Python. I think
we need to encourage our users to script in Python instead of adding
more and more command line parameters. Which, in my experience, really
just leads to scripting in bash instead of in Python anyway.

### Horror 3: Unexpected results

This was a very surprising error that I ran into while working on
creating a homework assignment for a graduate-level computer
architecture course. The point of the homework was to compare the
performance of instruction latency versus instruction throughput. I
wanted the students to take a particular instruction and change the
number of execution units, the latency, and how much the units were
pipelined. To do this, we looked at the divide instruction, since it is
a long latency instruction. Below is the code that we used:

```
for (int i = 0; i < N; i++) {
      Y[i] = X[i] / alpha + Y[i];
}
```

In this code, every divide is totally independent from every other.
Therefore, we would expect that with he out-of-order CPU, that if the
divide is pipelined it the code will speedup by how much the divide unit
is pipelined.

To test this, I looked at two different configurations, a 10 cycle
latency divide with *no* pipelining, and a 10 cycle latency divide that
is fully pipelined. Below is the data I found for ARM and x86. I only
changed the "obvious" options. Each functional unit has an option for
the execution latency and issue latency. If the issue latency is 1, then
the functional unit is fully pipelined. (Now this is a boolean flag.)
All of the data is relative to x86 with no pipelining.

  Configuration   Latency     Issue lat.   x86 Perf   ARM Perf
  --------------- ----------- ------------ ---------- -------------
  No Pipeline     10 cycles   10 cycles    1.0x       8.0x
  Full Pipeline   10 cycles   1 cycle      1.0x       9.6x (1.2x)

There are two very weird results in this data. First, when we fully
pipelined the divide unit, there was no performance change (at all!!) in
x86. Second, when running the exact same cod with ARM, there was a 8x
speedup compared to x86! I find it very hard to believe that the ARM ISA
is inherently better at divide than x86.

#### How to mitigate

This is a much harder problem to mitigate than the others on this list.
Nilay Vaish has taken a step in the right directions with these two
patches on reviewboard <http://reviews.gem5.org/r/2744/> and
<http://reviews.gem5.org/r/2744/>, which have been incorporated in gem5.

The underlying problem is that the implementation for ARM and x86 are
totally distinct. It is not clear to me what the right way to unify the
ISA implementation are. As a stop-gap, developers who are working on
implementing x86 features, need to make sure that they perform similarly
to ARM features. Maybe a solution is to have a single set of C programs
which exercise all ISAs and compare the performance across ISAs. There
should be some performance differences, but not an order of magnitude.

### Horror 4: Lack of new-user support

#### How to mitigate

What I think we need to do is to create a "gem5 for Dummies" book or a
"Learning gem5" book. This book would be similar to Learning Python or
Learning Mercurial. The book would be open source for anyone to
contribute to. In fact, it should be required to update the book if a
developer makes an API-breaking change.

An initial implementation of this book, which currently only includes
about a chapter of "getting started" and is in fact already out of date
can be found here:
[gem5-tutorial](http://pages.cs.wisc.edu/~david/courses/cs752/Spring2015/gem5-tutorial/index.html).
I began working on this in conjunction with the graduate computer
architecture class at Wisconsin, so it may currently have some
Wisconsin-specific text. I hope to continue working on this in my
*copious free time*.

There are many other horrors that other people experience as well. Here
I only discussed some of the horrors that I have heard people
discussing. The purpose in presenting these horrors is not to say that
gem5 is a bad simulator! The purpose is to highlight how there are
currently issues that need to be addressed by the gem5 development
community.

What can we do about it?
------------------------

A lot of the problems that I have discussed above come down to poor
software engineering. And yes, we are architects, not software
engineers, and there are a lot of things we could do better if we just
focused on software engineering. However, I do not think that this is
the underlying issue.

I believe these four horror stem from two systemic problems in the gem5
development community.

1)  There is no formal governance model.
2)  The gem5 developers do not think of the user first.

I believe that if we start to solve these high-level issues, gem5 will
be a much better tool for everyone. Next, I discuss one possible way to
address these two points.

gem5 Foundation
---------------

First, I want to say that I do not believe this is the only way, or the
right way, to move gem5 forward. This is one possibility that I believe
will make gem5 a better tool. I hope that this is a place to begin the
discussion and I am sure that others in our community can come up with
even better suggestions that this!

*I think we should create a gem5 Foundation.* The gem5 Foundation will
be the center for the gem5 community. It will be a formal way for the
community to set goals and push gem5 forward.

There are two main things I think the gem5 Foundation can help us with.
It can set up a formal governance structure and be a place for outside
interests to contribute money towards making gem5 better for everyone.

### Formalizing a governance structure

First, we need a governance structure. This is a document which defines
how decisions are made in the community, what matters to the community,
how to contribute to the community, etc.

There is a lot of documentation on how to write governance models and
what they are. [OSS-Watch](http://oss-watch.ac.uk/) is a great source
for this. Here is a link to a definition of a governance model, which
does a much better job that I can explaining it.
<http://oss-watch.ac.uk/resources/governancemodels> Additionally, here
is a link to an example governance model from an academic open-source
project:
<http://www.taverna.org.uk/about/legal-stuff/taverna-governance-model/>

### Money, Money, Money

What I think the main solution to all of these problems is to pay
software developers *not computer architects!* to solve some of these
problems. Already, within ARM and AMD there are a number of people who
get paid to work on gem5. However, these companies do not have gem5's
best interests as their key focus. Their focus is what ARM and AMD find
interesting.

So, I think that if we have something like the gem5 Foundation, these
companies and academia, can donate money towards coding things that are
good for the community as a whole. The gem5 Foundation can hire software
engineers to work on the parts of gem5 that grad students and
researchers do not want to do. If you look at other academic
communities, they often hire non researchers to do the "grunt work".
Overall, I think this is a good idea for computer architects too, and
specifically for gem5.

I recognize that this may be a crazy idea. I would love to hear what
others think. I am sure we will have some interesting discussion at the
gem5 workshop, and hopefully I will write another post with what other
people thought! Feel free to leave comments below.
