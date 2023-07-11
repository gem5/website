---
layout: page
title: A beginners guide to contributing
permalink: contributing
author: Bobby R. Bruce
---

This document serves as a beginners guide to contributing to gem5. If questions
arise while following this guide, we advise consulting [CONTRIBUTING.md](
https://github.com/gem5/gem5/blob/stable/CONTRIBUTING.md)
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

The gem5 git repository is hosted at <https://github.com/gem5/gem5>.
**Please note: contributions made to other gem5 repos
will not be considered. Please contribute to <https://github.com/gem5/gem5>
exclusively.**

To pull the gem5 git repo:

```Shell
git clone https://github.com/gem5/gem5
```

In order to make changes to this repo, fork the gem5 repo from the link
above into your own repository.

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

### C/CPP

Different tasks will require the project to be modified in different ways.
Though, in all cases, our style-guide must be adhered to. The full C/C++ style
guide is outlined [here](/documentation/general_docs/development/coding_style).

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

### Python

We use [Python Black](https://github.com/psf/black) to format our Python code
to the correct style. To install:

```sh
pip install black
```

Then run on modified/added python files using:

```sh
black <files/directories>
```

For varibale/method/etc. naming conventions, please follow the [PEP 8 naming
convention recommendations](
https://peps.python.org/pep-0008/#naming-conventions). While we try our best to
enforce naming conventions across the gem5 project, we are aware there are
instances where they are not. In such cases please **follow the convention
of the code you are modifying**.

### Using pre-commit

To help enforce our style guide we use use [pre-commit](
https://pre-commit.com). pre-commit is a git hook and, as such, must be
explicitly installed by a gem5 developer.

To install the gem5 pre-commit checks, execute the following in the gem5
directory:

```sh
pip install pre-commit
pre-commit install
```

Once installed pre-commit will run checks on modified code prior to running the
`git commit` command (see [our section on commiting](#committing) for more
details on commiting your changes). If these tests fail you will not be able to
commit.

These same pre-commit checks are run as part of GitHub's CI checks (those
which must pass the status checks required for a change to be
incorporated into the develop branch). It is therefore recommended that
developers install pre-commit to catch style errors early.

**Note:** As of the v22.0 release, the pre-commit hook is only available on the
develop branch.

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

Make sure these changes are being added to your forked repository.
Then commit using:

```Shell
git commit
```

The commit message must adhere to our style. The first line of the commit is
the "header". The header starts with a tag (or tags, separated by a comma),
then a colon. Which tags are used depend on which components of gem5
you have modified. **Please refer to the [MAINTAINERS.yaml](
https://github.com/gem5/gem5/blob/stable/MAINTAINERS.yaml) for
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

## Pushing to GitHub

Pushing to GitHub will allow others in the gem5 project to review the change to
be fully merged into the gem5 source.

To start this process, execute the following in your forked repository:

```
git push origin
```

In order to have these changes reviewed, now go onto GitHub and create a
pull request from your forked repo, onto the gem5-website repo.

## Code review

Now, at <https://github.com/gem5/gem5/pulls>, you can view the
change you have submitted. We suggest that, at this stage, you mark the
corresponding Jira issue as `In Review`. Adding a link to the change on
GitHub as a comment to the issue is also helpful.

Through the GitHub pull request we strongly advise you add reviewers.
GitHub will automatically notify those you assign. The "maintainers" of the
components you have modified should be added as reviewers. These should
correspond to the tags you included in the commit header. **Please consult
[MAINTAINERS.yaml](
https://github.com/gem5/gem5/blob/stable/MAINTAINERS.yaml) to
see who maintains which component**. As an example, for a commit with a header
of `tests,arch : This is testing the arch component` then the maintainers for
both `tests` and `arch` should be included as reviewers.

Reviewers will then review this change. There are two categories which the commit
shall be evaluated: "Code-Review", and the CI-tests workflow.

Any person can review your pull request. They can either approve your changes,
or make suggestions on what needs to be fixed before approval can be given.

Upon the creation of a pull request, our continuous integration system will process
the change. You can see what tests will be run in `.github/workflows/ci-tests.yaml`

If this executes successfully (i.e. the project builds and the tests pass) the
continuous integration system will pass the status checks within GitHub.

However, for first-time contributors, someone will first need to review,
and approve your pull request before the continous integration tests
begin.

In order for a pull request to be merged, one of the Maintainers of the
gem5 repo will have to hit the merge button. This allows for final checks
to be done, ensuring the quality of code entering the gem5 codebase.

For non-trivial changes, it is not unusual for a change to receive feedback
from reviewers that they will want incorporated before giving the commit a
score necessary for it to be merged. This leads to an iterative process.

### Making iterative improvements based on feedback

A reviewer will ask questions and post suggestions on GitHub. You should read
these comments and answer these questions. **All communications between
reviewers and contributors should be done in a polite manner. Rude and/or
dismissive remarks will not be tolerated.**

When you understand what changes are required, using the same workspace as
before, make the necessary modifications to the gem5 repo, and amend the
changes to the commit:

```Shell
git commit --amend
```

Then push the new changes to GitHub:

```Shell
git push origin
```

When your new change is uploaded via the `git push` command, the reviewers will
re-review the change to ensure you have incorporated their suggested
improvements. The reviewers may suggest more improvements and, in this case,
you will have to incorporate them using the same process as above. **This
process is therefore iterative, and it may therefore take several cycles until
the patch is in a state in which the reviewers are happy**. Please do not
be deterred, it is very common for a change to require several iterations.

## Submit and merge

Once this iterative process is complete. The patch may be merged. This is done
via GitHub (Simply click `Submit` within the relevant GitHub page).

As one last step, you should change the corresponding Jira issue status to
`Done` then link the GitHub page as a comment on Jira as to provide evidence
that the task has been completed.

Stable releases of gem5 are published three times per year. Therefore, a change
successfully submitted to the `develop` branch will be merged into the `stable`
branch within three to four months after submission.

## gem5 Bootcamp 2022

As part of [gem5's 2022 Bootcamp](/events/boot-camp-2022), contributing to gem5
was taught as a tutorial. Slides for this tutorial can be found [here](
https://ucdavis365-my.sharepoint.com/:p:/g/personal/jlowepower_ucdavis_edu/EQLtRAKI94JKjgk5pBmJtG8B3ssv9MaR0a2i92G0TwHK8Q?e=KN3NIppm2kg&action=embedview&wdbipreview=true).
A video recording of this tutorial can be found [here](
https://www.youtube.com/watch?v=T67wzFd1gVY).
