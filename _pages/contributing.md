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
issue tracker: <https://gem5.atlassian.net> or GitHub issue tracker:
<https://github.com/gem5/gem5/issues>.

Browse these open issues and see if there are any which you are capable of
handling. When you find a task you are happy to carry out, verify no one else
is presently assigned, then leave a comment asking if you may assign yourself
this task. Though not mandatory, we
advise first-time contributors do this so developers more familiar with the
task may give advice on how best to implement the necessary changes.

Once a developers has replied to your comment (and given any advice they may
have), you may officially assign yourself the task. This helps the gem5
development community understand which parts of the project are presently being
worked on.

**If, for whatever reason, you stop working on a task, please unassign
yourself from the task.**

## Obtaining the git repo

The gem5 git repository is hosted at <https://github.com/gem5/gem5>.
**Please note: contributions made to other gem5 repos
will not be considered. Please contribute to <https://github.com/gem5/gem5>
exclusively.**

To pull the gem5 git repo:

```sh
git clone https://github.com/gem5/gem5
```

If you wish to use gem5 and never contribute, this is fine. However, to
contribute, we use the [GitHub Pull-Request model](https://docs.github.com/en/pull-requests), and therefore recommend [Forking the gem5 repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo) prior to contributing.

### Forking

Please consult the [GitHub documentation on Forking a GitHub repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo).
As we will be working atop the `develop` branch, please ensure you Fork all the repository's branches, not just the `stable` branch.

This will create your own forked version of the gem5 repo on your own GitHub account.
You may then obtain it locally using:

```sh
git clone https://github.com/{your github account}/gem5
```

Via this forked repo you can contribute to gem5.

### stable / develop branch

When cloned the git repo will have the `stable` branch checked-out by default. The
`stable` branch is the gem5 stable release branch. I.e., the HEAD
of this branch contains the latest stable release of gem5. (execute `git tag`
on the `stable` branch to see the list of stable releases. A particular
release may be checked out by executing `git checkout <release>`). As the
`stable` branch only contains officially released gem5 code **contributors
should not develop changes on top of the `stable` branch** they should instead
**develop changes on top of the `develop` branch**.

To switch to the `develop` branch:

```sh
git switch develop
```

The develop `branch` is merged into the `stable` branch upon a gem5 release.
Therefore, any changes you make exist on the stable branch until the next release.

We recommend creating your own local branches to do changes.
This helps keep your changes organized across different branches in your forked repository.
For example, the following will create a new branch, from `develop`, called `new-feature`:

```sh
git switch -c new-feature
```

While working on your contribution, we recommend keeping your forked repository in-sync with the source gem5 repository.
To do so, regularly [Sync your fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork).

The develop branch is frequently updated so can be obtained locally, after a sync, with:

```sh
git switch develop # Switching back to the develop branch.
git pull
```

You can then incorporate these into your local branch with:

```sh
git switch new-feature # Switching back to your "new-feature" branch.
git rebase develop
```

Conflicts may need resolved between your branch and new changes.

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

For variable/method/etc. naming conventions, please follow the [PEP 8 naming
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
`git commit` command (see [our section on committing](#committing) for more
details on committing your changes). If these tests fail you will not be able to
commit.

These same pre-commit checks are run as part our CI checks (those
which must pass in order for a change to be merged into the develop branch). It
is therefore strongly recommended that developers install pre-commit to catch
style errors early.

## Compiling and running tests

The minimum criteria for a change to be submitted is that the code is
compilable and the test cases pass.

The following command both compiles the project and runs our "quick"
system-level checks:

```sh
cd tests
./main.py run
```

**Note: These tests can take several hours to build and execute. `main.py` may
be run on multiple threads with the `-j` flag. E.g.: `python main.py run
-j6`.**

The unit tests should also pass. To run the unit tests:

```sh
scons build/NULL/unittests.opt
```

To compile an individual gem5 binary:

```sh
scons build/ALL/gem5.opt
```

This compiles a gem5 binary containing "ALL" ISA targets. For more information
on building gem5 please consult our [building documentation](
/documentation/general_docs/building).

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

```sh
git commit --amend
```

This will give you opportunity to edit the commit message.

You may continue to add more commits as a chain of commits to be included in the pull-request.
However, we recommend that pull-requests are kept small and focused.
For example, if you wish to add a different feature or fix a different bug, we recommend doing so in another pull requests.

## Pushing and creating a pull request

Once you have completed your changes locally, you can push to your forked gem5 repository.
Assuming the branch we are working on is `new-feature`:

```sh
git push --set-upstream origin test-feature
```

Now, via the GitHub web interface, you can [create a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) of your changes from your forked repository's branch into the gem5 `develop` branch.

## Passing the checks

Once you have created a pull request, the gem5 Continuous Integration (CI) tests will run.
These run a series of checks to ensure your changes are valid.
These must pass before your changes can be merged into the gem5 `develop` branch.

In addition to the CI tests, your changes will be reviewed by the gem5 community.
Your pull-request must have the approval of at least one community member prior to being merged.

Once your pull-request has passed all the CI tests and has been approved by at least one community member, it will be merged a gem5 Project Maintainer will do a [Squash and Merge](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges#squash-and-merge-your-commits) on the pull-request.

### Making iterative improvements based on feedback

A reviewer will ask questions and post suggestions on GitHub. You should read
these comments and answer these questions. **All communications between
reviewers and contributors should be done in a polite manner. Rude and/or
dismissive remarks will not be tolerated.**

When you understand what changes are required make amendments to the pull
request by adding patches to the same branch and then pushing to the forked repository.

Once pushed to the forked repository, the pull request will automatically update with your changes.
A reviewer will then review your changes and, if necessary, ask for further changes, or approve your pull-request.
