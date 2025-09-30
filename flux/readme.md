# Kubernetes Services

This directory has everything installed in my clusters. It should bootstrap itself

The directory structure is as follows:
+ For namespaces with multiple applications -> `<cluster name>/<namespace>/<application>`
+ For namespaces that only have one application -> `<cluster name>/<application>`

## Bootstrapping

Use kustomize to install argocd