---
layout: page
title: About
parent: about
permalink: /about/
---
<!-- {% for item in site.data.documentation.docs %}
  {%for coll in item.collections%}
  {{coll.name}}
  {%for pg in site.coll.name%}
    {{pg.url}}<br>
    {{pg.path}}
  {%endfor%}


  {%endfor%}
{%endfor%} -->

{%for collection in site.collections%}
{{collection}}
{%endfor%}

About content goes here.

* A list item
* Another list item
