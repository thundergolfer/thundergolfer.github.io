---
layout:     post
title:      "Junior Theme: Why You Should Use It"
date:       2018-04-23
summary:    Sharing a new theme I developed for myself
categories: jekyll portfolio personal-website
---

![front page mockup of junior theme](/images/junior-theme/junior-front-page.png)

If you’re looking for a [Jekyll](https://jekyllrb.com/) theme that fulfils all the main use cases of a personal portfolio site and blog, where most themes only handle a subset, then you should use [Junior Theme](https://github.com/thundergolfer/junior-theme).

I started with a theme that handled basic static page blog posts and an ‘About’ page, but like most other blog-focused themes it was missing:

* A resumé page with high-fidelity printing functionality
* A way to showcase image-focused content, like design work or programming projects that could use visual communication
* A page showcasing my open-source work, that *wasn’t just a link to Github’s [user profile page](https://github.com/thundergolfer)*.

After a bit of toil, I introduced these features into my personal website and decided that it would be worth packaging into a theme. I also had a particular idea of how I wanted the theme to look. It’s hardly unique, just CSS to create a black and white minimal appearance, but it’s done it a way that differentiates it from the major minimalist Jekyll themes like [Pixyll](http://pixyll.com/),  [Centrarium](http://bencentra.com/centrarium/), or [Gravity](https://github.com/hemangsk/Gravity).

### The Resumé Page
[Here it is showing my resumé](/resume/). The content is plain markdown, and clicking the “PDF” button on the right gets you a `.pdf` doc that looks very close to what you see on the site.

That’s your CV solution, hosted and printable.

### Image-focused Content
Junior Theme shows off its `portfolio` layout on the [Sketch & Design](http://juniortheme.live/design/) page. On that demo page I have image dominated design content, but I had in mind that this sort of functionality would also be used for showing off programming projects.

### Open-Source Showcasing
The Github [user profile page](https://github.com/thundergolfer) can show only 6 repositories, which was the main annoyance for me. In general though I wanted more control over how I communicated my Github presence on my website. Just linking to my profile wasn’t really going to satisfy me.

What I’ve got now is a page that pulls from Github’s API *all* my public projects so that I can display their critical information in a list.

In future I’ll be looking to extend this page to show more relevant information to the page viewer that I wouldn’t want to just put in the repo’s description or it’s `README.md` . For example I’d like to display the tech stack for each project.

-----

If you become a user of the Junior theme and want to see a new feature introduced, or something improved/fixed, then [submit an issue](https://github.com/thundergolfer/junior-theme/issues). I’m keen to get this theme used by others, and will be happy to address your needs.
