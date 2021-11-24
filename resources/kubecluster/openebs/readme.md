https://docs.openebs.io/docs/next/installation.html

kubectl patch storageclass openebs-jiva-default -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'

