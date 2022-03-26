---
layout:     post
title:      Bazel is taking over
date:       2021-06-14
summary:    On the Bazel build system's potential to become a category-killer.  
categories: build-systems software-engineering bazel
---

> "I really think that Bazel has the opportunity to be a Linux-like project"  - [Oscar Boykin](https://youtu.be/t_Omlhh7IJc?t=172s)

You don't need to be excited about build systems. Really, they're most appreciated when they manage to just get out of your way. 
For a boring build system though, Bazel is catching on like wildfire, and I'll claim that in just five years it could be as dominant as `git`.

When Bazel (née Blaze) was open-sourced it garnered [a decent amount of attention and appreciation](https://news.ycombinator.com/item?id=9256844), but it was Tensorflow, 
open-sourced a couple of years later, that would become the jewel of Google's open-source suite and the most starred project on Github. In 2018 some would have made the 
'safe bet' that it would be Tensorflow not Bazel that dominated in its category, but it's 2021 and PyTorch sure makes that bet look shaky. 

Bazel has had a slow start on adoption because it has a very high cost to adoption and because it was open-sourced only after ex-Googlers had already copied it at their 
new companies ([Buck](https://github.com/facebook/buck), [Pants](https://github.com/pantsbuild/pants), [Please](https://github.com/thought-machine/please)) and then open-sourced those. 
The four Blaze clones made for an awkwardly crowded space at the top, and the few software teams large enough to justify a migration were left with the trouble of guessing a winner. 

With the recent announcement that Twitter, the creator of Pants, would be migrating to Bazel, I think we've arrived at the point where a winner has been picked. 
Bazel already had significant community momentum, which partly led to Twitter's decision, but with Twitter onboard and also Android onboard, Bazel is now the obvious first choice for large polyglot codebases. 

The list of companies that have fully or partially adopted Bazel includes some enormous engineering organizations: Google, Apple, Salesforce, VMWare, Nvidia. Also onboard are Uber, 
Twitter, SpaceX, Pinterest, Etsy, Square, Grab , Databricks, Brex, and my company, Canva. At least half of the 10 most valuable YCombinator companies use Bazel, including Dropbox, Stripe, AirBnB, and Coinbase. 
The total engineering headcount in those company's build engineering teams is huge, and the codebases involved basically guarantee that Bazel will be more battle-tested for software development at scale than any other open-source option. 

Over the next 3-5 years, good leadership from Google and active, positive participation from the rapidly accumulating group of adopters could see Bazel becoming obviously the best build system for most relatively large software codebases. 

Bazel isn't having this quiet success because the unsexy world of build engineering is in the grip of a fashion trend that favors Bazel. Compared with the status-quo in build technology, particularly multi-language build technology, 
[Bazel's fundamentals are really solid.](https://www.microsoft.com/en-us/research/uploads/prod/2018/03/build-systems.pdf) Bazel is not ideal, and it [does not convince everybody](https://blog.mozilla.org/nfroyd/2019/10/28/evaluating-bazel-for-building-firefox-part-1/). 
I'm not saying we couldn't do better than Bazel, but at its core is the principle that *your build should be a pure function*, and that core principle, given its due, produces a build technology that is a true level up on what's currently acceptable in software engineering. 

If we grant that Bazel will come to dominate the codebases of large engineering organizations (which is a hugely impactful sea change in professional software development) that still leaves 
*all the other* codebases. If Bazel is to become a 'linux-like' project, or be as ubiquitous as `git`, then Bazel's adoption cost will have to become dramatically lower, and 
it's developer experience will have to markedly improve. I think this can happen without too much trouble, but that's an argument to be made in another post.  

So Bazel is taking over. Our builds will be pure functions from source to deployable. This will represent a durable evolution in the software engineering field, and Bazel will become as 
essential as `git` and source control. Like `git`, we will often find it annoying. We will punch out comments about how it's API is not quite right, or that it's too hard to learn, and we will likely be right. But we will never suggest going back.
