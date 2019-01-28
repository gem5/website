# gem5 website redesign
Website for gem5 documentation, written in Jekyll.

## Development
Clone repository, bundle Gemfile
```
git clone https://github.com/gem5/new-website.git
cd new-website
bundle
```
Run Jekyll server
```
jekyll serve --config _config.yml,_config_dev.yml
or
bundle exec jekyll serve --config _config.yml,_config_dev.yml
```
## Directory
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
All pages (other than the index.html home page) should be placed in this folder. There is a subfolder /documentation where pages meant for documentation part of the site can be kept. This is purely for organization and ease of finding things. Reorganizing the _pages folder should not affect the site.

#### _posts
Holds blog posts.

#### _sass
All custom css is kept in _layout.scss.

#### assets
Images and javascript files.

#### blog
Holds index.html of blog page.

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

To edit the documentation navigation, simply edit the documentaiton.yml file in the _data folder. `docs` lists the parent topics, and within it `subitems` lists its subtopics. This is an example of how it should be formatted:
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
`id` is an identifier that links subtopics to its parent. It is required and must not contain any spaces. The subtopic pages must inclue in the frontmatter `parent: id` with `id` being the parent's id.

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
