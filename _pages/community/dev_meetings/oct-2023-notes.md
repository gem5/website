---
title: "Developer Meeting - Oct 2023"
permalink: dev_meetings/oct-2023-notes
---

#### Meeting Purpose:
- Monthly meetings for gem5 developers.
- Lower latency synchronization than mailing lists or GitHub.
- Recording for possible public sharing on YouTube or via a link.
- Transcripts will be used to create public notes.

#### Introductions:
- Host: Jason Lowe-Power, a professor at UC Davis and Chair of the Project Management Committee.
- Project Management Committee (PMC) oversees project administration.
- Maintainers have permission to merge changes.
- Developers are the focus of this meeting.
- Users are welcome too.

#### Community Additions:
- New additions: Ivana Mitrovic and Harshil Patel, paid programmers to support gem5.
- Melissa Jost left for new opportunities.

#### Status of the Project:
- Migrated to GitHub in June/July.
- Increased project velocity.
- One issue created per day.
- 30 open issues.
- Three or more pull requests per day.
- Can merge one to two pull requests per day.
- Weekly GitHub data scraping reveals good activity.
- Over 1,000 monthly clones of the project.

#### New GitHub Workflow:
- Goal: Migrate everything to GitHub for easier management.
- Suggestions for the community: 
    - Use real names in GitHub.
    - Use real emails, not GitHub anonymous ones.
    - Create pull requests on the develop branch.
- Things you need to do to get your PR committed:
    - Pass CI tests.
    - First-time contributors require Maintainer approval.
    - Tests run on infrastructure owned by UC Davis and University of Wisconsin.
    - Maintainers merge changes after test approval.
- Use the watch button in GitHub to receive notifications.
- Multiple repositories for gem5; watch them individually.

#### Behind the Scenes:
- Project boards track issues and pull requests.
- Projects are currently private but can be made public if there's interest.
- Purpose is to move changes from pull request to merge and issues from created to closed.

#### Open for Questions:
- No immediate questions or comments from the attendees.

#### GitHub Workflow:
- Significant improvement over the previous Gerrit workflow.
- Things working well:
    - Great reviews received quickly.
    - Maintainers are managing multiple merges daily, which is daunting but appreciated.
    - Testing infrastructure transitioned from using Google's internal infrastructure to GitHub Actions, running locally at Wisconsin and Davis.
- Some areas for improvement:
    - Discussion about merging vs. rebasing vs. squashing.
    - Current preference is to merge, unless it's a single commit, then use squashing.
    - Feedback on this approach is welcomed.
- Testing is always a challenge in projects.
- Testing is time-consuming for Maintainers but improving.
- Developers need to consider the costs of testing as more tests are added.
- There may be a need to invest in more testing machines as the project grows.

#### Challenges with Post-commit Tests:
- Post-commit tests are a pain point when they fail.
- Types of tests:
    - Pre-commit CI tests run before commits are merged.
    - Post-commit tests include daily tests (nightly), compiler tests (weekly), and weekly tests.
- Issues with fixing broken tests often fall on Maintainers.
- Challenges in quick action when post-commit tests fail.
- Potential for frustration when daily tests fail, and PRs are being pushed.
- Proposal to block PR merges until daily, weekly, and compiler tests pass.
- Maintainers can override the block if necessary.
- Community participation in fixing and reporting bugs is encouraged.

#### Difficult to Follow Updates:
- High project velocity makes it difficult to track changes in gem5.
- Changes are spread across multiple repositories.
- The need for solutions to these challenges.
- Open to ideas from the community to improve the process.

#### Discussion on Blocking PR Merges:
- Clarification on how blocking PR merges works when a test fails.
- Each PR will have a link to the specific failure.
- Consideration of how to handle complex issues that take time to resolve and might block other PRs.
- Suggestion to temporarily revert a PR if it cannot be fixed promptly.

#### Acknowledging Contributions:
- Nicholas Mosier for detailed bug reports and fixes, particularly for x86 KVM.
- Hoa Nguyen for fixing a floating-point bug that persisted for months.

#### Development Updates - ARM:
- Andreas and Giacomo discuss ARM development updates.
- Support for ARM v8.x extensions, including TLB range invalidation and new extended registers.
- Discussion on future developments, including David Schall's FDIP front end and performance regressions.
- [GitHub Discussion](https://github.com/orgs/gem5/discussions/446)
- Mention of possible prefetch support for CHI.

#### Integration with Capstone Disassembler:
- [Capstone Disassembler](http://www.capstone-engine.org/)
- Mention of integrating the Capstone disassembler to improve instruction disassembly.
- Discussion on ensuring accuracy in disassembling instructions.
- Potential to improve architectural instruction tracing and resolve discrepancies.

#### Development Updates - AMD GPU:
- Improvements in AMD GPU support, including better full-system mode.
- Ongoing work to get a Standard Library port for AMD GPUs.
- Testing for AMD GPUs in the to-do list.

#### Development Updates - Full System and AVX Support:
- Matthew Poremba provides updates on full system support.
- Mentions five bug fixes addressing hangs and page faults.
- Enabling AVX in the configuration for running rocBLAS and TensorFlow.
- Enabling PCI atomics for supporting host-call kernels.
- Implementation of scratch and timestamp instructions for HIP events.
- Discusses internal testing with a focus on ML frameworks for the next release.

#### Discussion on Testing and Docker Images:
- The testing challenges for the GPU and the limitations of the current setup.
- Suggestions to integrate GPU full system tests with existing testing structures.
- Discussion on the difficulties of ARM GPU testing and the need for specific workloads.
- Integration of Capstone disassembler to enhance instruction disassembly.
- Plans to separate and improve different testing environments for GPU testing.

#### Discussion on RVV Support (RISC-V Vector Extensions):
- Barcelona Supercomputing Center's work on RISC-V vector extensions (RVV).
- Confirmation that RVV support works with all timing CPUs.
- Discussions on outstanding atomic patches and resource support.

#### Discussion on gem5's Build System Changes:
- Introduction of changes to gem5's build system using Kconfig and SCons.
- Awareness of these changes, seeking comments, and the expected merge timeline.

#### Discussion on Prefetching Support for gem5 (GPU):
- Bhargav and David discuss their prefetching implementations.
- Focus on modifying gem5 to enhance GPU performance.
- Explanations of the current state and patch interdependencies.
- Mention the need for testing and ideal benchmarks, emphasizing performance gains.

#### Branch Predictor Performance Tests:
- Discussions on the importance of running benchmarks that require prefetching.
- Mention of the need for workloads larger than L2 cache for effective testing.
- The need for benchmarks with high branch prediction rates for validation.

#### Discussion on Removing Change IDs:  
- [GitHub Discussion](https://github.com/orgs/gem5/discussions/324)
- Jason proposes removing the requirement for change IDs in pull requests.
- Bobby suggests that this change simplifies the contribution process for new contributors.
- Andreas highlights the trade-off between making things easier for the minority who need change IDs versus making things harder for the general community.
- Giacomo asks for clarification on the motivation for removing change IDs.
- A discussion ensues about possible alternatives for tracking logical changes in contributions.
- Jason suggests that more discussion is needed and encourages those who need change IDs to provide feedback in the discussion on GitHub.

#### Upcoming Topics for Discussion:
- Jason announces that in future meetings, there will be discussions rather than broadcasts.
- Upcoming topics include development and contribution to the Standard Library, improvements to Gem5 resources with suites and multi-processing, and planning the gem5 23.1 release.
- Jason invites participants to reach out with any topics they want to discuss in future meetings.

#### Feedback and Closing Remarks:
- Jason asks for feedback on the usefulness of the meeting and how it can be improved.
- Bobby suggests leaving feedback on the discussions page on GitHub.
- Jason expresses gratitude for everyone who attended and promises more time for discussions in future meetings.