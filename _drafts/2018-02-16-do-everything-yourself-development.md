---
layout:     post
title:      “DEYD - Do Everything Yourself Development“
date:       2018-02-16
summary:  A strategy for building stronger programming fundamentals
categories: software-engineering methodology
---

DEYD is an initialism for a development methodology, like those other initialisms we have for Test-Driven-Development, Behaviour-Driven-Development, Storytest-Driven-Development, and [Copy-Driven-Development](https://en.wikipedia.org/wiki/Copy_and_paste_programming). It’s a style of programming that I think is potentially quite helpful to very junior programmers, like students. Described plainly, it is the avoidance of using built-in abstract data-type (ADT) implementations and common library functionality, instead opting to write and rewrite implementations of these things *yourself*. The intended benefit of this behaviour is not to make you more productive (it certainly won’t) but to make you a much better programmer by revealing gaps in your knowledge and capabilities and having you fill them. This is of particular importance I think to students who:

1. Use a highly expressive language like Python, which is very much ‘batteries included’
2. Will in future be attempting to succeed in difficult technical interviews

When you get going with Python, things can begin to feel easy. With so many built-in packages and utility functions, as well as a huge package ecosystem, many challenging tasks that help train a programmer to think better about their code and their software design are reduced to a Stack Overflow lookup and a single copy-and-pasted line. I myself love Python, and enjoy how quickly I can skate over tricky problems with it, but believe that in the long term it’s going to have me designing worse programs and being frustrated in technical interviews.

DEYD is part-way towards the solution, adopting a more bareback language like Golang, or C is probably also necessary to fully reintroduce yourself to core problems in programming. Remember integer overflows? Have you even forgotten *arrays*?

Here’s some interesting, non-trivial programming problems that once had to be solved by good programmers, but now have their solutions sit on [stackoverflow.com](https://stackoverflow.com/) or in the standard library:

* Reverse a string. `reverse = “hello world”[::-1]`  (6 characters!)
* Handle duplicates. `mySet = set([1, 2, 3]); mySet.add(2)`
* Edit distance. `pip install distance`
* The [Decorator pattern](https://en.wikipedia.org/wiki/Decorator_pattern). `@some_decorator`
* Caching. `from functools import lru_cache`
* Sorting. `sorted()` (I didn’t even know [how python sorted lists](http://svn.python.org/projects/python/trunk/Objects/listsort.txt) until recently. I just used it)

The sense for what tool will solve your problem is a good thing to have, and it seems often that it gets you quite close to being a half-productive programmer, but without getting into the mud and solving core programming problems you won’t be exercising your brain into become a fundamentally better coder.

So adopt this methodology and next time you reach for the ‘batteries included’ option, stop yourself and find out how well you really know the building blocks of your software. Instead of `set()` you’ll create `diySet()` and put it in a package in your project called `DIY` . Alongside your implementation you’ll write your unit tests, and be forced into actually thinking about the characteristics of things you take for granted.

It would be more than a little annoying to have to fully implement the `set()` ADT from scratch when you just want to de-dupe a list, so don’t. Write only what you need, write it well, and make sure it works.  Taking our de-duplication use-case, our DIY code could look like.

```python
# module: DIY.py

def deduplicate(collection):
    m = {} # Use OrderedDict if need ordering maintained
    for item in collection:
        m[item] = True
    return [*m.keys()]
```

Instead of doing `deduplicate = lambda collection: list(set(collection))` we’ve put down the `set()` builtin and used a hashmap,  and maybe discovered something about how the `set()` ADT is actually implemented.

### Is this just a way to do more Leetcode practice?

Well, kinda, but not really. [Leetcode](https://leetcode.com/) doesn’t bother asking you to design a `Set`  or a Decorator AFAIK. Solving these challenges is just as relevant to your programming training as typical data structures & algorithms stuff like sorting. Oh, and yes, I know that certain great companies like [Atlassian](https://www.atlassian.com/) and [Stripe](https://stripe.com) will ask you to do things like the above in interviews. They’ve asked me.

### It’s not DEYATTD

This isn’t do everything yourself all the time (ATT). Everytime you start typing `f.readlines()`  you don’t have to stop and start with `def  my_read_lines(f): ...`, but every time you come up to a non-trivial problem which you haven’t solved yourself in a long time (or ever), well, jump in and do-it-yourself.

### Closing

I came into this kind of thinking after being slapped by my own incompetence when tackling what appear as a software engineer’s bread-and-butter problems. I mean, I’ve been off training NLP classifiers, building web apps, wrangling distributed NoSQL DB systems, and yet here’s a bug in my DIY [multimap](https://github.com/google/guava/blob/master/guava/src/com/google/common/collect/Multimap.java)….

Adopting Golang as a development language also certainly contributed. There’s no `Set()` implementation in Golang, which I realised after jumping online. One of the supported responses to this absence though was “why don’t you just write it yourself? It’s not too much work”. It had been a while since I’d come across this attitude, but it is one that exists in the Golang community. I believe that since I started writing in Golang rather than Python the shroud has been pulled back a bit and I’ve been able to see weaknesses in myself that needed to be addressed but that were so easy to ignore in beautiful Python.

So yeah, DEYD, try it.
