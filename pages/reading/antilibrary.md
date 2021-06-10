---
layout: page
title: Anti-Library
permalink: /anti-library/
tags: antilibrary library
---

Books I haven't read, but like the idea of having read, and plan to read in the future.

<section style="display: flex; justify-content: space-between; flex-wrap: wrap">
{% for member in site.data.antilibrary %}
    <a target="_blank" rel="noopener noreferrer" href="https://www.librarything.com/isbn/{{ member.isbn }}" style="color: #333333; flex: 1; width: 100%; min-width: 250px; padding-top: 5%;">
        <div style="width: 250px">
            <img class="grow-me" src="http://covers.openlibrary.org/b/ISBN/{{ member.isbn }}-L.jpg">
        </div>
        <div style="width: 250px">
            <h4>{{ member.title }}</h4>
            <h6>{{ member.author }}</h6>
        </div>
    </a>
{% endfor %}
</section>

<style>
.grow-me {
  border-radius: 4px;
  transition: all .2s ease-in-out;
}

.grow-me:hover {
  transform: scale(1.02);
}

</style>
