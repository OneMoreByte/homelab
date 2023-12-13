#!/bin/bash

mkdir -p kickstart-isos

for ks_dir in kickstarts/*; do
    ks_hostname=$(echo $ks_dir | cut -d "/" -f 2)
    mkisofs -V OEMDRV -o kickstart-isos/${ks_hostname}.iso $ks_dir/ks.cfg
done