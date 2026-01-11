---
layout:     post
title:      "There's been a vibe shift in vibe coding"
date:       2026-01-11
summary:    Senior's eyes are lighting up in delight.
categories: ai llms agents
permalink: vibe-coding-vibe-shift
---

<figure style="margin: 0; margin-bottom: 1em;">
  <div style="display: flex; width: 100%; border-radius: 0.4em; overflow: hidden">
    <div style="flex: 1; overflow: hidden;">
      <img src="images/reverse-la-taureau.jpg" alt="Le Taureau (The Bull) by Pablo Picasso — a series of eleven lithographs showing the progressive abstraction of a bull" style="width: 100%;">
    </div>
  </div>
  <figcaption style="color: #777;">Pablo Picasso, <em>Le Taureau</em> (The Bull), 1945–1946 [Reversed]</figcaption>
</figure>

<!-- https://x.com/davidcrawshaw/status/2007995208638881860?s=46&t=bEd9Zc0R6z8J1hVoDNlFZw -->

<!-- https://x.com/JustJake/status/2007730898192744751?s=46&t=bEd9Zc0R6z8J1hVoDNlFZw -->

Just after Christmas something changed in the attitudes of the senior engineers I follow. LLM coding took another step forward.

Skeptics became converts, and converts became bulls.

<div style="display: flex; justify-content: center;">
  <blockquote class="twitter-tweet"><p lang="en" dir="ltr">&#39;bout half the engineers I admired pre-ChatGPT have become massive coding agent bulls in the past couple weeks. DHH flipped a few days ago. The others may join the mob before Q1 ends. Heady days.</p>&mdash; Jonathon Belotti (@jonobelotti_IO) <a href="https://twitter.com/jonobelotti_IO/status/2007949142933508350?ref_src=twsrc%5Etfw">January 4, 2026</a></blockquote>
</div>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

* **Linus Torvalds** is [letting AI review Linux patches](https://www.zdnet.com/article/linus-torvalds-ai-tool-maintaining-linux-code/). (Update: [he's also vibe coding](https://github.com/torvalds/AudioNoise))
* **Andrej Karpathy** (of course) tweeted that he's ["never felt this much behind as a programmer"](https://x.com/karpathy/status/2004607146781278521?s=20).
* Rails' **DHH** [became a convert](https://x.com/dhh/status/2007504187568074843?s=20).
* **Salvatore Sanfilippo (antirez)**, creator of Redis, said just a few hours ago that ["it is simply impossible not to see the reality of what is happening."](https://antirez.com/news/158)
* **George Hotz**, a notable grump, begrudingly called agents ["decent"](https://x.com/__tinygrad__/status/2000972812731998522?s=20).
* **Jake Cooper**, founder of Railway, just blogged that ["programming as we know it is dead"](https://x.com/JustJake/status/2007941551133982740) and that with the power we should start building "hyperstructures".
* **Steve Yegge** posted [_Welcome to Gas Town_](https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04) a delightfully unhinged but apparently working AI agent bonanza.
* **Mitchell Hashimoto**, retired founder of Hashicorp and creator of Ghosty, said ["Slop drives me crazy and it feels like 95+% of bug reports, but man, AI code analysis is getting really good"](https://x.com/mitchellh/status/2006114026191769924?s=46).
* **Marc Brooker**, distinguished eng at AWS, [endorsed and (kinda) named](https://brooker.co.za/blog/2025/12/16/natural-language.html) vibe coding's next phase: specification driven development (SDD).

We might be around 6 months from Jonathan Blow getting onboard.

In the past this has seemed like bluster and people hyping things up for attention. I'm thinking of 9 months ago when Tobi Lutke posted ["Reflexive AI usage is now baseline expectation at Shopify"](https://x.com/tobi/status/1909251946235437514?lang=en).

But now? I dunno if it's because I got ChatGPT Pro recently or because Opus 4.5 dropped and became my daily driver in Cursor, but the capabilities of coding agents feel _**much**_ better.

Here's what changed: the defining feature of vibe coding—shipping code without reading it—is becoming an accepted practice
by highly skilled, staff+ engineers. What has replaced vibes is _specification_, where the engineer uses their skill to define the solution and then
trusts the coding ability of the agent to autonomously implement and test itself against the solution spec. **Spec-driven development**.[^1][^2][^3]

This gain of trust has dilated pupils and spiked ambition. 

Heady days.

---

[^1]: [Natural Language is Replacing Programming Languages](https://brooker.co.za/blog/2025/12/16/natural-language.html).

[^2]: ["It would have taken me probably months to code by hand. Building on 5 years of work and 10 years of experience. Claude wrote all the code in Golang in 4 hours."](https://x.com/JustJake/status/2007730898192744751?s=20)

[^3]: ["I gave Claude Code a description of the problem, it generated what we built last year in an hour."](https://x.com/rakyll/status/2007239758158975130)
