https://github.com/olli-ai/glusterfs-subdir-external-provisioner

```
helm repository add olli-ai https://olli-ai.github.io/helm-charts/
helm install glusterfs-client olli-ai/glusterfs-client-provisioner \
    --namespace glusterfs \
    --set glusterfs.server='{192.168.13.233,192.168.13.133,192.168.13.13}' \
    --set glusterfs.volume=k8s-storage
kubectl patch storageclass glusterfs-client -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```
