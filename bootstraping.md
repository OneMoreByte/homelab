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

