---
layout: post
title: "Model deployment à la carte"
date: 2022-11-25
summary: A survey of ML model deployment system design space.
categories: machine-learning mlops
---

![hero image generated with stable diffusion using the following prompt: a table dinner of robots where robots are dressed like the characters from the midsommar movie, realistic detailed digital art by maxwell boas jessica rossier christian dimitrov anton fadeev trending on artstation cgsociety rendered in unreal engine 4 k hq](/images/model_deployment_a_la_carte/stable-diffusion-hero.png)

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

There are three broad categories, distinguished by the kind of client a deployed model has and the manner of interaction
between the client and the model. Within those categories, I break things down into subcategories of implementation.

## 1. **Deployed as first-party code library or data**

You can deploy a trained model by compiling it or packaging it into an application code module for
insertion into an existing application monolith or microservice.
As long as the model implementation is in a format compatible with your application runtime
the code/data is just an `import` away.

In this setup the client of the trained model is the same process that stores and executes the trained model itself.
Bog-standard intra-process communication, so simple and obvious no one really uses the term intra-process communication.

This method of model deployment has a lot to recommend it. The process of model delivery and evolution reduces to the
process of regular first-party code dependency management. Everything you already use to ship non-ML code to users just works**™** for ML models.
Operationally, you’ve added minimal complexity to your software systems.

Expressing trained models as first-party code and/or data is easy for simple models like logistic regression or Naive Bayes.
You can write the algorithm in Java, Python, whatever, and load the weights into memory at application start.

For complicated models, expressing implementation in code or data compatible with your application runtime becomes complicated.
Until recently, running neural networks in the common JVM runtime was difficult, but [now we have ONNX](https://onnxruntime.ai/docs/get-started/with-java.html).
ONNX brings neural networks to the JVM by defining a _serialization_ format for trained models that is runnable in ONNX’s specialized runtime.

### Not deployed, just living on a laptop

![Doing MLOps with 1 Macbook and a Juptyer Notebook](/images/model_deployment_a_la_carte/notebook-mlops-xkcd.png)

Starting with the absolute basics, you can just not deploy your model.
Imagine you write some program to produce the model and run inference on it, probably in Python.
For whatever reason, you and your company don't care enough to do the work to make that model work off your machine, so the model’s inference requests are brought to that one machine.
If this sounds like a massive tech debt issue, that’s because it is.

### Running on a server

![running-as-lib-on-server.svg](/images/model_deployment_a_la_carte/running-as-lib-on-server.svg)

If you’ve got a trained model that can run alongside the rest of your product’s application code in a single runtime,
an obvious move is just build the trained model into your application package and ship it to prod.

As said above, being able to treat model artefacts as just like normal first-party library dependencies is
quite an operational load-off. A lot of problems just don’t exist.

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

However, even if you _can_ get your trained model to execute within your application runtime alongside all the rest of your product’s code, you may not want to.

### Client/edge device

![client-device-ml.svg](/images/model_deployment_a_la_carte/client-device-ml.svg)

In this subcategory, the client process is still the same process as the model’s, but the _location_ of that process is different and interesting.
The process is running in an end-user’s internet browser, mobile phone, laptop, or on some other consumer computer digital device: a thermostat, weather sensor, or video camera.

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

This is probably not a common deployment pattern, but it is available to you. In this scenario, you don’t want to or cannot run
the trained model in the same process as the client. So you do inter-process communication but only local and relatively simple
file-based or socket-based communication. The client process and the model process still run within the same machine/VM.

This setup always felt hacky to me. ...

## 3. **Deployed as RPC server**

The final deployment category for setups where the trained model process is accessible only remotely over the network.
The client is another computer making a request to the model’s computer, likely over HTTP.

This setup is probably the most commonly talked about in the ML ecosystem. The ‘run your model in a Flask server’ approach is seen all over the blogosphere and open-source landscape.

TODO describe why you’d want to do RPC style deployment TODO

I see three major choices within this category, each with pretty interesting implications and tradeoffs.

- The first is to have all your models deployed to a centralized and typically platform/infra owned ‘inference service’ or ‘scoring service’.
- The second is to instead co-locate deployed models as servers responding _only_ to some specific parent service client —
  the model server is encapsulated by the parent service just as the parent service’s DB is encapsulated.
- The third option is to serialize your trained model and ship it to some third-party that will run the model for you and expose it via a HTTP API.

### Centralized RPC scoring/inference service

A centralized RPC ‘scoring service’ or ‘inference service’ is a ...

To further complicate things, there are at least two different styles of centralized inference service.

[https://doordash.engineering/2020/06/29/doordashs-new-prediction-service/](doordash.engineering/2020/06/29/doordashs-new-prediction-service/)

#### **Unified**

A ‘unified’ inference service is one where the inference service’s business logic (access control, rollbacks, feature retreival) and the models deployed within that service share an instance host.
This service may internally be known as the 'scoring service' or the 'inference service'.
At a high-level, the centralized inference service can be horizontally scaled by just stamping out more copies of a single inference service server application.
The service architecture would look something like this:

![inference-service-unified.svg](/images/model_deployment_a_la_carte/inference-service-unified.svg)

<p>
<strong style="color: #635bff">Stripe</strong> an example of a company with a unified inference service, which they call 
<a target="_blank" rel="noopener noreferrer" href="https://www.youtube.com/watch?v=HyYpMJNVoVk">Diorama</a>  — because a diorama is a kind of model, get it? 
<strong style="color: #FF3008">Doordash</strong> is another company following this path. They call their service <a target="_blank" rel="noopener noreferrer" href="https://doordash.engineering/2020/06/29/doordashs-new-prediction-service/">Sibyll</a> (an ancient Greek oracle).
</p>

#### **Decomposed**

A ‘decomposed’ inference service separates the service’s business logic concerns from the execution of the deployed models it manages.
Business logic and models run on different kinds of host instances.

The service architecture would look something like this:

![inference-service-decomposed.svg](/images/model_deployment_a_la_carte/inference-service-decomposed.svg)

In this structure the inference service’s business logic is fulfilled by what very closely resembles the common _API frontend_ architecture component.
This inference service API frontend is responsible for:

- request caching
- request validation and unpacking
- request enrichment by calling out to feature stores (or even other models)
- request dispatch (to deployed models)

The major trade-offs of the centralized service approach are:

1. Resource management. The simple horizontal scaleability of the unified setup may struggle with sets of models having wildly different resource demands.
2. The operational and organization complexity of an organization’s machine learning functionality is mostly borne by one team who owns and runs the centralized service.
   This is a single point of failure, and a communication bottleneck.

<p>
<strong style="color: #FF4500">Reddit</strong> is a company that deploys their ML like this, and they call the decomposed service the 
<a target="_blank" rel="noopener noreferrer" href="https://www.reddit.com/r/RedditEng/comments/q14tsw/evolving_reddits_ml_model_deployment_and_serving/">Gazette Inference Service</a>.
</p>

### Service-oriented, encapsulated

![service-oriented-ml-server.svg](/images/model_deployment_a_la_carte/service-oriented-ml-server.svg)

A significant aspect of the service-oriented approach to RPC server model deployment is that it likely better respects _Conway’s Law_.

The major trade-offs of this approach are:

1. foo
2. bar

<p>
<strong style="color: #04aeb5">Canva</strong> is a company that deploys their ML models like this.
</p>

### Managed/vendor API

![ml-vendor.svg](/images/model_deployment_a_la_carte/ml-vendor.svg)

The third and final choice, as I see it, is to pay someone some money to handle servers for you.
You pay money to X vendor, and they make your trained model available to you via API, hopefully cheaply and reliably.

The major trade-offs of this approach are:

1. Flexibility.
2. Cost. You’ll be paying a large premium over the base cloud/datacenter costs of running your own model serving.

### Serverless web endpoints

![serverless-cloud-ml-deployment.svg](/images/model_deployment_a_la_carte/serverless-cloud-ml-deployment.svg)

The best known serverless web endpoint solution is AWS Lambda, and when it launched in 2014 it was a poor
fit for model deployment. It only supported Node.JS, had a max memory limit of 1GB, and didn't support HTTP.
Fast-forward to 2022, and AWS Lambda now supports containers and has a memory limit of 10GB, and of
course supports HTTP — even without the painful API Gateway!

Open-source Function-as-a-Service (FaaS) systems have also been released, such as [Knative](https://knative.dev/docs/).

## Any more?

Have I missed something? ...

---

This post started life in early-2022 as a hastily made internal presentation at Canva. See the Canva preso below:

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
