---
layout: page
title: Reporting Problems
parent: documentation
permalink: documentation/reporting_problems/
author: Bobby R. Bruce
---

Many of the people on the [gem5-users mailing list](/mailing_lists) are happy
to help when someone has a problem or something doesn't work. However, please
keep in mind those working on gem5 have other commitments, so we'd appreciate,
prior to reporting, if users could put in some effort to solving their own
problems, or, at least, gather enough information to help others resolve the
issue.

Below we outline some general advise on issue reporting.

## Prior to reporting a problem

The most important thing to do prior to reporting a problem is to investigate
the issue as much as possible. This may lead you to a solution,
or enable you to provide more information to the gem5 community regarding the
problem. Below are a series of steps/checks we'd advise you carry out before
reporting an issue:

1. Please check if a similar question has already been asked on our
[mailing lists](/mailing_lists) (check the archives), or reported in our
[Jira Issue Tracking system](https://gem5.atlassian.net).

2. Ensure you're compiling and running the latest version of [gem5](
https://gem5.googlesource.com). The issue may have already been resolved.

3. Check changes [currently under review on our Gerrit system](
https://gem5-review.googlesource.com/dashboard/self). It's possible a fix to
your issue is already on its way to being merged into the project.

4. Make sure you're running with `gem5.opt` or `gem5.debug`, not `gem5.fast`.
The `gem5.fast` binary compiles out assertion checking for speed, so a problem
that causes a crash or an error on `gem5.fast` may result in a more informative
assertion failure with `gem5.opt` or `gem5.debug`.

5. If it seems appropriate, enable some debug flags (e.g.,`--debug-flags=Foo`
via the CLI). For more information on debug flags, please consult our
[debugging tutorial](/documentation/learning_gem5/part2/debugging).

6. Don't be afraid to debug using GDB if your problem is occurring on the C++
side.

# Reporting a problem

Once you believe you have gathered enough information about your problem. Then
feel free to report it.

* If you have reason to believe your problem is a bug then please report the
issue on gem5's [Jira Issue Tracking system](https://gem5.atlassian.net).
**Please include any information which may aid in someone else reproducing
this bug on their system**. Include the command line argument used, any
relevant system information (as a minimum, what OS are you using, and how
did you compile gem5?), error messages received, program outputs, stack traces,
etc.

* If you choose to ask a question on the [gem5-users mailing list](
/mailing_lists), please provide any information which may be helpful. If you
have a theory about what the problem might be, please let us know, but
include enough basic information so others can decide whether your theory is
correct or not.


# Solving the problem

If you have solved a problem that you reported, please let the community know
about your solution as a follow-up (either in the mailing list or in the Jira
Issue tracking system). If you have fixed a bug, we'd appreciate if you could
submit the fix to the gem5 source. Please see our
[beginners guide to contributing](/contributing)
on how to do this.

If your issue is with the content of a gem5 document/tutorial being incorrect,
then please consider submitting a change. Please consult our [README](
https://gem5.googlesource.com/public/gem5-website/+/refs/heads/stable/README.md)
for more information on how to make contributions to the gem5 website.
