---
layout: toc
title: Contributing
permalink: /contributing/
---
## Table of Contents
{:.no_toc}
* TOC
{:toc}

---
If you’ve made changes to gem5 that might benefit others, we strongly encourage you to contribute those changes to the public gem5 repository. There are several reasons to do this:

*   Share your work with others, so that they can benefit from new functionality.
*   Support the scientific principle by enabling others to evaluate your suggestions without having to guess what you did.
*   Once your changes are part of the main repo, you no longer have to merge them back in every time you update your local repo. This can be a huge time saving!
*   Once your code is in the main repo, other people have to make their changes work with your code, and not the other way around.
*   Others may build on your contributions to make them even better, or extend them in ways you did not have time to do.
*   You will have the satisfaction of contributing back to the community.

The main method for contributing code to gem5 is via our code review website: [https://gem5-review.googlesource.com/](https://gem5-review.googlesource.com/). This documents describes the details of how to create code changes, upload your changes, have your changes reviewed, and finally push your changes to gem5\. More information can be found from the following sources:

*   [http://gem5.org/Submitting_Contributions](http://gem5.org/Submitting_Contributions)
*   [https://gerrit-review.googlesource.com/Documentation/index.html](https://gerrit-review.googlesource.com/Documentation/index.html)
*   [https://git-scm.com/book](https://git-scm.com/book)



# High-level flow
---
<pre>

    +-------------+
    | Make change |
    +------+------+
           |
           |
           v
    +------+------+
    | Post review |
    +------+------+
           |
           v
    +--------+---------+
    | Wait for reviews | <--------+
    +--------+---------+          |
           |                      |
           |                      |
           v                      |
      +----+----+   No     +------+------+
      |Reviewers+--------->+ Update code |
      |happy?   |          +------+------+
      +----+----+                 ^
           |                      |
           | Yes                  |
           v                      |
      +----+-----+   No           |
      |Maintainer+----------------+
      |happy?    |
      +----+-----+
           |
           | Yes
           v
    +------+------+
    | Submit code |
    +-------------+

</pre>

After creating your change to gem5, you can post a review on our Gerrit code-review site: [https://gem5-review.googlesource.com](https://gem5-review.googlesource.com). Before being able to submit your code to the mainline of gem5, the code is reviewed by others in the community. Additionally, the maintainer for that part of the code must sign off on it.



# Cloning the repo to contribute
---
If you plan on contributing, it is strongly encouraged for you to clone the repository directly from our gerrit instance at [https://gem5.googlesource.com/](https://gem5.googlesource.com/).

To clone the master gem5 repository:

     git clone https://gem5.googlesource.com/public/gem5

## Other gem5 repositories<span class="anchor" data-clipboard-text="http://new.gem5.org/contributing/cloning/#other-gem5-repositories"></span>

There are a few repositories other than the main gem5 development repository.

*   public/m5threads: The code for a pthreads implementation that works with gem5’s syscall emulation mode.

## Other gem5 branches<span class="anchor" data-clipboard-text="http://new.gem5.org/contributing/cloning/#other-gem5-branches"></span>

None right now.



# Making changes to gem5
---
It is strongly encouraged to use git branches when making changes to gem5. Additionally, keeping changes small and concise and only have a single logical change per commit.

Unlike our previous flow with Mercurial and patch queues, when using git, you will be committing changes to your local branch. By using separate branches in git, you will be able to pull in and merge changes from mainline and simply keep up with upstream changes.

## Requirements for change descriptions<span class="anchor" data-clipboard-text="http://new.gem5.org/contributing/changes/#requirements-for-change-descriptions"></span>

To help reviewers and future contributors more easily understand and track changes, we require all change descriptions be strictly formatted.

A canonical commit message consists of three parts:

*   A short summary line describing the change. This line starts with one or more keywords (found in the MAINTAINERS file) separated by commas followed by a colon and a description of the change. This line should be no more than 65 characters long since version control systems usually add a prefix that causes line-wrapping for longer lines.
*   (Optional, but highly recommended) A detailed description. This describes what you have done and why. If the change isn’t obvious, you might want to motivate why it is needed. Lines need to be wrapped to 75 characters or less.
*   Tags describing patch metadata. You are highly recommended to use tags to acknowledge reviewers for their work. Gerrit will automatically add most tags.

Tags are an optional mechanism to store additional metadata about a patch and acknowledge people who reported a bug or reviewed that patch. Tags are generally appended to the end of the commit message in the order they happen. We currently use the following tags:

*   Signed-off-by: Added by the author and the submitter (if different). This tag is a statement saying that you believe the patch to be correct and have the right to submit the patch according to the license in the affected files. Similarly, if you commit someone else’s patch, this tells the rest of the world that you have have the right to forward it to the main repository. If you need to make any changes at all to submit the change, these should be described within hard brackets just before your Signed-off-by tag. By adding this line, the contributor certifies the contribution is made under the terms of the Developer Certificate of Origin (DCO) [[https://developercertificate.org/](https://developercertificate.org/)].
*   Reviewed-by: Used to acknowledge patch reviewers. It’s generally considered good form to add these. Added automatically.
*   Reported-by: Used to acknowledge someone for finding and reporting a bug.
*   Reviewed-on: Link to the review request corresponding to this patch. Added automatically.
*   Change-Id: Used by Gerrit to track changes across rebases. Added automatically with a commit hook by git.
*   Tested-by: Used to acknowledge people who tested a patch. Sometimes added automatically by review systems that integrate with CI systems.

Other than the “Signed-off-by”, “Reported-by”, and “Tested-by” tags, you generally don’t need to add these manually as they are added automatically by Gerrit.

It is encouraged for the author of the patch and the submitter to add a Signed-off-by tag to the commit message. By adding this line, the contributor certifies the contribution is made under the terms of the Developer Certificate of Origin (DCO) [[https://developercertificate.org/](https://developercertificate.org/)].

It is imperative that you use your real name and your real email address in both tags and in the author field of the changeset.

For significant changes, authors are encouraged to add copyright information and their names at the beginning of the file. The main purpose of the author names on the file is to track who is most knowledgeable about the file (e.g., who has contributed a significant amount of code to the file).

Note: If you do not follow these guidelines, the gerrit review site will automatically reject your patch. If this happens, update your changeset descriptions to match the required style and resubmit. The following is a useful git command to update the most recent commit (HEAD).

     git commit --amend



# Posting a review
---
If you have not signed up for an account on the Gerrit review site ([https://gem5-review.googlesource.com](https://gem5-review.googlesource.com)), you first have to create an account.

## Setting up an account<span class="anchor" data-clipboard-text="http://new.gem5.org/contributing/posting-review/#setting-up-an-account"></span>

1.  Go to [https://gem5.googlesource.com/](https://gem5.googlesource.com/)
2.  Click “Sign In” in the upper right corner. Note: You will need a Google account to contribute.
3.  After signing in, click “Generate Password” and follow the instructions.

## Submitting a change<span class="anchor" data-clipboard-text="http://new.gem5.org/contributing/posting-review/#submitting-a-change"></span>

In gerrit, to submit a review request, you can simply push your git commits to a special named branch. For more information on git push see [https://git-scm.com/docs/git-push](https://git-scm.com/docs/git-push).

There are three ways to push your changes to gerrit.

## Push change to gerrit review<span class="anchor" data-clipboard-text="http://new.gem5.org/contributing/posting-review/#push-change-to-gerrit-review"></span>

    git push origin HEAD:refs/for/master

Assuming origin is [https://gem5.googlesource.com/public/gem5](https://gem5.googlesource.com/public/gem5) and you want to push the changeset at HEAD, this will create a new review request on top of the master branch. More generally,

    git push <gem5 gerrit instance> <changeset>:refs/for/<branch>

See [https://gerrit-review.googlesource.com/Documentation/user-upload.html](https://gerrit-review.googlesource.com/Documentation/user-upload.html) for more information.

## Pushing your first change<span class="anchor" data-clipboard-text="http://new.gem5.org/contributing/posting-review/#pushing-your-first-change"></span>

The first time you push a change you may get the following error:

    remote: ERROR: [fb1366b] missing Change-Id in commit message footer
    ...

Within the error message, there is a command line you should run. For every new clone of the git repo, you need to run the following command to automatically insert the change id in the the commit (all on one line).

    curl -Lo `git rev-parse --git-dir`/hooks/commit-msg \
   	https://gerrit-review.googlesource.com/tools/hooks/commit-msg ; \
    chmod +x `git rev-parse --git-dir`/hooks/commit-msg

If you receive the above error, simply run this command and then amend your changeset.

    git commit --amend

## Push change to gerrit as a draft<span class="anchor" data-clipboard-text="http://new.gem5.org/contributing/posting-review/#push-change-to-gerrit-as-a-draft"></span>

    git push origin HEAD:refs/drafts/master

## Push change bypassing gerrit<span class="anchor" data-clipboard-text="http://new.gem5.org/contributing/posting-review/#push-change-bypassing-gerrit"></span>

Only maintainers can bypass gerrit review. This should very rarely be used.

    git push origin HEAD:refs/heads/master

## Other gerrit push options<span class="anchor" data-clipboard-text="http://new.gem5.org/contributing/posting-review/#other-gerrit-push-options"></span>

There are a number of options you can specify when uploading your changes to gerrit (e.g., reviewers, labels). The gerrit documentation has more information. [https://gerrit-review.googlesource.com/Documentation/user-upload.html](https://gerrit-review.googlesource.com/Documentation/user-upload.html)



# Reviewing patches
---
Reviewing patches is done on our gerrit instance at [https://gem5-review.googlesource.com/](https://gem5-review.googlesource.com/).

After logging in with your Google account, you will be able to comment, review, and push your own patches as well as review others’ patches. All gem5 users are encouraged to review patches. The only requirement to review patches is to be polite and respectful of others.

There are multiple labels in Gerrit that can be applied to each review detailed below.

*   Code-review: This is used by any gem5 user to review patches. When reviewing a patch you can give it a score of -2 to +2 with the following semantics.
    *   -2: This blocks the patch. You believe that this patch should never be committed. This label should be very rarely used.
    *   -1: You would prefer this is not merged as is
    *   0: No score
    *   +1: This patch seems good, but you aren’t 100% confident that it should be pushed.
    *   +2: This is a good patch and should be pushed as is.
*   Maintainer: Currently only PMC members are maintainers. At least one maintainer must review your patch and give it a +1 before it can be merged.
*   Verified: This is automatically generated from the continuous integrated (CI) tests. Each patch must receive at least a +1 from the CI tests before the patch can be merged. The patch will receive a +1 if gem5 builds and runs, and it will receive a +2 if the stats match.
*   Style-Check: This is automatically generated and tests the patch against the gem5 code style ([http://www.gem5.org/Coding_Style](http://www.gem5.org/Coding_Style)). The patch must receive a +1 from the style checker to be pushed.

Note: Whenever the patch creator updates the patch all reviewers must re-review the patch. There is no longer a “Fix it, then Ship It” option.

Once you have received reviews for your patch, you will likely need to make changes. To do this, you should update the original git changeset. Then, you can simply push the changeset again to the same Gerrit branch to update the review request.

Please see [governance](/contributing/governance/) and [reviewing patches](/contributing/governance/#reviewing).

     git push origin HEAD:refs/for/master

Note: If you have posted a patch and don’t receive any reviews, you may need to prod the reviewers. You can do this by adding a reply to your changeset review on gerrit. It is expected that at least the maintainer will supply a review for your patch.



# Committing
---
Each patch must meet the following criteria to be merged:

*   At least one review with +2
*   At least one maintainer with +1
*   At least +1 from the CI tests (gem5 must build and run)
*   At least +1 from the style checker

Once a patch meets the above criteria, the submitter of the patch will be able to merge the patch by pressing the “Submit” button on Gerrit. When the patch is submitted, it is merged into the public gem5 branch.



# Governance
---
## Overview

gem5 is a meritocratic, consensus-based community project. Anyone with an interest in the project can join the community, contribute to the project design and participate in the decision-making process. Historically, gem5 development has been carried out both in industry and in academia. This document describes how that participation takes place and how to set about earning merit within the project community.

The document is broken into a number of sections. Philosophy describes the ideas behind the gem5 community. The Roadmap section points to the roadmap document for gem5’s development. Users and Responsibilities describes the classes of users that use gem5, the types of gem5 contributors, and their responsibilities. Support describes how the community supports users and the Contribution process describes how to contribute. Finally, the Decision Process describes how decisions are made and then we conclude.

## Philosophy

The goal of gem5 is to provide a tool to further the state of the art in computer architecture. gem5 can be used for (but is not limited to) computer-architecture research, advanced development, system-level performance analysis and design-space exploration, hardware-software co-design, and low-level software performance analysis. Another goal of gem5 is to be a common framework for computer architecture. A common framework in the academic community makes it easier for other researchers to share workloads as well as models and to compare and contrast with other architectural techniques.

The gem5 community strives to balance the needs of its three user types (academic researchers, industry researchers, and students, detailed below). For instance, gem5 strives to balance adding new features (important to researchers) and a stable code base (important for students). Specific user needs important to the community are enumerated below:

*   Effectively and efficiently emulate the behavior of modern processors in a way that balances simulation performance and accuracy
*   Serve as a malleable baseline infrastructure that can easily be adapted to emulate the desired behaviors
*   Provide a core set of APIs and features that remain relatively stable
*   Incorporate features that make it easy for companies and research groups to stay up to date with the tip and continue contributing to the project

Additionally, the gem5 community is committed to openness, transparency, and inclusiveness. Participants in the gem5 community of all backgrounds should feel welcome and encouraged to contribute.

## gem5 Roadmap

The roadmap for gem5 can be found on [Roadmap](Roadmap "wikilink") page. The roadmap document details the short and long term goals for the gem5 software. Users of all types are encouraged to contribute to this document and shape the future of gem5\. Users are especially encouraged to update the roadmap (and get consensus) before submitting large changes to gem5.

## Roles And Responsibilities

### Users<span class="anchor" data-clipboard-text="http://new.gem5.org/contributing/governance/#users"></span>

Users are community members who have a need for the project. They are the most important members of the community and without them the project would have no purpose. Anyone can be a user; there are no special requirements. There are currently three main categories of gem5 users: academic researchers, industry researchers, and students. Individuals may transition between categories, e.g., when a graduate student takes an industry internship, then returns to school; or when a student graduates and takes a job in industry. These three users are described below.

#### Academic Researchers<span class="anchor" data-clipboard-text="http://new.gem5.org/contributing/governance/#academic-researchers"></span>

This type of user primarily encompasses individuals that use gem5 in academic research. Examples include, but are not limited to, graduate students, research scientists, and post-graduates. This user often uses gem5 as a tool to discover and invent new computer architecture mechanisms. Academic Researchers often are first exposed to gem5 as Students (see below) and transition from Students to Academic Researchers over time.

Because of these users’ goals, they primarily add new features to gem5. It is important to the gem5 community to encourage these users to contribute their work to the mainline gem5 repository. By encouraging these users to commit their research contributions, gem5 will make it much easier for other researchers to compare and contrast with other architectural techniques (see Philosophy section).

#### Industry Researchers<span class="anchor" data-clipboard-text="http://new.gem5.org/contributing/governance/#industry-researchers"></span>

This type of user primarily encompasses individuals working for companies that use gem5\. These users are distinguished from academic researchers in two ways. First, industry researchers are often part of a larger team, rather than working individually on gem5\. Second, industry researchers often want to incorporate proprietary information into private branches of gem5\. Therefore, industry researchers tend to have rather sophisticated software infrastructures built around gem5\. For these users, the stability of gem5 features and baseline source code is important. Another key consideration is the fidelity of the models, and their ability to accurately reflect realistic implementations. To enable industry participation, it is critical to maintain licensing terms that do not restrict or burden the use of gem5 in conjunction with proprietary IP.

#### Students<span class="anchor" data-clipboard-text="http://new.gem5.org/contributing/governance/#students"></span>

This type of user primarily encompasses individuals that are using gem5 in a classroom setting. These users typically have some foundation in computer architecture, but they have little or no background using simulation tools. Additionally, these users may not use gem5 for an extended period of time, after finishing their short-term goals (e.g., a semester-long class).

The project asks its users to participate in the project and community as much as possible. User contributions enable the project team to ensure that they are satisfying the needs of those users. Common user contributions include (but are not limited to):

*   evangelising about the project (e.g., a link on a website and word-of-mouth awareness raising)
*   informing developers of strengths and weaknesses from a new user perspective
*   providing moral support (a ‘thank you’ goes a long way)
*   providing financial support (the software is open source, but its developers need to eat)

Users who continue to engage with the project and its community will often become more and more involved. Such users may find themselves becoming contributors, as described in the next section.

### Contributors<span class="anchor" data-clipboard-text="http://new.gem5.org/contributing/governance/#contributors"></span>

Contributors are community members who contribute in concrete ways to the project. Anyone can become a contributor, and contributions can take many forms. There are no specific skill requirements and no selection process.

> There is only one expectation of commitment to the project: contributors must be respectful to each other during the review process and work together to reach compromises. See the “Reviewing Patches” section for more on the process of contributing.

In addition to their actions as users, contributors may also find themselves doing one or more of the following:

*   answering questions on the mailing lists, particularly the “easy” questions from new users (existing users are often the best people to support new users), or those that relate to the particular contributor’s experiences
*   reporting bugs
*   identifying requirements
*   providing graphics and web design
*   programming
*   assisting with project infrastructure
*   writing documentation
*   fixing bugs
*   adding features
*   acting as an ambassador and helping to promote the project

Contributors engage with the project through the Review Board and mailing list, or by writing or editing documentation. They submit changes to the project source code via patches submitted to Review Board, which will be considered for inclusion in the project by existing committers (see next section). The developer mailing list is the most appropriate place to ask for help when making that first contribution.

As contributors gain experience and familiarity with the project, their profile within, and commitment to, the community will increase. At some stage, they may find themselves being nominated for committership.

### Committers<span class="anchor" data-clipboard-text="http://new.gem5.org/contributing/governance/#committers"></span>

Committers are community members who have shown that they are committed to the continued development of the project through ongoing engagement with the community. Committership allows contributors to more easily carry on with their project related activities by giving them direct access to the project’s resources. That is, they can make changes directly to project outputs, although they still have to submit code changes via Review Board. Additionally, committers are expected to have an ongoing record of contributions in terms of code, reviews, and/or discussion.

Committers have no more authority over the project than contributors. While committership indicates a valued member of the community who has demonstrated a healthy respect for the project’s aims and objectives, their work continues to be reviewed by the community. The key difference between a committer and a contributor is committers have the extra responsibility of pushing patches to the mainline. Additionally, committers are expected to contribute to discussions on the gem5-dev list and review patches.

Anyone can become a committer. The only expectation is that a committer has demonstrated an ability to participate in the project as a team player. Specifically, refer to the 2nd paragraph of the Contributors section.

Typically, a potential committer will need to show that they have an understanding of the project, its objectives and its strategy (see Philosophy section). They will also have provided valuable contributions to the project over a period of time.

New committers can be nominated by any existing committer. Once they have been nominated, there will be a vote by the project management committee (PMC; see below). Committer nomination and voting is one of the few activities that takes place on the project’s private management list. This is to allow PMC members to freely express their opinions about a nominee without causing embarrassment. Once the vote has been held, the nominee is notified of the result. The nominee is entitled to request an explanation of any ‘no’ votes against them, regardless of the outcome of the vote. This explanation will be provided by the PMC Chair (see below) and will be anonymous and constructive in nature.

Nominees may decline their appointment as a committer. However, this is unusual, as the project does not expect any specific time or resource commitment from its community members. The intention behind the role of committer is to allow people to contribute to the project more easily, not to tie them into the project in any formal way.

It is important to recognise that commitership is a privilege, not a right. That privilege must be earned and once earned it can be removed by the PMC (see next section) in extreme circumstances. However, under normal circumstances committership exists for as long as the committer wishes to continue engaging with the project.

A committer who shows an above-average level of contribution to the project, particularly with respect to its strategic direction and long-term health, may be nominated to become a member of the PMC. This role is described below.

### Project management committee<span class="anchor" data-clipboard-text="http://new.gem5.org/contributing/governance/#project-management-committee"></span>

The project management committee consists of those individuals identified as ‘project owners’ on the development site. The PMC has additional responsibilities over and above those of a committer. These responsibilities ensure the smooth running of the project. PMC members are expected to review code contributions, participate in strategic planning, approve changes to the governance model and manage how the software is distributed and licensed.

Some PMC members are responsible for specific components of the gem5 project. This includes gem5 source modules (e.g., classic caches, O3CPU model, etc.) and project assets (e.g., the website). A list of the current components and the responsible members can be found on [Module owners](Module_owners "wikilink").

Members of the PMC do not have significant authority over other members of the community, although it is the PMC that votes on new committers. It also makes decisions when community consensus cannot be reached. In addition, the PMC has access to the project’s private mailing list. This list is used for sensitive issues, such as votes for new committers and legal matters that cannot be discussed in public. It is never used for project management or planning.

Membership of the PMC is by invitation from the existing PMC members. A nomination will result in discussion and then a vote by the existing PMC members. PMC membership votes are subject to consensus approval of the current PMC members. Additions to the PMC require unanimous agreement of the PMC members. Removing someone from the PMC requires N-1 positive votes, where N is the number of PMC members not including the individual who is being voted out.

#### Members<span class="anchor" data-clipboard-text="http://new.gem5.org/contributing/governance/#members"></span>

*   Ali Saidi
*   Andreas Hansson
*   Andreas Sandberg
*   Anthony Gutierrez
*   Brad Beckmann
*   Jason Lowe-Power
*   Nathan Binkerg
*   Steve Reinhardt

### PMC Chair<span class="anchor" data-clipboard-text="http://new.gem5.org/contributing/governance/#pmc-chair"></span>

The PMC Chair is a single individual, voted for by the PMC members. Once someone has been appointed Chair, they remain in that role until they choose to retire, or the PMC casts a two-thirds majority vote to remove them.

The PMC Chair has no additional authority over other members of the PMC: the role is one of coordinator and facilitator. The Chair is also expected to ensure that all governance processes are adhered to, and has the casting vote when any project decision fails to reach consensus.

## Support

All participants in the community are encouraged to provide support for new users within the project management infrastructure. This support is provided as a way of growing the community. Those seeking support should recognise that all support activity within the project is voluntary and is therefore provided as and when time allows.

## Contribution Process

Anyone, capable of showing respect to others, can contribute to the project, regardless of their skills, as there are many ways to contribute. For instance, a contributor might be active on the project mailing list and issue tracker, or might supply patches. The various ways of contributing are described in more detail in a separate document [Submitting Contributions](/contributing/changes/).

The developer mailing list is the most appropriate place for a contributor to ask for help when making their first contribution. See the [Submitting Contributions](/contributing/changes/) page on the gem5 wiki for details of the gem5 contribution process. Each new contribution should be submitted as a patch to our Review Board site. Then, other gem5 developers will review your patch, possibly asking for minor changes. After the patch has received consensus (see Decision Making Process), the patch is ready to be committed to the gem5 tree. For committers, this is as simple as pushing the changeset. For contributors, a committer should push the changeset for you. If a committer does not push the changeset within a reasonable window (a couple of days), send a friendly reminder email to the gem5-dev list. Before a patch is committed to gem5, it must receive at least 2 “Ship its” from reviewboard. If there are no reviews on a patch, users should send follow up emails to the gem5-dev list asking for reviews.

### Reviewing Patches<a id="reviewing" class="highlight"></a><span class="anchor" data-clipboard-text="http://new.gem5.org/contributing/governance/#reviewing-patches-a-id-reviewing-a"></span>

An important part of the contribution process is providing feedback on patches that other developers submit. The purpose of reviewing patches is to weed out obvious bugs and to ensure that the code in gem5 is of sufficient quality.

All users are encouraged to review the contributions that are posted on Review Board. If you are an active gem5 user, it’s a good idea to keep your eye on the contributions that are posted there (typically by subscribing to the gem5-dev mailing list) so you can speak up when you see a contribution that could impact your use of gem5\. It is far more effective to contribute your opinion in a review before a patch gets committed than to complain after the patch is committed, you update your repository, and you find that your simulations no longer work.

We greatly value the efforts of reviewers to maintain gem5’s code quality and consistency. However, it is important that reviews balance the desire to maintain the quality of the code in gem5 with the need to be open to accepting contributions from a broader community. People will base their desire to contribute (or continue contributing) on how they and other contributors are received. With that in mind, here are some guidelines for reviewers:

1.  Remember that submitting a contribution is a generous act, and is very rarely a requirement for the person submitting it. It’s always a good idea to start a review with something like “thank you for submitting this contribution”. A thank-you is particularly important for new or occasional submitters.
2.  Overall, the attitude of a reviewer should be “how can we take this contribution and put it to good use”, not “what shortcomings in this work must the submitter address before the contribution can be considered worthy”.
3.  As the saying goes, “the perfect is the enemy of the good”. While we don’t want gem5 to deteriorate, we also don’t want to bypass useful functionality or improvements simply because they are not optimal. If the optimal solution is not likely to happen, then accepting a suboptimal solution may be preferable to having no solution. A suboptimal solution can always be replaced by the optimal solution later. Perhaps the suboptimal solution can be incrementally improved to reach that point.
4.  When asking a submitter for additional changes, consider the cost-benefit ratio of those changes. In particular, reviewers should not discount the costs of requested changes just because the cost to the reviewer is near zero. Asking for extensive changes, particularly from someone who is not a long-time gem5 developer, may be imposing a significant burden on someone who is just trying to be helpful by submitting their code. If you as a reviewer really feel that some extensive reworking of a patch is necessary, consider volunteering to make the changes yourself.
5.  Not everyone uses gem5 in the same way or has the same needs. It’s easy to reject a solution due to its flaws when it solves a problem you don’t have—so there’s no loss to you if we end up with no solution. That’s probably not an acceptable result for the person submitting the patch though. Another way to look at this point is as the flip side of the previous item: just as your cost-benefit analysis should not discount the costs to the submitter of making changes, just because the costs to you are low, it should also not discount the benefits to the submitter of accepting the submission, just because the benefits to you are low.
6.  Be independent and unbiased while commenting on review requests. Do not support a patch just because you or your organization will benefit from it or oppose it because you will need to do more work. Whether you are an individual or someone working with an organization, think about the patch from community’s perspective.
7.  Try to keep the arguments technical and the language simple. If you make some claim about a patch, substantiate it.

## Decision Making Process

Decisions about the future of the project are made through discussion with all members of the community, from the newest user to the most experienced PMC member. All non-sensitive project management discussion takes place on the gem5-dev mailing list. Occasionally, sensitive discussion occurs on a private list.

In order to ensure that the project is not bogged down by endless discussion and continual voting, the project operates a policy of lazy consensus. This allows the majority of decisions to be made without resorting to a formal vote.

### Lazy consensus<span class="anchor" data-clipboard-text="http://new.gem5.org/contributing/governance/#lazy-consensus"></span>

Decision making typically involves the following steps:

*   Proposal
*   Discussion
*   Vote (if consensus is not reached through discussion)
*   Decision

Any community member can make a proposal for consideration by the community. In order to initiate a discussion about a new idea, they should send an email to the gem5-dev list or submit a patch implementing the idea to Review Board. This will prompt a review and, if necessary, a discussion of the idea. The goal of this review and discussion is to gain approval for the contribution. Since most people in the project community have a shared vision, there is often little need for discussion in order to reach consensus.

In general, as long as nobody explicitly opposes a proposal, it is recognised as having the support of the community. This is called lazy consensus—that is, those who have not stated their opinion explicitly have implicitly agreed to the implementation of the proposal.

Lazy consensus is a very important concept within the project. It is this process that allows a large group of people to efficiently reach consensus, as someone with no objections to a proposal need not spend time stating their position, and others need not spend time reading such mails.

For lazy consensus to be effective, it is necessary to allow at least two weeks before assuming that there are no objections to the proposal. This requirement ensures that everyone is given enough time to read, digest and respond to the proposal. This time period is chosen so as to be as inclusive as possible of all participants, regardless of their location and time commitments. For Review Board requests, if there are no reviews after two weeks, the submitter should send a reminder email to the mailing list. Reviewers may ask patch submitters to delay submitting a patch when they have a desire to review a patch and need more time to do so. As discussed in the Contributing Section, each patch should have at least two “Ship its” before it is committed.

### Voting<span class="anchor" data-clipboard-text="http://new.gem5.org/contributing/governance/#voting"></span>

Not all decisions can be made using lazy consensus. Issues such as those affecting the strategic direction or legal standing of the project must gain explicit approval in the form of a vote. Every member of the community is encouraged to express their opinions in all discussion and all votes. However, only project committers and/or PMC members (as defined above) have binding votes for the purposes of decision making. A separate document on the voting within a meritocratic governance model ([http://oss-watch.ac.uk/resources/meritocraticgovernancevoting](http://oss-watch.ac.uk/resources/meritocraticgovernancevoting)) describes in more detail how voting is conducted in projects following the practice established within the Apache Software Foundation.

This document is based on the example ([http://oss-watch.ac.uk/resources/meritocraticgovernancemodel](http://oss-watch.ac.uk/resources/meritocraticgovernancemodel)) by Ross Gardler and Gabriel Hanganu and is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License
