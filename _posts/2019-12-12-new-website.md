---
layout: post
title:  "gem5 Website Redesign"
author: Jason Lowe-Power
date:   2019-12-12
categories: project
---

Welcome to gem5's new website!
The old wiki has needed a refresh for a few years (see screenshot below), and we're excited to finally have something to share with the community!
We hope the new site has better usability and makes it easier to find information about gem5 and how to use it.
If you have any questions or comments, don't hesitate to reach out on the gem5-dev [mailing list](/mailing_lists)!

![](/assets/img/blog/old-website.png "screenshot of the old website")
*gem5's original website*


## Status of the new website

Details on the current status of the migration can be found [on Jira](https://gem5.atlassian.net/browse/GEM5-110).
We also have a specific issue for [migrating the old documentation to the new site](https://gem5.atlassian.net/browse/GEM5-115).
We've already moved most of the documentation, but there are still a few pages that we could use your help with!

There will be some rough edges as we transition.
Some links may be broken, and it's possible we missed pages that should be migrated.
If you find any issues, please let us know via the [mailing list](/mailing_lists) or by opening an issue on [Jira](https://gem5.atlassian.net/).

The website is currently hosted on GitHub pages.
If you'd like to contribute, feel free to create a [pull request](https://github.com/gem5/new-website/pulls) on the [source repository](https://github.com/gem5/new-website).

## Next steps

We will leave this website at new.gem5.org for the next few weeks.
Please let us know if there's any blocking issues before we turn off the old wiki pages.
Before fully transitioning, we will download a static copy of the entire old website (including the old code reviews) and move this to old.gem5.org for archival purposes (and in case we missed anything!).

### Open issues

There's many thing that can be improved with the new website, but I don't believe any are blocking.
A few things that we'd like help with include

- Improving the documentation interface. Adding documentation is confusing since you have to both create the file and update `_data/documentation.yml`.
- Making the documentation more easily discoverable.
- Adding more documentation (always!)
- Fixing broken links
- Minor style sheet cleanups (e.g., the logo scrolls away when on documentation pages)

### Blog posts

We're also looking for more blog contributors!
I would like to see 2-3 blog posts a month covering things like new gem5 features, how to use gem5 informally, workloads, cool papers published using gem5, etc.
Feel free to reach out to me (jason@lowepower.com) if you have other ideas as well!
If you'd like to contribute to the blog, open a PR on [GitHub](https://github.com/gem5/new-website).
