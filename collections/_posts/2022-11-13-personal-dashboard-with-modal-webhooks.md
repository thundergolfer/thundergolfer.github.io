---
layout:     post
title:      "Create a personal dashboard with Modal webhooks"
date:       2022-11-13
summary:    Learn how to add live stats to your static personal website, integrating with Spotify, Goodreads, and Github.
categories: modal webhooks dashboard
---

This is a how-to post about [adding a dashboard](/about/#dashboard) to your personal website using Modal webhooks and third-party APIs.

![screenshot of the new dashboard component](/images/personal-dashboard-with-modal/screenshot.png)

I have long admired [the website](https://leerob.io/) of Vercel's Lee Robinson, particularly his personal dashboard.
His dashboard shows you various auto-updating metrics, including Github stars, Youtube views, and most listened Spotify tracks.
I love this. It's exactly the kind of website early internet-adopters thought would be common in the future. 

However, it takes a lot of
skill, love, and time to build up a personal website this feature-packed and polished. I wanted a dashboard myself, but this personal
website is a patchwork [Jekyll](https://jekyllrb.com/) static site first setup eight years ago, and rewriting it to adopt Robinson's [Next.js API routes](https://leerob.io/blog/fetching-data-with-swr)
solution was just too much effort.

Enter [_Modal web endpoints_](https://modal.com/docs/guide/webhooks).

## Solution overview

I made and shipped this personal dashboard solution only because it is very
easy to develop and very low maintenance. It uses tools I already know and regularly use: Jekyll, Python, HTML, Javascript.

* The web endpoint is a single `.py` file, and is deployed with _zero_ infra code or config to [Modal](https://modal.com).
* The dashboard page component is plain HTML stuck into my existing `about.md` Markdown file at [github.com/thundergolfer/thundergolfer.github.io](https://github.com/thundergolfer/thundergolfer.github.io).

In about half a day I had a nice new dashboard up on this website, and it's as easy to maintain as the boring
and simple Github Pages + Jekyll website foundation. 

<h2>
    <span style="color: rgb(187, 255, 170); background-color: rgb(27, 27, 27); padding: 3px; border-radius: 4px">Modal webhook</span>
</h2>

The basic problem to solve is that static sites can't show users dynamic data, such as my constantly changing
Spotify listen history or the reading history I maintain in Goodreads. The Jekyll framework builds a fixed set
of `.html` and `.css` files on push to Github, and that's all users get until I push another change.

What I need is something my static HTML 'About me' page can send an XMLHTTPRequest to on load, which will return
up-to-date data for rendering. That something should be simple and cheap to run. A webhook, basically.

A Modal webhook is a serverless endpoint that run Python code, supporting the excellent FastAPI out-of-the-box.
My dashboard webhook application does just two things. It accepts a GET request at `/`, and uses a Python function
called `about_me()` to gather dashboard stats as a dictionary for FastAPI to send back to the client as JSON.

Let's get a bit more into the details.

### Responding to GET requests

The following is all the code needed to get a serverless Modal endpoint to return JSON.

```python
import modal
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

stub = modal.Stub("dash")
web_app = FastAPI()

def about_me():
    return {"dummy": "data"}


@web_app.get("/")
def hook(response: Response):
    response.headers["Cache-Control"] = "max-age=43200"
    return about_me()

@stub.asgi
def web():
    web_app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://thundergolfer.com","http://localhost:4000"],
        allow_methods=["*"], allow_headers=["*"],
    )
    return web_app
```

A asynchronous server gateway interface ([ASGI](https://asgi.readthedocs.io/en/latest/)) app is instantiated
and hooked into Modal by returning it from a function decorated with `@stub.asgi`. 

Deploy this on Modal and you'll immediately be able to hit the endpoint with `curl`. You'll get this:

```bash
curl https://thundergolfer-cgflgpx.modal.run/
{"dummy": "data"}%
```

That ain't interactive dashboard data because all `about_me()` does is return static placeholder data. Soon
I'll show how that function becomes extended to make authenticated requests against Spotify to retrieve top tracks.
But it's a start!

#### Making the browser happy: CORS, caching

Most of the complexity in the above snippet comes from needing to support [CORS](https://fastapi.tiangolo.com/tutorial/cors/) and caching the JSON response in the browser for 12 hours (43,200 seconds).

My website is served from the `thundergolfer.com` domain but the webhook is served from a Modal domain (`modal.run`).
By default the browser will prevent data (ie. resource) sharing between different domains because it's insecure.
But with the `CORSMiddleware` the web endpoitn can communicate that it allows sharing with my domains.

The `Cache-Control` header is set to minimize re-requests to the web endpoint. With this header, your browser
will disk cache the endpoint's JSON response for 12 hours. Try repeatedly refreshing [my about page](/about#dashboard) to see this working; the dashboard component loads instantly from the 2nd request onwards.


<aside>
<div class="callout-panel callout-panel-info">
    <span class="callout-panel-icon callout-panel-info-icon">
        <span class="" role="img" aria-label="Heads up">👋</span>
    </span>
    <div class="ak-editor-panel__content">
        <p data-renderer-start-pos="97">
            Code for the webhook is at <a target="_blank" rel="noopener noreferrer" href="https://github.com/thundergolfer/modal-fun/blob/main/thundergolferdotcom-dash/">github.com/thundergolfer/modal-fun</a>.
        </p>
    </div>
</div>
</aside>


## Getting access to Spotify

todo

## Scraping Goodreads

todo

## Add pinch of \<script\> 

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
