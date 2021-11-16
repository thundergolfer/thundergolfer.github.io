---
layout:     post
title:      The Bazel 'Elevator Pitch'
date:       2021-06-13
summary:    There's an elevator pitch for Bazel from early 2018 that I point people at and crib from so often that I thought it was well time I copied it out and put it online.  
categories: crossing-the-chasm build-systems evangelism bazel
---

There's a recorded elevator pitch for Bazel from early 2018 that I point people at and crib from so often that I thought it was well time I copied it out and put it online. 
It's tucked away in a Scale By The Bay talk about reproducible machine learning given by [Oscar Boykin](https://twitter.com/posco)<sup>1</sup>.

### The Pitch

<div style="display: flex; justify-content: center">
    <img style="align: center" src="/images/posts/bazel_elevator_pitch/oscar-boykin.png">
</div>

<blockquote>
  <p>
  [I'll give] a brief sales pitch for why Bazel is arguably one of the most exciting peices of technology that happening right now in the open-source world, that I'm a big big booster of, and I really want to see it succeed.<br><br>
  So we do use Bazel at Stripe, and what is Bazel? Bazel is a build tool. I think that functional programmers, in the future, will look back on these days and think that the way that we're building code right now is as, you know, primitive and grotesque as the days before code review or CI.<br><br>
  And each of us thinks, 'Ohh, back in the days before code review I would've done code-review, those people were terrible'. Or unit-testing; 'I would've done unit-testing', but actually people developed software for a long time with out doing unit-testing, and then now we snear at them, and functional programmers, sadly, can be a bit of an arrogant bunch, they may even look down on these people.<br><br>
  But what Bazel is trying to sell you on is that your build should be a pure-function. So, I'm from The South, and I've had half a drink, so you know, we need to, you know, *get religion* about that.<br><br>
  I think functional programmers should understand, they should be like "hallelulah" on that. That builds should totally be a pure function. If I come with my sources, if I come with my dependencies, the output of that should be the same thing today, as tomorrow, as the following day.<br>
  It's kinda crazy that we would accept anything otherwise. Now people accept otherwise will sometimes say 'oh it's hard to do that', or 'it will take too long to do that'. They'll have a long list of while it can't be done. But it *can* be done, so therefore in 5 years when this idea has won, and everyone knows it, and it's like 'of course you have reproducible builds and of course you have unit-testing, and code coverage'. You want to look back and say that you were one of the people that understood that, you know, way back, and you helped usher it in.<br><br>
  So that's why you should be excited about Ulf's talk.<br><br>
  He's gonna talk to you probably about caching, and how Bazel is very programmable, but to me I think that Bazel has the opportunity to be a linux-like project. That we stop, like, like, having these like parochial build tools, you know, SBT here, Maven there, maybe some weird package manager for my new fancy language over here.<br><br>
  Here's one way that we describe functions from source into the outputs, and I can git-bisect, rebuild that, and get the same thing in the past. I don't have weird things that like your laptop builds it one way, CI builds it another, et cetera. So it's hugely important, and people who don't get it yet, they're gonna get it, and you wanna get it early.<br><br>
  So that's all I'm gonna say about Bazel.<br>
  </p>
  <footer><a href="https://twitter.com/posco"><cite title="Oscar Boykin">~ Oscar Boykin</cite></a></footer>
</blockquote>

---

Back in 2019 that pitch did quite a good job getting me on board, so spread it around and get more on board the 'your build as a pure function' bandwagon. 

---

1. ["Reproducible Machine Learning with Functional Programming"](https://www.youtube.com/watch?v=t_Omlhh7IJc&t=30s)
