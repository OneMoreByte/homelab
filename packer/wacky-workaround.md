Hi future me. Getting rocky to work with curitan and maas was a pain. Upstream has rocky support but it hasn't be put into a release yet, this is what I had to do to make it work

Navigate to epthermial image it was offering to my r630 machine (I got this from the failed install logs): 
```
/var/snap/maas/common/maas/boot-resources/current/ubuntu/amd64/ga-22.04/jammy/stable
```

There is the files it uses for PXE boot
+ squashfs
+ boot-initrd
+ boot-kernel

In the squashfs file is the filesystem for the epthermial image. There I added a PPA for a repo with the rocky support patch.
Curtin wasn't installed yet, so it's installed with cloudinit

First I needed to unsquash it:
```
mkdir temp-squash
cd temp-squash
unsquash ../squashfs
```

Then I chrooted and installed the PPA:
```
chroot ./squashfs-root
add-apt-repository ppa:dbungert/curtin-lp-195567
exit
```

Then I needed to re-squash the fs:
```
mksquashfs squashfs-root/ squashfs -noappend -always-use-fragments
```

Then I replaced the squashfs:
```
mv ../squashfs ../squashfs.old
mv squashfs ../
```

This didn't do anything! It overwrites the image each boot it seems.

So I tried this:
https://discourse.maas.io/t/support-for-rockylinux/4760/25

I had to modify it. But it seems to have worked!

Instead of following those directions exactly, I used the current head of the master branch instead of the release, and the snap package number was also different so I used the one I had on my machine.
