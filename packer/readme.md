
# How to use:

Build this image:
```
./build.sh
```

Copy it to the maas host:
```
rsync -av --progress rocky-8.6.tar.gz root@192.168.13.13:/root
```

Get a maas api key if you don't have it:
```
maas apikey --username=admin > api-key-file
```

Log into maas api:
```
maas login admin http://192.168.13.13:5240/MAAS
```


Add new vm image:
```
maas admin boot-resources create name='rocky/8-zfs-wireguard' title='Rocky 8 ZFS Wireguard' architecture='amd64/generic' filetype='tgz' content@=rocky-8.6.tar.gz
```