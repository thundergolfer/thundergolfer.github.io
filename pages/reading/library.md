---
layout: page
title: Library
permalink: /library/
tags: library
---

Books that I've read.

<ul>
{% for member in site.data.books %}
  <li>
    <a href="https://github.com/{{ member.github }}">
      {{ member.name }}
    </a>
  </li>
{% endfor %}
</ul>