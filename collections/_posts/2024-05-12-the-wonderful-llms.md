---
layout: post
title: The Wonderful LLMs
date: 2024-01-14
summary: Praise for ChatGPT after one year of use.
categories: software culture llms ai
---

![Charles Lindbergh lands in Paris, France](/images/the_wonderful_llms/Charles_Lindbergh_Lands_in_France.jpg)

There’s an old [Louis CK bit](https://www.youtube.com/watch?v=b3dYS7PcAG4) where he gets comically exasperated at the complaints of typical airline passengers. I’m a grumbly air traveller myself, and will always find something to get pissed off about when I fly. But on the plane I always remember that bit from Louis CK and spend some part of my flight smiling quietly to myself, thinking “isn’t this incredible?”

In keeping with the technological acceleration of our time, it seemed that ChatGPT enjoyed around 1 day of unabashed wonder before concerns about copyright, the children, and one journalist’s threatened marriage overshadowed the tech. 

ChatGPT has been out for around 18 months, and I think only in the last three have I enjoyed a regular and productive relationship with the product, on top of an immense respect and appreciation for the technology. ChatGPT, and LLMs more generally, are an astonishing feat of human achievement, a genuinely new and useful software engineering tool. But there’s also of course wariness. They’re plausibly a threat to the web, the human spirit, and don’t forget the children. 

### The tech is good

If you haven’t listened to [Acquired’s history of the Taiwan Semiconductor Company](https://www.acquired.fm/episodes/tsmc), or any other storytelling, go and do that now. Because without at least some sense of how deep an NVIDIA A100 GPU’s supply chain goes you won’t understand what a gargantuan feat of science and engineering GPT4 is. What started as rock mined in Bizana, Mount Cattlin, or Minas Gerais has been refined and arranged to run more tensor multiplications in a day than there are stars in the Milky Way. How many people had to do their job well to make GPT4 possible?  

After a while, this contemplation should lead to awe. Yes, the venture capital hype is heady, but engineers should still take this software very seriously. Software engineers I [admire](https://colah.github.io/about.html) [greatly](https://nelhage.com/) [have](https://simonwillison.net/) [directed](https://justine.lol/oneliners/) [their](https://thume.ca/) brains and labour directly to LLMs. Although I initially hadn’t found ChatGPT useful and most serious attempts at [building products with LLMs were discouraging](https://www.honeycomb.io/blog/hard-stuff-nobody-talks-about-llm), from what I’ve now experienced with LLMs, failing to build world-changing products with this technology would be an all-time fumble.

I signed up for ChatGPT Plus in April 2023, and now just over a year later I’m a regular user, almost exclusively at work. In April 2024 I added a Claude Pro subscription. Around ChatGPT’s release I had mostly heard how effective it was at writing simple common programs. I didn’t need help writing simple common programs, and in fact thought that outsourcing these exercises to ChatGPT would over time degrade my programming ability. I still don’t really use LLMs to write programs, but I do use them to debug issues and there they have exceeded expectations. I did not, for example, expect ChatGPT to be so good at understanding and explaining problems in iptables configuration. 

At work we had a confounding security issue where containers on the same network bridge interface were unexpectedly able to talk to each other. Our iptables configuration was supposed to prevent this, and it did when the containers were not on the same bridge. I thought hard about what this could be, Googled it a lot, tried a few things, then gave up and stuck the details in Linear. A few weeks later a brilliant intern picked up the ticket and fixed the issue in an hour or so. I asked, “how did you figure it out?” He’d asked ChatGPT! I was so surprised and skeptical that I asked for the ChatGPT share link, and sure enough it correctly had pointed the intern at the `net.bridge.bridge-nf-call-iptables = 1` flag.

That was probably the moment I became a convert, or maybe when a colleague showed me the *[Advanced Data Analysis](https://mitsloanedtech.mit.edu/ai/tools/data-analysis/how-to-use-chatgpts-advanced-data-analysis-feature/)* feature and I was finally free off the maddening Matplotlib API. I thought ChatGPT could just help solve homework problems, but I was wrong.

### The interface is good

The prompt understanding and answer quality is not actually the biggest reason I keep coming back to ChatGPT. It’s the lack of ads and other distracting bullshit. As others are now saying, Google is both user hostile in its ad-stuffing and has also completely failed to cut out the SEO-optimized cancer in its index. At work I want to get shit done and Google is nowadays just not optimizing for technical user productivity.

Coding interviews are place where a programmer is highly motivated to get shit done. At work we ban the use of ChatGPT in interviews for obvious reasons, but I wince when candidates return again and again to the [#1 ranked page on Google for Python decorators](https://realpython.com/primer-on-python-decorators/).

![A screenshot of the number one ranked page on Google for the query 'python decorators'](/images/the_wonderful_llms/py_decorators_tute.png)

The #1 ranked page for “python decorator” is a bloated mess full of ads, cross-promotion, and waffling.

Candidates are sometimes novice programmers, sometimes experienced programmers but not in Python, and the rank #1 Google result has them scrolling up and down stressfully for the information they need. ChatGPT gives exactly the right information after basic prompting and about 400ms of token generation. Too good, too powerful. 

Beyond the ad-free experience and a training corpus free of bad SEO crap, I find the chat interface really natural after spending a decade in chat forums and Slack workspaces. The medium is the message. It is under-appreciated how focusing and productive a primarily text-based, two-party conversation can be. It is now said that private chat applications such as Discord and Facebook Messenger have become the safe haven away from ads, bots, and distracting bullshit. It sometimes happens that Reddit and Youtube have the technical information I’m searching for at work, but these are entertainment platforms and always do their best to get me clicking on some cotton-candy video once they’ve served me an interesting r/rust comment or Jon Gjengset video.

This product side of ChatGPT is obviously the bit to worry most about. In these early days the incentives between producers and consumers are well aligned. If LLMs are genuinely useful then people will pay $20/month for a subscription and businesses will pay $1000s a day to build products and features on top of them. But is this enough for OpenAI, Anthropic, and the rest? We must be ready for ads to enter the revenue stream, and when they do we’re basically back where we started.

This incentive misalignment doesn’t pose a fundamental problem to my LLM usage though. I bet that this incentive problem will be a huge boon to open-source LLM development and spur the creation of multiple unicorn startups offering LLM products to professionals. But the *free* users of LLM products? Well, they’re in trouble. 

LLMs, just like the internet, are on net a big help to the media literate, educated, and experienced. When using an LLM I’m quite familiar with how it works, how it’s limited, I have a clear idea of my problem and my goal, and [I know how to ask the right questions](http://antirez.com/news/140). Effective use of LLMs for serious purposes require a user to know a lot about the topic of conversation. LLMs hallucinate and they get lost and they babble. I like antirez’s characterization of them as a “stupid savant”.

Unfortunately, most users of LLMs and of the internet cannot and will not approach LLMs in this fashion. The world-wide-web “information superhighway” has not led to an increase in public knowledge. And just as “you can see the computer age everywhere but in the productivity statistics”, you can see the PC revolution in schools but not in the national testing results (which are trending down in my country, Australia). I don’t think LLMs are close to an answer to Bloom’s 2 sigma problem. I don’t think they’re good learning tools, and I don’t think they are tools of mass literacy. They’re tools best for the already literate, the already learned. I won’t say more on the dehumanizing side of LLMs, as this post is about how fantastic LLMs are, but I’ve generally found [Ezra Klein’s commentary](https://www.nytimes.com/2024/04/05/podcasts/transcript-ezra-klein-interviews-nilay-patel.html) to be an appropriate mix of appreciation and concern.

### The LLMs are good

I got into software because I read stuff like Tim’s Urban’s [AI Revolution](https://waitbutwhy.com/2015/01/artificial-intelligence-revolution-1.html) series and got massively hyped on AGI. I could not code my way out of a wet paper bag, but I wanted to help make a two-bit god. I was young. I was naive. But I’m not embarrassed about it. Every since the dawn of computing people way smarter than me have dreamt of building AI. Their part to play was the Difference Machine, The Test, the vacuum tube, LISP, Shakey, A* search, Arpanet, it goes on and on. Sure, these LLMs aren’t AGI and I personally don’t believe that just 5 OOMs more data will be enough. But it’s fucking crazy that this LLM thing actually works at all. It says something about society’s disassociation, jadedness and alienation from industrial progress that these LLM breakthroughs didn’t spawn a parade or even a public party. In 1927 Charles Lindbergh crossed the Atlantic ocean in a airplane, touched down in Paris, and the whole city went bananas. 

GPT-4 is a marvel. It’s brilliant. It’s wonderful. Now—how do we stick ads in it?

