---
layout:     post
title:      ddiaflashcards.com - Flashcards for Designing Data Intensive Applications 
date:       2022-04-13
summary:    Releasing a study deck for a much loved software textbook. 
categories: system-design flashcards
---

![product hero shot](/images/ddiaflashcards_mvp/hero.png)

I am among the many engineers who love the *Designing Data Intensive Applications* textbook. 
I’ve read it cover to cover a couple of times, and keep it open on my desk for surprisingly frequent reference. 
At the end of 2021 I started creating flashcards with questions drawn directly from the book, and other questions 
that I found supplemented my understanding of the book.

Inspired by [https://machinelearningflashcards.com/](https://machinelearningflashcards.com/) I have released 
these flashcards as a cheap digital product, available at [**ddiaflashcards.com**](http://ddiaflashcards.com).

### The MVP website

![screenshot of website](/images/ddiaflashcards_mvp/website.png)

As far as side projects go, this one is extremely simple. It's a combo of HTML, Stripe for payments, and Zapier (no-code platform) 
for order fulfilment. 

Order fulfilment is pretty rudimentary right now. A small payment gives you access, via email attachment, to the 
latest version of the flashcards at time of purchase. I’d really like to offer permanent access to the latest version of 
the flashcards, so in future I’ll find a free or very cheap way to do authorized download access for purchasers. 
Chris Albon’s [machinelearningflashcards.com](http://machinelearningflashcards.com) uses [Podia](https://www.podia.com/pricing) which I found works well, but at $30+ a month it’s far too expensive for a product I expect will generate less than $10 monthly. [Gumroad.com](http://Gumroad.com) looks promising, with no monthly fee.

### The deck

Contained in this DDIA deck is ~175 cards, with a mix of cards drawn directly from the textbook and cards I created when 
studying system design and distributed systems generally.

Below is an example flashcard question drawn from Chapter 8.

> **Q:** What are *fencing tokens*, used in the context of distributed systems?
> 

As said above, some flashcards are not drawn the textbook, and test general system design knowledge.
The following are a couple of examples.

> **Q:** At two nines of availability, 99%, how much downtime is there per year?
>
> **Q:** Approx how much does 1GB of blob storage cost per month, in the cloud? (eg. S3, GCS)

Overall I’ve found the deck to be helpful in both my day to day backend engineering work and in interviews. I hope you’ll find it similarly helpful.
