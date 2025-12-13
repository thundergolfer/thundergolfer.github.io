---
layout:     post
title:      "Larval stage support engineering: great at what doesn’t scale"
date:       2025-12-13
summary:    The three core mantras of early support engineering success.
categories: startups support
---

![Slack waiting for response](/images/support-eng/slack-waiting-druglog.png)

When I took my first startup job, I wanted a place that would train me as a good programmer. When I took the second one, as employee #7, I wanted a place that would train me on *everything.* 

At startups “everything” is engineering, support, sales, marketing, growth, operations, and recruiting[^1]. 

This post, probably the first in a series, is about **support**[^2]. In particular, it’s about the core of support engineering in a “larval stage” startup, one with fewer than 30 engineers.

At Modal we have a strong customer focused culture. At Modal, **all engineers talk to users directly.** 

We try to reply instantly. We sometimes reply at 1:36AM in the morning. We may get on planes and fly to you that day. We check back in.

The post is my distillation of the core mantras of early support engineering success, mantras which have served us well for more than three years.

1. Reply to the customer.
2. Get on a call
3. Follow up fast

## The #1 rule: reply to the customer

This mantra is what motivated me to write a post about customer support, something I’ve never done before. As Modal went beyond fifteen engineers, we started having existing engineers (incl. the CTO) delegating support work to engineering teams.

Modal uses Slack for internal communication, community support, and paid customer support. It’s quite convenient. Because we use Slack, the delegation of a support issue looks like a message link landing in different Slack channel.

![Akshat Support](/images/support-eng/akshat-support.png)

It is remarkable how often engineers will swarm on a support issue for hours, pinging back and forth questions, theories, and debugging information—and no one thinks to message the customer! 

A particularly interesting customer issue can function as a nerd snipe. All of a sudden there’s a four person, multi-hour, 50+ comment Slack thread going. And the customer remains left on read. They’ve just been sitting there, probably thinking we were ignoring them when in reality they had the keen attention of multiple engineers.

Besides failing to reply in the first place, another failure mode is an engineer will accept a support question and work hard on it for hours before reaching end of day and closing their laptop without updating the customer. 

Think of the customer’s perspective here. It would be fair for them to think that their question or request was abandoned, especially if it’s time sensitive. The reality is that an engineer worked hard for hours but the problem needs to span multiple days. Solution: the engineer needs to update the customer regularly.

To start improving as support engineers at a startup an engineer needs to start mentally putting the user first. User first, technical investigations second.

## Get on a call

Some engineers get energized by customer calls and customer visits. These engineers are great early startup hires. (Our CTO is like this.) Most engineers, including usually myself to be honest, don’t gain energy. Some engineers palpably *fear* calls with customers.

But in the early days of Modal I repeatedly saw engineers getting on calls with customers, and I naturally adopted it as standard practice.

But it’s a non-default behavior of engineers, and so it needs regular affirmation as something that does not feel natural, and yet it is remarkably *high value,* meaning engineers should push themselves to make calls with customers.

If a back-and-forth with a customer just isn’t getting the issue squashed, get on a call. If a customer is complaining, get on a call. If you need to sell a feature—if you need to sell the whole product—get on a call. If there was an outage and the customer is pissed, get on a call and show them you care, listen to their pain.

> There are two reasons founders resist going out and recruiting users individually. One is a combination of shyness and laziness. They'd rather sit at home writing code than go out and talk to a bunch of strangers and probably be rejected by most of them. — [Do Things That Don’t Scale](https://paulgraham.com/ds.html)
> 

Getting on calls is hard work, it’s social labour. You have to turn off Spotify, move away from your desk. You have to be *on*, for at least twenty minutes. It’s possible you won’t understand their problem, or their code. Maybe so. 

But startups must show up for their customers. Startup engineers must get on a call[^3].

## Follow up *fast*

> “I wrote a little program to look at this, like how quickly our best founders — the founders that run billion-plus companies — answer my emails versus our bad founders. … I don’t remember the exact data, but it was mind-blowingly different. It was a difference of minutes versus days on average response times.” — [Sam Altman](https://conversationswithtyler.com/episodes/sam-altman/)
> 

This core mantra has a caveat. For engineers, tunnel vision on maximizing response and resolution speed will cause distraction, myopia, and overfitting to customer feedback.

But engineers at startup should know and feel the massive difference between replying to a customer in 30 seconds versus replying in 30 minutes, even though both are fast responses.

The lightning reply, or quick bug fix, delights customers in a few ways:

- They feel they have your close attention—they matter.
- They feel you are engaged, and thus the product is of active concern (ie. not deprecated)
- The product they’re using feels *interactive*; their feedback quickly produces response and evolution.
- The producers of the product seem highly competent. They understand their customers and their product intimately and comprehensively. If they didn’t, they couldn’t reply so fast.

Fast follow ups are infectious and energizing. The speed of feedback and evolution in a startup is one of the best reasons to participate in them. 

<div style="display: flex; justify-content: center;">
  <blockquote class="twitter-tweet"><p lang="en" dir="ltr">&quot;we feel like you are a team at our company&quot;<br><br>&quot;we feel like we&#39;re your only customer&quot;<br><br>🥹 exactly how we want our customers to feel ❤️</p>&mdash; Simon Eskildsen (@Sirupsen) <a href="https://twitter.com/Sirupsen/status/1935711748629078452?ref_src=twsrc%5Etfw">June 19, 2025</a></blockquote>
</div>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

As initially warned, you shouldn’t push this too far, to the point of rushing responses or becoming distracted hovering over a community Slack channel. But when an opportunity to quickly answer a question or fix a bug arises, take it. Don’t leave it for after lunch, or the next day.

## Go forth and delight customers

![Bezos customer obsession](/images/support-eng/bezos-shmiternet.png)

A lot of the above is what you get when you take Paul Graham’s famous [*Do Things That Don’t Scale*](https://www.notion.so/227-A-post-about-support-engineering-stage-1-great-at-what-doesn-t-scale-2ad99ea4b26f80228ae4f40201223a2c?pvs=21) essay and apply it just to customer support engineering. That essay is advice for founders, but advice for founders applies pretty well to early startup employees. It’s a principle advantage of being an early employee at a startup that you get work in close proximity to people (the founders) who are compelled into maintaining an uncommon, “insanely great” attention to users and customer service.

Because the now old advice really is true: if you're [customer obsessed, you have a good chance of winning](https://www.youtube.com/watch?v=UPwdjfYYgzI).

---

[^1]: I have not become good at most of these, but it's been great to try, great to learn.
[^2]: I have two related posts on Slack skills. (1) [Against DMs](/against-slack-dms), and (2) [how to ask for help](/help-in-slack).
[^3]: Customer calls are one of the heartbeats of a startup engineers work life. If you haven't been on a customer call in the last month or so, something might be wrong. Come out of the cave.
