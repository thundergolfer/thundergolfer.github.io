---
layout: post
title: "Create an email newsletter from an RSS feed with Modal"
date: 2022-12-10
summary: I built an automated email newsletter feature for my blog. Learn how to set it up for yourself.
categories: modal newsletter email
---

This is a how-to post showing how to run an email subscribers list for your personal website using Modal webhooks and Gmail API.
The application functionality allows a blog maintainer to accept and manage email suscribers who will automatically receive notifications
when the maintainer publishes a new post to their RSS feed. This Jekyll static site you're reading has [RSS support built-in](/feed.xml), and
most other static site generating software does as well.

![screenshot of the new email subscriber call-to-action component](/images/email-subs-with-modal/hero.png)

Besides the RSS feed, this newsletter solution requires only two other things: a [Gmail](https://www.google.com/gmail/about/) account and a [Modal](https://modal.com/) account.
Both are free to setup, so do that before proceeding 🙂.

Once you have those three things, we're ready to start!

## 1. Gmail API setup

- I didn't have Google Workspaces with my personal Google Account so needed to create an 'External OAuth' app
- This is fine because Google will put the app in 'testing mode' and still allow me to authenticate my own email account.
  - This is similar to how it works for Spotify (link to my dashboards post)
- Fill in the form, adding links to your personal website and whatever logo you want. Only you should ever need to see this consent screen
- Adding scopes:

## 2. Modal app setup

While I would prefer to inline all the code for this solution into the blog post, it would be too much, so I will
just provide a summary of its structure. The code is heavily documented so as to be beginner friendly, and shouldn't
require modification besides changing some configuration values according to the commented instructions.

### App structure

The subscribers application is comprised of three web endpoint handlers (subscribe, confirm, unsubscribe) and a simple
SQlite database to store subscribers and notification history. The three endpoints initiate state-transitions for the email passed as query parameter:

## 3. Signup web component setup

Your readers will _not_ want to hit the Modal web endpoint with `curl` to do signup. There should be a familiar, friendly web component interface with a simple text box input. That's what you see at the top of this post. All it does
is accept a (valid) email address and pass that to the web endpoint's `/subscribe` handler, which will process the subscription and send back a confirmation.

If you're a frontend afficianado you might be want write this functionality yourself into your website, maybe in React, Vue.js, or Svelte.

As this website is boring old Jekyll, the web component and I wrote and provide in the source code is a rudimentary
HTML and vanilla Javascript component, with CSS style. The file is called `subscribe.html`. You should be able to just copy paste this into your site, just update the endpoint URL and maybe tweak the CSS a bit 👍.

## Testing, and launch

If you need a first subscriber to test your setup, hit me up on Twitter or Reddit and I'll
be happy to be a testcase!
