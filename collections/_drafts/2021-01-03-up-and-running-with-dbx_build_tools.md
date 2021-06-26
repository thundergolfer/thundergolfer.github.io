---
layout:   post
title:    Up And Running with Dropbox's Bazel Python Rules, <code>dropbox/dbx_build_tools</code>
date:     2021-01-03
summary:  TODO
categories: software-engineering bazel
---

Being a maintainer of `bazelbuild/rules_python` (whenever I scrounge sometime) I had to eventually checkout Dropbox's Python rules for Bazel, open-sourced mid-2020. Dropbox adopted Bazel really soon after it escaped Google in 2015, and so their rules are highly mature and battle-tested, worked on by super-experienced Python devs like [Benjamin Peterson](https://discuss.python.org/t/steering-council-nomination-benjamin-peterson/665), and even on by the most senior Python person there is, the BDFL. I think the `bazelbuild/rules_python` ruleset has much to learn from the Dropbox rules. So, finally having some free time once finishing part-time study, I christened a brand-new Git repository `[dropbox-style-github-repo](https://github.com/thundergolfer/dropbox-style-python-repo)` and had some fun stitching C code to Python using Dropbox's rules.

I hit some roadblocks on the way to getting a working Python C-bindings demo, but did get things going. The Dropbox rules have a hermetic toolchain setup that does not support OSX, in contrast to `rules_python` which is not hermetic in a standard setup but therefore can more easily be run on Linux, OSX, or Windows. I also came across places where the Dropbox rules didn't work because they made an assumption that was valid when they lived in Dropbox's internal systems, but didn't work post-open-sourcing. These problems weren't blockers though, so I documented them in comments and Jason from Dropbox fixed them really quickly after we got in touch via the Bazel Slack. However, AFAIK the MyPy integration in their rules still has the 'works within Dropbox only' issue.

### Github Codespaces

Because I couldn't use these rules on my OSX-based laptop, I needed a Linux development environment. I'd been curious about trying Github's *Codespaces* feature, released around 8 months ago, and so figured that'd be the first thing I tried.

I expected a pretty slick web IDE experience from Github, and that's basically what I got. I'd already requested early access so could jump in and create one of maximum two codespaces (shown below). 

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e75dc02e-0e51-45a8-87b4-4473bd9bc310/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e75dc02e-0e51-45a8-87b4-4473bd9bc310/Untitled.png)

I switched away from the default codespaces development container to ensure I had a high enough version of `gcc` for the Dropbox rules to work, and went for the [Python3 image](https://github.com/thundergolfer/dropbox-style-python-repo/commit/2d6c286f71aaede3a0ac4c97b03654f6ce29125d) from `[microsoft/vscode-dev-containers](https://github.com/microsoft/vscode-dev-containers/tree/master/containers/codespaces-linux)`. After doing this, getting the hermetic Python toolchain to work was complete.

If you've got access to Github Codespaces, it should be trivial to open up the same web-based development environment that I used and just `bazel build //...` the Bazel workspace, which is pretty nice.

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/7603a78d-1751-458f-9365-288830df7de0/showing-how-to-open-gh-codespaces.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/7603a78d-1751-458f-9365-288830df7de0/showing-how-to-open-gh-codespaces.png)

### Using the Dropbox rules to bind C to Python

The Dropbox rules are not documented, and there's not much else online about them, so I'd bet that they're not beginner friendly, but I've got a decent amount of experience in Python and Bazel so it wasn't too hard for me to get something going. 

TODO

**The `BUILD` file generator, `bzl gen`**