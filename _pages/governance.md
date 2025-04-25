---
layout: page
title: Governance
parent: about
permalink: /governance/
---


gem5 is a meritocratic, consensus-based community project. 
Anyone interested in the project is welcome to join the community, contribute to its design, and participate in the decision-making process. Historically, gem5 has been developed within both industry and academia. 
This document outlines how community participation takes place and how individuals can earn merit within the project.

The document is organized into several sections. 
[Philosophy](#philosophy) outlines the core principles of the gem5 community. 
[GitHub Issues](#gem5-github-issue-tracker) directs users to our GitHub issue tracker for gem5 development. 
[Roles and Responsibilities](#roles-and-responsibilities) defines the different classes of gem5 users, types of contributors, and their responsibilities. 
[Support](#support) explains how the community assists users, while [Contribution Process](#contribution-process) details how to make contributions. 
Finally, [Decision Making Process](#decision-making-process) describes how decisions are made.

---
## Philosophy

The goal of gem5 is to provide a tool to further the state of the art in computer architecture. gem5 can be used for (but is not limited to) computer-architecture research, advanced development, system-level performance analysis and design-space exploration, hardware-software co-design, and low-level software performance analysis. Another goal of gem5 is to be a common framework for computer architecture. A common framework in the academic community makes it easier for other researchers to share workloads as well as models and to compare and contrast with other architectural techniques.

The gem5 community strives to balance the needs of its three user types (academic researchers, industry researchers, and students, detailed below). For instance, gem5 strives to balance adding new features (important to researchers) and a stable code base (important for students). Specific user needs important to the community are enumerated below:

*   Effectively and efficiently emulate the behavior of modern processors in a way that balances simulation performance and accuracy
*   Serve as a malleable baseline infrastructure that can easily be adapted to emulate the desired behaviors
*   Provide a core set of APIs and features that remain relatively stable
*   Incorporate features that make it easy for companies and research groups to stay up to date with the tip and continue contributing to the project

Additionally, the gem5 community is committed to openness, transparency, and inclusiveness. Participants in the gem5 community of all backgrounds should feel welcome and encouraged to contribute.

---
## gem5 GitHub issue tracker 

The [gem5 GitHub issue tracker](https://github.com/gem5/gem5/issues) lists known bugs, feature and improvement suggestions.
Those wishing to work on gem5 may browse issues and request assignment to the tasks they believe they can undertake.
Users of all types are encouraged to open their own bug reports or put forward improvement suggestions.
While contributions to gem5 may be made without first being logged in our GitHub issue tracker, that remains the project's primary method of prioritizing and managing work items for upcoming releases.

---
## Roles And Responsibilities

### Users

Users are community members who have a need for the project. They are the most important members of the community and without them the project would have no purpose. Anyone can be a user; there are no special requirements. There are currently three main categories of gem5 users: academic researchers, industry researchers, and students. Individuals may transition between categories, e.g., when a graduate student takes an industry internship, then returns to school; or when a student graduates and takes a job in industry. These three users are described below.

#### - Academic Researchers

This type of user primarily includes individuals who use gem5 for academic research.
Examples include, but are not limited to, graduate students, research scientists, and post-graduates. This user often uses gem5 as a tool to discover and invent new computer architecture mechanisms. Academic Researchers often are first exposed to gem5 as [Students](#--students) and transition from Students to Academic Researchers over time.

Because of these users' goals, they primarily add new features to gem5. It is important to the gem5 community to encourage these users to contribute their work to the mainline gem5 repository. By encouraging these users to commit their research contributions, gem5 will make it much easier for other researchers to compare and contrast with other architectural techniques (see [Philosophy](#philosophy) section).

#### - Industry Researchers

This type of user primarily includes individuals working for companies that use gem5\. These users are distinguished from academic researchers in two ways. First, industry researchers are often part of a larger team, rather than working individually on gem5\. Second, industry researchers often want to incorporate proprietary information into private branches of gem5\. Therefore, industry researchers tend to have rather sophisticated software infrastructures built around gem5\. For these users, the stability of gem5 features and baseline source code is important. Another key consideration is the fidelity of the models, and their ability to accurately reflect realistic implementations. To enable industry participation, it is critical to maintain licensing terms that do not restrict or burden the use of gem5 in conjunction with proprietary IP.

#### - Students

This type of user primarily includes individuals that are using gem5 in a classroom setting. These users typically have some foundation in computer architecture, but they have little or no background using simulation tools. Additionally, these users may not use gem5 for an extended period of time, after finishing their short-term goals (e.g., a semester-long class).

The project asks its users to participate in the project and community as much as possible. User contributions enable the project team to ensure that they are satisfying the needs of those users. Common user contributions include (but are not limited to):

*   evangelising about the project (e.g., a link on a website and word-of-mouth awareness raising)
*   informing developers of strengths and weaknesses from a new user perspective
*   providing moral support (a ‘thank you' goes a long way)
*   providing financial support (the software is open source, but its developers need to eat)

Users who continue to engage with the project and its community will often become more and more involved. Such users may find themselves becoming contributors, as described in the next section.

### Contributors

Contributors are community members who contribute in concrete ways to the project. Anyone can become a contributor, and contributions can take many forms. There are no specific skill requirements and no selection process.

There is only one expectation of commitment to the project: **contributors must be respectful to each other during the review process and work together to reach compromises**. See the [Reviewing Patches](#reviewing-patches) section for more on the process of contributing.

In addition to their actions as users, contributors may also find themselves doing one or more of the following:

*   answering questions on the mailing lists, particularly the "easy" questions from new users (existing users are often the best people to support new users), or those that relate to the particular contributor's experiences
*   reporting bugs
*   identifying requirements
*   providing graphics and web design
*   programming
*   assisting with project infrastructure
*   writing documentation
*   fixing bugs
*   adding features
*   acting as an ambassador and helping to promote the project

Contributors engage with the project primarily through the GitHub. They submit changes to the project source code via patches submitted to GitHub, which will be considered for inclusion in the project by existing maintainers (see next section). The developer mailing list is the most appropriate place to ask for help when making that first contribution.

As contributors gain experience and familiarity with the project, their profile within, and commitment to, the community will increase. At some stage, they may find themselves being nominated for maintainership.

### Maintainers

Maintainers are community members who have shown that they are committed to the continued development of the project through ongoing engagement with the community. Maintainership allows contributors to more easily carry on with their project related activities by giving them direct access to the project's resources. That is, they can make changes directly to project outputs, although they still have to submit code changes via GitHub. Additionally, maintainers are expected to have an ongoing record of contributions in terms of code, reviews, and/or discussion.

Maintainers have no more authority over the project than contributors. While maintainership indicates a valued member of the community who has demonstrated a healthy respect for the project's aims and objectives, their work continues to be reviewed by the community. The key difference between a maintainer and a contributor is maintainers have the extra responsibility of merging pull requests to the mainline. Additionally, maintainers are expected to contribute to discussions review patches.

Anyone can become a maintainer. The only expectation is that a maintainer has demonstrated an ability to participate in the project as a team player. Specifically, refer to the 2nd paragraph of the [Contributors](#contributors) section.

Typically, a potential maintainer will need to show that they have an understanding of the project, its objectives and its strategy (see [Philosophy](#philosophy) section). They will also have provided valuable contributions to the project over a period of time.

New maintainers can be nominated by any existing maintainer. Once they have been nominated, there will be a vote by the project management committee (PMC; see below). Maintainer nomination and voting is one of the few activities that takes place on the project's private management list. This is to allow PMC members to freely express their opinions about a nominee without causing embarrassment. Once the vote has been held, the nominee is notified of the result. The nominee is entitled to request an explanation of any ‘no' votes against them, regardless of the outcome of the vote. This explanation will be provided by the [PMC Chair](#pmc-chair) and will be anonymous and constructive in nature.

Nominees may decline their appointment as a maintainer. However, this is unusual, as the project does not expect any specific time or resource commitment from its community members. The intention behind the role of maintainer is to allow people to contribute to the project more easily, not to tie them into the project in any formal way.

It is important to recognise that maintainership is a privilege, not a right. That privilege must be earned and once earned it can be removed by the [PMC](#project-management-committee) in extreme circumstances. However, under normal circumstances Maintainership exists for as long as the maintainer continues engaging with the project.

A maintainer who shows an above-average level of contribution to the project, particularly with respect to its strategic direction and long-term health, may be nominated to become a member of the PMC. This role is described below.

Note: The definitive list of maintainers is kept via a GitHub Team which is not publicly visible due to GitHub limitations. Lists on the website, etc. may be out of date.

### Project management committee

The project management committee consists of those individuals identified as "project owners" on the development site. The PMC has additional responsibilities over and above those of a maintainer. These responsibilities ensure the smooth running of the project. PMC members are expected to review code contributions, participate in strategic planning, approve changes to the governance model and manage how the software is distributed and licensed.

Some PMC members are responsible for specific components of the gem5 project. This includes gem5 source modules (e.g., classic caches, O3CPU model, etc.) and project assets (e.g., the website). A list of the current components and the responsible members can be found within the [MAINTAINERS](https://github.com/gem5/gem5/blob/stable/MAINTAINERS.yaml) document.

Members of the PMC do not have significant authority over other members of the community, although it is the PMC that votes on new maintainers. It also makes decisions when community consensus cannot be reached. In addition, the PMC has access to the project's private mailing list. This list is used for sensitive issues, such as votes for new maintainers and legal matters that cannot be discussed in public. It is never used for project management or planning.

Membership of the PMC is by invitation from the existing PMC members. A nomination will result in discussion and then a vote by the existing PMC members. PMC membership votes are subject to consensus approval of the current PMC members. Additions to the PMC require unanimous agreement of the PMC members. Removing someone from the PMC requires N-1 positive votes, where N is the number of PMC members not including the individual who is being voted out.

#### - Members

*   Ali Saidi
*   Andreas Sandberg
*   Brad Beckmann
*   David Wood
*   Gabe Black
*   Giacomo Travaglini
*   Jason Lowe-Power (chair)
*   Matt Sinclair
*   Tony Gutierrez
*   Steve Reinhardt

### PMC Chair

The PMC Chair is a single individual, voted for by the PMC members. Once someone has been appointed Chair, they remain in that role until they choose to retire, or the PMC casts a two-thirds majority vote to remove them.

The PMC Chair has no additional authority over other members of the PMC: the role is one of coordinator and facilitator. The Chair is also expected to ensure that all governance processes are adhered to, and has the casting vote when any project decision fails to reach consensus.

---
## Support

All participants in the community are encouraged to provide support for new users within the project management infrastructure. This support is provided as a way of growing the community. Those seeking support should recognise that all support activity within the project is voluntary and is therefore provided as and when time allows.

---
## Contribution Process

Anyone, capable of showing respect to others, can contribute to the project, regardless of their skills, as there are many ways to contribute. For instance, a contributor might be active on the project mailing list and issue tracker, or might supply patches. The various ways of contributing are described in more detail in a separate document [Submitting Contributions](/contributing).

[GitHub discsussions](https://github.com/orgs/gem5/discussions) or [GitHub issues](https://github.com/gem5/gem5/issues) are the most appropriate place for a contributor to ask for help when making their first contribution. See the [Submitting Contributions](/contributing) page on the gem5 website or the [CONTRIBUTING.md](CONTRIBUTING.md) for details of the gem5 contribution process. Each new contribution should be submitted as a patch to our GitHub site. Then, other gem5 developers will review your patch, possibly asking for changes. After the patch has received consensus (see [Decision Making Process](#decision-making-process)), the patch is ready to be committed to the gem5 tree. For contributors, a maintainer should approve and merge the changeset for you. If a maintainer does not merge the changeset within a reasonable window (a couple of days), send a friendly reminder email to the gem5-dev list. Before a patch is committed to gem5, it must receive at least 2 approvals. If there are no reviews on a patch, users should send follow up notes asking for reviews.

#### Reviewing Patches

An important part of the contribution process is providing feedback on patches that other developers submit. The purpose of reviewing patches is to weed out obvious bugs and to ensure that the code in gem5 is of sufficient quality.

All users are encouraged to review the contributions that are posted on GitHub. If you are an active gem5 user, it's a good idea to keep your eye on the contributions that are posted there (typically by subscribing to the gem5-dev mailing list) so you can speak up when you see a contribution that could impact your use of gem5\. It is far more effective to contribute your opinion in a review before a patch gets committed than to complain after the patch is committed, you update your repository, and you find that your simulations no longer work.

We greatly value the efforts of reviewers to maintain gem5's code quality and consistency. However, it is important that reviews balance the desire to maintain the quality of the code in gem5 with the need to be open to accepting contributions from a broader community. People will base their desire to contribute (or continue contributing) on how they and other contributors are received. With that in mind, here are some guidelines for reviewers:

1.  Remember that submitting a contribution is a generous act, and is very rarely a requirement for the person submitting it. It's always a good idea to start a review with something like "thank you for submitting this contribution". A thank-you is particularly important for new or occasional submitters.
2.  Overall, the attitude of a reviewer should be "how can we take this contribution and put it to good use", not "what shortcomings in this work must the submitter address before the contribution can be considered worthy".
3.  As the saying goes, "the perfect is the enemy of the good". While we don't want gem5 to deteriorate, we also don't want to bypass useful functionality or improvements simply because they are not optimal. If the optimal solution is not likely to happen, then accepting a suboptimal solution may be preferable to having no solution. A suboptimal solution can always be replaced by the optimal solution later. Perhaps the suboptimal solution can be incrementally improved to reach that point.
4.  When asking a submitter for additional changes, consider the cost-benefit ratio of those changes. In particular, reviewers should not discount the costs of requested changes just because the cost to the reviewer is near zero. Asking for extensive changes, particularly from someone who is not a long-time gem5 developer, may be imposing a significant burden on someone who is just trying to be helpful by submitting their code. If you as a reviewer really feel that some extensive reworking of a patch is necessary, consider volunteering to make the changes yourself.
5.  Not everyone uses gem5 in the same way or has the same needs. It's easy to reject a solution due to its flaws when it solves a problem you don't have—so there's no loss to you if we end up with no solution. That's probably not an acceptable result for the person submitting the patch though. Another way to look at this point is as the flip side of the previous item: just as your cost-benefit analysis should not discount the costs to the submitter of making changes, just because the costs to you are low, it should also not discount the benefits to the submitter of accepting the submission, just because the benefits to you are low.
6.  Be independent and unbiased while commenting on review requests. Do not support a patch just because you or your organization will benefit from it or oppose it because you will need to do more work. Whether you are an individual or someone working with an organization, think about the patch from community's perspective.
7.  Try to keep the arguments technical and the language simple. If you make some claim about a patch, substantiate it.

---
## Decision Making Process

Decisions about the future of the project are made through discussion with all members of the community, from the newest user to the most experienced PMC member. All non-sensitive project management discussion takes place on the gem5-dev mailing list. Occasionally, sensitive discussion occurs on a private list.

In order to ensure that the project is not bogged down by endless discussion and continual voting, the project operates a policy of lazy consensus. This allows the majority of decisions to be made without resorting to a formal vote.

#### Lazy consensus

Decision making typically involves the following steps:

*   Proposal
*   Discussion
*   Vote (if consensus is not reached through discussion)
*   Decision

Any community member can make a proposal for consideration by the community. In order to initiate a discussion about a new idea, they should create a post on GitHub discussions or submit a patch implementing the idea to GitHub. This will prompt a review and, if necessary, a discussion of the idea. The goal of this review and discussion is to gain approval for the contribution. Since most people in the project community have a shared vision, there is often little need for discussion in order to reach consensus.

In general, as long as nobody explicitly opposes a proposal, it is recognised as having the support of the community. This is called lazy consensus—that is, those who have not stated their opinion explicitly have implicitly agreed to the implementation of the proposal.

Lazy consensus is a very important concept within the project. It is this process that allows a large group of people to efficiently reach consensus, as someone with no objections to a proposal need not spend time stating their position, and others need not spend time reading such mails.

For lazy consensus to be effective, it is necessary to allow at least two weeks before assuming that there are no objections to the proposal. This requirement ensures that everyone is given enough time to read, digest and respond to the proposal. This time period is chosen so as to be as inclusive as possible of all participants, regardless of their location and time commitments. For GitHub pull requests, if there are no reviews after two weeks, the submitter should send a reminder. Reviewers may ask patch submitters to delay submitting a patch when they have a desire to review a patch and need more time to do so. As discussed in the Contributing Section, each patch should have at least two approvals before it is committed.

#### Voting

Not all decisions can be made using lazy consensus. Issues such as those affecting the strategic direction or legal standing of the project must gain explicit approval in the form of a vote. Every member of the community is encouraged to express their opinions in all discussion and all votes. However, only project maintainers and/or PMC members (as defined above) have binding votes for the purposes of decision making. A separate document on the voting within a meritocratic governance model ([http://oss-watch.ac.uk/resources/meritocraticgovernancevoting](http://oss-watch.ac.uk/resources/meritocraticgovernancevoting)) describes in more detail how voting is conducted in projects following the practice established within the Apache Software Foundation.

This document is based on the example ([http://oss-watch.ac.uk/resources/meritocraticgovernancemodel](http://oss-watch.ac.uk/resources/meritocraticgovernancemodel)) by Ross Gardler and Gabriel Hanganu and is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License
