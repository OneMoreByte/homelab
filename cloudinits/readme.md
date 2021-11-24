# Cloud-inits

#### Note about ubuntu raspberry pi vm
I was having issues.
Needed to do some for it to work:
- Add `autoinstall ds=nocloud;s=/media/nocloud` to the end of the kernel params in `cmdline.txt` in the `system-boot` partition
- Add `LABEL=CIDATA  /media/nocloud        vfat   defaults        0 0` to `/etc/fstab` in the `writable` partition
- Create a fat32 partition at the end with the label `cidata` (this can be small. Maybe 128 Mib?)
- Copy the `user-data` and `meta-data` files in