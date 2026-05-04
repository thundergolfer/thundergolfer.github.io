---
layout: post
title: "Can an AI datacenter be beautiful?"
date: 2026-05-02
summary: Intelligence too cheap to meter. Industry too cheap to inspire.
categories: ai datacenters
permalink: beautiful-datacenter
side_footnotes: true
---

<figure class="abilene-hero" aria-label="A comparison of ugly and beautiful AI datacenters">
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
    One of eight buildings in the ongoing OpenAI Stargate Abilene project. (Move across the image to slide from ugly to beautiful.)
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

The computer industry has always had a weak relationship with beauty. Recently parts of the valley have become a bit self-conscious of their ugliness. We need a [“new aesthetic”](https://newaesthetics.art/) and billionaires will grant their couch coins for good ideas. Combine this self-consciousness with an AI datacenter backlash and you get the suggestion: **AI datacenters should be beautiful.**

Can our datacenters be beautiful? Architecturally, yes, absolutely. Datacenters are a box. Apply good architects to a box and you get the Institut du Monde Arabe in Paris. Most of the Twitter posting I've seen has offered the idea—perhaps novel to software engineers—that it is _possible_ to reskin a box. We could make them [12th century castle forts](https://x.com/Birdyword/status/2049932291393081620?s=20), or Parthenon de Plano, Texas. I've been thinking about datacenter economics a bit lately, and so I'd like to go a little further and work out the financing.

Can the trillion-dollar OpenAI _afford_ beauty?

<div style="display: flex; gap: 1rem; margin: 2rem 0;">
  <figure class="post-image" style="flex: 1 1 0; margin: 0;">
    <img src="/images/Institut-du-monde-arabe-in-Paris-Jean-Nouvel-8.jpg.webp" alt="Institute du Monde Arab in Paris by Jean Nouvel." style="aspect-ratio: 4 / 3; object-fit: cover;" />
    <figcaption>
      Institute du Monde Arab in Paris, Jean Nouvel.
    </figcaption>
  </figure>
  <figure class="post-image" style="flex: 1 1 0; margin: 0;">
    <img src="/images/satellite-photo-of-openais-stargate-project-football-field-v0-ll8erbwz051f1.webp" alt="Satellite image of Stargate Abilene, Texas." style="aspect-ratio: 4 / 3; object-fit: cover; object-position: bottom;" />
    <figcaption>
      Satellite image of Stargate Abeline, Texas.
    </figcaption>
  </figure>
</div>

## Ugly Stargate Abilene

Let's take the OpenAI Stargate project's Abilene, Texas site for our worked example. When finished this site will house 400,000 Nvidia GB200 (Blackwell) GPUs across
eight buildings. The image at the top of this post shows just two of those eight buildings.

ChatGPT 6.0 will gain exactly nothing in its benchmark scores from the prettiness of the walls of Stargate Abilene, Texas. Nevertheless, could it afford to grant us monkeys an eye opener? Absolutely it could.

My simple and approximate financial model puts the GPU-hour cost of Stargate Abilene at $1.826.

| Size of facility (critical load Megawatts)       | 1,000           |
| ------------------------------------------------ | --------------- |
| Average power usage (%)                          | 80%             |
| Power usage effectiveness (PUE)[^pue]            | 1.10            |
| Cost of power ($/kWh)                            | $0.07           |
| CAPEX for facility (excl. compute equipment)     | $5,000,000,000  |
| Number of GPUs                                   | 400,000         |
| Cost/GPU[^cost-gpu]                              | $30,000         |
| CAPEX for servers (incl. GPUs, excl. networking) | $15,000,000,000 |
| CAPEX for networking                             | $2,000,000,000  |
| Server amortization time[^server-amortization]   | 5 years         |
| Networking amortization time                     | 6 years         |
| Facilities                                       | 10 years        |
| Annual cost of money                             | 5%              |

[^pue]: Power usage effectiveness is total facility power divided by the amount of power which reaches the IT equipment. Hyperscalers have reached PUEs around 1.09-1.11 which is remarkable given industry averages were over 2.5 a few decades ago.

[^cost-gpu]: A GB200 chip is two B200 chips. Estimates of the cost of a B200 are around $40,000 USD. I dropped it to $30,000 to crudely account for the huge volume discount NVIDIA would give to OpenAI.

[^server-amortization]: Five years is a simplifying assumption for useful economic life, not a claim that the servers physically stop working after five years. In 2024 analysts were claiming that the NVIDIA H100 SXM5 had a depreciation term of only 3-4 years. This turned out to be very wrong. H100s are _increasing_ in price in early 2026, almost 4 years after release.

The bones of this breakdown come from the latest (7th) edition of the quantitative [Computer Architecture](https://shop.elsevier.com/books/computer-architecture/hennessy/978-0-443-15406-5) textbook from Patterson, Hennessy, and Kozyrakis. What's important to notice is that the capital
expenditure (CAPEX) for the IT equipment nearly dwarfs the cost of facilities, _and_ the IT equipment has a much shorter depreciation time.

To get to a per-GPU-hour cost we need to translate from CAPEX to operating expenditure (OPEX). Upfront costs combine with depreciation to become costs-over-time, and we add in ongoing service, maintenance, and operations cost, e.g. people! Assume 300 fully loaded staff at $250,000/year (generous). CAPEX costs are converted to monthly costs using a 5% capital recovery factor over each amortization period.

### Converting to OPEX

| **Expense (% total)** | **Category**         | **Monthly cost** | **% monthly cost** |
| --------------------- | -------------------- | ---------------- | ------------------ |
| CAPEX (88.0%)         | Servers              | $288.7M          | 67.7%              |
|                       | Networking           | $32.8M           | 7.7%               |
|                       | Facilities           | $54.0M           | 12.6%              |
| OPEX (12.0%)          | Monthly power use    | $45.0M           | 10.5%              |
|                       | Monthly people costs | $6.3M            | 1.5%               |
|                       | Total OPEX           | $51.2M           | 12.0%              |

Ugly Stargate Abeline is spending _75%_ of its monthlys on IT equipment alone. We're going to see just how cheap it is to buy beauty when your
datacenter cost sheet looks like this.

## Beautiful Stargate Abilene

<figure class="post-image" style="max-width: 750px; margin-left: auto; margin-right: auto;">
  <img src="/images/abilene-beautiful-2.jpeg" alt="Artist's impression of its home in Abeline." style="width: 100%; height: auto; display: block;" />
  <figcaption>Artist's impression of its home in Abeline.</figcaption>
</figure>

<figure class="post-image" style="margin: 2rem 0;">
  <div style="display: flex; gap: 1rem;">
    <img src="/images/monumental-1.jpeg" alt="Monumental architecture concept for a data center." style="flex: 1 1 0; width: 0; min-width: 0; object-fit: cover;" />
    <img src="/images/monumental-2.jpeg" alt="Monumental architecture concept for a data center." style="flex: 1 1 0; width: 0; min-width: 0; object-fit: cover;" />
    <img src="/images/monumental-3.webp" alt="Monumental architecture concept for a data center." style="flex: 1 1 0; width: 0; min-width: 0; object-fit: cover;" />
  </div>
  <figcaption>Some work done by Monumental Labs of NYC</figcaption>
</figure>

To turn this cluster of buildings into a soul warmer you need only raise the GPU-hour cost by **0.25%–0.5%**, to $1.830–$1.834 per GPU-hour.
Yes, half of one percent.

I've chosen here to beautify Stargate Abeline using the work of New York's [Monumental Labs](https://www.monumentallabs.co/). They use robotics
to dramatically drop the cost of producing stone ornamentation. They count a Stripe founder and a Coinbase founder amongst their customers, and recently completed restoration work at Carnegie Hall and The Frick in Manhattan.

| ------------------------------------------ | -------------- |
| Building wall surface area (square meters) | 240,000 |
| Stone cladding cost ($/square meter) | $500–$1,200/m² |
| 200 corbels[^monumental-list-prices] | $400,000 |
| 50 relief panels | $2,000,000 |
| 128 Ionic columns | $480,000 |
| Landscaping | $10,000,000 |
| Ornament amortization[^ornament-amortization] | 25 years |

[^ornament-amortization]: A nice thing about stone ornamentation is that it ages gracefully and thus holds its value over a very long time. It's not outlandish to say that it would need to be replaced every 50 or 100 years.

[^monumental-list-prices]: I'm using list prices from the website of Monumental Labs.

### OPEX

| **Expense (Category)** | **Monthly cost**            | **% monthly cost** |
| ---------------------- | --------------------------- | ------------------ |
| Landscape maintenance  | $200,000[^cost-landscaping] | 0.05%              |

With the stone cladding range, beautification adds $0.00422–$0.00847 per GPU-hour, or about $0.00634 at the midpoint. The new GPU-hour cost is $1.830–$1.834, with a midpoint of $1.832.

[^cost-landscaping]: "I mean it's one banana, Michael, what could it cost? Ten dollars?"

<figure class="post-image">
  <img src="/images/beautiful-abilene-cost-sankey.svg" alt="Sankey diagram showing that a beautiful Abilene data center would spend most monthly costs on servers, facilities, power, networking, and people, with beautification adding about 0.35 percent of total monthly cost." />
  <figcaption>
    Monthly cost apportionment at the midpoint beautification estimate.
  </figcaption>
</figure>

Even if my analysis is off by 10x, architectural beautification is absurdly cheap when GPU capital expenditure is at this scale.
I believe it does reinforce a sense of blindness and meagreness in Silicon Valley. In San Francisco one is surrounded by so much beauty—the Painted Ladies, the Palace of Fine Arts, of course the bridge. But tech made none of that. They adore the bridge, as they should, but it is a bridge they did not build.

It is plausible that this industry of immense wealth, one that can make a 22 year old in college sweatpants a billionaire, may fail to leave a legacy of public works. In my city, I walk with millions of others by the good works of a grocer (Woolworth), an automaker (Chrysler), and a steel magnate (Frick). In Brooklyn a sugar refinery is proudly restored next to a park named for it. Just five years ago a New York billionaire put in $200M for a [little park](https://en.wikipedia.org/wiki/Little_Island_at_Pier_55).

Maybe Silicon Valley's noble era is coming. They're in such a rush to cure cancer. But the population is clearly uneasy, and part of it is a sense that the Valley
is unendingly rapacious, that it lacks a public spirit, lacks vitality.

They might actually put a country full of Einsteins in a datacenter that looks like a Costco Wholesale. In the bad old days we had just one Einstein,
but we at least put him in a building worthy of his work and caring for the people that walked by its walls.

<figure class="post-image">
  <img src="/images/prussian-academy-of-sciences.jpg" alt="Prussian Academy of Sciences building." />
</figure>
