---
layout: post
title: "Can an AI datacenter be beautiful?"
date: 2026-05-02
summary: “TODO”
categories: ai datacenters
permalink: beautiful-datacenter
---

<figure class="abilene-hero" aria-label="A comparison of ugly and beautiful AI data centers">
  <div class="abilene-hero__frame">
    <img
      class="abilene-hero__image"
      src="/images/abilene-ugly.avif"
      alt="An unornamented AI data center in Abilene, Texas."
    />
    <div class="abilene-hero__beautiful" aria-hidden="true">
      <img
        class="abilene-hero__image"
        src="/images/abilene-beautiful.jpeg"
        alt=""
      />
    </div>
    <span class="abilene-hero__handle" aria-hidden="true"></span>
  </div>
  <figcaption>
    One of eight building in the ongoing OpenAI Stargate Abilene project. (Move across the image to slide from ugly to beautiful.)
  </figcaption>
</figure>

<script>
  (function () {
    const hero = document.querySelector(".abilene-hero");
    const frame = hero && hero.querySelector(".abilene-hero__frame");

    if (!frame) {
      return;
    }

    function setReveal(event) {
      const bounds = frame.getBoundingClientRect();
      const x = Math.min(Math.max(event.clientX - bounds.left, 0), bounds.width);
      const reveal = (x / bounds.width) * 100;

      frame.style.setProperty("--hero-reveal", reveal + "%");
    }

    frame.addEventListener("pointerenter", function (event) {
      frame.classList.add("is-interacting");
      setReveal(event);
    });

    frame.addEventListener("pointermove", setReveal);

    frame.addEventListener("pointerleave", function () {
      frame.classList.remove("is-interacting");
    });
  })();
</script>

The computer industry has always had a weak relationship with beauty. Perhaps only the medical industry, with its 5000K spike spectra white fluorescent lighting and scrubs, sits below computing as the field into which so much so much care and wealth has been poured with so little resulting that you would want to look at, touch, and hear. Silicon Valley today is seriously concerned with “taste”, a friend of beauty. But for the valley elite taste is a private club with ineffable rules of application. If you have taste you get to make the next decacorn CRM or issue tracker.

Recently parts of the valley have become a bit self-conscious of their ugliness. We need a [“new aesthetic”](https://newaesthetics.art/) and those with ideas may be granted 0.000001% of the industry’s wealth. Combine this self-consciousness with an AI data center backlash and you get the suggestion: AI data centers should be beautiful.

Can our data centers be beautiful? Architecturally, yes, absolutely. Data centers are a box. Apply good architects to a box and you get the Institut du Monde Arabe in Paris. But can OpenAI afford it?

<figure class="post-image">
  <img src="/images/Institut-du-monde-arabe-in-Paris-Jean-Nouvel-8.jpg.webp" alt="Institute du Monde Arab in Paris by Jean Nouvel." />
  <figcaption>
    Institute du Monde Arab in Paris, Jean Nouvel.
  </figcaption>
</figure>

## Ugly Stargate Abilene

Let's take the OpenAI Stargate project's Abilene, Texas site for our worked example. When finished this site will house 400,000 Nvidia GB200 (Blackwell) GPUs across
eight buildings. The image at the top is just two of those eight buildings.

ChatGPT 6.0 will gain exactly nothing in its benchmark scores from the prettiness of the walls of Stargate Abilene, Texas. but could it afford to grant us monkeys an eye opener?

This simple and approximate financial model puts the GPU-hour cost of Stargate Abilene at $1.826.

| Size of facility (critical load Megawatts)   | 1,000          |
| -------------------------------------------- | -------------- |
| Average power usage (%)                      | 80%            |
| Power usage effectiveness (PUE)[^pue]        | 1.10           |
| Cost of power ($/kWh)                        | $0.07          |
| CAPEX for facility (excl. compute equipment) | $5,000,000,000 |
| Number of GPUs                               | 400,000        |

| Cost/GPU[^cost-gpu] | $30,000 |
| CAPEX for servers (incl. GPUs, excl. networking) | $15,000,000,000 |
| CAPEX for networking | $2,000,000,000 |
| Server amortization time[^server-amortization] | 5 years |
| Networking amortization time | 6 years |
| Facilities | 10 years |
| Annual cost of money | 5% |

[^pue]: Power usage effectiveness is total facility power divided by the amount of power which reaches the IT equipment. Hyperscalers have reached PUEs around 1.09-1.11 which is remarkable given industry averages were over 2.5 a few decades ago.

[^cost-gpu]: A GB200 chip is two B200 chips. Estimates of the cost of a B200 are around $40,000. I dropped it to $30,000 to crudely account for the huge volume discount NVIDIA would give to OpenAI.

[^server-amortization]: Five years is a simplifying assumption for useful economic life, not a claim that the servers physically stop working after five years. In 2024 analysts were claiming that the NVIDIA H100 SXM5 had a depreciation term of only 3-4 years. This turned out to be very wrong. H100s are _increasing_ in price in early 2026, almost 4 years after release.

Assume 300 fully loaded staff at $250,000/year. CAPEX costs are converted to monthly costs using a 5% capital recovery factor over each amortization period.

OPEX

| **Expense (% total)** | **Category**         | **Monthly cost** | **% monthly cost** |
| --------------------- | -------------------- | ---------------- | ------------------ |
| CAPEX (88.0%)         | Servers              | $288.7M          | 67.7%              |
|                       | Networking           | $32.8M           | 7.7%               |
|                       | Facilities           | $54.0M           | 12.6%              |
| OPEX (12.0%)          | Monthly power use    | $45.0M           | 10.5%              |
|                       | Monthly people costs | $6.3M            | 1.5%               |
|                       | Total OPEX           | $51.2M           | 12.0%              |

## Beautiful Stargate Abilene

<figure style="display: flex; gap: 1rem; margin: 2rem 0;">
  <img src="/images/monumental-1.jpeg" alt="Monumental architecture concept for a data center." style="flex: 1 1 0; width: 0; min-width: 0; object-fit: cover;" />
  <img src="/images/monumental-2.jpeg" alt="Monumental architecture concept for a data center." style="flex: 1 1 0; width: 0; min-width: 0; object-fit: cover;" />
  <img src="/images/monumental-3.webp" alt="Monumental architecture concept for a data center." style="flex: 1 1 0; width: 0; min-width: 0; object-fit: cover;" />
</figure>

That’s ugly Stargate. To turn this cluster of building into a soul warmer you need only raise the GPU-hour cost by **0.25%–0.5%**, to $1.830–$1.834 per GPU-hour.

| Building wall surface area (square meters) | 240,000        |     |
| ------------------------------------------ | -------------- | --- |
| Stone cladding cost ($/square meter)       | $500–$1,200/m² |     |
| 200 corbels                                | $400,000       |     |
| 50 relief panels                           | $2,000,000     |     |
| 128 Ionic columns                          | $480,000       |     |
| Landscaping                                | $10,000,000    |     |
| Ornament amortization                      | 25 years       |     |

OPEX

| **Expense (Category)** | **Monthly cost** | **% monthly cost** |
| ---------------------- | ---------------- | ------------------ |
| Landscape maintenance  | $200,000         | 0.05%              |

With the stone cladding range, beautification adds $0.00422–$0.00847 per GPU-hour, or about $0.00634 at the midpoint. The new GPU-hour cost is $1.830–$1.834, with a midpoint of $1.832.

<figure class="post-image">
  <img src="/images/beautiful-abilene-cost-sankey.svg" alt="Sankey diagram showing that a beautiful Abilene data center would spend most monthly costs on servers, facilities, power, networking, and people, with beautification adding about 0.35 percent of total monthly cost." />
  <figcaption>
    Monthly cost apportionment at the midpoint beautification estimate.
  </figcaption>
</figure>

A bridge they did not build.

An industry of immense wealth, one that can make a 22 year old in college sweatpants a billionaire, would fail to leave a legacy on the earth. In my city, I walk with millions of others by the good works of a grocer (Woolworths), an automaker (Chrysler), and a Y. In Brooklyn a sugar refinery is proudly restored next to a park named for it.

![A beautiful AI data center in Abilene, Texas.](/images/abilene-beautiful-2.jpeg)
