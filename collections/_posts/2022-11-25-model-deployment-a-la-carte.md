---
layout: post
title: "Model deployment à la carte"
date: 2022-11-25
summary: A survey of ML model deployment system design space.
categories: machine-learning mlops
---

What are all the viable ways of deploying a machine learning model?
In the interest of avoiding system design tunnel vision, I’ve been thinking about this question in recent months.
To expel the nagging question from my mind, I’ve written this quick overview.

Before going into details of each, here’s a high-level breakdown:

- **Deployed as first-party code library or data**
  - Not deployed, just living on a laptop
  - Server based
  - Client/edge device
    - Browser
    - Mobile device
    - Embedded
  - Search / database backend
  - Batch job
- **Deployed as local subprocess**
- **Deployed as RPC server**
  - Centralized RPC service
    - Unified
    - Decomposed
  - Service-oriented, encapsulated
  - Managed/Vendor API

I’ve come up with three broad categories, distinguished by the kind of client a deployed model has and the manner of interaction
between the client and the model. Within those categories, I break things down into subcategories of implementation.

## 1. **Deployed as first-party code library or data**

You can deploy a trained model by compiling it or packaging it into an application code module. As long as the model implementation is in a format compatible with your application runtime the code/data is just an `import` away.

In this setup the client of the trained model is the same process that stores and executes the trained model itself. Bog-standard intra-process communication, so simple and obvious no one really uses the term intra-process communication.

This method of model deployment has a lot to recommend it. The process of model delivery and evolution reduces to the process of regular first-party code dependency management. Everything you already use to ship non-ML code to users just works**™** for ML models. Operationally, you’ve added minimal complexity to your software systems.

Expressing trained models as first-party code and/or data is easy for simple models like logistic regression or Naive Bayes. You can write the algorithm in Java, Python, whatever, and load the weights into memory at application start.

For very complicated models, expressing implementation in code or data compatible with your application runtime becomes complicated. Until recently, running neural networks in the common JVM runtime was difficult, but [now we have ONNX](https://onnxruntime.ai/docs/get-started/with-java.html). ONNX brings neural networks to the JVM by defining a _serialization_ format for trained models that is runnable in ONNX’s specialized runtime.

### Not deployed, just living on a laptop

Starting with the absolute basics, you can just not deploy your model. Imagine your write some program to produce the model and run inference on it, probably in Python. For whatever reason, you and your company doesn’t care enough to do the work to make that model work off your machine, so the model’s inference requests are brought to that one machine. If this sounds like a massive tech debt issue, that’s because it is.

### Running on a server

![running-as-lib-on-server.svg](/images/model_deployment_a_la_carte/running-as-lib-on-server.svg)

If you’ve got a trained model that can run alongside the rest of your product’s application code in a single runtime, an obvious move is just build the trained model into your application package and ship it to prod.

As said above, being able to treat model artefacts as quite like normal first-party library dependencies is quite an operational load-off. A lot of problems just don’t exist.

```python
import models

def handle_order_creation(req):
    job = _create_job(req)  # send to job queue
		...
    features = _fetch_order_wait_time_features(req) # feature retrieval
		predicted_wait_time_secs = models.wait_time_v1.predict(req)
    ...
    return response({
        "id": job.id,
        "type": "order",
        "metadata": {
            "expected_wait_time_secs": predicted_wait_time_secs,
        }
    }, 200)
```

However, even if you can get your trained model to execute within your application runtime alongside all the rest of your product’s code, you may not want to.

### Client/edge device

![client-device-ml.svg](/images/model_deployment_a_la_carte/client-device-ml.svg)

In this subcategory, the client process is still the same process as the model’s, but the _location_ of that process is different and interesting. The process is running in an end-user’s internet browser, mobile phone, laptop, or on some other non-personal computer tech: a thermostat, weather sensor, or video camera.

**Browser**

todo

**Mobile device, (_or laptop)_**

todo

**Embedded**

todo

Linux supported by TFlite

### Search / database backend

todo

### Batch job

todo

## 2. **Deployed as local subprocess**

![local-subprocess.svg](/images/model_deployment_a_la_carte/local-subprocess.svg)

This is probably not a common deployment pattern, but it is available to you. In this scenario, you don’t want to or cannot run the trained model in the same process as the client. So you do inter-process communication but only local and relatively simple file-based or socket-based communication. The client process and the model process still run within the same machine/VM.

This setup always felt hacky to me. ...

## 3. **Deployed as RPC server**

The final deployment category for setups where the trained model process is accessible only remotely over the network. The client is another computer making a request to the model’s computer, likely over HTTP.

This setup is probably the most commonly talked about in the ML ecosystem. The ‘run your model in a Flask server’ approach is seen all over the blogosphere and open-source landscape.

TODO describe why you’d want to do RPC style deployment TODO

I see three major choices within this category, each with pretty interesting implications and tradeoffs. The first is to have all your models deployed to a centralized and typically platform/infra supported ‘inference service’ or ‘scoring service’. The second is to instead ‘colocate’ deployed models as servers responding _only_ to some parent service client; the model server is encapsulated by the parent service just as the parent service’s DB is. The third option is to serialize your trained model and ship it to some third-party that will run the model for you and expose it via a HTTP API.

### Centralized RPC scoring/inference service

A centralized RPC ‘scoring service’ or ‘inference service’ is a ...

To further complicate things, there are at least two different styles of centralized inference service.

[https://doordash.engineering/2020/06/29/doordashs-new-prediction-service/](doordash.engineering/2020/06/29/doordashs-new-prediction-service/)

**Unified**

![inference-service-unified.svg](/images/model_deployment_a_la_carte/)

A ‘unified’ inference service is one where the service’s business logic and the models deployed within that service share an instance host. A high-level, the centralized inference service can be horizontally scaled by just stamping out more copies of a single inference service server application. The service architecture would look something like this:

**Decomposed**

A ‘decomposed’ inference service separates the service’s business logic concerns from the execution of the deployed models it manages. Business logic and models run on different kinds of host instances.

The service architecture would look something like this:

![inference-service-decomposed.svg](/images/model_deployment_a_la_carte/inference-service-decomposed.svg)

In this structure the inference service’s business logic is fulfilled by what very closely resembles the common _API frontend_ architecture component. This inference service API frontend is responsible for:

- request caching
- request validation and unpacking
- request enrichment by calling out to feature stores (or even other models)
- request dispatch (to deployed models)

The major trade-offs of the centralized service approach are:

1. Resource management. The simple horizontal scaleability of the unified setup may struggle with sets of models having wildly different resource demands.
2. The operational and organization complexity of an organization’s machine learning functionality is mostly borne by one team who owns and runs the centralized service. This is a single point of failure, and a communication bottleneck.

### Service-oriented, encapsulated

![service-oriented-ml-server.svg](/images/model_deployment_a_la_carte/service-oriented-ml-server.svg)

A significant aspect of the service-oriented approach to RPC server model deployment is that it likely better respects _Conway’s Law_.

The major trade-offs of this approach are:

1. foo
2. bar

### Managed/vendor API

![ml-vendor.svg](/images/model_deployment_a_la_carte/ml-vendor.svg)

The third and final choice, as I see it, is to pay someone some money to handle servers for you. You pay money to X vendor, and they make your trained model available to you via API, hopefully cheaply and reliably.

The major trade-offs of this approach are:

1. Flexibility.
2. Cost. You’ll be paying a large premium over the base cloud/datacenter costs of running your own model serving.

## Any more?

Have I missed something? ...

---

This post started life as a hastily made internal presentation at Canva. See the Canva preso below:

<div style="position: relative; width: 100%; height: 0; padding-top: 56.2500%;
 padding-bottom: 0; box-shadow: 0 2px 8px 0 rgba(63,69,81,0.16); margin-top: 1.6em; margin-bottom: 0.9em; overflow: hidden;
 border-radius: 8px; will-change: transform;">
  <iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none; padding: 0;margin: 0;"
    src="https:&#x2F;&#x2F;www.canva.com&#x2F;design&#x2F;DAFTEb0AoSc&#x2F;view?embed" allowfullscreen="allowfullscreen" allow="fullscreen">
  </iframe>
</div>
<code style="background-color: #fff">title:</code>
<a href="https:&#x2F;&#x2F;www.canva.com&#x2F;design&#x2F;DAFTEb0AoSc&#x2F;view?utm_content=DAFTEb0AoSc&amp;utm_campaign=designshare&amp;utm_medium=embeds&amp;utm_source=link" target="_blank" rel="noopener">
    <strong> ML model deployment, N ways</strong>
</a>
