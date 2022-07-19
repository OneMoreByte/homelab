# Installing with KS files

Change the kernel parameters:
```
inst.ks=hd:LABEL=OEMDRV:/ks.cfg bond=bond0:eno1,eno2:mode=802.3ad,lacp_rate=0
```
We're using lacp and slow mode because that's what our cisco switch supports


Adjust bond0:
```
nmcli c modify bond0 connection.autoconnect-retries 30
nmcli c modify bond0 ethernet.cloned-mac-address <whatever the mac is currently>
```