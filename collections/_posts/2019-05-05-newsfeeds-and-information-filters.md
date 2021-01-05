---
layout:     post
title:      Newsfeeds and Information Filters
date:       2019-05-05
summary:    We need information-filtering tools and we need them yesterday.
categories: newsfeeds information-retrieval information-filtering
---

*A lot* of my time nowadays is captured by the newsfeeds on platforms like [Reddit](https://www.reddit.com/),[Hacker News](https://news.ycombinator.com/), and [Twitter](https://twitter.com/). 
I don’t hate the fact that I'm a bit addicted to their streams, I mostly consume interesting and informative software-centric content, but I have find myself wanting more powerful information filtering tools.
[Information Filtering](https://en.wikipedia.org/wiki/Information_filtering_system) (IF) as a consumer technology seems to have either fallen out of vogue or never gotten into it,
but I'd argue that strong IF tooling is becoming more and more needed by users to ensure their personal happiness and effectiveness. 
Currently, the world's information geysers, great aggregators like Facebook, Google, RenRen, and Toutiauo have misaligned incentives with their users. 
Despite billions in recommender engine research, today's production recommender systems are still inadequate.
Further, the dominance of *implicit* signals in user profiling have seen the great aggregators serving the [*Instant Gratification Monkey*](https://waitbutwhy.com/2013/10/why-procrastinators-procrastinate.html) inside us, or the [*Anger Golem*](https://vignette.wikia.nocookie.net/pixar/images/7/7a/Io_Anger_standard2.jpg/revision/latest/scale-to-width-down/2000?cb=20150425021210).
In the absence of these problems, ie. in a system where the great aggregators are 'perfect information retrievers', personal IF tooling is not so much needed.
But until then, it's a thing we should begin to consider more seriously.

### Can I just tell you what I want?

If you're a user of Netflix, Amazon, or Facebook, you know the powers and the weaknesses of an implicit feedback system for user profiling and recommendations. 
Compared with explicit, implicit has the large advantage of providing the user a super-smooth user experience. No need to tell the system what you're interested in, it's busy figuring that out for itself. The clear problem though, the problem that I think necessitates IFs, is many of the things that leak through in implicit feedback we would not at all claim as preferences.

I’ll admit, I sometimes click on dumb clickbait. Frustratingly, the machine learning system behind whatever site I’m on will not notice the *instant regret* I feel having done so, and instead register a positive signal to show more me more articles like “23 times Kloé Kardashian left the house without shoes”. I don’t care about this person, any time I happen to click on anything about them was a moment of brain failure, perhaps at 2am and in a state where I might not be tapping things quite so precisely. Too late though, down the line I’ll be updated when her boyfriend is seen suspicuously grocery shopping with another woman. A woman that’s probably just his sister.

From what I’ve come to learn about natural language processing, knowledge graphs, and information filtering generally, it *should* be more-or-less possible for me to just type in:

> Do not show me celebrity gossip. I do not care about the Bachelorettes, the Kardashians, or anyone Instagram famous.

It *should* be possible for me to type in:

> I like sport, particularly Tennis, Soccer, and AFL, but do not show me anything about Cricket

Currently Facebook and Google News *do* have systems that partially have this functionality, though crucially you have to *wait* for it to show up before you can click a drop down and select “don’t show me stories about X”. I think this is an anti-pattern. The filtering configuration is hidden from me, so I can only fix it through a couple of knobs that only appear once the system has made a mistake. I would *really* like these filtering configurations to be shareable. If someone discovers/designs a really good way to filter out stuff about horoscopes, they should be able to share it and I should be able to install it into my system. We could even build customisable user profiles to solve the cold-start problem. I’d really like [Tristan Harris’s](http://www.tristanharris.com/) filtering configuration, or Noam Chomsky’s.

### Good recommendation systems are apparently an AI-complete challenge

Beyond the struggles with the implicit vs. explicit self, for some reason recommender engines struggle immensely with [fairly straightforward things](https://twitter.com/kibblesmith/status/724817086309142529?lang=en). In an age where we're getting constantly bombarded with useless, irrelevant crap, even if they wanted to our recommender systems couldn't save us.

I get much better recommendations from informed friends and colleagues than I do from any multi-billion dollar recommendation engine. The familiar human beings don’t need to rely on proxy signals for quality like ‘this is getting clicked a lot’, or ‘this contains a lot of words usually found in articles you’ve saved’. They have their own personal human General Intelligence, a wealth of relevant experience in specific areas, and deep understanding of my own experiences and needs. To the extent that recommendation engines succeed right now, I think most of it is driven by a well-curated group of 'followees'. This is at least the experience I’ve had with Twitter, where much of the content delivered is relevant because I follow almost exclusively AI researchers and prominent software engineers. Francois Chollét still dumps loads of shit into my feed though, and Twitter hasn’t fixed that.

So newsfeeds may really need a really solid group of humans to deliver relevant content and filter out rubbish, but looking beyond the current paradigm of recommender systems which optimise for the likelihood of a user clicking on the things it recommends, we can see that good recommendations are an incredibly complex problem. [Information Filtering can be reframed as a twist on Information Retrieval (IR)](http://maroo.cs.umass.edu/getpdf.php?id=131), and under this reframing we can think about a filtering system that blocked content under the kinds of highly complicated criteria embedded in highly complicated search queries.

If I ask of an Information Retrieval system (ie. a search engine), “Which distributed graph database best optimises for HTTP request trace storage?", anything not featured on the first page is essentially *filtered*. For an example of the IF <-> IR relationship that is more applicable to newsfeeds and online media space, think of the question “How can I engage and act politically in order to safeguard the economic futures of local miners in my community?”. The IF mirror of that is "I don’t want information that hinders my goal of safeguarding the economic futures of local miners in my community".  We recently had a period where people *really* needed answers to these kinds of questions, and unfortunately their newsfeed technologies failed them.

### What have we got to work with

Wanting to whack together an information filterer myself, I went after existing implementations and research. Information Filtering was a bit of a thing 30 years ago, before even Google, and well  before Facebook. Systems like ["The Information Lens"](http://delivery.acm.org.ezproxy.lib.rmit.edu.au/10.1145/30000/22340/p1-malone.pdf?ip=131.170.21.110&id=22340&acc=ACTIVE%20SERVICE&key=65D80644F295BC0D%2E124032AC6F25F239%2E4D4702B0C3E38B35%2E4D4702B0C3E38B35&CFID=826579750&CFTOKEN=62469482&__acm__=1510028698_c214de9c28b7c096c548454bc93d06a2), [INFOS](https://eric.ed.gov/?id=EJ552498), [SIFT](http://ilpubs.stanford.edu:8090/73/1/1994-7.pdf), and NewsClip. Most were concerned with managing and improving the user experience with [UseNet](https://en.wikipedia.org/wiki/Usenet). God knows how they'd deal with today's content networks, but at least they were trying and at least they seemed to be *for the user*.

As an interesting analogue to problems with today's platforms that 'push' content to the user, similar push-based system existed for research and business use-cases in the 90’s. Even with the use of information-filtering tooling, such systems were found to be [*distracting and time-consuming for users*](https://books.google.com.au/books?id=g00Gz5nR4s0C&pg=PT329&lpg=PT329&dq=%22BackWeb%22+information+filtering&source=bl&ots=VHxxIRnI5z&sig=_DrzywjFBuUyevvMdbpqnbKB0xM&hl=en&sa=X&ved=0ahUKEwjt2OHIzqvXAhXCJJQKHb2ADWYQ6AEIKjAB#v=onepage&q=%22BackWeb%22%20information%20filtering&f=false). The lesson here in that linked passage is so clear it’s like it leaps out of 2003 and smacks you in the face. In professional environment, *people recognise the value of employee time*, and wasted time is an expense. For social networks, user time is an *asset*, and wasted time barely makes any sense to them.

If I had to speculate, the user experience on internet back in the late 90’s and early 2000’s was such that information filtering tools weren’t required, and now fast-forwarding to 2017 we have a paucity of good software tooling in the problem space. UseNet was created back then, and heaps of tooling around the RSS format, because they addressed the peculiar needs of the time.  Then everyone and their nana joined the internet, [Aggregation Theory](https://stratechery.com/2015/aggregation-theory/) took hold, and now the internet is a place dominated by great aggregators and ad-revenue incentives.

### Going Forward
For now I think the highest priority in the IF space is fostering an open-source, public community led effort to make user content preferences explicitly defined, compose-able, and shareable.

* **Explicitly defined:** not ‘I didn’t click on this show don’t show me it’, but ‘filter out anything involving X’.
* **Compose-able:** the characterisation of everything I *don’t* want show to me is a a complicated thing. The content-based equivalent of a hostfile blacklist won’t cut it.
* **Shareable:** I should be able to share my IF configuration both with other people and with new content providers I want to engage with. Don’t make me select topics I’m interested in or not interested in over and over again.

Those three above would let users take back control of their content feeds from companies whose predominant goal is to cultivate large groups of eyeballs for advertisers.

----

Thank you for reading. If your interested in further exploration this stuff, [here’s a link to this posts’ notes, with lots of good links](https://www.evernote.com/l/AcRny-ZPqKxPJpAalW7HL95OYqWL1Ld7qvQ).