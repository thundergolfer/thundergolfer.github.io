---
layout:     post
title:      Digital Reasoning. What They Do and Why I'm Interested
date:       2016-09-05
summary:    During an internship search this company caught my eye, so I'm looking further into them.
categories: internship review general
---

<div class="callout-panel callout-panel-info">
    <span class="callout-panel-icon callout-panel-info-icon">
        <span class="" role="img" aria-label="Panel info">
            <svg width="24" height="24" viewBox="0 0 24 24" focusable="false" role="presentation">
                <path d="M12 20a8 8 0 1 1 0-16 8 8 0 0 1 0 16zm0-8.5a1 1 0 0 0-1 1V15a1 1 0 0 0 2 0v-2.5a1 1 0 0 0-1-1zm0-1.125a1.375 1.375 0 1 0 0-2.75 1.375 1.375 0 0 0 0 2.75z" fill="currentColor" fill-rule="evenodd"></path>
            </svg>
        </span>
    </span>
    <div class="ak-editor-panel__content">
        <p data-renderer-start-pos="97">
            One of this company's ML engineers, <a href="https://twitter.com/iamtrask?lang=en">Andrew Trask</a>, eventually went on to join Deepmind and is now a leader in privacy-first AI.
        </p>
    </div>
</div>

I read through Digital Reasoning's [Technology Review of their *Synthesys* System](http://www.digitalreasoning.com/resources/Synthesys_v3.9_Technology_Overview_FINAL_Jan_2015.pdf), which is their main commercial product offering.

### This is a cool company

Digital Reasoning (DR) starts off outlining their playground, the booming world of unstructured-data. Unstructured-data, apparently a whole new class of economic asset, is filled with mysteries, and stories, and conspiracies. DR sets itself up as a company to build new approaches to understanding human communication in unstructured datasets, and their work will have huge utility to the financial and intelligence communities in particular (their targets I assume).

As described, DR's Synthesys machine learning platform seems to be a straightforward application of supervised learning techniques, in the realm of natural language, and some unsupervised learning as well. The mention that unsupervised techniques are used in their analytics, but don't ever expand on it. I could guess that they use it for anomaly detection, given their work with fraud detection.

In section 1.3, DR detail a few of the tools they employee in Synthesys; Hadoop, Cassandra and Accumulo to name a few. These tools manage data storage and retrieval and I'm pretty sure they're open-source so I'll be able to get to know them.

As a system, DR identifies Synthesys as having a *READ*, *RESOLVE*, and *REASON* phase. Here's how they describe them:

> The “Read” phase ingests the data and performs Natural Language Processing (NLP), entity
extraction, and fact extraction. The “Resolve” phase assembles, organizes, and relates the results
from the “Read” phase to perform global concept resolution (i.e. entity resolution) and detect
synonyms (i.e. synonym generation) and closely related concepts. The final “Reason” phase
applies spatial and temporal reasoning and uncovers relationships that allow resolved entities to
be compared and correlated using advanced graph analysis techniques. These three phases of
analysis are performed in a distributed processing environment, and their results are stored into a
unified entity storage architecture called a Knowledge Base (KB).

How exactly they implement their *spatial and temporal reasoning* would be really interesting, as well as seeing how exactly a *Unified Entity Storage Architecture* is organised.

...and I've read a little further and apparently is a "combination of persistent storage and intelligent data caching". A little clearer but I still essentially have no idea how to begin building that.

DR's report then gets even more specific about what's going on in the Read, Resolve, and Reason steps. It's detailed enough to sketch out their system and possibly build an ugly-sister of Synthesys if you had a lot of free time.

The technology report closes out with some less interesting (to me) information about information retrieval query systems and APIs. Once all the work has been done to put it all together, DR makes the effort so that it isn't a headache for clients to pull the good stuff out.


### Takeaway

The work these guys do, and the intention behind it, seems right up my alley. For me the most interesting thing about tech at the moment is how machine learning can be used to understand the motivations, beliefs and goals of large numbers of people.

They aren't a big company, online searches put their revenue between $5M and $10M, but the work they do is interesting and their CEO seems great.

There's also already a review from an intern up on Glassdoor for DR, so it is possible to intern there. Here's hoping.


<style>
.callout-panel {
    border-radius: 3px;
    margin: 1.145rem 0px 1rem 0px;
    padding: 12px;
    min-width: 48px;
    display: flex;
    /*-webkit-box-align: baseline;*/
    /*align-items: baseline;*/
    word-break: break-word;
    border: none;
}

.callout-panel p {
    margin-bottom: 0;
    line-height: 24px;
}

.callout-panel-icon {
    display: block;
    flex-shrink: 0;
    height: 24px;
    width: 24px;
    box-sizing: content-box;
    padding-right: 8px;
    color: rgb(0, 82, 204);
}

.callout-panel-info {
    background-color: rgb(222, 235, 255);
}

.callout-panel-info-icon {
    color: blue;
}

</style>
