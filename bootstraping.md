# Bootstraping the homelab

I wouldn't copy this if the reader is not myself reviewing how I did things. I don't think I'm doing this right.


## Setup Router and Switch


## ZFS pool creation
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

## Run non-Kubernetes installing ansible

ansible-galaxy install githubixx.ansible_role_wireguard




## Install Kubernetes with kubespray

kubectl create ns argocd
kubectl create -k ./argocd