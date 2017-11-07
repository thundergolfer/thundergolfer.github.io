---
layout:     post
title:      "We've got the newsfeeds, where are the information filters?"
date:       2017-11-05
summary:    Users are getting bombarded with online content and they need better filters
categories: information-filters newsfeeds recommender-systems
---

*A lot* of my time nowadays is captured by the newsfeeds on platforms like Reddit, Hackernews, and Twitter. I don't hate the fact that I'm a bit addicted to their streams, I mostly consume interesting and informative software-centric content, but I have find myself wanting more powerful information filtering tools. [Information Filtering]() (IF) as a technology seems have either fallen out of vogue or never gotten into it, but I'd argue that strong IF tooling is become more and more needed by users to ensure their personal happiness and effectiveness, and protect their time. Currently, the world's information geysers, the [great aggregators]() (Facebook, Google, RenRen, Toutiauo etc.) have misaligned incentives with their users. Despite billions in recommender engine research, today's production recommender systems are still inadequate. Further, the dominance of *implicit* signals in user profiling have seen the great aggregators serving the [Instant Gratification Monkey]() inside us, or the [Anger Golem]. In the absence of these problems, ie. in a system where the great aggregators are 'perfect information retrievers', personal IF tooling is not so much needed. But in then, it's a thing we should begin to consider more seriously.

### Come on in, stick around, we've got things to sell you

Facebook IPO'd with the mission to ["make the world more open and connected."](https://www.engadget.com/2012/02/01/zuckerberg-outlines-idealistic-facebook-mission-in-ipo-filing/), and whether not Facebook was ever heading towards that goal, its newsfeed, since it became home to news media and not just user status updates, has done nothing of the sort. #TODO: revise


### Can I just tell you what I want?

If you're a user of Netflix, Amazon, or Facebook, you know the powers and the weaknesses of an implicit feedback system for user profiling and recommendations. Compared with explicit, implicit has the large advantage of providing the user a super-smooth user experience. No need to tell the system what you're interested in, it's busy figuring that out for itself. The clear problem though, the problem that I think necessitates IFs, is many of the things that leak through in implicit feedback we would not at all claim as preferences.

### Good recommendation systems are apparently an AI-complete challenge

Beyond the struggles with the implicit vs. explicit self, for some reason recommender engine struggle immensely with [fairly straightforward things](https://twitter.com/kibblesmith/status/724817086309142529?lang=en). In an age where we're getting constantly bombarded with useless, irrelevant crap, even if that wanted to our recommender systems couldn't save us. They can't figure out what's what's, but you know, with our help I reckon they could do a lot better.

### What have we got to work with

Wanting to whack together an information filterer myself, I went after existing implementations and research. Information Filtering was a bit of thing, 30 years ago, before even Google and definitely before Facebook. Systems like ["The Information Lens"](http://delivery.acm.org.ezproxy.lib.rmit.edu.au/10.1145/30000/22340/p1-malone.pdf?ip=131.170.21.110&id=22340&acc=ACTIVE%20SERVICE&key=65D80644F295BC0D%2E124032AC6F25F239%2E4D4702B0C3E38B35%2E4D4702B0C3E38B35&CFID=826579750&CFTOKEN=62469482&__acm__=1510028698_c214de9c28b7c096c548454bc93d06a2), [INFOS](https://eric.ed.gov/?id=EJ552498), [SIFT](http://ilpubs.stanford.edu:8090/73/1/1994-7.pdf), NewsClip. Most were concerned with managing and improving the user experience with [UserNet](https://en.wikipedia.org/wiki/Usenet). God knows how they'd deal with today's content networks, but at least they were trying and at least they seemed to be *for the user*. 

A an interesting analogue to today's problems with today's platforms that 'push' content to the user, similar push-based system existed for research and business use-cases. Even with the use of information-filtering tooling, such systems were found to be
