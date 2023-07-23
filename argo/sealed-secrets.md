

# List of sealed secrets
> NOTE: These would need to be regenerated if the cluster got rebuilt

```yaml
argo/argocd/base/repository.yaml
argo/argocd/base/wailord-cluster.yaml   # Sealed
argo/argocd/base/standalone-clusters/*.yaml
argo/argocd/overlays/argocd-secret.yaml

argo/cert-manager/templates/aws-route53-creds.yaml

# TODO: 

# TODO: Delete plex claim. We don't need it anyway
# TODO: Mva has secrets in it's config. Move them out.

argo/observability/jaeger/base/jaeger-secret.yaml
argo/routed-svcs-gateway/gateway/templates/mulvad-creds.yaml


# TODO: jmusicbot into sealed-secret


# TODO: Grafana client id

argo/traefik/templates/tuner-auth.yaml
argo/traefik/templates/keycloak-secret.yaml
# TODO: Influxdb token
```