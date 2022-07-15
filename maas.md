
# *NOTE* Hard drives will all be wiped. Make sure big storage pools are removed either from maas or physically (or both)



# Commissioning and Testing

Because we're using bonds there's a bit of a process. LACP bonded ports (at least for our cisco catalyst switch) don't fall back to non-lacp bonded ports so PXE booting will not work.

I think the _real_ way to get this working, would be to have a single interface for pxe booting, but we don't have enough ports on producers for that to be worth it.

### Process to get PXE boot:

1. Disabled Port bonding on switch
```
# Example for producers
interface GigabitEthernet3/0/35
 no channel-group
interface GigabitEthernet3/0/36
 no channel-group

```


2. Start comissioning on Maas
** NOTE ** For the supermicro board, you will need to get into the kvm. For some reason the redfish endpoints don't support triggering the pxe boot, but the dell one does.

3. Wait for commission to finish

4. When rebooting into system, re-enable bonding on switch
```
# Example for producers
interface GigabitEthernet3/0/35
 channel-group 3 mode active
interface GigabitEthernet3/0/36
 channel-group 3 mode active

```
5. ????

6. Profit
