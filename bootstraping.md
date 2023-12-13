# Bootstraping the homelab

I wouldn't copy this if the reader is not myself reviewing how I did things. I don't think I'm doing this right.

## Setup Router and Switch

## ZFS pool creation

Get the drives. You can do it like this:

```
fdisk -l
# Then use that info here
ls -la /dev/disk/by-id/
```

In the past (Aug 2022) this is what I ran to create the pools:

producers zfs hdd

```
zpool create -f store \
    -o ashift=12 \
    raidz \
    /dev/disk/by-id/wwn-0x5000c500db36e105 \
    /dev/disk/by-id/wwn-0x5000c500db36e802 \
    /dev/disk/by-id/wwn-0x5000c500db36eda6 \
    /dev/disk/by-id/wwn-0x5000c500e344c173 \
    raidz \
    /dev/disk/by-id/wwn-0x50014ee26803ce4d \
    /dev/disk/by-id/wwn-0x50014ee26803d01e \
    /dev/disk/by-id/wwn-0x50014ee2bd597ee6 \
    /dev/disk/by-id/wwn-0x50014ee2bd59a2cd
    zfs set compression=on store
    zfs set relatime=on store
```

fateful zfs ssds

```
zpool create -f store \
    -o ashift=12 \
    raidz \
    /dev/disk/by-id/wwn-0x5001b448bcd31588 \
    /dev/disk/by-id/wwn-0x5001b448bcd3b430 \
    /dev/disk/by-id/wwn-0x5002538d41cc7b8b
    zfs set compression=on store
    zfs set relatime=on store
```

create an encryption key

```
dd if=/dev/random of=/path/to/key bs=1 count=32
```

create volumes

```
zfs create -o encryption=on -o keyformat=raw -o keylocation=file:///path/to/key store/example
```

create this service for loading keys on boot in `/etc/systemd/system/zfs-load-key.service`

```
[Unit]
Description=Load all ZFS encryption keys
DefaultDependencies=no
Before=zfs-mount.service
After=zfs-import.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/sbin/zfs load-key -a

[Install]
WantedBy=zfs-mount.service
```

and enable

```
systemctl enable zfs-load-key
```

## Run non-Kubernetes installing ansible

ansible-galaxy install githubixx.ansible_role_wireguard

## Install Kubernetes with kubespray

Label storage node:

```
kubectl label node producers app=bulk-datastore
```

Bookstrap argo so it can deploy all the apps in this repo:

```
kubectl create ns argocd
kubectl create -k ./argocd
```

Set up longhorn UI

```
USER=<USERNAME_HERE>; PASSWORD=<PASSWORD_HERE>; echo "${USER}:$(openssl passwd -stdin -apr1 <<< ${PASSWORD})" >> auth
kubectl -n longhorn-system create secret generic basic-auth --from-file=auth
```

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: longhorn-ingress
  namespace: longhorn-system
  annotations:
    # type of authentication
    nginx.ingress.kubernetes.io/auth-type: basic
    # prevent the controller from redirecting (308) to HTTPS
    nginx.ingress.kubernetes.io/ssl-redirect: 'false'
    # name of the secret that contains the user/password definitions
    nginx.ingress.kubernetes.io/auth-secret: basic-auth
    # message to display with an appropriate context why the authentication is required
    nginx.ingress.kubernetes.io/auth-realm: 'Authentication Required '
    # custom max body size for file uploading like backing image uploading
    nginx.ingress.kubernetes.io/proxy-body-size: 10000m
spec:
  rules:
  - http:
      paths:
      - pathType: Prefix
        path: "/"
        backend:
          service:
            name: longhorn-frontend
            port:
              number: 80
```

# Installing standalone clusters.

Some requirements:

- Requires that main cluster is up (uses argo and sealed secrets)
- Requires kubeseal installed on machine
- Requires a roles is downloaded ``
