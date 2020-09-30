---
layout: page
title: A beginners guide to contributing
permalink: contributing
author: Bobby R. Bruce
---

This document serves as a beginners guide to contributing to gem5. If questions
arise while following this guide, we advise consulting [CONTRIBUTING.md](
https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/CONTRIBUTING.md)
which contains more details on how to contribute to gem5.

The following subsections outline, in order, the steps involved in contributing
to the gem5 project.

## Determining what you can contribute

The easiest way to see how you can contribute to gem5 is to check our Jira
issue tracker: <https://gem5.atlassian.net>. From Jira you can check open
issues.

Browse these open issues and see if there are any which you are capable of
handling. When you find a task you are happy to carry out, verify no one else
is presently assigned, then leave a comment asking if you may assign yourself
this task (this will involve creating a Jira account). Though not mandatory, we
advise first-time contributors do this so developers more familiar with the
task may give advice on how best to implement the necessary changes.

Once a developers has replied to your comment (and given any advice they may
have), you may officially assign yourself the task. After this you should
change the status of the task from `Todo` to `In progress`. This helps the gem5
development community understand which parts of the project are presently being
worked on.

**If, for whatever reason, you stop working on a task, please unassign
yourself from the task and change the task's status back to `Todo`.**

## Obtaining the git repo

The gem5 git repository is hosted at <https://gem5.googlesource.com>.
**Please note: contributions made to other gem5 repos (e.g., our GitHub mirror)
will not be considered. Please contribute to <https://gem5.googlesource.com>
exclusively.**

To pull the gem5 git repo:

```Shell
git clone https://gem5.googlesource.com/public/gem5
```

### stable / develop branch

By default, the git repo will have the `stable` branch checked-out. The
`stable` branch is the gem5 stable release branch. I.e., the HEAD
of this branch contains the latest stable release of gem5. (execute `git tag`
on the `stable` branch to see the list of stable releases. A particular
release may be checked out by executing `git checkout <release>`). As the
`stable` branch only contains officially released gem5 code **contributors
should not develop changes on top of the `stable` branch** they should instead
**develop changes on top of the `develop` branch**.

To checkout the `develop` branch:

```Shell
git checkout --track origin/develop
```

Changes may be made on this branch to incorporate changes assigned to yourself.

As the develop branch is frequently updated, regularly obtain the latest
`develop` branch by executing:

```
git pull --rebase
```

Conflicts may need resolved between your local changes and new changes on the
`develop` branch.

## Making modifications

Different tasks will require the project to be modified in different ways.
Though, in all cases, our style-guide must be adhered to. The full style guide
is outlined [here](/documentation/general_docs/development/coding_style).

As a high-level overview:

* Lines must not exceed 79 characters in length.
* There should be no trailing white-space on any line.
* Indentations must be 4 spaces (no tab characters).
* Class names must use upper camel case (e.g., `ThisIsAClass`).
* Class member variables must use lower camel case (e.g.,
`thisIsAMemberVariable`).
* Class member variables with their own public accessor must start with an
underscore (e.g., `_variableWithAccessor`).
* Local variables must use snake case (e.g., `this_is_a_local_variable`).
* Functions must use lower camel case (e.g., `thisIsAFunction`)
* Function parameters must use snake case.
* Macros must be in all caps with underscores (e.g., `THIS_IS_A_MACRO`).
* Function declaration return types must be on their own line.
* Function brackets must be on their own line.
* `for`/`if`/`while` branching operations must be followed by a white-space
before the conditional statement (e.g., `for (...)`).
* `for`/`if`/`while` branching operations' opening bracket must be on the
same line, with the closing bracket on its own line (e.g.,
`for (...) {\n ... \n}\n`). There should be a space between the condition(s)
and the opening bracket.
* C++ access modifies must be indented by two spaces, with method/variables
defined within indented by four spaces.

Below is a simple toy example of how a class should be formatted:

```C++
#DEFINE EXAMPLE_MACRO 7
class ExampleClass
{
  private:
    int _fooBar;
    int barFoo;

  public:
    int
    getFooBar()
    {
        return _fooBar;
    }

    int
    aFunction(int parameter_one, int parameter_two)
    {
        int local_variable = 0;
        if (true) {
            int local_variable = parameter_one + parameter_two + barFoo
                               + EXAMPLE_MACRO;
        }
        return local_variable;
    }

}
```

## Compiling and running tests

The minimum criteria for a change to be submitted is that the code is
compilable and the test cases pass.

The following command both compiles the project and runs our system-level
checks:

```Shell
cd tests
python main.py run
```

**Note: These tests can take several hours to build and execute. `main.py` may
be run on multiple threads with the `-j` flag. E.g.: `python main.py run
-j6`.**

The unit tests should also pass. To run the unit tests:

```Shell
scons build/NULL/unittests.opt
```

To compile an individual gem5 binary:

```Shell
scons build/{ISA}/gem5.opt
```

where `{ISA}` is the target ISA. Common ISAs are `ARM`, `MIPS`, `POWER`,
`RISCV`, `SPARC`, and `X86`. So, to build gem5 for `X86`:

```Shell
scons build/X86/gem5.opt
```

## Committing

When you feel your change is done, you may commit. Start by adding the changed
files:

```Shell
git add <changed files>
```

Then commit using:

```Shell
git commit
```

The commit message must adhere to our style. The first line of the commit is
the "header". The header starts with a tag (or tags, separated by a comma),
then a colon. Which tags are used depend on which components of gem5
you have modified. **Please refer to the [MAINTAINERS.md](
https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/MAINTAINERS) for
a comprehensive list of accepted tags**. After this colon a short description
of the commit must be provided. **This header line must not exceed 65
characters**.

After this, a more detailed description of the commit can be added. This is
inserted below the header, separated by an empty line. Including a description
is optional but it's strongly recommended. The description may span multiple
lines, and multiple paragraphs. **No line in the description may exceed 72
characters.**

To improve the navigability of the gem5 project we would appreciate if commit
messages include a link to the relevant Jira issue/issues.

Below is an example of how a gem5 commit message should be formatted:

```
test,base: This commit tests some classes in the base component

This is a more detailed description of the commit. This can be as long
as is necessary to adequately describe the change.

A description may spawn multiple paragraphs if desired.

Jira Issue: https://gem5.atlassian.net/browse/GEM5-186
```

If you feel the need to change your commit, add the necessary files then
_amend_ the changes to the commit using:

```
git commit --amend
```

This will give you opportunity to edit the commit message.

## Pushing to Gerrit

Pushing to Gerrit will allow others in the gem5 project to review the change to
be fully merged into the gem5 source.

To start this process, execute:

```
git push origin HEAD:refs/for/develop
```

At this stage you may receive an error if you're not registered to contribute
to our Gerrit. To resolve this issue:

1. Create an account at <https://gem5-review.googlesource.com>.
2. Go to `User Settings`.
3. Select `Obtain password` (under `HTTP Credentials`).
4. A new tab shall open, explaining how to authenticate your machine to make
contributions to Gerrit. Follow these instructions and try pushing again.

Gerrit will amend your commit message with a `Change-ID`. Any commit pushed
to Gerrit with this `Change-ID` is assumed to be part of this change.

## Code review

Now, at <https://gem5-review.googlesource.com>, you can view the
change you have submitted (`Your` -> `Changes` -> `Outgoing reviews`). We
suggest that, at this stage, you mark the corresponding Jira issue
as `In Review`. Adding a link to the change on Gerrit as a comment to the
issue is also helpful.

Through the Gerrit portal we strongly advise you add reviewers.
Gerrit will automatically notify those you assign. The "maintainers" of the
components you have modified should be added as reviewers. These should
correspond to the tags you included in the commit header. **Please consult
[MAINTAINERS.md](
https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/MAINTAINERS) to
see who maintains which component**. As an example, for a commit with a header
of `tests,arch : This is testing the arch component` then the maintainers for
both `tests` and `arch` should be included as reviewers.

Reviewers will then review this change. There are three scores which the commit
shall be evaluated: "Code-Review", "Maintainer", and "Verified".

Each reviewer can give a score from `-2` to `+2` to the "Code-Review" score,
where `+2` indicates the reviewer is 100% okay with the patch in its current
state and `-2` when the reviewer is certain they do not want the patch
merged in its current state.

Maintainers can add `+1` or `-1` to the "Maintainer" score. A `+1` score
indicates that the maintainer is okay with the patch.

When a Maintainer gives a `+1` our continuous integration system will process
the change. At the time of writing, the continuous integration system will run:

```
scons build/NULL/unittests.opt
cd tests
python main.py run
```

If this executes successfully (i.e. the project builds and the tests pass) the
continuous integration system will give a `+1` to the "Verifier" score, and a
`-1` if it did not execute successfully.

Gerrit will permit a commit to be merged if at least one reviewer has given a
`+2` to the "Reviewer" score, one maintainer has given a `+1` to the
"Maintainer" score, and the continuous integration system has given a `+1` to
the "Verifier" score.

For non-trivial changes, it is not unusual for a change to receive feedback
from reviewers that they will want incorporated before giving the commit a
score necessary for it to be merged. This leads to an iterative process.

### Making iterative improvements based on feedback

A reviewer will ask questions and post suggestions on Gerrit. You should read
these comments and answer these questions. **All communications between
reviewers and contributors should be done in a polite manner. Rude and/or
dismissive remarks will not be tolerated.**

When you understand what changes are required, using the same workspace as
before, make the necessary modifications to the gem5 repo, and amend the
changes to the commit:

```Shell
git commit --amend
```

Then push the new changes to Gerrit:

```Shell
git push original HEAD:refs/for/develop
```

If for some reason you no longer have your original workspace, you may pull
the change by going to your change in Gerrit, clicking `Download` and executing
one of the listed commands.

When your new change is uploaded via the `git push` command, the reviewers will
re-review the change to ensure you have incorporated their suggested
improvements. The reviewers may suggest more improvements and, in this case,
you will have to incorporate them using the same process as above. **This
process is therefore iterative, and it may therefore take several cycles until
the patch is in a state in which the reviewers are happy**. Please do not
be deterred, it is very common for a change to require several iterations.

## Submit and merge

Once this iterative process is complete. The patch may be merged. This is done
via Gerrit (Simply click `Submit` within the relevant Gerrit page).

As one last step, you should change the corresponding Jira issue status to
`Done` then link the Gerrit page as a comment on Jira as to provide evidence
that the task has been completed.

Stable releases of gem5 are published three times per year. Therefore, a change
successfully submitted to the `develop` branch will be merged into the `stable`
branch within three to four months after submission.
