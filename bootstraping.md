# Bootstraping the homelab

I wouldn't copy this if the reader is not myself reviewing how I did things. I don't think I'm doing this right.

## Pre-reqs
1. A linux box, or a desire to modify the packer stuff.
2. A cloud account for the off-site k8s node.
3. These tools/packages installed:
```
ssh
python 3
qemu and kvm (+ you should have a bridge set up with the name br0. Packer will want/expect that)
https://docs.ansible.com/ansible-core/devel/installation_guide/index.html
https://www.packer.io/downloads
https://www.terraform.io/downloads
https://helm.sh/docs/intro/install/
https://kubernetes.io/docs/tasks/tools/
https://argo-cd.readthedocs.io/en/stable/cli_installation/

```

## Setup Router and Switch


## Setup MaaS


## Build PXE Image for MaaS with packer


## Commission servers into MaaS



## Using Terraform to get an off-site k8s node



## Run non-Kubernetes installing ansible




## Install Kubernetes with kubespray

