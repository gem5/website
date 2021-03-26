# gem5 website

The website for gem5 is written in Jekyll markdown. It serves as the primarily
source of information for those interested in the gem5 project. In the spirit
of gem5's community-led, open governance model, anyone who wishes may make
contributions and improvements to the website. This README outlines the basic
procedure to do so, as well as notes the directory structure and general
guidelines.

## Development

You may clone the repository, and run a local instance of the website
using:

```
git clone https://gem5.googlesource.com/public/gem5-website
cd gem5-website
bundle
jekyll serve --config _config.yml,_config_dev.yml
```

The jekyll server may also be run using:

```
bundle exec jekyll serve --config _config.yml,_config_dev.yml
```

Changes may be made and committed using:

```
git add <changed files>
git commit
```

The commit message must adhere to our style. The first line of the commit
is the "header". **The header line must not exceed 65 characters and adequately
describe the change**. To be consistent with commits made to the gem5 gerrit,
the header should start with a `website` tag followed by a colon.

After this, a more detailed description of the commit can be included. This is
inserted below the header, separated by an empty line. Including a description
is optional but strongly recommended for complex changes. The description may
span multiple lines, and multiple paragraphs. **No line in the description
may exceed 72 characters**. We also recommend adding reference to any relevant
Jira issue (from the gem5 Jira: <https://gem5.atlassian.net>) so the context
of a change can be more easily understood.

Below is an example of how a gem5 website commit message should be formatted:

```
website: This is an example header

This is a more detailed description of the commit. This can be as long as
is necessary to adequately describe the change.

A description may spawn multiple paragraphs if desired.

Jira: https://gem5.atlassian.net/browse/GEM5-186
```

## Submitting a contribution

We utilize Gerrit to review changes made to the website. Once changes are
committed to a local repository they may be submitted for review by executing:

```
git push origin HEAD:refs/for/stable
```

At this stage you may receive an error if you're not registered to contribute
to our Gerrit. To resolve this issue:

1. Create an account at https://gem5-review.googlesource.com
2. Go to `User Settings`
3. Select `Obtain password` (under `HTTP Credentials`).
4. A new tab shall open, explaining how to authenticate your machine to make
contributions to Gerrit. Follow these instructions and try pushing again.

Gerrit will amend your commit message with a `Change-ID`. Any commit pushed to
Gerrit with this Change-ID is assumed to be part of this change.

### Code Review

Once a change has been submitted to Gerrit, you may view the change at
<https://gem5-review.googlesource.com> under `Your` -> `Changes` ->
`Outgoing reviews`).

Through the Gerrit prowl we strongly advise you add reviewers to your change.
Gerrit will automatically notify those you assign. We recommend you add both
**Bobby R. Bruce <bbruce@ucdavis.edu>** and **Jason Lowe-Power
<jlowepower@ucdavis.edu>** as reviewers.

Reviewers will review the change. For non-trivial edits, it is not unusual
for a change to receive feedback from reviewers that they want incorporated
before flagging as acceptable for merging into the gem5 website repository.
**All communications between reviewers and contributors should be done in a
polite manner. Rude and/or dismissive remarks will not be tolerated**.

Once your change has been accepted by reviewers you will be able to click
`Submit` within your changes Gerrit page. This focally merges the change
into the gem5 website repository. The website will be automatically updated
with your changes within 30 minutes.

## Directory Structure

#### _data

Yaml files, for easily editing navigation.

#### _includes

Page <head> section and main navigation bar are here.

#### _layouts

Different layout templates used on the site.
* default: base layout
* page: any regular page
* toc: a page that requires table of contents
* post: blog post page
* documentation: documentation page

#### _pages

All pages (other than the index.html home page) should be placed in this folder. There is a subfolder /documentation where pages meant for the documentation part of the site can be kept. This is purely for organization and ease of finding things. Reorganizing the _pages folder should not affect the site.

#### _posts

Holds blog posts.

#### _sass

All custom css is kept in _layout.scss.

#### assets

Images and javascript files.

#### blog

Holds index.html of blog page.


## Navigation

To edit the navigation bar:
Go to `_includes/header.html`
Navigation element without submenu:

```
<li class="nav-item {% if page.title == "Home" %}active{% endif %}">
  <a class="nav-link" href="{{ "/" | prepend: site.baseurl }}">Home</a>
</li>
```

Replace `Home` in `{% if page.title == "Home" %}` to your page's title.
Replace `/` in `href="{{ "/" | prepend: site.baseurl }}"` to the page's permalink.
Replace `Home` in `>Home</a>` with what you want the navbar to show.


Navigation element with submenu:

```
<li class="nav-item dropdown {% if page.parent == "about" %}active{% endif %}">
  <a class="nav-link dropdown-toggle" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
    About
  </a>
  <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
    <a class="dropdown-item" href="{{ "/about" | prepend: site.baseurl }}">About</a>
    <a class="dropdown-item" href="{{ "/publications" | prepend: site.baseurl }}">Publications</a>
    <a class="dropdown-item" href="{{ "/governance" | prepend: site.baseurl }}">Governance</a>
  </div>
</li>
```

Replace `about` in `{% if page.parent == "about" %}` with a word that will represent the parent of all pages in the submenu. Make sure the frontmatter in those pages includes parent: [your_parent_identifier].
Replace the permalink and title in all the `<a></a>` submenu items.



## Documentation

#### Edit Documentation Navigation

##### Structure:

Parent Topic:
- subtopic
- subtopic
- ...

Parent Topic:
- subtopic
- ...

To edit the documentation navigation, simply edit the documentation.yml file in the _data folder. `docs` lists the parent topics, and within it `subitems` lists its subtopics. This is an example of how it should be formatted:

```
title: Documentation

docs:
  - title: Getting Started     # Parent Topic
    id: gettingstarted     # see below
    url: /gettingstarted     # see below
    subitems:
      - page: Introduction     # Name that will appear in navigation
        url: /introduction     # url
      - page: Dependencies
        url: /dependencies
  - title: Debugging     # Parent Topic
    id: debugging     # see below
    subitems:
      - page: Piece 1
        url: /piece1
      - page: Piece 2
        url: /piece2

```

Notes:
`id` is an identifier that links subtopics to its parent. It is required and must not contain any spaces. The subtopic pages must include in the frontmatter `parent: id` with `id` being the parent's id.

`url` is optional for parent topics, if a parent topic has its own a page. If no url is provided, it will automatically link to the first subtopic.

#### Add New Page

To add a new documentation page, first add frontmatter at the top of either the markdown or html file to be added.

```
---
layout: documentation     // specify page layout
title: Getting Started     // title of the page
parent: gettingstarted     // see below
permalink: /gettingstarted/     // url
---
```

Notes:

`parent` should be the exact same as the id of its parent topic that is assigned to it in _data/documentation.yml file. (If the page is the parent topic, `parent` is the same as the id assigned to it in _data/documentation.yml file.)

Place the file in _pages/documentation. Make sure to add the page to the documentation navigation, explained by the section above.

#### Indicating outdated information

To flag information in a page as valid, use an outdated notice in the .md file of that page:

```
{: .outdated-notice}
This page is outdated!
```

This will be replaced by a warning element containing the text "**Note: This page is outdated.**", followed by the content succeeding the notice - in this case, "This page is outdated!". In this way, you can add additional information explaining why or how the page is outdated, and general tips on what to do to mitigate this issue.

Notes:

Make sure that the text following `{: .outdated-notice}` is not used as a title, heading, or any other important Markdown element, as it will be incorporated into the outdated notice and break formatting.

## Blog

Add blog page to _posts folder.
Page must be named in this format:
`yyyy-mm-dd-name-of-file.md`
At the top of the page add:

```
---
layout: post     // specify page layout
title: How to Debug
author: John
date: yyyy-mm-dd
---
```
