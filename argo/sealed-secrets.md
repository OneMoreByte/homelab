# List of sealed secrets

> NOTE: These would need to be regenerated if the cluster got rebuilt

```yaml
# TODO: Factorio has some secrets that aren't secrets
argo/wailord/argocd/base/repository.yaml 
argo/wailord/argocd/base/clusters/*.yaml 
argo/wailord/argocd/base/argocd-secret.yaml 
argo/wailord/cert-manager/templates/aws-route53-creds.yaml 
argo/wailord/home-automation/frigate/templates/frigate-rstp-credentials.yaml 
argo/wailord/home-automation/infludxdb/templates/argocd-admin.yaml 
argo/wailord/keycloak/templates/admin-user-sealed.yaml 
argo/wailord/keycloak/templates/db-secret-sealed.yaml 
argo/wailord/media-svcs/mva/templates/sealed-variables.yaml
argo/wailord/observability/jaeger/base/jaeger-secret.yaml 
argo/wailord/routed-svcs-gateway/gateway/templates/mulvad-creds-sealed.yaml 
argo/wailord/svcs/jmusicbot/templates/secret-sealed.yaml 
argo/wailord/svcs/grafana/templates/sealed-client-secret.yaml 
argo/wailord/traefik/templates/tuner-auth.yaml 
argo/wailord/traefik/templates/keycloak-secret.yaml 
```
