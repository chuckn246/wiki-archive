# LUKS Encrypted Partition

------------------------------------------------------------------------

## Change LUKS Partition Password

- Find the drive with the luks headers:
```bash
cat /etc/crypttab
```

- Find the partition using the disk label from the previous command:
```bash
sudo fdisk -l /dev/sda
```

- If it is listed by uuid, use:
```bash
ls -l /dev/disk/by-uuid/{insert your uuid here}
```

- Verify the Keyslots used:
```bash
sudo cryptsetup luksDump /dev/sda5
```

- Test passphrase:
```bash
sudo cryptsetup --verbose open --test-passphrase /dev/sda5
```

- Change Keyslot 0's key:
```bash
sudo cryptsetup luksChangeKey /dev/sda5 -S 0
```

- Verify new passphrase:
```bash
sudo cryptsetup --verbose open --test-passphrase /dev/sda5
```

------------------------------------------------------------------------

## Unlock LUKS Partition from GRUB

- Insert luks module:
```
grub rescue> insmod luks
```

- List all divices:
```
grub rescue> ls
```

- Mount encrypted `/boot/` partition:
```
grub rescue> cryptomount (hd0,gpt2)
```

- To use uuid instead, use the `-u` option:
```
grub rescue> cryptomount -u 8f5fc81c-41bb-11ec-81d3-0242ac130003
```

- Enter passphrase:
```
Attempting to decrypt master key...
Enter passphrase for hd0,gpt2 (<disk uuid>):
```

- Output on success:
```
Slot 3 opened
```

- Insert LVM Module:
```
grub rescue> insmod lvm
```

- Load module for normal boot:
```
grub rescue> insmod normal
```

- Boot:
```
grub rescue> normal
```

------------------------------------------------------------------------

## Links

- <https://www.gnu.org/software/grub/manual/grub/html_node/Commands.html#Commands>
- <https://www.gnu.org/software/grub/manual/grub/html_node/GRUB-only-offers-a-rescue-shell.html#GRUB-only-offers-a-rescue-shell>
