---
layout: about
permalink: /about/
title: A little bit about me.
tags: about
---

### Origins

I was born and raised in the southeast suburbs of Victoria, Australia — a place almost perfecting the ['surbubia as giant nursery'](http://www.paulgraham.com/nerds.html) vision of urban development.

<div class="hero-images-container">
  <div class="hero-images">
    <div>
      <img src="/images/about/brighton-beach-melbourne.png" alt="Brighton Beach, Melbourne" style="border-radius: 0.4em;">
      <div style="color: #777; font-size: 0.96em; padding-top: 0.4em; text-align: center;">
        Brighton Beach, Melbourne &mdash; famous for its colorful beach boxes.
      </div>
    </div>
    <div>
      <img src="/images/about/bentleigh-birds-eye-view.jpg" alt="Bentleigh Bird's Eye View" style="border-radius: 0.4em;">
      <div style="color: #777; font-size: 0.96em; padding-top: 0.4em; text-align: center;">
        A bird’s-eye view of Bentleigh, the suburb where I grew up in Victoria, Australia.
      </div>
    </div>
  </div>
</div>

Until I found programming I could usually be found at Brighton Beach, our local spot. You can buy one of those 'beach boxes' pictured for around
$300k. The most expensive deck chair and jet ski storage you can find. Fortunately, broke uni kids can use their decks for free.

<style>
.hero-images-container {
  width: 100vw;
  position: relative;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
  margin-bottom: 2em;
}

.hero-images {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.hero-images img {
  width: 100%;
  height: 400px;
  object-fit: cover;
}

@media screen and (max-width: 768px) {
  .hero-images {
    grid-template-columns: 1fr;
  }

  .hero-images img {
    height: 300px;
  }
}

.modal-images-container {
  width: 100vw;
  position: relative;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
  margin-bottom: 2em;
}

.modal-images {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.modal-images img {
  width: 100%;
  height: 400px;
  object-fit: cover;
}

.modal-captions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  max-width: 1200px;
  margin: 0.5rem auto 0;
  padding: 0 1rem;
}

.modal-captions figcaption {
  text-align: center;
}

@media screen and (max-width: 768px) {
  .modal-images {
    grid-template-columns: 1fr;
  }

  .modal-images img {
    height: 300px;
  }

  .modal-captions {
    grid-template-columns: 1fr;
  }
}

.highlight-face {
  position: relative;
}

.highlight-face img {
  position: relative;
}

.highlight-face::after {
  content: '';
  position: absolute;
  top: 40%;
  left: 50%;
  width: 30px;
  height: 30px;
  border: 3px solid rgba(255, 87, 34, 0.9);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
  box-shadow: 0 0 10px rgba(255, 87, 34, 0.5);
}

.highlight-face:hover::after {
  opacity: 1;
}
</style>





### Day-by-day

Currently, I help build [**modal.com**](https://modal.com), AI infrastructure that developers love.
I joined in August 2022 as lucky #7. At the time the company was pre-PMF and pre-revenue, but full of 
shockingly capable engineers with whom I still enthusiastically struggle to keep up with. 

In August 2025 Modal announced its $1.1B Series B, and by year end we'd hit 70+ people and 9-figure ARR.

<span style="color: #777; cursor: pointer; text-decoration: underline;" onclick="document.getElementById('dashboard').scrollIntoView({ behavior: 'smooth' });">
  (Scroll down to see some personal dashboard stats powered by Modal!)
</span>

<div class="modal-images-container">
  <div class="modal-images">
    <div class="highlight-face">
      <img src="/images/portugal-offsite.jpeg" alt="Portugal Offsite" style="border-radius: 0.4em;">
    </div>
    <img src="/images/about/modal-office-view.jpeg" alt="Modal Office View" style="border-radius: 0.4em;">
  </div>
  <div class="modal-captions">
    <figcaption style="color: #777;">The team is bigger than this now, but in that photo my eyes are closed!</figcaption>
    <figcaption style="color: #777;">This office view will never get old.</figcaption>
  </div>
</div>



I have been at Modal for almost 3.5 years now, and these days do mostly engineering management. Necessarily, my coding pace has slipped a bit, from #2 committer
to around #5. Alas.

### Where

<figure style="margin: 0; margin-bottom: 1em;">
  <img src="/images/about/fort-greene.avif" alt="Fort Greene Park, Brooklyn" style="border-radius: 0.4em;">
</figure>

Today, I live in NYC. When I'm not working, you can find me walking a new part of the five boroughs, or stopped in a park to read. There's a lot to love in this vast, grubby city, and I hope to see all of it by foot.


More specifically, I live in East Village. It's great, but my paradise is still Fort Greene and I'll move back there in the midyear.
### Past

I spent 3.5 years at [Canva](https://www.canva.com/), joining when it had almost 300 engineers and leaving when it had about 1,800. I joined as a graduate, hobbling around with a broken leg, and ended up as team lead
of ML Platform. The whole way through I grew under the mentorship of [Greg Roodt](https://www.linkedin.com/in/groodt/).

When not doing Data or ML Platform stuff, I spent quite a bit of time working with the [Bazel](https://bazel.build/) build system, and helped maintain the [Python rules](https://github.com/bazelbuild/rules_python) for Bazel. It's the future, get on it.

Previous to Canva I worked at [Zendesk](https://www.zendesk.com/) on their [Answer Bot](https://www.zendesk.com/answer-bot/) machine learning product, and at [Atlassian](https://www.atlassian.com) as an application developer intern in their reliability/monitoring team.

### Life

2025 was capped off with a proposal to Keeli, my girlfriend of 8 years. We're pretty excited about what's next. 

A litore ad astra.

<figure style="margin: 0; margin-bottom: 1em;">
  <img src="/images/about/proposal.jpg" alt="Proposal"
       style="border-radius: 0.4em; object-fit: cover; object-position: bottom; width: 100%; height: 600px;">
</figure>

<div id="stats" class="hidden">

<h3 id="dashboard"><code>#dashboard</code></h3>

<h2>Just finished.</h2>

<p>Curious what I'm reading? Here's my most recent reads, updating daily. And my <a href="https://www.goodreads.com/user/show/88184044-jonathon-belotti)" target="_blank" rel="noopener noreferrer">Goodreads profile</a> has more history.</p>

<div id="recent-finished-books"></div>

<h2>Top tracks.</h2>

<p>Curious what I'm currently listening to? Here's my top tracks on Spotify, updating daily.</p>

<ol id="top-spotify-tracks"></ol>

</div>

<script>
/**
 * @param {String} HTML representing a single element
 * @return {Element}
 */
function htmlToElement(html) {
    var template = document.createElement('template');
    /* Never return a text node of whitespace as the result */
    html = html.trim();
    template.innerHTML = html;
    return template.content.firstChild;
}

function populateDashboardHTML(data) {
    const topSpotifyTracksList = document.querySelector('#top-spotify-tracks');
    data.spotify.forEach(track => {
        topSpotifyTracksList.appendChild(htmlToElement(`
            <li>
                <a target="_blank" rel="noopener noreferrer" href="${track.link}"><strong>${track.name}</strong></a>
                <p>${track.artist}</p>
            </li>
        `));
    });

    const recentFinishedBooks = document.querySelector('#recent-finished-books');
    data.goodreads.slice(0, 3).forEach(book => {
        recentFinishedBooks.appendChild(htmlToElement(`
            <a target="_blank" rel="noopener noreferrer" class="book-item" target="_blank" rel="noopener noreferrer" href="${book.link}">
            <div class="cover-container">
                <img class="grow-me" src="${book.cover_image_link}">
            </div>
            <div class="book-info">
                <h4>${book.title}</h4>
                <p>${book.authors[0]}</p>
            </div>
            </a>
        `));
    });
}

fetch('https://thundergolfer--thundergolferdotcom-about-page-web.modal.run')
  .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return response.json();
  })
  .then((data) => {
    populateDashboardHTML(data);
    /* Reveal the now populated stats section. */
    document.getElementById("stats").classList.remove("hidden");
  });

</script>

<style>
#stats {
  background-color: #e8e4d9;
  border-radius: 1rem;
  padding: 1.5em;
  margin-top: 2.5em;
}

#dashboard {
  margin: 0rem;
}

#dashboard code {
  background-color: #e8e4d9;
}

#recent-finished-books {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: center;
}

#recent-finished-books a {
    color: #111;
}

.book-item {
    margin-left: 0.4em;
    margin-right: 0.4em;
}

.book-item div {
    width: 200px;
}

.book-info h4 {
    color: #222;
}

.book-info p {
    color: #555;
}

.grow-me {
  border-radius: 4px;
  transition: all .2s ease-in-out;
}

.grow-me:hover {
  transform: scale(1.02);
}

#top-spotify-tracks {
    padding-left: 1em;
}

#top-spotify-tracks li {
    color: #888;
    border-bottom: 1px solid #ededed;
    margin-top: 1rem;
}

#top-spotify-tracks a {
    color: #111;
}

#top-spotify-tracks a:hover {
    color: #1DB954; /* Spotify green */
}

#top-spotify-tracks p {
    color: #555;
}

.hidden {
    display: none;
}

@media screen and (max-width: 900px) {


  #recent-finished-books {
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .book-item div {
    width: 400px;
  }

  .book-item {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .cover-container, .book-info {
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 80%;
  }

  #top-spotify-tracks {
    padding-left: 1.2em;
  }
}
</style>
