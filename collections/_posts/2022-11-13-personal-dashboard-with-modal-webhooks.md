---
layout:     post
title:      "Create a personal dashboard with Modal webhooks"
date:       2022-11-13
summary:    Learn how to add live stats to your static personal website, integrating with Spotify, Goodreads, and Github.
categories: modal webhooks dashboard
---

This is a how-to post about [adding a dashboard](/about/#dashboard) to your personal website using Modal webhooks and third-party APIs.

I have long admired [the website](https://leerob.io/) of Vercel's Lee Robinson, particularly his personal dashboard.
His dashboard shows you various auto-updating metrics, including Github stars, Youtube views, and most listened Spotify tracks.
I love this. It's exactly the kind of website early internet-adopters thought would be common in the future. 

However, it takes a lot of
skill, love, and time to build up a personal website this feature-packed and polished. I wanted a dashboard myself, but this personal
website is a patchwork Jekyll static site first setup eight years ago, and rewriting it to adopt Robinson's [Next.js API routes](https://leerob.io/blog/fetching-data-with-swr)
solution was just too much effort.

Enter [_Modal web endpoints_](https://modal.com/docs/guide/webhooks).

## Solution overview

I made and shipped this personal dashboard solution only because it is very
easy to develop and very low maintenance. It uses tools I already know and regularly use: Jekyll, Python, HTML, Javascript.

* The web endpoint is a single `.py` file, and is deployed with _zero_ infra code or config.
* The dashboard page component is plain HTML stuck into my existing `about.md` Markdown file.

In about half a day I had a nice new dashboard up on this website, and it's as easy to maintain as the boring
and simple Github Pages + Jekyll website foundation. 

![screenshot of the new dashboard component]()

## Modal webhook

Hello my friend. This is the thing.

## Getting access to Spotify

todo

## Scraping Goodreads

todo

## Add pinch of <script> 

todo

## Extensions

todo

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
