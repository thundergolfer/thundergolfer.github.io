---
layout: post
title: "Create an email newsletter from an RSS feed with Modal"
date: 2023-01-09
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

<aside>
<div class="callout-panel callout-panel-info">
    <span class="callout-panel-icon callout-panel-info-icon">
        <span class="" role="img" aria-label="Heads up">👋</span>
    </span>
    <div class="ak-editor-panel__content">
        <p data-renderer-start-pos="97">
            All code for this solution is at <a target="_blank" rel="noopener noreferrer" href="https://github.com/thundergolfer/modal-fun/blob/main/thundergolferdotcom-email-subs/">github.com/thundergolfer/modal-fun</a>.
        </p>
    </div>
</div>
</aside>

## 1. Gmail API setup

To set up the application to send emails on my behalf, I followed this [Python quickstart guide](https://developers.google.com/gmail/api/quickstart/python) from the official Google docs.
The only non-trivial part was setting up the OAuth app, so I'll walk you through that in a bit of detail.

### Adding a constent screen and Oauth scopes:

After enabling the Gmail API in your Google Cloud project (mine is called `thundergolfer-dotcom`) the quickstart guide linked above tells you to create an OAuth client ID.
This is necessary, but before I could do that I need to create an OAuth app registration, specify the requisite Oauth scopes, and fill-in a form to create an OAuth consent screen.
The form is pictured below.

<img width="60%" style="margin: 0 20%" src="/images/email-subs-with-modal/gcloud-gmail-oauth-app-setup.png" alt="setting up gmail oauth app with appropriate oauth scopes">

This is a Yak-shave, as this application won't ever use the consent form, but Google made me do it so I did it. I don't pay for Google Workspaces with my personal Google Account so I needed to create an 'External OAuth' app.
This is fine because Google will put the app in 'testing mode' and still allow me to authenticate my own email account. Deploying with an OAuth app in 'testing mode' works for stuff like this; I had to
do the similar to how it works for [my Spotify OAuth app integration](/modal/webhooks/dashboard/2022/11/13/personal-dashboard-with-modal-webhooks/).

Some of the form fields are irrelevant but required, such as adding links to your app website and adding a logo. I just linked to my blog, and added a picture of myself 🤷.

### Create OAuth Client ID

![creating an oauth client ID](/images/email-subs-with-modal/gcloud-create-oauth-client-id.png)

After finishing the consent page go back to `Menu menu > APIs & Services > Credentials` and create an OAuth client ID (pictured above). This will allow you to download a JSON file
with personal credentials, including a `client_id` and `client_secret`. This file will be used to go through the OAuth flow yourself and acquire a crucial `refresh_token` granting
indefinite access to Gmail sending for your account.

To go through the OAuth flow, take my code (linked above) and run the `create_refresh_token_and_test_creds()` function locally. The end result of the process is a `.json` file written to local disk.

```bash
python3 -m email_subs.main create-refresh-token
```

Once you have the `.json` file containing the `refresh_token`, copy from it the following
fields into a [Modal Secret](https://modal.com/docs/reference/modal.Secret) called `gmail`.

| JSON file field | `'gmail'` Modal Secret key |
| --------------- | -------------------------- |
| `client_id`     | `GMAIL_AUTH_CLIENT_ID`     |
| `client_secret` | `GMAIL_AUTH_CLIENT_SECRET` |
| `refresh_token` | `GMAIL_AUTH_REFRESH_TOKEN` |

Done! The Modal application will use this populated `gmail` secret to
authenticate with the GMail API.

### Put your Google Cloud app 'in production'

![ensure the Google Cloud app is 'in production'](/images/email-subs-with-modal/in-production.png)

This last step is quick and _very important_. If you don't do it, your unexpiring `refresh_token` will actually expire in 7 days.
Go to the _OAuth Consent Screen_ tab and under "Publishing Status" change your app from being in "testing" mode to being "in production".

Now, Google will then say your app needs verification, but you can ignore this. What matters is that a production app's refresh tokens
will not expire and so the Modal email subscribers app won't break after seven days.

For background on this crucial step, check out [this StackOverflow answer](https://stackoverflow.com/a/65936387/4885590).

## 2. Modal app setup

While I would prefer to inline all the code for this solution into the blog post, it would be too much, so I will
just provide a summary of its structure. The code is heavily documented so as to be beginner friendly, and shouldn't
require modification besides changing some configuration values according to the commented instructions within.

### App structure

The subscribers application is comprised of three web endpoint handlers (subscribe, confirm, unsubscribe), a simple
SQlite database to store subscribers and notification history, and a cronjob function that checks the RSS feed and sends emails with GMail's API. The three endpoints initiate state-transitions for the email passed as query parameter:

<svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1101.52734375 310.21009639329816" width="100%" height="100%">
  <!-- svg-source:excalidraw -->
  <!-- payload-type:application/vnd.excalidraw+json --><!-- payload-version:2 --><!-- payload-start -->eyJ2ZXJzaW9uIjoiMSIsImVuY29kaW5nIjoiYnN0cmluZyIsImNvbXByZXNzZWQiOnRydWUsImVuY29kZWQiOiJ4nO1cXFlT28hcdTAwMTZ+z6+gSNV9XG6d3pepmppLXHUwMDAwXHUwMDA3Jlx1MDAwNEhcYlx1MDAxMLgzRVx0S8ZcdTAwMWFcdTAwMGLJkWWWTOW/39NcdTAwMDKs3diOTcjiqlCgpd3qPt9yuo/y77OlpeXkpu8t/7a07F23ncB3Y+dq+YU9funFXHUwMDAzP1xu4Vx1MDAxNE3/XHUwMDFlRMO4nV7ZTZL+4LeXL7M7UDu6uL3LXHUwMDBivFx1MDAwYi9MXHUwMDA2cN3/4O+lpX/Tn3DGd+29XHUwMDFir/45ver4J1x1MDAxN/T4gnW24q34dStJb00vXHUwMDFhdSZcYvz+wMtOXFzDUUK4QFxcKMxcYlx1MDAxNaMzN3CGMYKM1Co7euW7SdfewzQyRmLDcie7nn/eTdKzXGZRUjzphOeB7Vx1MDAwM1x1MDAxZVx1MDAxZFx1MDAxOSRx1PPWoiCKbd+e4/ST9e3MaffO42hcdTAwMTi6o2uS2Fx0XHUwMDA3fSeGociu6/hBsJ/cXHUwMDA0t4PotLvDOPeEt99ydNdvWjo+um9cdTAwMTDBkGd3wdeed0NvYFx1MDAwN5yMjkZ9p+0ndmRcYs6ew/axv+Wmc/N3voXQvWvhfrKymaB3R75k/fE8O5NUa0xcdONZ81nASM7LR3eiMFxyXHUwMDFlXCIlIVxuk9x9/mBcdTAwMWSiJklb7TjBwMtcdTAwMDbWdm2jXHUwMDFjUfmoKlx1MDAwNE3iXWejnYu5la1VJ17bJFvb65/Od/i61ENcdTAwMTYuj6778qK+2dubj/Hxq9X400ky/Hh+wlx1MDAwZVvdzd7qSvFb7r/fiePoatJ2dy+3lYu3P3AuyZH50OHHXHUwMDFir8PJ2r37LZvCYd91bsePSEWoXHUwMDExXGY+ho3OXHUwMDA3ftiDk+EwXGKyY1G7l1xy+bNcXIdLiK1cdTAwMWa9XG5iXHUwMDBig39cdTAwMDdXZeEqsNJcdTAwMTW8aomw4pTUQVaZKlDpU8Mn+Sb4LMzgXHUwMDFkXHUwMDEwXHUwMDE1Z0LCgOpcdTAwMWEgXG6qXHUwMDFhgchcdTAwMDXRRtDcfZNcdTAwMDOx0I+vj74smGxcdTAwMTDBILZjL20ym5ooTPb9zykj4cLRlnPhXHUwMDA3N4XRta2sXHUwMDA2/nmYNlx1MDAwNV324uX8MCQ+6Nboglx1MDAwYt91XHUwMDAzL1x1MDAxZi1cdTAwMDNcdTAwMGa6nI5RNjZt+CpcdTAwMDeOxluTyFhcdTAwMTT7537oXHUwMDA0XHUwMDFmSs9TXHUwMDBis0bNy+aRkeZ5xIxRrKichFBvXHUwMDExve52X1x1MDAwZuX+ZuvkI9vdWvkwlFx1MDAxZLz5dGBQXHUwMDA1eMomXFxhJDWRXHUwMDFjyzKbcI4g9IpcdTAwMDZgXqQwu5G4w6dkWHBpcFx1MDAxNkvz0eE5ieOadtd7bzaP38ur1tp29y3tnG5cdTAwMWZ/a3FU5NBcdTAwMWPwg/WNdmDWjvhqK2yxgzm0u1x1MDAxNb3vXHIv42FXtXZayZ9esPb21d6cRJdrXGbMl/m2XHUwMDE5RbdeT3NmnFSI/p5cbpRWXHUwMDAwXHUwMDBlhidh9HGT/+SZwFxiREpwT3nAaERcdTAwMTXjbIE0YHBcdTAwMTX8tIJ5zTlcdTAwMTbUSD5cdTAwMDXmXHUwMDBigTKV4E5cdTAwMWZ5s+tqqmZR2PHji7w+14vm11x0cUlyXHUwMDFmUK2K5I46OavoXHUwMDFh3JzFKIOJXHUwMDAwSZhcdTAwMWNq17RzeXoqRUBaQpz1er13fP1cdOWGXHJQ01x1MDAxOCNcIjAzVdFcdTAwMTVcdTAwMDRcdTAwMDHVXGKzSLTNLLpAhVpKo+hcdTAwMTRcdTAwMDB8RNHt9C9X6ZXaaFx1MDAwNauuXHUwMDFjXvrDoOe8/pHFXHUwMDExXHUwMDFjkFA6XHUwMDBirlx1MDAwNYmjpqZcdTAwMTGyRkBcZlx1MDAxM0P5xJCtn6Wnro5cdTAwMWFcdTAwMWJEuC6ooL1cdTAwMTVcdTAwMTRcdHFSdM9zxyslVZhW5Vx1MDAxMYBcdTAwMGL5KjV65tx3uoR06uD7On1cdTAwMWOGg+HZoFx1MDAxZPtnjyyRXHUwMDBmaExZXCJcdTAwMGL9rMXbJC6/RFxuxWCkWiFcdLPNIO7Kds1cdTAwMDYkXGJcYpPEMMrhR83qrVx1MDAxNODoXHUwMDE0JXCzhuDNLWeMwlx1MDAwYiMhidBKXHUwMDExuMAuhqgxXGL5eZaKpljKtYaaSKpcdTAwMDXNR95cdTAwMWSlXHUwMDEyhln5cGaDqKJWgbNcdTAwMWK//Vx1MDAxYVI/8svanP22lMVC+sfo979f1F7dXHUwMDFjgOntldDL2qtIYuBcZpK16OLCT+BB92wny1x1MDAwZjRInDh55YeuXHUwMDFmnlx1MDAxN2fwbldlkrWnlJ7aw0GKXGbwRlx1MDAxYXOF4TEwNiSbSVx1MDAxYkJO39o4xFxyKFx1MDAwMsZSXHUwMDE5bsDVykqUeKH7cKd6YlVfnK5cXFx1MDAxZP/Z8b29zaP2/lx1MDAwN9dp6JTgXHUwMDFjLKWQWlx1MDAxMyY1U5VOXHRksFwi8KFgLzEholx1MDAxYbl2qFYt4XQ9xy1cdTAwMGYk9Dh/Lm9X6lx1MDAxOW68pVx1MDAxYctwknJcdTAwMDShXG4jXGKPw3WGhJTiXGJBVMK4aka0kErIXHUwMDFhiuNcYiRbSqyUYIrkcsZcdTAwMTHFScSVMoBcdTAwMGKlIL2H0fvFcFMyXHUwMDFjXHUwMDAwlDDB61x1MDAxOY5KUT48YjhcbiFqt7nmv0o+uymZM8M1xZ/9VFwi7zFcYm58pp/jklx1MDAxNSBcdTAwMTNOqZK220AnNuurkFx04UiCXHUwMDA1wVx1MDAxMlx1MDAwYsmBXHUwMDEw6YxcZjfeXFyVe8W10dbzXHUwMDEwLriinFe7RVx1MDAxMMYgKFxcXHUwMDE4zojBeOEkNz6/XHUwMDFiS3KaXHQ7iFx1MDAwNlx1MDAxYlx1MDAxOETIqzPwpiynMdKaXHUwMDAxZTPQQZCcKstRbTfopaSQkkNAcVxcx3JcdTAwMThcdTAwMTFDrJCCK8SSZJf8Yrn8XGY1b8nD4GHFZd2WPHxpM8lcdMC/XHUwMDEw4Fx1MDAwMX9UklsxQHKAM1x1MDAwNZ1J45flb69cdTAwMDTeg801h7P9XHUwMDAwVsBqSbtcdTAwMDIl4UtcdTAwMTnN2ltcdTAwMWNpTkNPgmhcdTAwMGVsSTVcdTAwMTaUcSVzV92SXHUwMDEzWFx1MDAxYSqpVFxmRlxmmIyRhZtCQ1x1MDAwNPRcdTAwMDdSQYhEa6QqXaJ2tZFcdTAwMGJIXHUwMDEzrU1cdTAwMDU+Z4vmy/FcdTAwMTVcdTAwMWHj+NJIgyikXHUwMDBiMH5aU5FbJb7dplx1MDAwMNNcctmEgvPwj+ZWpPKm0ChONMyBwJTrutVPXHUwMDA0XHUwMDE3MCoopsaA8uFfee+0fIlcdTAwMDVcdTAwMDST5KTWXHUwMDE1atG4llxiQlx1MDAwN3dNttE2bdqr2Fx1MDAxM+DL5vhLz1ZcIu8xXGJuS1x1MDAxZlx1MDAxZlx1MDAwZlx1MDAxY4ZPN1x1MDAwNvxwfXNn7bJ3876B4FxiY1xmjJXkQlx0gjmrsV/AcFx1MDAwNvjPJqNAcVx1MDAxMFxis1HcNMk4U8BxWIIhtCtitNZcdTAwMTNSxSTjVMD4UshcdTAwMWNcdTAwMTfuXHTHXHUwMDBl6ojjXFzfuYhCt8hyWihcdTAwMTA6Q+pcbjKA0EH6qF3lXHUwMDE1XHUwMDEwPjVcZkdcdTAwMTTCorR9lHFcdTAwMWIxSKtFXHUwMDE0Zj5vey7PidBcdTAwMGbGaIRyu9ajKzuX1l/zMVx1MDAwZVx1MDAxMGZcdTAwMGKGeyZcdTAwMDc441x1MDAxZdjNXHUwMDFl31x1MDAwZdTZzkrX9Y/ab1x1MDAwZvtcdTAwMWY6zlOpnpyShMdcdTAwMDCs/ikrXHUwMDAwq1ZPam2QrNnGXHUwMDAxR4HAb1x1MDAxYVx1MDAwNYZd1WNLsCqiflx1MDAxNVA2XHUwMDE2UFx1MDAxMqVA6KyLr1x1MDAwMVxypO9NoKFcdTAwMDI8vlAzVTIvylx1MDAwNdxvQe1cdTAwMWNsbz/d6slcdTAwMDdUp7xPlT5MLcYmqOJcdTAwMTCqMq1Z6aTGXHUwMDE48p8pqjjGZzRPtYqDXHUwMDBijWStUDOOXHUwMDE0tWbJsJJQz31rWIK5XHUwMDExxVLwTO9cdTAwMDVGXHUwMDEy0ES0guxcdTAwMGU+WS5zX9BBuaE4b9VcdTAwMWa1oGOx5Y5fUXkxtl2ne9x9c7hzdXhzvcXfnbjbR0a6c1JJXHUwMDBluYFWc3rHILg+61x1MDAwZbx/4nPv/PrEbJycnu5fXU+ikpCkIFx1MDAwMSiuvmJcdTAwMDBcdTAwMTlcbqJcZvw9a/agqqZagZkxaPp53lx1MDAwNGpcdTAwMTBKmzLnN0Ny+TJcdTAwMDC8iWi1sovh+SmYn1JcbpFbP5lBKV+OaiD+XG7tiT+8XHUwMDBix1x1MDAwZn6//u/NZ9SOajU055JcdTAwMGJcdTAwMWHKXG6NjyQy8DrJXHUwMDE4XHUwMDA1TaJ+rXzmyiGK8ll4urJWPvA4Y1W0qapcbjKKxtdcdTAwMGY04cRgISZJXHUwMDFjbrF+1npcdTAwMTdtXHUwMDFmtm5OW9tvL1x1MDAwZte33uxFb86eXHUwMDBlNEagR4BsgpVcdTAwMDQjXHUwMDBlaajUQlKS3XxX3Vx1MDAwMlx1MDAxZV3CdcZgyXHuJY1bXHUwMDA20lxiXHUwMDE0l9lcblx0m/MvUltrqpJzy1f3+MXEgJ81fJpXXHUwMDExvqLsijFbdDdcdTAwMGI4p1x1MDAwNltcdTAwMWH6dyW/f9xGfiHwb1x1MDAwZv2nXHUwMDFkud7vhDK/XHUwMDAxc0JcdTAwMTRanVx0wtOAdbpcdTAwMWXPXHUwMDA2Xp1cdTAwMWLByu625EKYKV5cdTAwMThcdTAwMTj01902PVxc+SxON5TukPf7vYOV71x1MDAxM7ySYkSN1rT6dlwiZ0gpblx1MDAxNa1sXHUwMDFkvlx1MDAxNXKZ3fkg+Vx1MDAxZLrFXCKXU5HbT1g4cnOViFx1MDAwZmHhyou1wU9cdTAwMDK90/d6Nlx1MDAwNFx1MDAxYt1cXIFHXHUwMDA0pYbkq4ZcdTAwMWWCsFx1MDAxN1x1MDAxY1x1MDAxZr0/Odhcci6Zq9+92j37uNtrf69cdTAwMTBcdTAwMTaIXHUwMDEwwqpcdTAwMTDmXFwg8KmPk9hOXHUwMDA2YSExeFx1MDAwMKlcdTAwMWbnnSDBJWdGPlx1MDAxZYR/SvGdJM1cdTAwMWVbWFx1MDAwM1x0KtJY2VxuXGZuVzhMIYqpMojZXXhcdTAwMDNGiovaXG5pplx1MDAxMFdcdTAwMTJcdTAwMGJqtcq2VFxyRkmRolxuazB+ym4/6Wkqa+iZdpg3XHUwMDE2XHUwMDFlz4lwnLPObFx1MDAxY1JcdTAwMDbmJFx1MDAxY5L19lx1MDAxMfZU7Dq7xrj2/XquKlvH98xstFx1MDAxMEDObFx1MDAwMTU1ym4+z4Lsue5cdTAwMTErjpjhmNqSukLgpSeRXHJoJc19xD3UWnNcdTAwMWPbTzWCs/aeldqd347z5blcdTAwMWaRg+iT2qWbXHUwMDA34T/DZE/uNpXUUGzfLbIvtcDcXGKW/Vx1MDAxZlx1MDAxNkv3m7tcdTAwMWFpo1x1MDAwMeN2jVMoXCJ1JeDmXVNcdTAwMDOJJ7c1eyCgtr5LV+t8XHUwMDE00lYoQMKYrWEnXHUwMDBi3G9+2OWY5tctITJcYqa5MspcdTAwMDddzvi5+65cXE76XHUwMDEyJDYgXHUwMDA2RkhT9DnU6lx1MDAwN2T0hGhty3NzdFMmcuCx2U1cdTAwMGXFNXuKudw+t8KgpeLzMzlj1+NcdTAwMTe5vm1JRtOZaHaml8b2XHUwMDEz+PqlpOskS7HX9vxLb/BXmJqSpTBK/Fx1MDAwZXieXHUwMDA0IDGotU58XHUwMDBlS49TWKeJ+/rsfqzTcV52+v301lx1MDAxMb0tX/re1atcdTAwMWFH0Uk/9v6URyxevVS3vzz78n826r7xIn0=<!-- payload-end -->
  <defs>
    <style class="style-fonts">
      @font-face {
        font-family: "Virgil";
        src: url("https://excalidraw.com/Virgil.woff2");
      }
      @font-face {
        font-family: "Cascadia";
        src: url("https://excalidraw.com/Cascadia.woff2");
      }
    </style>
  </defs>
  <rect x="0" y="0" width="1101.52734375" height="310.21009639329816" fill="#ffffff"></rect><g stroke-linecap="round" transform="translate(297.837890625 91.13026840743953) rotate(0 69.498046875 66.60546875)"><path d="M73.36 -0.44 C82.98 -0.98, 94.67 2.96, 103.42 7.62 C112.17 12.27, 120.11 19.56, 125.86 27.49 C131.61 35.41, 136 45.8, 137.91 55.18 C139.83 64.57, 139.99 74.42, 137.35 83.8 C134.71 93.17, 128.77 104.19, 122.08 111.43 C115.4 118.66, 106.65 123.58, 97.27 127.23 C87.88 130.87, 75.93 133.79, 65.79 133.3 C55.66 132.8, 45.11 128.75, 36.47 124.24 C27.83 119.73, 19.91 114, 13.93 106.23 C7.96 98.46, 2.45 87.16, 0.62 77.62 C-1.21 68.07, 0.06 58.08, 2.96 48.97 C5.87 39.85, 11.41 30.1, 18.05 22.92 C24.7 15.75, 32.07 9.57, 42.82 5.9 C53.56 2.22, 74.65 1, 82.53 0.86 C90.41 0.73, 90.36 4.08, 90.11 5.09 M96.68 5.8 C106.22 8.6, 116.69 16.15, 123.26 23.44 C129.84 30.73, 133.47 40.12, 136.12 49.53 C138.76 58.94, 141.09 70.44, 139.14 79.88 C137.18 89.33, 130.33 98.69, 124.38 106.19 C118.43 113.68, 112.12 120.26, 103.41 124.87 C94.71 129.47, 82.51 133.15, 72.15 133.83 C61.79 134.51, 50.24 133.09, 41.26 128.94 C32.28 124.8, 24.87 116.61, 18.29 108.98 C11.71 101.34, 4.89 92.29, 1.79 83.13 C-1.32 73.96, -2.02 63.31, -0.34 54 C1.34 44.69, 5.53 34.74, 11.88 27.27 C18.23 19.81, 28.78 13.55, 37.76 9.23 C46.74 4.91, 55.94 2.19, 65.75 1.37 C75.57 0.56, 91.52 3.56, 96.66 4.33 C101.8 5.11, 97.07 4.7, 96.6 6.04" stroke="#000000" stroke-width="2" fill="none"></path></g><g transform="translate(327.8359375 145.23573715743953) rotate(0 39.5 12.5)"><text x="39.5" y="18" font-family="Virgil, Segoe UI Emoji" font-size="20px" fill="#000000" text-anchor="middle" style="white-space: pre;" direction="ltr">created</text></g><g stroke-linecap="round" transform="translate(623.0625 103.32948715743953) rotate(0 69.498046875 66.60546875)"><path d="M68.74 0.78 C78.29 -0.22, 90.54 2.56, 99.81 6.39 C109.09 10.22, 118.34 16.3, 124.41 23.77 C130.48 31.23, 134.12 41.76, 136.23 51.16 C138.35 60.56, 139.04 70.76, 137.09 80.16 C135.13 89.57, 130.53 100.02, 124.5 107.6 C118.47 115.17, 109.96 121.27, 100.9 125.59 C91.85 129.9, 80.35 133.17, 70.19 133.47 C60.02 133.77, 49.07 131.72, 39.91 127.39 C30.76 123.06, 21.75 114.97, 15.25 107.48 C8.76 99.98, 3.24 91.72, 0.92 82.42 C-1.39 73.11, -1.04 61.19, 1.36 51.65 C3.76 42.11, 9.05 32.58, 15.32 25.19 C21.58 17.8, 29.57 11.44, 38.96 7.32 C48.35 3.2, 65.92 1.31, 71.67 0.46 C77.42 -0.38, 73.38 1.13, 73.43 2.23 M44.23 4.21 C52.75 -0.17, 64.82 -1.85, 74.39 -1.03 C83.96 -0.21, 93.22 4.39, 101.66 9.13 C110.09 13.88, 119.15 19.74, 125.03 27.44 C130.91 35.14, 134.87 45.83, 136.92 55.34 C138.98 64.84, 140.05 75.12, 137.36 84.47 C134.67 93.81, 127.8 104.06, 120.77 111.4 C113.75 118.74, 104.49 124.96, 95.22 128.5 C85.94 132.05, 75.23 133.31, 65.13 132.65 C55.04 131.99, 43.22 129.22, 34.64 124.56 C26.07 119.9, 19.44 112.52, 13.69 104.7 C7.95 96.88, 2.24 87.27, 0.18 77.66 C-1.88 68.05, -1.4 56.3, 1.36 47.04 C4.11 37.77, 9.88 28.89, 16.7 22.08 C23.51 15.27, 37.93 8.73, 42.25 6.2 C46.58 3.66, 42.09 6, 42.62 6.88" stroke="#000000" stroke-width="1" fill="none"></path></g><g transform="translate(647.560546875 157.43495590743953) rotate(0 45 12.5)"><text x="45" y="18" font-family="Virgil, Segoe UI Emoji" font-size="20px" fill="#000000" text-anchor="middle" style="white-space: pre;" direction="ltr">confirmed</text></g><g stroke-linecap="round" transform="translate(952.53125 110.47011215743953) rotate(0 69.498046875 66.60546875)"><path d="M82.98 1.78 C92.36 2.53, 103.22 7.36, 111.46 13.04 C119.7 18.72, 127.87 27.13, 132.41 35.86 C136.95 44.59, 138.68 55.76, 138.68 65.44 C138.68 75.11, 136.45 85.08, 132.41 93.89 C128.36 102.69, 122.3 112.15, 114.41 118.26 C106.52 124.38, 95.02 128.35, 85.07 130.56 C75.12 132.77, 64.28 133.27, 54.72 131.51 C45.16 129.75, 35.44 125.92, 27.69 119.98 C19.93 114.04, 12.74 104.46, 8.19 95.88 C3.64 87.3, 0.63 78.05, 0.38 68.5 C0.12 58.95, 2.63 47.34, 6.66 38.57 C10.7 29.81, 17.01 22.14, 24.6 15.93 C32.18 9.72, 41.71 3.44, 52.19 1.3 C62.68 -0.84, 80.99 2.6, 87.5 3.08 C94.01 3.55, 91.48 3.39, 91.25 4.17 M80.86 1.75 C90.72 2.38, 103.77 6.91, 112.09 12.45 C120.41 17.99, 126.47 26.47, 130.78 34.99 C135.1 43.51, 137.46 53.65, 137.98 63.55 C138.5 73.45, 137.96 85.54, 133.89 94.41 C129.82 103.27, 121.05 110.73, 113.54 116.73 C106.03 122.74, 98.4 128.1, 88.85 130.46 C79.3 132.81, 66.57 132.63, 56.23 130.86 C45.89 129.08, 34.75 125.2, 26.81 119.82 C18.86 114.43, 12.95 107.05, 8.56 98.54 C4.18 90.04, 1.06 78.6, 0.49 68.79 C-0.08 58.98, 1.28 48.43, 5.13 39.68 C8.98 30.92, 15.94 22.36, 23.59 16.24 C31.25 10.13, 41.35 5.43, 51.05 3 C60.75 0.56, 76.47 1.86, 81.79 1.66 C87.12 1.46, 83.05 0.85, 83 1.8" stroke="#000000" stroke-width="2" fill="none"></path></g><g transform="translate(961.529296875 164.57558090743953) rotate(0 60.5 12.5)"><text x="60.5" y="18" font-family="Virgil, Segoe UI Emoji" font-size="20px" fill="#000000" text-anchor="middle" style="white-space: pre;" direction="ltr">unsubscribed</text></g><g stroke-linecap="round"><g transform="translate(440.01469344375005 164.24688033985888) rotate(0 82.34342881403961 -0.2647089182098341)"><path d="M-0.09 -0.36 C27.76 -0.34, 138.72 -0.16, 166.28 -0.12 M-1.59 -1.59 C26.25 -1.42, 138.17 0.65, 165.86 1.06" stroke="#000000" stroke-width="1" fill="none"></path></g><g transform="translate(440.01469344375005 164.24688033985888) rotate(0 82.34342881403961 -0.2647089182098341)"><path d="M136.9 12.52 C143.04 8.57, 149.74 7.14, 165.89 -0.18 M137.02 10.64 C146.82 8.49, 154.65 4.67, 165.41 0.31" stroke="#000000" stroke-width="1" fill="none"></path></g><g transform="translate(440.01469344375005 164.24688033985888) rotate(0 82.34342881403961 -0.2647089182098341)"><path d="M137.25 -8 C143.27 -7.13, 149.89 -3.73, 165.89 -0.18 M137.37 -9.88 C146.94 -5.61, 154.65 -3.01, 165.41 0.31" stroke="#000000" stroke-width="1" fill="none"></path></g></g><mask></mask><g stroke-linecap="round"><g transform="translate(776.7203602564821 170.4265167260071) rotate(0 82.31717522363124 4.1065615594631595)"><path d="M0.23 1.14 C27.91 2.31, 138.39 6.53, 165.74 7.53 M-1.1 0.69 C26.52 1.5, 137.88 5.22, 165.28 5.95" stroke="#000000" stroke-width="1" fill="none"></path></g><g transform="translate(776.7203602564821 170.4265167260071) rotate(0 82.31717522363124 4.1065615594631595)"><path d="M138.68 16.9 C146.3 11.89, 153.42 11.32, 166.22 6.86 M137.12 15.57 C146.19 12.61, 157.51 9.01, 164.51 6.88" stroke="#000000" stroke-width="1" fill="none"></path></g><g transform="translate(776.7203602564821 170.4265167260071) rotate(0 82.31717522363124 4.1065615594631595)"><path d="M139.31 -3.61 C146.84 -3, 153.79 2.05, 166.22 6.86 M137.75 -4.94 C146.49 -0.6, 157.58 3.11, 164.51 6.88" stroke="#000000" stroke-width="1" fill="none"></path></g></g><mask></mask><g stroke-linecap="round"><g transform="translate(988.0447684316691 240.0445897489334) rotate(0 -141.23757993059428 29.49255080810019)"><path d="M0.66 -1.18 C-15.11 8.49, -48.68 57.88, -95.83 59.16 C-142.98 60.44, -251.1 15.49, -282.23 6.51 M-0.45 0.81 C-15.74 11.1, -46.49 59.52, -93.6 60.16 C-140.72 60.8, -251.61 13.63, -283.14 4.63" stroke="#000000" stroke-width="1" fill="none"></path></g><g transform="translate(988.0447684316691 240.0445897489334) rotate(0 -141.23757993059428 29.49255080810019)"><path d="M-255.11 2.71 C-260.87 4.06, -263.69 3.45, -283.74 2.67 M-253.25 5.1 C-258.91 4.56, -267 4.21, -283.9 5.27" stroke="#000000" stroke-width="1" fill="none"></path></g><g transform="translate(988.0447684316691 240.0445897489334) rotate(0 -141.23757993059428 29.49255080810019)"><path d="M-261.89 22.08 C-266.48 19.5, -267.93 15.01, -283.74 2.67 M-260.03 24.47 C-264.2 19.57, -270.78 14.93, -283.9 5.27" stroke="#000000" stroke-width="1" fill="none"></path></g></g><mask></mask><g stroke-linecap="round"><g transform="translate(121.66503276325875 152.63999014461177) rotate(0 81.80506770945635 1.1736846667640464)"><path d="M-1.09 0.02 C26.42 0.44, 137.19 1.66, 164.7 1.8 M0.54 -1.02 C27.89 -0.32, 135.98 2.92, 163.6 3.37" stroke="#000000" stroke-width="1" fill="none"></path></g><g transform="translate(121.66503276325875 152.63999014461177) rotate(0 81.80506770945635 1.1736846667640464)"><path d="M135.2 12.49 C143.07 8.91, 149.23 9.98, 161.87 3.91 M135.55 12.05 C142.89 10.29, 153.28 7.85, 163.64 3.22" stroke="#000000" stroke-width="1" fill="none"></path></g><g transform="translate(121.66503276325875 152.63999014461177) rotate(0 81.80506770945635 1.1736846667640464)"><path d="M135.69 -8.03 C143.3 -6.03, 149.32 0.63, 161.87 3.91 M136.04 -8.47 C143.24 -4.03, 153.49 -0.29, 163.64 3.22" stroke="#000000" stroke-width="1" fill="none"></path></g></g><mask></mask><g stroke-linecap="round" transform="translate(10 100.13094708996437) rotate(0 58.529296875 59.935546875)"><path d="M10.05 49.82 C10.05 49.82, 10.05 49.82, 10.05 49.82 M10.05 49.82 C10.05 49.82, 10.05 49.82, 10.05 49.82 M5.2 61.5 C20.11 44.76, 33 28.26, 46.53 13.95 M5.2 61.5 C17.37 48.77, 29.44 35.07, 46.53 13.95 M6.25 66.38 C24.9 43.95, 39.98 26.17, 58.08 6.76 M6.25 66.38 C23.87 44.96, 41.71 25.41, 58.08 6.76 M9.27 69.01 C23.02 53.16, 34.21 40.73, 63.72 6.37 M9.27 69.01 C26.56 48.67, 43.91 29.34, 63.72 6.37 M12.29 71.63 C26.6 53.16, 45.06 35.64, 66.74 8.99 M12.29 71.63 C26.96 55.19, 41.04 39.77, 66.74 8.99 M14.65 75.01 C25.12 60.58, 38.51 49.04, 69.76 11.62 M14.65 75.01 C37.79 48.7, 59.7 24.07, 69.76 11.62 M17.67 77.64 C35.27 58.67, 51.32 40.48, 72.78 14.24 M17.67 77.64 C32.09 61.13, 46.15 44.56, 72.78 14.24 M20.69 80.26 C32.95 66.9, 45.05 53.67, 75.8 16.86 M20.69 80.26 C41.33 57.14, 60.76 36.1, 75.8 16.86 M23.05 83.64 C44.59 58.36, 66.55 37.09, 78.82 19.49 M23.05 83.64 C36.29 69.71, 49.41 53.82, 78.82 19.49 M26.07 86.26 C44.18 67.11, 56.55 49.1, 81.18 22.87 M26.07 86.26 C47.8 61.07, 71.24 34.79, 81.18 22.87 M29.09 88.89 C44.72 69.36, 60.34 54.14, 84.2 25.49 M29.09 88.89 C50.35 64.68, 70.84 39.77, 84.2 25.49 M32.11 91.51 C47.29 76.14, 56.98 61.4, 87.22 28.12 M32.11 91.51 C46.4 74.96, 60.52 58.11, 87.22 28.12 M34.47 94.89 C55.03 69.74, 75.34 44.47, 89.58 31.5 M34.47 94.89 C49.47 76.54, 65.45 58.18, 89.58 31.5 M37.49 97.51 C48.47 84.75, 59.64 69.85, 92.6 34.12 M37.49 97.51 C50.04 80.97, 63.63 67.22, 92.6 34.12 M40.51 100.14 C60.04 76.09, 82.71 53.69, 94.96 37.5 M40.51 100.14 C54.29 84.46, 67.9 69.2, 94.96 37.5 M42.87 103.52 C63.23 82.47, 80.72 59.27, 97.98 40.12 M42.87 103.52 C62.78 80.49, 82.66 58.77, 97.98 40.12 M45.89 106.14 C59.19 90.36, 77.34 72.77, 101 42.75 M45.89 106.14 C63.33 86.4, 79.42 67.09, 101 42.75 M48.91 108.77 C67.11 89.45, 83.83 69.48, 103.36 46.13 M48.91 108.77 C68.92 84.79, 87.54 61.8, 103.36 46.13 M51.27 112.15 C66.8 91.32, 84.18 73.26, 106.38 48.75 M51.27 112.15 C65.82 95.35, 80.87 78.53, 106.38 48.75 M54.95 114.02 C75.34 93.25, 91.23 72.04, 108.74 52.13 M54.95 114.02 C66.89 100.65, 76.99 86.98, 108.74 52.13 M58.62 115.88 C71.29 104.22, 82.34 88.73, 111.76 54.75 M58.62 115.88 C71.26 100.42, 86.41 84.33, 111.76 54.75 M65.58 113.98 C75.38 103, 87.93 89.43, 113.47 58.89 M65.58 113.98 C81.97 95.18, 97.72 75.97, 113.47 58.89" stroke="#ced4da" stroke-width="0.5" fill="none"></path><path d="M73.75 15 M73.75 15 C83.4 27.41, 92.06 37.83, 102.31 45 M73.75 15 C83.91 25.58, 95.88 38.43, 102.31 45 M102.31 45 C117.36 60.78, 116.69 58.71, 102.31 75 M102.31 45 C119.24 61.07, 118.77 61.03, 102.31 75 M102.31 75 C94 82.04, 89.15 89.89, 73.75 104.87 M102.31 75 C93.59 84.49, 84.56 91.94, 73.75 104.87 M73.75 104.87 C57.28 121.38, 58.12 118.7, 44.25 104.87 M73.75 104.87 C58.18 121.59, 59.1 121.54, 44.25 104.87 M44.25 104.87 C34.68 96.06, 28.76 88.92, 14.75 75 M44.25 104.87 C35.16 97.04, 27.49 87.6, 14.75 75 M14.75 75 C1.29 58.11, -0.36 58.48, 14.75 45 M14.75 75 C0.39 62.01, -0.75 58.38, 14.75 45 M14.75 45 C26.42 34.06, 36.59 25.7, 44.25 15 M14.75 45 C23.65 36.44, 31.71 27.67, 44.25 15 M44.25 15 C59.84 -0.86, 58.9 1.38, 73.75 15 M44.25 15 C59.26 -0.8, 59.19 -1.63, 73.75 15" stroke="#000000" stroke-width="1" fill="none"></path></g><g transform="translate(42.029296875 147.56649396496437) rotate(0 26.5 12.5)"><text x="26.5" y="18" font-family="Virgil, Segoe UI Emoji" font-size="20px" fill="#000000" text-anchor="middle" style="white-space: pre;" direction="ltr">NULL</text></g><g stroke-linecap="round" transform="translate(611.072265625 93.88485333996437) rotate(0 80.62890625 75.318359375)"><path d="M86.47 -0.74 C96.95 -1.13, 109.07 3.71, 118.55 8.72 C128.03 13.74, 136.67 21.37, 143.35 29.34 C150.04 37.3, 155.93 46.8, 158.65 56.51 C161.37 66.22, 161.67 77.42, 159.7 87.61 C157.72 97.8, 152.67 109.06, 146.79 117.65 C140.92 126.24, 133.57 133.79, 124.47 139.16 C115.37 144.53, 103.14 148.35, 92.21 149.87 C81.28 151.39, 69.43 151.11, 58.88 148.27 C48.32 145.42, 37.31 139.4, 28.89 132.8 C20.48 126.2, 13.3 117.75, 8.37 108.66 C3.44 99.58, -0.32 88.49, -0.67 78.28 C-1.03 68.07, 1.97 56.93, 6.22 47.39 C10.47 37.85, 16.94 28.02, 24.82 21.06 C32.69 14.1, 41.91 8.87, 53.47 5.61 C65.04 2.35, 86.49 1.94, 94.21 1.49 C101.93 1.04, 100.2 1.76, 99.79 2.91 M54.66 3.25 C64.02 -0.72, 77.47 -1.17, 88.7 -0.05 C99.93 1.08, 112.43 4.77, 122.02 10 C131.62 15.24, 139.9 23.01, 146.27 31.38 C152.64 39.75, 157.97 50.42, 160.27 60.22 C162.56 70.03, 162.33 80.07, 160.05 90.2 C157.78 100.33, 153.09 112.71, 146.62 121.02 C140.14 129.33, 130.77 135.41, 121.2 140.05 C111.63 144.7, 100.28 147.63, 89.2 148.9 C78.12 150.18, 65.1 150.67, 54.73 147.69 C44.36 144.71, 35.18 138.21, 26.98 131.03 C18.78 123.86, 10.23 114.06, 5.54 104.64 C0.85 95.23, -1.39 84.48, -1.17 74.53 C-0.95 64.58, 1.95 54.17, 6.85 44.93 C11.75 35.69, 20.08 26.08, 28.26 19.09 C36.43 12.11, 50.97 5.37, 55.92 3.04 C60.86 0.7, 57.69 3.65, 57.93 5.09" stroke="#000000" stroke-width="2" fill="none"></path></g><g transform="translate(126.9609375 172.39657208996437) rotate(0 85.5 19.5)"><text x="0" y="15.5" font-family="Cascadia, Segoe UI Emoji" font-size="16px" fill="#000000" text-anchor="start" style="white-space: pre;" direction="ltr">/subscribe</text><text x="0" y="35" font-family="Cascadia, Segoe UI Emoji" font-size="16px" fill="#000000" text-anchor="start" style="white-space: pre;" direction="ltr">    ?email=x@yz.co</text></g><g transform="translate(442.0408692814017 177.22384051291294) rotate(0.006170124842949231 80 29.5)"><text x="0" y="15.666666666666668" font-family="Cascadia, Segoe UI Emoji" font-size="16px" fill="#000000" text-anchor="start" style="white-space: pre;" direction="ltr">/confirm?</text><text x="0" y="35.333333333333336" font-family="Cascadia, Segoe UI Emoji" font-size="16px" fill="#000000" text-anchor="start" style="white-space: pre;" direction="ltr">    email=x@yz.co</text><text x="0" y="55" font-family="Cascadia, Segoe UI Emoji" font-size="16px" fill="#000000" text-anchor="start" style="white-space: pre;" direction="ltr">    &amp;code=123iop</text></g><g transform="translate(772.6796875 102.93563458996437) rotate(0.006170124842949231 80 29.5)"><text x="0" y="15.666666666666668" font-family="Cascadia, Segoe UI Emoji" font-size="16px" fill="#000000" text-anchor="start" style="white-space: pre;" direction="ltr">/unsubscribe?</text><text x="0" y="35.333333333333336" font-family="Cascadia, Segoe UI Emoji" font-size="16px" fill="#000000" text-anchor="start" style="white-space: pre;" direction="ltr">    email=x@yz.co</text><text x="0" y="55" font-family="Cascadia, Segoe UI Emoji" font-size="16px" fill="#000000" text-anchor="start" style="white-space: pre;" direction="ltr">    &amp;code=wer890</text></g><g transform="translate(777.4921875 204.50985333996437) rotate(0.006170124842949231 80 29.5)"><text x="0" y="15.666666666666668" font-family="Cascadia, Segoe UI Emoji" font-size="16px" fill="#000000" text-anchor="start" style="white-space: pre;" direction="ltr">/confirm?</text><text x="0" y="35.333333333333336" font-family="Cascadia, Segoe UI Emoji" font-size="16px" fill="#000000" text-anchor="start" style="white-space: pre;" direction="ltr">    email=x@yz.co</text><text x="0" y="55" font-family="Cascadia, Segoe UI Emoji" font-size="16px" fill="#000000" text-anchor="start" style="white-space: pre;" direction="ltr">    &amp;code=123iop</text></g><g stroke-linecap="round"><g transform="translate(503.18801031749285 38.52885760289888) rotate(0 68.73802609125357 31.361134813608885)"><path d="M0 0 C12.4 1.18, 51.48 -3.36, 74.39 7.09 C97.31 17.55, 126.96 53.45, 137.48 62.73 M0 0 C12.4 1.18, 51.48 -3.36, 74.39 7.09 C97.31 17.55, 126.96 53.45, 137.48 62.73" stroke="#2b8a3e" stroke-width="4" fill="none"></path></g><g transform="translate(503.18801031749285 38.52885760289888) rotate(0 68.73802609125357 31.361134813608885)"><path d="M110.38 49.86 C120.07 54.46, 129.77 59.07, 137.48 62.73 M110.38 49.86 C118.61 53.77, 126.85 57.68, 137.48 62.73" stroke="#2b8a3e" stroke-width="4" fill="none"></path></g><g transform="translate(503.18801031749285 38.52885760289888) rotate(0 68.73802609125357 31.361134813608885)"><path d="M124.99 35.45 C129.46 45.21, 133.92 54.97, 137.48 62.73 M124.99 35.45 C128.78 43.74, 132.58 52.03, 137.48 62.73" stroke="#2b8a3e" stroke-width="4" fill="none"></path></g></g><mask></mask><g transform="translate(291.29013933195006 10.01093028788489) rotate(0.006170124842949231 101.5 25)"><text x="0" y="18" font-family="Virgil, Segoe UI Emoji" font-size="20px" fill="#555" text-anchor="start" style="white-space: pre;" direction="ltr">State that receives</text><text x="0" y="43" font-family="Virgil, Segoe UI Emoji" font-size="20px" fill="#555" text-anchor="start" style="white-space: pre;" direction="ltr">email notifications</text></g></svg>

These endpoints are implemented by a FastAPI app and live in the `main.py` module.

```python
web_app = FastAPI()

...

@web_app.get("/subscribe")
def subscribe(email: str): ...

@web_app.get("/confirm")
def confirm(email: str, code: str): ...

@web_app.get("/unsubscribe")
def unsubscribe(email: str, code: str): ...
```

#### Datastore

As said before, these endpoints store and manipulate state using an SQLite database file that lives on a
Modal [persistent shared volume](https://modal.com/docs/guide/shared-volumes#persisting-volumes) ("persistent" means the data remains even if the application stops, and "shared" means it can be access by multiple Modal Functions).

The code for the database and its simple ORM is in `datastore.py`. The web handler functions use it like so:

```python
conn = datastore.get_db(DB_PATH)
store = datastore.Datastore(
    conn=conn,
    codegen_fn=lambda: str(uuid.uuid4()),
    clock_fn=lambda: datetime.now(timezone.utc),
)

notifications = store.list_notifications()  # Show sent newsletter email notifications
confirmed = store.confirm_sub(email=email, code=code)  # Confirm a subscriber
unsubbed = store.unsub(email=email, code=code)  # Unsubscribe a subscriber
```

#### Emailer

Our application needs to be able to send emails to subscribers, and this is implemented in the `emailer.py` module.

It merely defines an 'emailer' interface and a single implementation, `GmailSender(EmailSender)`:

```python
class EmailSender(Protocol):
    def send(self, message: EmailMessage) -> None:
        ...
```

A `FakeEmailer(EmailSender)` implementation exists in the tests.

#### Cronjob function

Finally, we have the cron-scheduled Modal Function which uses the [`feedparser`](https://pypi.org/project/feedparser/) Python package to download and parse the configured RSS feed.

It then checks the fetched RSS entries for blog posts that haven't been previously sent to subscribers, creates basic
HTML emails using the `email_copy.py` module, and sends them to subscribers.

<aside>
<div class="callout-panel callout-panel-info">
    <span class="callout-panel-icon callout-panel-info-icon">
        <span class="" role="img" aria-label="Heads up">👋</span>
    </span>
    <div class="ak-editor-panel__content">
        <p data-renderer-start-pos="97">
            <strong>Reminder:</strong> All code for the app is at <a target="_blank" rel="noopener noreferrer" href="https://github.com/thundergolfer/modal-fun/blob/main/thundergolferdotcom-email-subs/">github.com/thundergolfer/modal-fun</a>.
        </p>
    </div>
</div>
</aside>

## 3. Signup web component setup

Your readers will _not_ want to hit the Modal web endpoint with `curl` to do signup. There should be a familiar, friendly web component interface with a simple text box input. That's what you see at the top of this post. All it does
is accept a (valid) email address and pass that to the web endpoint's `/subscribe` handler, which will process the subscription and send back a confirmation.

If you're a frontend afficianado you might be want write this functionality yourself into your website, maybe in React, Vue.js, or Svelte.

As this website is boring old Jekyll, the web component I wrote and provide in the source code is a rudimentary
HTML and vanilla Javascript component, with CSS style. The file is called `subscribe.html`. You should be able to just copy paste this into your site; just update the endpoint URL and maybe tweak the CSS a bit 👍.

## Testing, and launch

![dramatization of launching email subscribers by showing Immortan Joe releasing water from his desert tower](/images/email-subs-with-modal/release-the-emails.png)

I released the functionality on my site recently and now have four, count em, four (4) subscribers! Gmail's SREs feel trouble in the air
whenever I push a new blog post.

Here's what the last sent email looked like. I published a new post on my website around 5PM on the day, and an hour or so later the Modal cronjob ran and delivered
this email to each subscriber.

![example sent email](/images/email-subs-with-modal/example-sent-email.png)

If you set this up and need a first subscriber to test things, hit me up on Twitter or Reddit and I'll
be happy to be a testcase!

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
