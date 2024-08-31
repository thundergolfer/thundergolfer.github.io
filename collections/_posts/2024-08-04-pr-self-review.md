---
layout: post
title: The Pull Request Self-Review
date: 2024-08-4
summary: Out of the crooked timber of humanity...
categories: software-engineering programming process fallibility
permalink: pr-self-review
---

![illustration of the self-review process on a git diff](/images/zune-diff-2.jpg)

> "I am not a great programmer, I am just a good programmer with great habits" — Kent Beck. 

The pull request self-review is something I have proselytized to junior colleagues enough times now that I ought to write down the pitch. It is a simple thing: before you get someone to review your pull request (a.k.a change list, abbrev. PR), review it yourself. It may seem painfully obvious, but almost all material on the pull request process [elides this useful step](https://www.atlassian.com/git/tutorials/making-a-pull-request). The self-review is both less obvious and more difficult than it sounds.

The self-review is not the continuous, implicit process of self-critique that happens when an engineer is producing a code change. No, that is an additional, prior process of mental editing. The self-review is when you, the author, look at the same commit stack in a diff viewer like Github’s and think about whether that commit stack is ready to review. You aim to consider the change *as the reviewer would.* You may even comment on the change as the reviewer would, before the actual reviewer is requested.  Easy, right?

I personally have found that adopting the reviewer’s—or better, critic’s—mindset is actually quite challenging. If you’ve ever had someone point out an obvious and stupid mistake in work you submitted for merge to `main` you’ll know that familiar feeling of being *blind to your own mistakes*. It is tricky to stand at a distance from your own work, work you probably labored hard to ‘get working’, to ‘finish’. You must transition from author to critic, something our human psychology is ill-suited to perform.

During my college years I worked with friends at a large 5-star wedding venue under a cranky and severe venue manager, Mark, whom we feared and adored. He kept standards high, and we genuinely attempted to meet them. 
But we failed. At the end of a wedding day, once the guests had left and we’d worked to get the rooms back spick and span, we’d invite manager Mark to look at our work. Too often he’d meet it with displeasure,
eye us wryly, and drop a line Jeff Bezos was fond of using: Are you lazy or just incompetent?

Within five seconds he’d have pointed to out-of-order glassware, a rag on a chair, a table set for five not eight. How had we missed it? We weren’t really looking.

To properly self-review my own code I have to become a critic like Mark and really believe I’ve just walked in on someone else’s work. In the critic’s mindset you’re questioning assumptions, checking unhappy paths. In this mindset I feel *rewarded* for finding my own mistakes, and I do often find them.

But I usually find it hard to become the critic. At work [code review is (controversially) not mandatory](https://x.com/bernhardsson/status/1755633103865831679) and so the self-review is especially important. 
I weirdly find that even after doing a self-review, it’s sometimes only after I merge that I *really* switch my mentality into critic mode. There’s something about escalating the situation that knocks me out of complacency.

The pull request self-review is hardly going to be a game-changer for your code quality and uptime, but I do believe it is a meaningful contributor to it. 
Self-reviewing engineers take more responsibility for their work, ship fewer bugs, and reduce time spent by colleagues pointing out typos, missing edge-cases, incomplete testing. 
Self-reviewing engineers exercise that meta-cognition muscle which has them pay attention to the ways they fool themselves. 
[The first principle is that you must not fool yourself and you are the easiest person to fool.](https://www.goodreads.com/quotes/193533-the-first-principle-is-that-you-must-not-fool-yourself)

That’s the pitch. If you wish you could more often put up flawless PRs which receive no comments and merges into production like cream into coffee, practice the self-review. Divide for a short while against yourself and see the bugs.
