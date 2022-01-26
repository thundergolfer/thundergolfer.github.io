---
layout:     post
title:      How To Ask For Help In Slack
date:       2021-02-24
summary:    The help-needer's and question-asker's checklist 
categories: communication slack
---

## The Checklist

- [x]  I have 'rubber duck debugged' my own question.
- [x]  I checked that this question hasn't been asked before.
- [x]  I have noted in my message what I've tried.
- [x]  I have avoided the 'XY problem' by clearly detailing the core problem, X.
- [x]  I have provided specifics of my issue, not vague references or descriptions.
- [x]  I have provided URL links to relevant content, and where possible the URL links are immutable.
- [x]  I have **not** included screenshots of text in my message.
- [x]  I have not used obscure acronyms or abbreviations.
- [x]  I have formatted my message well, particularly paying attention to code formatting and headings.
- [x]  I have not just said “hi” and waited for a reply.
{: style='list-style-type: none; padding-left: 0'}

## Checklist Item Details

### **1. I have 'rubber duck debugged' my own question.** ✔️

["Rubber duck debugging"](https://en.wikipedia.org/wiki/Rubber_duck_debugging) is a well known debugging trick in programming, and it should be done where appropriate before asking a question or dumping an error into Slack.

> 👩🏻‍🔧 I created my model. I made my controller. I’m using the model to retrieve my video games in my controller… but right now it’s retrieving them all. 
> 
> 🐤 ...
> 
> 👩🏻‍🔧 I only want to retrieve the ones made after…”
> 
> 👩🏻‍🔧 Oh dammit. OF COURSE. I need to use a `where` clause in the video game retrieval line to restrict it to fetching only video games with a `production_date` greater than or equal to `'1999-01-01'`!
> 
> 🐤 ...

### **2. I checked that this question hasn't been asked before.** ✔️

This is a really simple one, and this step should be burned in to your mind as a pre-step before seeking any help from team members. The main places to check:

- **Google:** *LetMeGoogleThatForYou* is to be avoided.
    - Github Issues and StackOverflow posts are key resources reachable via Google.
- **Slack:** Certainly worth checking because there's a chance a team member has had the same question or problem. This doesn't mean posting a Slack message. It means typing your problem into Slack search.
- **Confluence:** the search is garbage, but it's still worth a try for internal stuff.
- **Engineering Handbook:** At Canva we're building an 'Engineering Handbook' for high-quality and long-lived technical content and more and more questions are becoming answerable by reference to the right handbook document instead of Confluence.

![](/images/how_to_ask_for_help_in_slack/02.png)

### **3. I have noted in my message what I've tried.** ✔️

If you haven't tried to answer a question yourself or debug a problem yourself, that's not good. This checklist item will prompt you to think about doing that.

In your message you can note:

- That you checked the question hasn't been answered before
- Any resources you've you consulted already (StackOverflow, Github)
- Any debugging you've done (post specifics!)

Now if you've been awesome and done a lot of prior work attempting to answer your question or fix your problem, you might find that including preamble about 'what you've tried' seriously bloats your message. Not to worry! This is where Slack's [threading functionality](https://slack.com/intl/en-au/help/articles/115000769927-Use-threads-to-organise-discussions-), or Github's [collapsible section](https://gist.github.com/pierrejoubert73/902cc94d79424356a8d20be2b382e1ab) formatting come in handy:

> 👩🏻‍🔧 Hey I'm having trouble discovering the root cause of the bug described in [foocorp.atlassian.net/browse/MX-123](http://foocorp.atlassian.net/browse/MX-123) and I'd love some assistance. Details of my investigation so far in thread. 🧵...

### **4. I have avoided the 'XY problem' by clearly detailing the core problem, X.** ✔️

The XY problem shows up when the person asking for help obscures their real issue, X, because instead of asking directly about issue X, they ask how to solve a secondary issue, Y, which they believe will allow them to resolve issue X. However, resolving issue Y often does not resolve issue X, or is a poor way to resolve it, wasting time and producing suboptimal solutions if the transgression of the XY problem is not discovered during communication.

*In summary:*

**X:** Your *actual* problem

**Y:** The problem you're asking for help with.

✅  `X == Y`

❌  `X != Y`

*As an example:*

> 🙎‍♂️ How can I echo the last three characters in a filename?
> 
> 😼 If they're in a variable: `echo ${foo: -3}`
> 
> 😼 Why 3 characters? What do you REALLY want?
> 
> 😼 Do you want the extension?
> 
> 🙎‍♂️ Yes.
> 
> 😼 There's no guarantee that every filename will have a three-letter extension, so blindly grabbing three characters does not solve the problem.
> 
> 😼 Go with `echo ${foo##*.}`

There is a neat website dedicated to this problem: [https://xyproblem.info/](https://xyproblem.info/)

### **5. I have provided specifics of my issue, not vague references or descriptions. ✔️** 

This one is easy to slip up on, but in my opinion diligently reviewing questions and problem descriptions for specifics provides outsized value to message receivers and *particularly* future searchers.

Here is an example of a vague message, which below will be edited to be more specific:

> 🙎‍♂️ Hey I'm having trouble with this DB thing. I ran the setup command but it didn't work.

And now edited to be specific:

> 🙎‍♂️ Hey I'm working on setting up the new billing micro-service's DB locally . I ran `rake db:setup` but keep getting the error:
`rake aborted!
Gem::LoadError: mysql2 is not part of the bundle. Add it to Gemfile.`

The effect of vagueness and implicitness is that it burdens the reader with the need to do many extra brain-cycles to resolve all the ambiguity and missing information, so you should write messages like the second not the first.

The second provides access to background context, isn't vague about their task being running the database locally, provides the exact command they ran, and the exact error message.

### **6. I have provided URL links to relevant content, and where possible the URL links are immutable ✔️** 

URLs are certainly a way to provide specificity, so this checklist item is related to the one above. Good URL usage quickly connects readers to the information they need to help you. Don't say "We have run into a strange Argo problem to do with volume claims". Say "We have run into [https://github.com/argoproj/argo/issues/2415](https://github.com/argoproj/argo/issues/2415)". Then readers, present and future, will know *exactly* what you're talking about.

Any URL you use should be immutable, whenever possible. Immutable URL links are those that will link to functionally the same content whether a reader clicks it the day you pasted it in, or years later. A great example of a mutable link versus an immutable link is URL links to Github code. The following is a *mutable* link, tracking the `master` branch reference, which obviously changes frequently:

[https://github.com/facebook/react/blob/master/packages/react/src/React.js](https://github.com/facebook/react/blob/master/packages/react/src/React.js)

This, on the other hand, is an immutable link to code because it uses the git commit hash:

[https://github.com/facebook/react/blob/efc57e5cbbd618f3c98d941c48eec859026c2dcb/packages/react/src/React.js](https://github.com/facebook/react/blob/efc57e5cbbd618f3c98d941c48eec859026c2dcb/packages/react/src/React.js) 

That link will always point to the same content, as long as Github is around. 

A similar dynamic can be found in versioned developer documentation. The following link tracks "latest", and "latest" is clearly a moving target:

[https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_registry](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_registry) 

This link will always point to the same version: 

[https://registry.terraform.io/providers/hashicorp/aws/3.24.1/docs/resources/glue_registry](https://registry.terraform.io/providers/hashicorp/aws/3.24.1/docs/resources/glue_registry)

Now, there's a small caveat that sometimes it is inappropriate to link to immutable links. In cases where what you link to updates with new information and you desire that future readers view those latest updates, use the mutable link. In other cases immutable links aren't available, and thus you have to use mutable links.

When you anticipate that a reader will be expecting to clicking a mutable link, it can be good idea to call attention to your use of an immutable link with a short parenthetical statement like "(link pinned at @1.2.3)" or "(link pinned at latest commit)".

### **7. I have NOT included screenshots of text in my message. ✔️**

Screenshots of text are a usability and accessibility disaster. They:

- Cannot be searched
- Cannot be copy-pasted into a Google search, a REPL, or an IDE
- Cannot be parsed by a screen-reader

Taking a screenshot is quick, a fraction quicker than copying and formatting text in the message box, but that fractional saving is more than wiped out by the struggles it causes over time.

An example of what *not* to do 👇

![](/images/how_to_ask_for_help_in_slack/07.png)


### **8. I have not used obscure acronyms or abbreviations. ✔️** 

Among people 'in the know' acronyms work usually just fine, and do save time. Over time though, acronym use creates an organisational communication mess where your teammates, *particularly* the new ones, get lost in a sea of literally hundreds of acronyms, dozens of them company and even team specific.

Elon Musk sent a now famous memo to his SpaceX team: 

> There is a creeping tendency to use made up acronyms at SpaceX. Excessive use of made up acronyms is a significant impediment to communication and keeping communication good as we grow is incredibly important. Individually, a few acronyms here and there may not seem so bad, but if a thousand people are making these up, over time the result will be a huge glossary that we have to issue to new employees. No one can actually remember all these acronyms and people don't want to seem dumb in a meeting, so they just sit there in ignorance. This is particularly tough on new employees. - Elon Musk

It is annoying to take the extra effort to unroll your acronyms, say from "SoT" to "Source of Truth (SoT)", but outsiders and new employees will thank you for stopping them confusing "SoT" for ["Sea of Theives"](https://www.google.com/search?q=SoT&oq=SoT&aqs=chrome..69i57j46i199i291i433j0i433j46i175i199j46i175i199i395j0i131i395i433j0i395i433.1155j1j7&sourceid=chrome&ie=UTF-8), the [french word for "fool"](https://translate.google.com/?sl=fr&tl=en&text=SOT&op=translate&hl=en), or a [person who frequently drinks too much alcohol](https://www.vocabulary.com/dictionary/sot).

### **9. I have formatted my message well, particularly paying attention to code formatting and headings. ✔️**

Markdown formatting, a very minimal markup standard which Slack and Github closely follow, provides a handful of formatting options. They ought not to be neglected. The most often neglected is the `code` formatting. Code is much easier to scan and parse out of messages when formatted properly. Even when code is not competing with other text in a message, the `code` formatting calls out to a viewer that they're reading code, not prose, which is useful in of itself.

Logs without formatting are a particularly bad case. Consider these unformatted logs:

![](/images/how_to_ask_for_help_in_slack/09a.png)

This example is better than others I've seen, as it contains no stack-traces which tend to look unreadable in horizontally-compressed plaintext, but we can see that Slack has interpreted parts of the logs *as emojis*. That clearly won't do.

Besides code, good use of **bold**, *italics,* and hyperlinking is always appreciated. Like this message:

![](/images/how_to_ask_for_help_in_slack/09b.png)

### **10. I have not just said "hi" and waited for a reply. ✔️** 

Give all the necessary context up-front, so your question or problem can be immediately actioned *asynchronously* by the receivers. We don't want this:

![](/images/how_to_ask_for_help_in_slack/10.png)


There is a neat website dedicated to this problem: [https://nohello.net/](https://nohello.net/). 

## That's it. That's the checklist.

Do all 10 things and people will love to interact with you on Slack, Github, or any other work messaging platform. You will also be loved by the people that tread the same paths that you once did, running into the same questions and the same issues.

Oh, and **bonus item**. If you solve your problem some time after you posted the original question or issue, go back and post the answer.

![](/images/how_to_ask_for_help_in_slack/bonus.png)

---
