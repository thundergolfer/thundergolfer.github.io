---
layout:     post
title:      "A Foundation Result in Machine Learning..."
date:       2017-07-07
summary:    Diving into single-layer perceptrons and information theory
categories: machine-learning information-theory rnn
---

> A foundational result in machine learning is that a single-layer perceptron with N<sup>2</sup> parameters can store at least 2 bits of information per parameter ([Cover, 1965](http://webcourse.cs.technion.ac.il/236941/Winter2012-2013/ho/WCFiles/Cover65.pdf); [Gardner, 1988](http://iopscience.iop.org/article/10.1088/0305-4470/21/1/030/pdf); [Baldi & Venkatesh, 1987](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.58.913)). More precisely, a perceptron can implement a mapping from 2N, N-dimensional, input vectors to arbitrary N-dimensional binary output vectors, subject only to the extremely weak restriction that the input vectors be in general position.

....Wait what? Foundational? Was this in the Coursera Course?!

This short passage comes from [*Capacity and Trainability in Recurrent Neural Networks*](https://arxiv.org/pdf/1611.09913.pdf), a paper exploring empirically the nature of Recurrent Neural Networks. Their exploration extends much earlier work done to study simple single-layer perceptron networks, and it is from that decades old work that this "foundation result" comes.

So, I found this passage quite dense when I first read it. The following questions featured immediately and prominently:

* What does it mean for a network parameter to "store information"?
* What is "general position"?
* How does the implementation of that mapping from inputs to outputs entail "2 bits of information per parameter"?
* Why are their 3 references from physics journals? They talk about a *Spin Glass*. What's that?

I didn't get it, but this is apparently a foundational result, so off I went trying to.

>  a single-layer perceptron with N<sup>2</sup> parameters ... can implement a mapping from 2N, N-dimensional, input vectors to arbitrary N-dimensional binary output vectors...

The network described looks like this:

### IMAGE OF NETWORK

It is single-layer, so there are no intermediate (hidden) layers between the input nodes and the output nodes. Because it receives `N` dimensional vectors, and outputs `N` dimensional vectors we have `2N` nodes with `N X N` (or N<sup>2</sup>) connections. Each of these connections has an associated *weight*, and it is these N<sup>2</sup> weights that are our N<sup>2</sup> "parameters".

This is the network can can store `2 X N X N` bits of information utilising `N X N` parameters.

> 2 bits of information per parameter

It is important to understand what it means for the neural network to store information, and it may be quite a foreign idea to those who are used to thinking of neural network's ability to decide sentiment, recognise faces, or translate languages, rather than think about their relationship with the mathematical idea of *information* and it's storage in parametric models like neural networks.

I will quickly give an intro to Information Theory, but see [this from Stanford University](https://web.stanford.edu/~montanar/RESEARCH/BOOK/partA.pdf) for something more comprehensive.

Information exists in contrast to uncertainty. Given a unknown variable or set of variables, uncertainty is higher when it is 'harder' to predict the values of that variable/variable group. For example, a typical coin can be flipped and the outcome will be heads or tails. The outcome of the flip is the unknown variable; it is 50% likely to be heads and 50% likely to be tails. `2` possible outcomes.

A die on the other hand has `6` equally possible outcomes. So for a die throw, predicting the value of the unknown variable is 'harder'. How is extra uncertainty quantified? *Entropy* is the equation that defines uncertainty. This is the equation for Entropy, where `X` is the uncertain outcome, and `p(x)` is the probability distribution of the values that outcome can take. In our examples things are simple, because all potential values of the outcome are equally likely.

H<sub>X</sub> ≡ − (SUM over x∈X) p(x) log2 p(x)





------
