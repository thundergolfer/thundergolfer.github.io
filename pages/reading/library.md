---
layout: page
title: Library
permalink: /library/
tags: library read_list
update_date: 2025-01-05
---

<div class="post-header mb2">
  <span class="post-meta">Last updated: {{ page.update_date | date: site.date_format }}</span><br />
</div>

Selected books that I've read for enjoyment or learning. I also wrote [a post]({{ site.baseurl }}/read) about how I read.

To see things I haven't yet read browse the [/anti-library]({{ site.baseurl }}/anti-library). All my (crappy) book reviews are at [/reviews]({{ site.baseurl }}/reviews).

<div style="text-align: right;">
    <button id="sort-rating" style="outline: 1px solid; margin-right: 10px; border-radius: 5px; color: gray;" onclick="sortLibrary('rating')">Sort by <strong>Rating</strong></button>
    <button id="sort-date" style="outline: 1px solid; margin-left: 10px; border-radius: 5px; color: black;" onclick="sortLibrary('default')">Sort by <strong>Date</strong></button>
</div>

<section id="library-section" style="display: flex; justify-content: center; flex-wrap: wrap; gap: 40px;">
    {% assign sorted_library = site.data.library %}
    {% for member in sorted_library limit:120 %}
        {% if member.review_path %}
            <a target="_blank" rel="noopener noreferrer" href="{{ site.baseurl }}/reviews/{{ member.review_path }}" style="color: #333333; flex: 1; max-width: 200px; padding-top: 5%;" data-original-order="{{ forloop.index }}">
        {% else %}
            <a target="_blank" rel="noopener noreferrer" href="https://openlibrary.org/isbn/{{ member.isbn }}" style="color: #333333; flex: 1; max-width: 200px; padding-top: 5%;" data-original-order="{{ forloop.index }}">
        {% endif %}
            <div style="width: 200px">
                <img class="grow-me" src="/images/book-covers/{{ member.isbn }}.jpg" onerror="this.onerror=null; this.src='http://covers.openlibrary.org/b/ISBN/{{ member.isbn }}-L.jpg'">
            </div>
            <div style="width: 200px">
                <h4>{{ member.title }}</h4>
                <h6>{{ member.author }}</h6>
                <h6 id="rating">{{ member.rating }}</h6>
            </div>
        </a>
    {% endfor %}
</section>

<script>
    function sortLibrary(criteria) {
        const section = document.getElementById('library-section');
        let items = Array.from(section.children);
        
        if (criteria === 'rating') {
            items.sort((a, b) => {
                let ratingA = (a.querySelector('#rating').innerText.match(/★/g) || []).length;
                let ratingB = (b.querySelector('#rating').innerText.match(/★/g) || []).length;
                if (ratingB === ratingA) {
                    let orderA = parseInt(a.getAttribute('data-original-order'));
                    let orderB = parseInt(b.getAttribute('data-original-order'));
                    return orderA - orderB;
                }
                return ratingB - ratingA;
            });
            document.getElementById('sort-rating').style.color = 'black';
            document.getElementById('sort-date').style.color = 'gray';
        } else {
            items.sort((a, b) => {
                let orderA = parseInt(a.getAttribute('data-original-order'));
                let orderB = parseInt(b.getAttribute('data-original-order'));
                return orderA - orderB;
            });
            document.getElementById('sort-rating').style.color = 'gray';
            document.getElementById('sort-date').style.color = 'black';
        }

        items.forEach(item => section.appendChild(item));
        console.log(section);
        console.log('Number of items:', items.length);
    }
</script>

<script>
    const placeholderCoverImg = "/images/placeholder-book-cover.png";
    Promise.all(Array.from(document.images).filter(img => !img.complete).map(img => new Promise(resolve => { img.onload = img.onerror = resolve; }))).then(() => {
        let imgs = Array.from(document.images);
        for (let i = 0; i < imgs.length; i++) {
            let current = imgs[i];
            if (current.width < 20) {
                /* Image failed to be found. Replace with placeholder. */
                current.src = placeholderCoverImg;
            }
        }
    });
</script>

<style>
.grow-me {
  border-radius: 4px;
  transition: all .2s ease-in-out;
}

.grow-me:hover {
  transform: scale(1.02);
}

</style>
