---
layout: post
title: "The First LLM"
date: 2025-03-23
categories: genai llm machine-learning
summary: A tracing of the history of GPT-1 and its predecessors.
permalink: /blog/the-first-llm
---

<figure style="margin: 0; margin-bottom: 1em;">
  <img 
    src="/images/gpt-1-illustration.webp" 
    alt="Illustration: Ben Barry (GPT-1 announcement cover illustration)" 
    style="border-radius: 0.4em;"
    width="100%"
    height="auto"
    style="aspect-ratio: 16/9; object-fit: cover; border-radius: 0.4em;"
  >
  <figcaption style="color: #777;">Illustration: Ben Barry</figcaption>
</figure>

<div id="toc" style="background: #f8f9fa; padding: 1em; border-radius: 0.4em; position: absolute; right: calc(50% - 45em); top: 54em; width: 15em; max-height: 80vh; overflow-y: auto;">
  <div id="toc-content"></div>
</div>

<script>document.addEventListener('DOMContentLoaded', function() {
  if (window.innerWidth < 768) {
    document.getElementById('toc').style.display = 'none';
    return;
  }

  const toc = document.getElementById('toc');
  const headings = document.querySelectorAll('h2, h3');
  const tocContent = document.getElementById('toc-content');
  const lastTwoHeadingIndexes = new Set([headings.length - 1, headings.length - 2]);

  headings.forEach((heading, index) => {
    if (lastTwoHeadingIndexes.has(index)) {
      return;
    }
    if (!heading.id) {
      heading.id = `heading-${index}`;
    }
    const link = document.createElement('a');
    link.href = `#${heading.id}`;
    link.textContent = heading.textContent;
    link.style.color = '#777';
    const div = document.createElement('div');
    div.appendChild(link);
    if (heading.tagName === 'h3') {
      div.style.marginLeft = '1.5em';
    }
    div.style.marginBottom = '0.5em';
    tocContent.appendChild(div);
  });

  /* Update TOC visibility on window resize */
  window.addEventListener('resize', function() {
    document.getElementById('toc').style.display = window.innerWidth < 768 ? 'none' : 'block';
  });
});</script>


What were you doing while the LLM revolution was birthed and in a few short years remade the computing industry? 

Was the first LLM really made by an Australian, in between surfs? 


These questions have sat with me since I revisited, chronologically, the research papers which scaled up language modelling and the 
market capitalization of our juggernaut industry by more trillions of dollars.

‘We’ did it. The most famous benchmark in computing history, Turing’s, is now _too easy_.  
Today, dozens of new benchmarks measure the expanding frontier of AI accomplishment: can it win the Putnam, can it beat Pokémon?

In 2016, one year before the 'first LLM' was born I was sitting in computer science classes hearing professors talk of Chomsky’s hierarchy of the grammars. 
In these lectures, they used Turing’s test to inject a little wonder, a little mysticism into the dry mechanics of push-down automata. 
Would we ever make a program that passed this test? 

When the 'first LLM' was born I was wrapping up an internship on a team building a language model. 
It was not large, and wasn’t a transformer, but with hindsight I was relatively close to the LLM revolution. 
But I wasn't really paying attention. Most of us weren't.

In 2016 my teammates made summarizer models which went “Return return return return return return shipment shipment…“, as well as a genuinely state-of-the-art chat bot which genuinely sucked at chatting. I lost faith.

In January 2018, as I wrestled with Golang in my second internship, Australian Jeremy Howard published *ULMFit*, the first LLM.

<figure style="margin: 0; margin-bottom: 1.4em;">
  <img 
    src="/images/gpt-timeline-2.png" 
    alt="Timeline of GPT-1 through GPT-3.5" 
    style="border-radius: 0.4em; border: 2px solid #ddd;"
  >
</figure>

Alec Radford published *Improving Language Understanding by Generative Pre-Training* (GPT-1) on June 11, 2018. 

GPT-1 (Generative Pre-Train One) is widely accepted as an LLM. 
According to many it _is_ the first. But Jeremy Howard claims otherwise. 
If we’re to understand the LLM birth, we’ll have to mark down what exactly makes an LLM an LLM.

<div style="display: flex; justify-content: center;">
<blockquote class="twitter-tweet" data-lang="en" data-dnt="true"><p lang="en" dir="ltr">What I&#39;ve been working on for the past year! <a href="https://t.co/CAQMYS1rR7">https://t.co/CAQMYS1rR7</a><br><br>Inspired by CoVE, ELMo, and ULMFiT we show that a single transformer language model can be finetuned to a wide variety of NLP tasks and performs very well with little tuning/tweaking.</p>&mdash; Alec Radford (@AlecRad) <a href="https://twitter.com/AlecRad/status/1006247734691545089?ref_src=twsrc%5Etfw">June 11, 2018</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
</div>

## What is an LLM?

**LLM** <span style="color: #546E7A;">(_**noun**_)</span>: a language model which has been so effectively self-supervisedly trained as a 'next word predictor' that it can be easily and successfully adapted to many specific text-based tasks.

Having read GPT-1, 2, 3, and a few other papers, this is the definition I like. It’s not a trivial definition, so let's break it down:

- **"is a language model"** → the inputs and predicted outputs are components of human written language (e.g. English). These components are not necessarily, and not typically, words. They may be characters, or character sequences (tokens).
- **"self-supervisedly trained"** → the dataset is *unlabelled* text from which (x,y) examples are produced. This was an important departure from task-specific, exspesive, labelled text datasets.
- **"next word predictor"** → the model is given a sequence of words/characters/tokens and must predict what comes next. "The cat in the" → "hat".
- **"easily adapted"** → no architectural changes are made to the model; model has few-shot, even one-shot capabilities.
- **"successfully adapted"** → achieve state of the art performance
- **"many specific text-based tasks"** → the model can perform classification, question-answering, parsing, and other text challenges with state-of-the-art performance. This is an important leap beyond task-specific language models which are good at one thing and bad at basically everything else.

I’ve conspicuously left out the “large” part of the LLM definition, but it’s implied by the success of the self-supervised generative training. Before a certain parameter size, this language model architecture didn’t work. Nowadays, the largest LLMs are 1000x larger than the smallest. 

I’ve also left out any tying down of the LLM category to the transformer architecture. Despite that being the most dominant LLM architecture, others exist (LSTM, Mamba, [Diffusion](https://x.com/InceptionAILabs/status/1894847919624462794)).

Everything else in the definition was I think key to GPT-1 and the ‘LLM moment’.

If you read the GPT-2 and GPT-3 papers they proceed almost straightforwardly from the success of GPT-1. 
Although GPT-1 does not include the words “large language model” at all, the latter papers do and refer to GPT-1 as such. 
So GPT-1 is an early LLM, and maybe the first, if its precedents—ULMFit, ELMo, and CoVE—can’t make the claim.

## Are any of CoVE, ELMo, and ULMFit LLMs?

<figure style="margin: 0; margin-bottom: 1.4em;">
  <img 
    src="/images/gpt-timeline.png" 
    alt="Timeline of GPT-1 showing its relationship to references discussed in this post." 
    style="border-radius: 0.4em; border: 2px solid #ddd;"
  >
  <figcaption style="color: #777;">Timeline of GPT-1 showing its relationship to references discussed in this post.</figcaption>
</figure>

[Contextualized Word Vectors (CoVE)](https://arxiv.org/pdf/1708.00107) were an important innovation in transfer learning but are not much like GPT-1. The CoVE vectors were created with supervised learning (on English to German translation) not self-supervised learning, and the vectors only become an initial component in a larger task-specific model.

<figure style="margin: 0; margin-bottom: 1em;">
  <img 
    src="/images/CoVE.png" 
    alt="“Figure 1: We a) train a two-layer, bidirectional LSTM as the encoder of an attentional sequence-tosequence model for machine translation and b) use it to provide context for other NLP models.”" 
    style="border-radius: 0.4em; border: 2px solid #ddd;"
  >
  <figcaption style="color: #777;">"Figure 1: We a) train a two-layer, bidirectional LSTM as the encoder of an attentional sequence-tosequence model for machine translation and b) use it to provide context for other NLP models.”</figcaption>
</figure>

[Embeddings From Language Models (ELMo)](https://arxiv.org/pdf/1802.05365) also trains word embeddings and bolts them into task-specific models. From GPT-1’s **Related Work** section:

> [ELMo and CoVE] use hidden representations from a pre-trained language or machine translation model as auxiliary features while training a supervised model on the target task. This involves a substantial amount of new parameters for each separate target task, whereas we require minimal changes to our model architecture during transfer.
> 

Neither of these is an LLM in my opinion, though for Alec Radford they were clearly stepping stones. Let’s turn to ULMFit then, which the GPT-1 authors say is the “closest line of work to ours”.

Universal Language Model Fine-tuning for Text Classification (ULMFit) is a next-word predictor LSTM self-supervisedly trained on WikiText, adaptable cheaply and without architecture changes to perform a number of text classification tasks with state-of-the-art performance. (Seeing how well ULMFit performed on the IMDb movie review dataset was a 🤯 moment for its author, Jeremy Howard.)

<figure style="margin: 0; margin-bottom: 1.4em;">
  <img 
    src="/images/ulmfit-architecture.png" 
    alt="Overview of the ULMFit architecture, with its quote 'intricate learning schemes' at middle and right." 
    style="border-radius: 0.4em; border: 2px solid #ddd;"
  >
  <figcaption style="color: #777;">Overview of the ULMFit architecture, with its "intricate learning schemes” at middle and right.</figcaption>
</figure>

This ULMFit seems a lot like GPT-1 and the above definition of an LLM. The only parts that are arguably not GPT-like are the ease of finetuning and the breadth of applied tasks. 
The GPT-1 paper fairly calls out the complexity of ULMFit’s “triangular learning rates” and “gradual unfreezing” of parameters. 
The GPT-1 paper also claims that by swapping at the LSTM architecture for the transformer they unlock wider task-specific competency than ULMFit by lengthening the prediction ability of the pre-trained model. 

After trawling back into the past, I’m satisified to call ULMFit the first LLM. This is surely arguable. I’ve not given much attention to Dai and Le’s 2015 [*Semi-supervised Sequence Learning*](https://arxiv.org/pdf/1511.01432) paper which was the other “closest line of work” called out in the GPT-1 paper. It’s also given more prominence than ULMFit in Radford’s [own 2020 history](https://www.youtube.com/watch?v=BnpB3GrpsfM) of the GPT moment.

Does being first even matter? I think it does, a bit. The software industry and academia honors its founders. We are all part of a culture that [homesteads the noosphere](https://en.wikipedia.org/wiki/Homesteading_the_Noosphere).


<div style="display: flex; justify-content: center;">
<blockquote class="twitter-tweet" data-conversation="none" data-dnt="true"><p lang="en" dir="ltr">ofc the real reason I&#39;m pushing back on this is that I&#39;m worried some folks might realise I didn&#39;t actually create the first LLM at on my own at <a href="https://t.co/GEOZunWoXj">https://t.co/GEOZunWoXj</a>, but that actually I&#39;m just a token figurehead for a CCP conspiracy that created it &amp; had me take credit</p>&mdash; Jeremy Howard (@jeremyphoward) <a href="https://twitter.com/jeremyphoward/status/1882964239520071926?ref_src=twsrc%5Etfw">January 25, 2025</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
</div>

Further to the point, understanding the non-OpenAI lineage of LLMs helps understand the competitive dynamics of the industry. 
Although OpenAI caught their competitors flatfooted, the LLM story was always multi-polar, multi-generational, and geographically diverse. 
With hindsight we may ask: if Australians can push forward the state-of-the-art, why not China?


## The last LLM

<script type="text/javascript" src="https://ssl.gstatic.com/trends_nrtr/4017_RC01/embed_loader.js"></script> <script type="text/javascript"> trends.embed.renderExploreWidget("TIMESERIES", {"comparisonItem":[{"keyword":"LLM","geo":"US","time":"today 5-y"}],"category":0,"property":""}, {"exploreQuery":"date=today%205-y&geo=US&q=LLM&hl=en","guestPath":"https://trends.google.com:443/trends/embed/"}); </script>

Having gone back to the start of the LLM craze, it’s made me curious as to when we’ll see the end of it. GPT-4V was the introduction of image understanding capabilities to the previously text-only model family, and since then the ‘frontier labs’ have gone multimodal. With ChatGPT, Claude, and Gemini adding image and audio processing, it not longer feels apt to call these language models. In place of LLM, we’re seeing increasing (but still minor) usage of “foundation model”. 

If I had to guess, I'd say that the term LLM sticks around. It will become like the graphics processing unit (GPU). 
The general public will eventually be using these models as video-in video-out, and they'll call them LLMs.
What started as a term for something that analyzed IMDb movie reviews will become a term for something that makes movies. 
At least, that's how I'll think about it. 

The first LLM was an LSTM pre-trained on Wikipedia and fine-tuned on IMDb movie reviews. 
GPT-1 crucially subbed in the transformer architecture, cutting out ULMFit's complexity and offering the industry a scaling ramp that will extend to [at least 2030](https://epoch.ai/blog/can-ai-scaling-continue-through-2030). 
Many, many more LLMs to come.

Strap in, and maintain attention on the road ahead.


<figure style="margin: 0; margin-top: 1.4em; margin-bottom: 1.4em;" class="magnify-container">
  <img 
    src="/images/scaling-till-2030.png" 
    alt="Extended LLM timeline till 2020, showing how much road is ahead." 
    style="border-radius: 0.4em; border: 2px solid #ddd;"
    class="magnify-image"
  >
  <div class="magnifying-glass"></div>
  <style>
    @media (hover: hover) {
      .magnify-container {
        position: relative;
        overflow: visible;
      }
      
      .magnifying-glass {
        display: none;
        position: absolute;
        width: 150px;
        height: 150px;
        border: 2px solid #fff;
        border-radius: 50%;
        pointer-events: none;
        background-repeat: no-repeat;
        box-shadow: 0 0 0 7px rgba(255, 255, 255, 0.85),
                    0 0 7px 7px rgba(0, 0, 0, 0.25),
                    inset 0 0 40px 2px rgba(0, 0, 0, 0.25);
      }

      .magnify-container:hover .magnifying-glass {
        display: block;
      }
    }
  </style>
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      const containers = document.querySelectorAll('.magnify-container');
      
      containers.forEach(container => {
        const img = container.querySelector('.magnify-image');
        const glass = container.querySelector('.magnifying-glass');
        
        container.addEventListener('mousemove', function(e) {
          const bounds = container.getBoundingClientRect();
          const x = e.clientX - bounds.left;
          const y = e.clientY - bounds.top;
          
          const magnification = 2;
          const glassRadius = glass.offsetWidth / 2;
          
          glass.style.left = `${x - glassRadius}px`;
          glass.style.top = `${y - glassRadius}px`;
          
          const bgX = x * magnification - glassRadius;
          const bgY = y * magnification - glassRadius;
          
          glass.style.backgroundImage = `url(${img.src})`;
          glass.style.backgroundSize = `${img.width * magnification}px ${img.height * magnification}px`;
          glass.style.backgroundPosition = `-${bgX}px -${bgY}px`;
        });
      });
    });
  </script>
</figure>


----

**Update:** @levelsio and Jeremy Howard [got into it over this question](https://x.com/jonobelotti_IO/status/1906086472349786595) on March 29th 2025. 
Out of that came feedback that I should pay more attention in the post to BERT ("ULMFiT's first demo predated BERT.") and the 2015 *Semi-supervised Sequence Learning* paper.
