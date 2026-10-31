# LUKS Encrypted Container

------------------------------------------------------------------------

{: .tip }
> With cryptsetup 2.1.0, the LUKS header takes up just under
> 16MiB, so the partition size must be 16MiB + the size of the data you
> want to store in it.

## Create a LUKS Storage Container

- Create a 20Mb file filled with random data: [^1]
```bash
sudo dd if=/dev/urandom of=encrypted.luks.img iflag=fullblock bs=1M count=20
```

- Switch to root:
```bash
sudo -s
```

- Set permissions:
```bash
chmod go= encrypted.luks.img
```

- Configure encryption:
```bash
cryptsetup --verbose luksFormat encrypted.luks.img
cryptsetup --verbose --use-random luksFormat encrypted.luks.img
```

- Open the encrypted container:
```bash
cryptsetup --verbose luksOpen encrypted.luks.img encrypted
```

- Create filesystem:
```bash
mkfs.ext4 /dev/mapper/encrypted
```

- Create directory to mount the container:
```bash
mkdir /mnt/encrypted
```

- Mount the container:
```bash
mount -t ext4 -o journal_checksum /dev/mapper/encrypted /mnt/encrypted
```

- Chown it:
```bash
chown chuck: /mnt/encrypted
```

- Set permissions:
```bash
chmod go= /mnt/encrypted
```

- Switch back to \$USER:
```bash
exit
```

------------------------------------------------------------------------

## Copy Files to the LUKS Storage Container

- Copy or create your files:
```bash
cp /files/to/copy /mnt/encrypted
```

------------------------------------------------------------------------

## Close the LUKS Storage Container and Lock it

- Switch to root:
```bash
sudo -s
```

- Unmount the container:
```bash
umount /mnt/encrypted
```

- Close the encrypted container:
```bash
cryptsetup luksClose encrypted
```

- Switch back to \$USER:
```bash
exit
```

------------------------------------------------------------------------

## Change Password on a LUKS Encrypted Storage Container

- If you want/need to change the password:
``` bash
sudo cryptsetup luksChangeKey encrypted.luks.img
```

------------------------------------------------------------------------

[^1]: <https://pthree.org/2012/02/20/randomize-first-the-encrypt-your-block-device/>
