Install the joplin-postgres then this

```
helm repo add k8s-at-home https://k8s-at-home.com/charts/
helm install joplin-server k8s-at-home/joplin-server --namespace joplin -f ./values.yaml
