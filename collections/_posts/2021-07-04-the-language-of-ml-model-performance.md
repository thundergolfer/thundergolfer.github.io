---
layout:     post
title:      How can an ML model perform highly and poorly at the same time? 
date:       2021-07-04
summary:    An instance of unhelpful term overloading in machine learning engineering. 
categories: machine-learning communication
---

It can when you are using the word "performance" in two distinct ways. 

This is a short post about how I feel that the term "performance" is unhelpfully overloaded in machine learning engineering. Recently this overloading has created communication annoyances at work as we attempt to talk about software systems involving machine learning amongst data scientists, backend engineers, and product managers. I don't reach firm conclusions about how to resolve the term overloading, and welcome help in finding a way to do so that isn't too weird.

The two distinct kinds of performance that a machine learning model can be said to have are:

1. The speed, volume, and stability of system behaviour subject to system resource constraints (CPU, memory, network bandwidth, etc.). We desire fast *response times* and maximum system *throughput*.
2. The extent to which a system performs its objective. With machine learning models this typically involves predicting some label with a certain accuracy, but may involve optimizing a number of other statistical metrics (perplexity, ROC, precision, log loss, etc.)

In this post these distinct meanings are called *first-kind performance* and *second-kind performance*, respectively.

When writing about second-kind performance, the dominant terminology online appears to be an embrace of the overloaded "model performance". [Model Cards for Model Reporting](https://arxiv.org/pdf/1810.03993.pdf) describes industry-advancing work in communication about machine learning models, and uses "performance" only to mean second-kind performance. Google's [*Rules of Machine Learning*](https://developers.google.com/machine-learning/guides/rules-of-ml) uses "model performance", "ranking performance", and "performance of the system", all referring to second-kind performance. The well known paper *[Machine Learning: The High-Interest Credit Card of Technical Debt](https://storage.googleapis.com/pub-tools-public-publication-data/pdf/43146.pdf)* uses "prediction performance" and "system performance" to refer to the same. You get the idea. In cases where only the second kind of performance is being discussed, the writer can get away with ignoring the other kind of performance. The majority of machine learning content online is focused on model training, where the first kind of performance is much less relevant. But when needing to integrate machine learning into production backend systems first-kind performance is very much relevant, and you run into problems with the term overloading.

In Facebook's [*Powered by AI: Instagram's Explore recommender system*](https://ai.facebook.com/blog/powered-by-ai-instagrams-explore-recommender-system/), their system uses tiers of trained models *because it is constrainted by first-kind performance concerns*. Here we have a clear mixing of the two kinds of performance. Instagram's Explore recommender system is run at such scale that it matters both that the system has fast response time (first-kind performance) and best fulfils its objective function (second-kind performance). In order to avoid term overloading in their post they use "computational efficiency" to mean first-kind performance. 

> we use a three-stage ranking infrastructure to help balance the trade-offs between ranking relevance and computation efficiency.

This language quoted above is how they avoid saying "balance the trade-offs between model performance and model performance". 

## Isn't *model* performance clearly the first kind?

I don't think so. The Facebook example is demonstrative enough; some ranking models are so computationally expensive that their first-kind performance is salient in system design. At work the serving code used by HTTP model servers is so standardised that meaningful differences in first-kind system performance can only be differences in the first-kind performance of the models housed in that serving infrastructure. 

## Isn't this making a mountain out of a molehill?

Quite possibly, but a large enough part of software engineering is technical communication and ambiguous communication is bad technical communication. I've been involved in enough confusion about this already to make a short post, and I'd like it if we just have better terminology here to avoid the term overloading and get on with our work. 

I've previously suggested "model quality" to mean second-kind performance,  but this is not frequently used out in industry and so it's not a great option. An alternative to using a whole other word is just adding specifiers:

- model serving performance: first-kind performance
- model objective performance: second-kind performance

**Using different words**

- model accuracy: obviously first-kind performance but accuracy isn't always the relevant metric
- model quality: should only be used for second-kind performance
- model fitness: second-kind performance. No one uses this.

## Conclusion

So that's my short fuss about the use of the word "performance" in machine learning engineering. If you can't say what you mean you can't mean what you say.
