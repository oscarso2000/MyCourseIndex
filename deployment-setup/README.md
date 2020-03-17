# Deployment of a secure by default Kubernetes cluster with a basic CI/CD pipeline on AWS

## Overview

## TOC
1. [Overview](#overview)
    1. [Kubernetes](#kubernetes)
    1. [Before you start](#before-you-start)
1. [Creating the Cluster](#creating-the-cluster)
1. [CI/CD](#ci/cd)

### Kubernetes

### Before you start

To build our cluster, we need to following tools installed:

* **kubectl**\
    _kubectl_ (Kubernetes Control) is a command line tool for interacting with a Kubernetes cluster.

* **kops**\
    The [Kubernetes Operations (kops) project](https://github.com/kubernetes/kops) provides tooling for building and operating Kubernetes clusters in the cloud. We’ll be using kops to create and manage our cluster.

* **Terraform**\
    [Terraform](https://www.terraform.io/intro/index.html) is an Infrastructure as Code (IAC) tool which allows users to define infrastructure in a high-level configuration language which can then be used to build infrastructure in a service provider such as AWS or Google Cloud Platform. We’ll be using Terraform to create our prerequisites for kops and to modify the IAM policies created by kops.

* **aws cli**\
    [AWS CLI](https://aws.amazon.com/cli/) is a command line tool for interacting with AWS. This is required by kops & Terraform to perform operations on AWS.

## Creating the cluster

**Step 1: Setup a FQDN that will be used for the cluster in Route53**

The Kubernetes cluster that we will setup will use a FQDN hosted in Route53 to expose service endpoints. We will register a new domain name `courseindex.net`.

**Step 2: Prepare kops prereqs**

For kops to build the cluster, it needs an S3 bucket to hold the cluster configuration and an IAM user account that has the following policies attached to it:

```
AmazonEC2FullAccess
AmazonRoute53FullAccess
AmazonS3FullAccess
IAMFullAccess
AmazonVPCFullAccess
```

Our file `prereqs/kops_prereqs.tf` will do all of this for us. It will also create an S3 bucket that will actually hold our state in a remote location. This will allow all of us to work with one set of Infrastructure as Code without causing conflicts. We then run the following

```bash
$ cd prereqs
$ terraform init
$ terraform plan
$ terraform apply
```

We now see 2 new S3 buckets (terraform-state and kops-config) as well as a new IAM user.

**Step 3: Use kops to deploy**
We go to our terraform.tfstate from the S3 bucket + find the `iam id` and `secret key`. We then run the following to create a kops profile to run aws commands

```bash
$ aws configure --profile kops
AWS Access Key ID [None]: {iam id}
AWS Secret Access Key [None]: {aws secret key}
Default region name [None]: us-east-1
Default output format [None]: text
```

We need some environment variables so kops can know where to access everything. We need to either run these every time or place in our `.bashrc`/`.bash_profile` setting these to be the default.

```
export AWS_PROFILE=kops
export KOPS_STATE_STORE=s3://kops-config
```

Now the big boi

```bash
$ kops create cluster --cloud aws \
 --bastion \
 --node-count 1 \
 --node-size t2.medium \
 --master-size t2.medium \
 --zones us-east-1a \
 --master-zones us-east-1a \
 --dns-zone k8s.mycourseindex.vpc \
 --vpc vpc-3adeed40 \
 --dns private \
 --topology private \
 --networking calico \
 --authorization RBAC \
 --name cs4300.k8s.mycourseindex.vpc \
 --out=k8s \
 --target=terraform --yes
```

We get an output like:

```
I0316 16:26:02.445740   15492 subnets.go:184] Assigned CIDR 172.31.32.0/19 to subnet us-east-1a
I0316 16:26:02.445813   15492 subnets.go:198] Assigned CIDR 172.31.0.0/22 to subnet utility-us-east-1a
```

This command tells kops that we want to build a cluster that:
* Will use AWS

* Has a master node of size t2.medium in each of the specified availability zones

* Has 1 worker nodes of size t2.medium. kops will spread the worker nodes evenly across each of the availability zones

* Uses a private network topology, meaning that the all the nodes have private IP addresses and are not directly accessible from the public Internet

* Uses Calico as a Container Network Interface replacing kubenet as a result of the requirements of the private network topology

* Uses RBAC for Kubernetes access permissions

* Is described in a Terraform configuration file to be written to the directory specified by --out

kops generates a set of Terraform configuration files in a newly created k8s directory that can be applied to create the cluster. Before we build our cluster, we want to add a configuration file to tell Terraform to keep its state store on the S3 bucket that we just created.

```bash
$ cd k8s
$ terraform init
$ terraform plan
$ terraform apply
```

This takes some time (like 20 min so take a Brooklyn 99 break rn).

We check the status with

```bash
$ kops validate cluster
```

When the cluster is finished, we should see

```bash
```

## CI/CD
We will use travis ci for our CI/CD. Sign in to travis ci and turn on TravisCI for our repo. Ensure that for this repo both of the following are on:

* build pushed branches
* build pushed pull requests

**Step 1: Triggers**

We have a `.travis.yml` file that tells Travis CI what to do.

```yaml
branches:
  only:
    - master
sudo: required
before_install:
- chmod +x ./build-scripts/install-dependencies.sh
- chmod +x ./build-scripts/deploy-terraform.sh
- chmod +x ./build-scripts/inject-secrets.sh
install:
- "./build-scripts/install-dependencies.sh"
- "./build-scripts/inject-secrets.sh"
script:
- "./build-scripts/deploy-terraform.sh"
```

This specifies only on the master branch will we run, we need sudo access, what we run before anything else, what we do to install everything, and lastly what we run to deploy.

**Step 2: Secrets**\
We don’t want to keep our AWS secrets in a public repository in clear text; this would be extremely bad information security practice. Travis has a CLI tool that lets us inject secrets at build time.

```
$ sudo gem install travis
$ travis login --org
```

We have two scripts in build_scripts: `kube-secrets.txt` (all found in `~/.kube/config`) and `setup-secrets.sh` (in `~/.kube/config` and `~/.aws/credentials`).

We then run the following:

```bash
$ chmod 755 build-scripts/setup-secrets.sh
$ ./build-scripts/setup-secrets.sh
```

We need to _*Make a note of the openssl command the `setup-secrets.sh` script returns for later, as we will need this to decrypt the secrets.*_

This script will encrypt our secrets using Travis and update our .travis.yml file.

**Step 3: Install Dependencies**\
We have an `install_dependencies.sh` which install all our tools.

**Step 4: Inject Secrets**\
We also have a script `inject_secrets.sh`. This script will pull our secrets from the Travis environment, decrypt them, and inject them into the pertinent config files.

**Step 5: Environment**\
We now have to set up the external-dns and the kube2iam role.

We need to update external_dns/pod-role-trust-policy.json and replace {your-node-iam-role-arn} with the IAM ARN for Kubernetes nodes in our cluster. This can be found by running the following command:

```bash
$ aws iam list-roles | grep node
```

We also need to update external-dns.yaml where it says {our-external-dns-iam-role-arn} with the IAM ARN for the role that was created when the Terraform configuration was applied. This can be found by running the following command:

```bash
$ aws iam get-role --role-name external_dns_pod_role
```

We also have a `deploy-k8s.sh` which performs the deployment of our service accounts and our applications.

**Step 6: Final Release**\
Have our final docker build + release
