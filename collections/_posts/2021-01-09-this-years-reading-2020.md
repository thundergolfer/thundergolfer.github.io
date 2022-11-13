---
layout:     post
title:      The Books I Read - 2020 
date:       2021-01-09
summary:    Every book I read in our COVID-19 year, with reviews. 
categories: reading learning
---

I did a post in 2019 reviewing all the books I read that year. That post was "a retrospective on my best year of reading in a decade." I read 16 books that year, and in 2020 I read 26 so I've kept up the habit 🙂.

I still use [Goodreads.com](http://goodreads.com) to track my reading, but recently Goodreads killed their public API so the [Command Line Interface (CLI) application that I built](https://github.com/thundergolfer/goodreads-sh) for Goodreads is now dead. Alas.

Instead of inlining my reviews of books in this post, I'll leverage the new functionality I added to this site to power my [library page]({{ site.url }}/library) to link to reviews of all the books I read this year.

**Below are the covers, titles, authors, and ratings of the <code>26</code> books I read this year. Click them to read my short review.**

<section style="display: flex; justify-content: space-between; flex-wrap: wrap">
{% for member in site.data.library %}
    {% if member.year_i_finished_reading == "2020" %}
        {% if member.review_path %}
        <a target="_blank" rel="noopener noreferrer" href="{{ site.baseurl }}/reviews/{{ member.review_path }}" style="color: #333333; flex: 1; width: 100%; min-width: 200px; padding-top: 5%;">
        {% else %}
        <a target="_blank" rel="noopener noreferrer" href="https://www.librarything.com/isbn/{{ member.isbn }}" style="color: #333333; flex: 1; width: 100%; min-width: 200px; padding-top: 5%;">
        {% endif %}
            <div style="width: 200px">
                <img class="grow-me" src="http://covers.openlibrary.org/b/ISBN/{{ member.isbn }}-L.jpg">
            </div>
            <div style="width: 200px">
                <h4>{{ member.title }}</h4>
                <h6>{{ member.author }}</h6>
                <h6>{{ member.rating }}</h6>
            </div>
        </a>
    {% endif %}
{% endfor %}
</section>

I've set my 2021 reading goal [at 30 books](https://www.goodreads.com/user/show/88184044-jonathon-belotti).

<style>
.grow-me {
  border-radius: 4px;
  transition: all .2s ease-in-out;
}

.grow-me:hover {
  transform: scale(1.02);
}

</style>
