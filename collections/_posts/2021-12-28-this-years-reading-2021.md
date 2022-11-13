---
layout:     post
title:      The Books I Read - 2021 
date:       2021-12-28
summary:    The 38 books I read in our <em>second</em> COVID-19 year (with some reviews). 
categories: reading learning
---

16 books in 2019: 📚📚📚📚📚

26 books in 2020: 📚📚📚📚📚📚📚📚📚

38 in 2021: 📚📚📚📚📚📚📚📚📚📚📚📚📚

An encouraging trend.

I've never read more books in a single year, and it feels good. I've continued to use reading to detach
my iPhone from my brain-stem, often carrying a book around and reading in short periods instead of fiddling
with my phone. I didn't play video games at all this year, replacing it with reading – keen to play a little next year though, if the new PS5 games are good.
After three years of consistent reading, I feel like I've made significant progress breaking out of ['the shallows'](https://en.wikipedia.org/wiki/The_Shallows_(book)).

To cap off the year of reading. Here's some simple stats/facts:

* Worst book: _100 Plus_
* 11,800+ pages, apparently 
* 11/38 from women authors (gf rightly nags me about this)
* 18/38 second hand books

I read a lot of famous and well regarded books this year, and they were so good I couldn't pick a favourite.
That said, these are a top 5 in terms of how much they durably affected my emotions and thinking.

* The Grapes of Wrath
* The Cathedral & the Bazaar: Musing on Linux and Open Source by an Accidental Revolutionary
* The Nickel Boys
* Debt: The First 5,000 years
* Dark Money: The Hidden History of the Billionaires Behind The Rise of the Radical Right 

---

As in [the 2020 post]({% post_url 2021-01-09-this-years-reading-2020 %}), clicking the book cover takes you to a short review.

**Below are the covers, titles, authors, and ratings of the <code>38</code> books I read this year. Click them to read my short review.**

<section style="display: flex; justify-content: space-between; flex-wrap: wrap">
{% for member in site.data.library %}
    {% if member.year_i_finished_reading == "2021" %}
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

I've set my 2022 reading goal [at 40 books](https://www.goodreads.com/user/show/88184044-jonathon-belotti).

<style>
.grow-me {
  border-radius: 4px;
  transition: all .2s ease-in-out;
}

.grow-me:hover {
  transform: scale(1.02);
}

</style>
