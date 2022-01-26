---
layout:     post
title:      Using Terraform to make my many side-projects 'pick up and play'
date:       2021-06-14
summary:    A post contending that Terraform is a no-brainer addition to your side-project development toolkit. 
categories: devops side-projects software-engineering
---

![](/images/posts/using_tf_in_side_projects/new-side-project-distracted-bf-meme.jpg)

[Terraform](https://www.terraform.io/) is an infrastructure-as-code technology providing a way to describe cloud infrastructure like AWS S3 buckets and SQS queues as code objects and manage the full lifecycle of that AWS infrastructure programmatically. It has very recently reached the 1.0 version milestone. Like `git`, learning Terraform is not easy and using Terraform is not fun, but it's so obviously better than alternatives that it has become a 'no-brainer' choice in my software engineering toolkit. I had to learn Terraform for work and use it extensively there, but I also now also put in the effort to use it from day one in any side project that runs in the cloud. 

[thundergolfer/example-bazel-monorepo](https://github.com/thundergolfer/example-bazel-monorepo/tree/master/infrastructure) is a public repository where I have an `infrastructure/` top-level folder with all the project's Terraform, and there's at least a few private repositories where I'm doing the same. Although some might have the reaction that the effort involved in writing and maintaining Terraform for multiple side-projects is overkill, Terraform's value proposition is really well suited to my side-project needs.

The two most important benefits of Terraform for side-projects are the declarative specification of resources and their interrelations, and the fast spin-up-then-teardown workflow. I develop side-projects in spurts and often get busy with the rest of my life, leaving a side project alone for months. If I set up a project's AWS resources in the web UI, known as the *'click ops'* approach, and then ditched the project for a while I would definitely be lost upon return. I'd have to click around AWS's pretty unpleasant web UI searching for security groups and S3 bucket policies, and importantly I'd have to figure out which resources were missing because they were too expensive to leave around doing nothing. Nearly all modern developers have the experience of accidentally leaving on an expensive EC2 instance to sit idle. Without Terraform, I find this situation is much more likely to happen. *With* Terraform, I can quickly set up a script that can delete and recreate the project's entire cloud infrastructure setup in around 10 minutes, with essentially no effort. Such a script is used like this:

```bash
# Destroy all expensive AWS resources.
# Takes ~10 minutes because some resource, such as EKS clusters, are slow to delete.
./scripts/cloud.sh down
# Recreate the project's infrastructure
# Takes ~10 minutes because some resources, such as EKS clusters or ALBs, are slow to create.
./scripts/cloud.sh up
```

On a weekend I may use this kind of script across multiple side-projects, spinning up and spinning down expensive resources such as EKS clusters, Application Load Balancers, Apache Spark clusters, and GPU-enabled VMs. 

This saves money, but even better saves a hell of a lot of time and toil that would be involved if I didn't have Terraform setup and instead had to 'click ops' my way through infrastructure maintenance.

To give a proper test of my claim that the up-front investment in doing Terraform pays off, I jumped back into a private repo that I hadn't touched *for over six months,* and went about spinning up its Kubernetes cluster and submitting one of the repo's applications to the cluster for execution. It doesn't have a script with `cloud.sh down` or `cloud.sh up` available, but using the README instructions I'd written down way back then and plain `terragrunt`, I was able to spin up the cluster and run an application in just over 20 minutes, and 13 minutes of that was just waiting for AWS to create the resources. 🏎

Here's a run down of that ~22 minutes, from 4:21PM to 4:43PM. For some context, this side-project is concerned with getting hands-on with the various batch-pipeline or workflow systems used in data engineering (think Spotify's Luigi, Lyft's Flyte, Apache Airflow, Kedro, etc). 

### Begin ⏱  ~ **4:21PM**

```bash
# 4:21PM - Begin
$ cd infrastructure/aws/k8s && terragrunt apply
...
aws_eks_cluster.demo: Still creating... [10s elapsed]
aws_eks_cluster.demo: Still creating... [20s elapsed]
...
# Go get a ☕️
aws_eks_cluster.demo: Still creating... [4m10s elapsed]
...
# Finished! ✅
$ export REGION="us-east-2" && export CLUSTER_NAME="foobar-demo-cluster" && aws eks --region "${REGION}" update-kubeconfig --name ${CLUSTER_NAME}
# 4:34 - Test cluster access
$ kubectl get nodes
NAME                                      STATUS   ROLES    AGE     VERSION
ip-10-0-0-65.us-east-2.compute.internal   Ready    <none>   4m34s   v1.18.9-eks-d1db3c
```

### 13 minutes later... ⏱  ~ **4:35PM**

I had to wait for AWS a bit, but now the cluster is active. Let's setup some basic cluster functionality:

```bash
# 4:35PM
# Apply some YAMl
kubectl apply -f dashboard/
kubectl apply -f metrics-server/
# Now let's spin up Luigi, a batch pipeline management system
$ cd (git rev-parse --show-toplevel) && cd workflows_and_pipelines/luigi
$ kubectl apply -f k8s-objects/
# Done. Now let's create a cronjob that runs a basic Luigi pipeline every 15 mins
$ cd k8s-objects/workflow_cronjobs/
$ kubectl apply -f hello_luigi.yaml
$ kubectl create job --from=cronjob/hello-luigi-wf adhoc-run
# Check that it's all been created
```

### YAML Applied ⏱ ~ **4:41PM**

Sweet, I've now run a Luigi pipeline in the fresh Kubernetes cluster. (I spent some time reading the notes in my READMEs to check I'd done everything correctly, so there's a gap in time between commands)

```bash
# 4:41PM
$ kubectl get pods
NAME                      READY   STATUS      RESTARTS   AGE
adhoc-run-kc2tp           0/1     Completed   0          7s
luigid-5689dfd84d-tl7dt   1/1     Running     0          2m4s
$ kubectl logs adhoc-run-kc2tp
DEBUG: Checking if demo.HelloWorldTask(foo=249) is complete
/tmp/Bazel.runfiles_w_tfrz7e/runfiles/pypi/pypi__luigi/luigi/worker.py:409: UserWarning: Task demo.HelloWorldTask(foo=249) without outputs has no custom complete() method
  is_complete = task.complete()
INFO: Informed scheduler that task   demo.HelloWorldTask_249_fab3ce8be8   has status   PENDING
INFO: Done scheduling tasks
INFO: Running Worker with 1 processes
DEBUG: Asking scheduler for work...
DEBUG: Pending tasks: 1
INFO: [pid 7] Worker Worker(salt=264513973, workers=1, host=adhoc-run-kc2tp, username=root, pid=7) running   demo.HelloWorldTask(foo=249)
INFO: [pid 7] Worker Worker(salt=264513973, workers=1, host=adhoc-run-kc2tp, username=root, pid=7) done      demo.HelloWorldTask(foo=249)
DEBUG: 1 running tasks, waiting for next task to finish
INFO: Informed scheduler that task   demo.HelloWorldTask_249_fab3ce8be8   has status   DONE
DEBUG: Asking scheduler for work...
DEBUG: Done
DEBUG: There are no more tasks to run at this time
INFO: Worker Worker(salt=264513973, workers=1, host=adhoc-run-kc2tp, username=root, pid=7) was stopped. Shutting down Keep-Alive thread
INFO:
===== Luigi Execution Summary =====

Scheduled 1 tasks of which:
* 1 ran successfully:
    - 1 demo.HelloWorldTask(foo=249)

This progress looks :) because there were no failed tasks or missing dependencies

===== Luigi Execution Summary =====

HelloWorldTask says: Hello world!
foo equals 249
```

### Done ⏱ ~ **4:43PM**

So to sum that up, I went from having nothing for my side-project set up in AWS to having a Kubernetes cluster with the basic metrics and dashboard, a proper IAM-linked `ServiceAccount` support for a smooth IAM experience in K8s, and [Luigi](https://github.com/spotify/luigi) deployed so that I could then run a Luigi workflow using an ad-hoc run of a `CronJob`. That's quite remarkable to me. All that took *hours* to figure out and define when I first did it, over six months ago. 

If I hadn't used Terraform, I'd have to have jumped into the shitty, confusing AWS user interface and clicked around to recreate the cluster, it's networking configuration, and it's IAM configuration. Even if I got it working there's a high chance it would have been different from my previous configuration and not worked with other code and configuration in the project. I'd estimate that in just this one spin-up-spin-down cycle I've saved almost two hours of my time.

Now that I've run that to validate my argument for Terraform, let's tie off loose ends. 

```bash
$ terragrunt destroy
...
...
Plan: 0 to add, 0 to change, 19 to destroy.

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes
# --- WAIT FOR AWS TO TEAR DOWN ---
# Done! 💯
```

### Complement your Terraform with good notes

Terraform cannot capture *everything* about your environment setup, so I aim to write down any non-trivial detail, either in comments around the Terraform or in READMEs. 

Here's some examples:

```bash
# These values are a real pain to get at the moment. Hopefully Terraform makes it easier in future.
# https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc_verify-thumbprint.html
thumbprint_list = [
  # ⚠️ This value *might* need to be updated whenever cluster is destroyed and recreated.
  # ⚠️ Any IAM Roles using the OIDC outputs do need to be updated.
  # ⚠️ See README.md in this folder.
  "9988776655aabbcc0b539foobar6bb7f3b02e22da2b1122334455aabbcc"
] 
```

and in that [README.md](http://readme.md) I have:

```bash
⚠️ **NOTE:** Setting this up is a pain, but worth it. IAM-linked ServiceAccounts are much nicer to use than having the cluster role do _everything_
              or have the cluster role-assume into other roles.

**Setup:**           

1. `aws eks describe-cluster --name workflows-and-pipelines-demo-cluster --query "cluster.identity.oidc.issuer" --output text`

2. Follow the "AWS Management Console" instructions here: https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html
```

After six months, it's very easy to get lost in your own work and want to tear your hair out. The idea is that these comments are there for me right when I hit a 'wait, what next?' moment or 'huh?' moment and need guidance.

## Convinced?

After exercising this system in one of my side-projects, I'm certainly convinced. Kubernetes is a 500lb gorilla of a system, IAM is a regular headache, and Spotify's Luigi is complex enough itself, but in about 20 minutes I was able to get it all set up to the point where I could run some basic code I wrote over half a year and a half-dozen side projects ago. I really think this is a no-brainer in terms of side-project maintenance and cost management.
