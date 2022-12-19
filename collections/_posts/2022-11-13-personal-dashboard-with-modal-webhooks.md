---
layout: post
title: "Create a personal dashboard with Modal webhooks"
date: 2022-11-13
summary: Learn how to add live stats to your static personal website, integrating with Spotify, Goodreads, and Github.
categories: modal webhooks dashboard
---

This is a how-to post about [adding a dashboard](/about/#dashboard) to your personal website using Modal webhooks and third-party APIs.

![screenshot of the new dashboard component](/images/personal-dashboard-with-modal/screenshot.png)

I have long admired [the website](https://leerob.io/) of Vercel's Lee Robinson, particularly his personal dashboard.
The dashboard shows you various auto-updating metrics, including Github stars, Youtube views, and most listened Spotify tracks.
I love this. It's exactly the kind of website early and optimisitic netizens thought would predominate in the future.

However, it takes a lot of
skill, love, and time to build up a personal website that feature-packed and polished. I wanted a dashboard myself, but my personal
website — the one you're on right now — is a patchwork [Jekyll](https://jekyllrb.com/) static site first setup eight years ago, and rewriting it to adopt Robinson's [Next.js API routes](https://leerob.io/blog/fetching-data-with-swr)
solution was just too much effort.

But then came [Modal web endpoints](https://modal.com/docs/guide/webhooks).

## Solution overview

I was able to sit down and ship this personal dashboard solution only because it is very
easy to develop and very low maintenance. It uses tools I already know and regularly use: Jekyll, Python, HTML, Javascript. You probably know all these too.

The setup is two parts: the **data**, provided by a web endpoint, and the **view**, implemented by HTML and JS.

- **data:** the dash stats are served by a JSON web endpoint defined by a single `.py` module and deployed with _zero_ infra code or config to [Modal](https://modal.com).
- **view:** the dashboard UI component is plain HTML and JS stuck at the end of my existing `about.md` Markdown file in [github.com/thundergolfer/thundergolfer.github.io](https://github.com/thundergolfer/thundergolfer.github.io).

In about half a day I had a nice new dashboard up on this website, and it's as easy to maintain as the website's boring
and simple Github Pages + Jekyll foundation.

<h2>
    <span style="color: rgb(187, 255, 170); background-color: rgb(27, 27, 27); padding: 3px; border-radius: 4px">Modal web endpoint</span>
</h2>

The basic data problem to solve is that static sites can't show a user's dynamic data, such as my constantly changing
Spotify listen history or the reading history I maintain in Goodreads. The Jekyll framework builds a fixed set
of `.html` and `.css` files on push to Github, and nothing updates until I `git push` another change.

The dashboard solution needs something a static HTML 'About me' page can fire an XMLHTTPRequest request at on load, returning up-to-date data for rendering by the view. That something should be simple and cheap to run.

A Modal webhook is a serverless endpoint that executes Python code, supporting the excellent FastAPI out-of-the-box.
My dashboard application uses this, and does just two things. It accepts a GET request at `/`, and calls a Python function
named `about_me()` to build a dashboard stats `dict` for FastAPI to send back to the browser client as JSON.

<aside>
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
            A <a target="_blank" rel="noopener noreferrer" href="https://workers.cloudflare.com/">Cloudflare Webworker</a> is an alternate option here. Doesn't support Python though.
        </p>
    </div>
</div>
</aside>

Let's get a bit more into the details.

### Responding to GET requests

The following is all the code needed to have a serverless Modal endpoint return some JSON to clients.

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

In the code above, an asynchronous server gateway interface ([ASGI](https://asgi.readthedocs.io/en/latest/)) app is instantiated
and hooked into Modal by returning the app from a function decorated with Modal's `@stub.asgi` decorator.

Deploy this on Modal and you'll immediately be able to hit the endpoint with `curl`.

```bash
curl https://thundergolfer-cgflgpx.modal.run/
{"dummy": "data"}%
```

No interactive dashboard stats yet because all `about_me()` does is return static placeholder data. Soon
I'll show how that function becomes extended to make authenticated requests against Spotify to retrieve top tracks.
But a working webhook is a start!

#### Making the browser happy: CORS, caching

Most of the complexity in the above snippet comes from needing to support [CORS](https://fastapi.tiangolo.com/tutorial/cors/) and cache the JSON response in the browser for 12 hours (43,200 seconds).

My website is served from the `thundergolfer.com` domain but the webhook is served from a Modal domain (`modal.run`).
By default the browser will prevent data sharing between different domains because it's a security risk.
But with the `CORSMiddleware` a web endpoint can communicate that it allows data sharing with my personal domain.

The `Cache-Control` header is set to minimize re-requests to the web endpoint. With this header, your browser
will disk-cache the endpoint's JSON response for 12 hours. Try repeatedly refreshing [my about page](/about#dashboard) to see this working; the dashboard component loads instantly from the 2nd request onwards.

<aside>
<div class="callout-panel callout-panel-info">
    <span class="callout-panel-icon callout-panel-info-icon">
        <span class="" role="img" aria-label="Heads up">👋</span>
    </span>
    <div class="ak-editor-panel__content">
        <p data-renderer-start-pos="97">
            All code for the webhook is at <a target="_blank" rel="noopener noreferrer" href="https://github.com/thundergolfer/modal-fun/blob/main/thundergolferdotcom-dash/">github.com/thundergolfer/modal-fun</a>.
        </p>
    </div>
</div>
</aside>

## Getting access to Spotify

In order for the web endpoint to provide up-to-date listening stats to clients, it needs to authenticate against
Spotify's APIs and access my private Spotify account data.

Getting this done will require creating a Spotify developer app, setting a Modal secret, and crudely implementing
an OAuth flow. This should all take about 10-15 minutes.

### Spotify developer app setup

![Spotify developers apps webpage](/images/personal-dashboard-with-modal/spotify-dev-app.png)

First, we need to create a Spotify application to give us credentials to authenticate with the API.

1. Go to your [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and log in.
2. Click **Create an App**.
3. Fill out the name and description and click **create**.
4. Click **Show Client Secret**.
5. Save your Client ID and Secret. You'll need these soon.
6. Click **Edit Settings**.
7. Add `http://localhost:3000` as a **redirect URI**. (This address won't be used, but it needs to match what's in our code)

Done! You now have a properly configured Spotify application and the correct credentials to make requests.

(Don't worry about the app being in _developer mode_. That mode is fine for our purposes.)

<h3>
    <span style="color: rgb(187, 255, 170); background-color: rgb(27, 27, 27); padding: 3px; border-radius: 4px">Modal secret</span>
</h3>

With the Client ID and Secret you saved just before, populate and execute the following command:

```bash
modal secret create "spotify-about" SPOTIFY_CLIENT_ID="..." SPOTIFY_CLIENT_SECRET="..."
```

With that done, we'll be able to run some code to complete an OAuth flow for the Spotify app
and acquire a `refresh_token` which will allow the webhook to access private personal listening information
via API.

### Doing the OAuth flow to get a refresh_token

```python
# main.py
import base64
import json
import os
import urllib.parse
import urllib.request


def manual_spotify_auth() -> None:
    redirect_uri = urllib.parse.quote("http://localhost:3000/callback", safe="")
    authorize_url = (
        "https://accounts.spotify.com/"
        f"authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={redirect_uri}"
        "&scope=user-read-currently-playing%20user-top-read"
    )

    code = input(
        f"Visit \n{authorize_url}\n and then paste back the code found in the URL.\nCode: "
    ).strip()

    with stub.run():
        refresh_token = create_spotify_refresh_token(code)
    print(f"SPOTIFY_REFRESH_TOKEN: {refresh_token}")
    print(
        "Save the refresh_token back into the `spotify-aboutme` secret in Modal as SPOTIFY_REFRESH_TOKEN"
    )


@stub.function(secret=modal.Secret.from_name("spotify-aboutme"))
def create_spotify_refresh_token(code: str):
    auth_str = os.environ["SPOTIFY_CLIENT_ID"] + ":" + os.environ["SPOTIFY_CLIENT_SECRET"]
    encoded_client_id_and_secret = base64.b64encode(auth_str.encode()).decode()
    req = urllib.request.Request(
        "https://accounts.spotify.com/api/token",
        data=urllib.parse.urlencode(
            {
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": "http://localhost:3000/callback",
            }
        ).encode(),
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
            "Authorization": f"Basic {encoded_client_id_and_secret}",
        },
    )
    response = urllib.request.urlopen(req).read().decode()
    return json.load(response)["refresh_token"]

if __name__ == "__main__":
    manual_spotify_auth()
```

Run this module and follow the URLs and printed instructions.
We only need to do this step once, so it's fine that it is human-in-the-loop. Notice that the second function
is a Modal function, with access to the `spotify-aboutme` secret created earlier. This means that when you do
`python3 main.py` the first function, `manual_spotify_auth()`, will run on your computer and the second function will
_run in the cloud_.

We could have had this function run locally and populated our terminal environment with the `SPOTIFY_*` variables, but it's nice to test that our Modal Secret is setup properly.

If you've done things correctly, you should see a `SPOTIFY_REFRESH_TOKEN` in your terminal output.
Go to [modal.com/secrets](https://modal.com/secrets) and update the `spotify-aboutme` secret to include this
new value.

Now with the Modal Secret having all three `SPOTIFY_` values, you're web endpoint is able to retreive personal listening
stats. I won't copy in all the code that does that into the post. Just go to the full source and check out this function:

```python
def request_spotify_top_tracks(max_tracks=5) -> list[SpotifyTrack]:
    ...
```

## Scraping Goodreads

In the interest of brevity, I won't go into detail on this bit of the dashboard. I needed a PyPi package, _BeautifulSoup_,
so I created a `modal.Image` and attached that to the function that scrapes my Goodreads profile:

```python
bs4_image = modal.Image.debian_slim().pip_install(["beautifulsoup4"])
# >--SNIP--<
@stub.function(image=bs4_image)
def request_goodreads_reads(max_books=3) -> list[Book]:
    from bs4 import BeautifulSoup
    ...
```

The rest is just classic DOM munging, aided by the Modal Function's `interactive=True` feature which lets you drop into an IPython terminal in the middle of a remotely executing function.

<aside>
<div class="callout-panel callout-panel-info">
    <span class="callout-panel-icon callout-panel-info-icon">
        <span class="" role="img" aria-label="Heads up">👋</span>
    </span>
    <div class="ak-editor-panel__content">
        <p data-renderer-start-pos="97">
            <strong>Reminder:</strong> All code for the webhook is at <a target="_blank" rel="noopener noreferrer" href="https://github.com/thundergolfer/modal-fun/blob/main/thundergolferdotcom-dash/">github.com/thundergolfer/modal-fun</a>, including the <code>request_goodreads_reads()</code> fn.
        </p>
    </div>
</div>
</aside>

## A stats-filled `about_me()`

Once you have Modal functions that acquire Spotify and Goodreads stats, the webhook is almost done.
The main thing remaining was to add some caching. I found that the `about_me()` function took 600-1000ms
to finish, probably because sequential requests to Spotify's API and then Goodreads is slow.

Because my reading and track listening stats are very slow changing, there's no need to keep calculating them.
We can cache every with a [`modal.Dict`](https://modal.com/docs/reference/modal.Dict):

```python
stub = modal.Stub(name="thundergolferdotcom-about-page")
stub.cache = modal.Dict()
CACHE_TIME_SECS = 60 * 60 * 12

# >--SNIP--<

@stub.function(secret=modal.Secret.from_name("spotify-aboutme"))
def about_me():
    from modal import container_app
    # Cache the retrieved data for 10x faster endpoint performance.
    now = int(time.time())
    try:
        (store_time, response) = container_app.cache["response"]
        if now - store_time <= CACHE_TIME_SECS:
            return response
    except KeyError:
        pass

    # >--SNIP--<

    response = dataclasses.asdict(stats)
    container_app.cache["response"] = (now, response)
    return response
```

This is how you cache a result for 12 hours using a [`modal.Dict`](https://modal.com/docs/reference/modal.Dict). With this caching in place, end-to-end
latency on a warm webhook request was about 60ms, rather than 600ms.

## Add pinch of \<script\>

That's the JSON web endpoint accounted for, but the static HTML page at [thundergolfer.com/about](https://thundergolfer.com) needs to actually _use it_. This happens with a standalone `<script>` in the Markdown page.

```html
<!-- /about.md -->

<div id="stats" class="hidden">
  <div id="recent-finished-books"></div>
  <ol id="top-spotify-tracks"></ol>
</div>

<script>
  function htmlToElement(html) {
      var template = document.createElement('template');
      html = html.trim();
      template.innerHTML = html;
      return template.content.firstChild;
  }

  function populateDashboardHTML(data) {
      const topSpotifyTracksList = document.querySelector('#top-spotify-tracks');
      data.spotify.forEach(track => {
          topSpotifyTracksList.appendChild(htmlToElement(`
              <li>
                  <a href="${track.link}">
                      <strong>${track.name}</strong>
                  </a>
                  <p>${track.artist}</p>
              </li>
          `));
      });
      const recentFinishedBooks = document.querySelector('#recent-finished-books');
      data.goodreads.slice(0, 3).forEach(book => { ... });
  }

  fetch('https://thundergolfer-cgflgpx.modal.run')
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      return response.json();
    })
    .then((data) => {
      populateDashboardHTML(data);
      /* Reveal the now populated stats section. */
      document.getElementById("stats").classList.remove("hidden");
    });
</script>
```

The Goodreads HTML hydration code and some CSS is omitted for brevity, but this is basically everything!
On page load `fetch` issues an XMLHTTPRequest to my deployed web endpoint and once this is complete a JS
function is called to populate the a `<div>` before it is revealed on the page.

## Extensions

There's so many additions we could make to this personal dashboard: [Strava](https://www.strava.com/), Youtube,
[Letterboxd](https://letterboxd.com/), Pocket, Twitter, Apple Photos, the list goes on.

The next move for me is Github, but that's a project for another weekend :)

![icons of possible dashboard stats sources](/images/personal-dashboard-with-modal/extensions.png)

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

<script>
var dashLinks = document.querySelectorAll("a[href='/about/#dashboard']");
dashLinks.forEach((link) => link.addEventListener("mouseover", wakeWebhook));
async function wakeWebhook(event) {
    await fetch('https://thundergolfer-cgflgpx.modal.run');
};
</script>
