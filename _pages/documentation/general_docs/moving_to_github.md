---
layout: documentation
title: Moving Active Changes from Gerrit to GitHub
doc: gem5 documentation
parent: moving_to_github
permalink: /documentation/general_docs/moving_to_github/
---

# Moving Active Changes from Gerrit to GitHub

As we transition to using GitHub to host the gem5 project, we need to have a way to move any active changes from Gerrit onto GitHub for review.  If your change won’t be ready to be merged by the time Gerrit becomes read-only, follow the steps below to create a pull request with your changes for review on GitHub.

* Go to https://github.com/gem5/gem5 and create a fork of the gem5 repository, making sure to uncheck the box “Copy the stable branch only”
* Once you create this fork, clone your forked repository, then run `git checkout --track origin/develop` so that your changes are on top of the develop branch
* Now that your forked repository is set up, navigate to https://gem5-review.googlesource.com/q/status:open+-is:wip and find your changes
* Once you’ve opened your change, click the “Download” button on the right side of the screen, and copy the command to cherry-pick your change
* Cherry pick your change to your forked repository, and handle any merge conflicts that may come up.  If these changes are part of a relation change, make sure to cherry pick every part of it.
* Once all changes are cherry picked, run `git push origin` to update your forked repository
* Now that all the changes are up, you can create a pull request. To do so, open your repository on https://github.com, and hit the Contribute button in the middle of the page.  Make sure you’re on the develop branch when doing so.  Once you hit Contribute, a button saying “Open pull request” should appear.
* This navigates you to a page to create a pull request.  For the base repository, it should be gem5/gem5, and the branch should be develop.  Any pull requests to the stable branch will be ignored.  The head repository will be your forked repository, and the branch should also be develop.  In the body of your pull request, you can include a link to your changes from Gerrit, so any comments can be easily accessible.  In addition, on the right hand side of the page, you can add reviewers, so you can request anyone that looked over your changes on Gerrit to review your pull request
* Once you’re happy with your pull request, you can hit the “Create pull request” button at the bottom of the page.

If you’re a first-time contributor to the gem5 GitHub repository, you will need a positive review of your pull request before any continuous integration tests can be run.  For your change to be merged, you need both the positive review, as well as for these tests to pass.  Finally a gem5 maintainer will squash and merge your changes once all prior checks pass.
