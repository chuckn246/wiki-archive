# Debian 10 Preseed

Not much has changed since the Debian 9 preseed that I can tell.

This is a basic implementation of what is possible with preseeding.

------------------------------------------------------------------------

## Gathering Information

Investigating to see what can be preseeded was quite the learning
experience! You quickly find out that there isn't much recent info
readily available to figure these things out.

- Start with the [example preseed](https://www.debian.org/releases/buster/example-preseed.txt)
- You can run the following commands on an existing install for additional preseedable questions to browse:
```bash
sudo debconf-get-selections --installer > filename
debconf-get-selections >> filename
```

- A couple other files we can parse are located here on an existing install:
```
/var/log/installer/cdebconf/templates.dat
/var/log/installer/cdebconf/questions.dat
```

------------------------------------------------------------------------

### Filter Script

I created this script to help me sort through the dat files (and to test my **awk** and **sed** skills).

You can find it in my [gitlab repo](https://gitlab.com/preseed/preseed-scripts) as well.

- Create a directory:
```bash
mkdir ~/preseed && cd ~/preseed
```

- Download the script:
```bash
wget https://gitlab.com/preseed/preseed-scripts/raw/master/filterdat
```

- Make the script executable:
```bash
chmod +x filterdat
```

- Copy the files to the new directory:
```bash
sudo cp /var/log/installer/cdebconf/*.dat ~/preseed
```

- Change owner:
```bash
sudo chown $USER ~/preseed/*.dat
```

- Run the script:
```bash
./filterdat templates.dat
./filterdat questions.dat
```

- Read the output:
```bash
less ~/preseed/templates.dat.filtered
less ~/preseed/questions.dat.filtered
```

- Here's the code:
```bash
#!/usr/bin/env bash

outfile="$1.filtered"

# Only print the lines we want
filter_dat() {
  awk 'BEGIN { RS = "" ; FS = "\n" }
    {
      if ( $2 !~ /(text|error|note|title)/)
      {
        print $1
        print $2
        print $3
        if ($4 !~ /UTF-8/) print $4
        if ($5 !~ /UTF-8/) print $5
        if ($6 !~ /UTF-8/) print $6
        if ($7 !~ /UTF-8/) print $7
      }
    }' $1
}

# Run filter_dat then pipe output to sed to strip all empty
# lines, then add one newline above Name and save it to a file
filter_dat $1 | sed '/^$/d; s/Name/\n&/g' > "$outfile"

printf '%s%s\n' 'Processing complete! The filtered file is: ' "$outfile"
```

------------------------------------------------------------------------

## Passwords

- Set a cleartext password.
```
d-i passwd/user-password insecure
d-i passwd/user-password-again insecure
```

- You can expire the cleartext password at first login.
```
# Expire it at the bottom of the file
d-i preseed/late_command string in-target passwd --expire chuck
```

- Set the password encrypted within the preseed file itself.
```
# Generate the password
mkpasswd -m sha-512 -S $(pwgen -ns 16 1) mypassword

# Set the password
d-i passwd/user-password-crypted password $6$UyIcAz99JRIjOF9d$R/x4Z6JgS0ICE5U/VhIyqKMMK29aPhlBfj1MXuFuww9i9ry9fLVy/LzfO4QPExAWAYZX97euihMU8yHtmF4wI0
```

------------------------------------------------------------------------

## Partitioning

Preseed partitioning is still a thorn in my side. Every time I think I
have it figured out, it slaps me around for a few hours and puts me back
in my place. I'll put all the links and info I've gathered below.

Please note that some of these links have moved on me from time to time
and they were just a few clicks away from where I had originally
bookmarked them.

- [Debian Installer Guide - Preseeding](https://www.debian.org/releases/stable/i386/apb.en.html)
- [Partman-auto-recipe](https://salsa.debian.org/installer-team/debian-installer/-/blob/master/doc/devel/partman-auto-recipe.txt)


You can also browse the default recipes located inside the installer.

- Start a Debian install
- Let it proceed for a little bit
- Go to the shell with `<F2>` `<F3>`
- Or Exit to the Menu: Press `<ESC>`
  - Select: Execute a Shell
- `ls /lib/partman/recipes-amd64-efi`
  * 30atomic
  * 50home
  * 80multi
- `ls /lib/partman/recipes`
  * 30atomic
  * 50home
  * 80multi
- You can use the `more` command to read the contents.


{: .tip }
> Try performing the install over ssh which will allow
> you to select and copy the text to a file to your local machine


------------------------------------------------------------------------

## Installing Additional Applications

Here's a couple ways to install some additional programs.

- In the *###Package Selection* section:
      d-i pkgsel/include string firmware-amd-graphics \
        firmware-linux-nonfree firmware-misc-nonfree git intel-microcode libgl1-mesa-dri \
        linux-headers-amd64 mesa-utils openssh-server pulseaudio vim xorg
- At the end:
      d-i preseed/late_command string \
        in-target apt-get install firmware-amd-graphics \
        firmware-linux-nonfree firmware-misc-nonfree git intel-microcode libgl1-mesa-dri \
        linux-headers-amd64 mesa-utils openssh-server pulseaudio vim xorg

I'm sure there are other ways, but those two are what has worked for me
so far.

------------------------------------------------------------------------

### Running Commands

You can also run commands on the target system. Here's some examples:

    d-i preseed/late_command string \
      mkdir -p -m 700 /target/home/chuck/.ssh; \
      echo "ssh-ed25519 YOURxwxPUBLICxxxSSHxyxKEYxzx" > /target/home/chuck/.ssh/authorized_keys; \
      in-target chown --recursive chuck:chuck /home/chuck/.ssh; \
      in-target chmod 0644 /home/chuck/.ssh/authorized_keys; \
      in-target update-alternatives --set editor /usr/bin/vim.basic; \
      in-target passwd --expire chuck

#### Notes

- The new filesystem is available at `/target` so you can
  copy/create/modify the files there:
      d-i preseed/late_command string mkdir -p -m 700 /target/home/chuck/.ssh
- You can chroot into the system:
      d-i preseed/late_command string chroot /target <commands>
- You can chain commands together using a semicolon `;`
  - Make sure the last command does **not** have a semicolon.
- If your commands fail, you can check why by viewing the log screen
  with F4.

------------------------------------------------------------------------

## Using the Preseed file

There's a few ways to use the preseed file.

- [Add it to the ISO](#add-it-to-the-iso)
- [Host it locally](#host-it-locally)
- Pull it from the internet
- Probably something else..

I'll cover the first 2 for now.

------------------------------------------------------------------------

### Add it to the ISO

<https://wiki.debian.org/DebianInstaller/Preseed/EditIso>

I used the following packages to complete these steps:

- `xorriso`
- `isolinux`
- `zip`
- `unzip`

#### Steps

- Download a Debian iso
- Rename it to debian.iso
- Make a directory to hold the extracted iso:
      mkdir isofiles
- Extract ISO to the isofiles directory:
      xorriso -osirrox on -indev debian.iso -extract / isofiles
- Add write permissions to initrd:
      chmod +w -R isofiles/install.amd
- Unzip initrd:
      gunzip isofiles/install.amd/initrd.gz
- Add preseed to the initrd:
      echo preseed.cfg | cpio -H newc -o -A -F isofiles/install.amd/initrd
- Re-zip initrd:
      gzip isofiles/install.amd/initrd
- Remove write abilities of initrd:
      chmod -w -R isofiles/install.amd
- Enter isofiles directory:
      cd isofiles
- If you want to have a "zero interaction" install, do the [zero
  interaction](#zero-interaction) steps first.
- Generate new md5sum.txt:
      chmod 666 md5sum.txt
      find -follow -type f -exec md5sum {} \; > md5sum.txt
      chmod 444 md5sum.txt
- Move back a directory:
      cd ..
- Generate new iso:
      xorriso -as mkisofs \
      -isohybrid-mbr /usr/lib/ISOLINUX/isohdpfx.bin \
      -c isolinux/boot.cat \
      -b isolinux/isolinux.bin \
      -no-emul-boot \
      -boot-load-size 4 \
      -boot-info-table \
      -eltorito-alt-boot \
      -e boot/grub/efi.img \
      -no-emul-boot \
      -isohybrid-gpt-basdat \
      -o preseed-debian.iso \
      isofiles/

\


{: .note }
> #### Script it!
>
> After doing that a couple of times when making changes, it got a little
> old. I figured why not create a bash script to handle most of it for me?
> You can check it out at my [git
> repo](https://gitlab.com/preseed/preseed-scripts/-/blob/master/preseed2iso).


#### Install using the ISO

Take the generated iso (preseed-debian.iso if you're using the commands
from above) and write it to a USB jump drive or upload it to Proxmox.

Boot the computer/VM from it and at the menu, select **Advanced Options
\> Automated Install**.

Wait a few seconds and it should start the installation process!

If you don't feel like navigating the menu and selecting the Automated
Install, follow the [zero interaction](#zero-interaction) steps!

------------------------------------------------------------------------

### Host it Locally

- Move into the directory with your preseed file on the host pc:
  - `cd ~/preseed/`
- Start a simple http server:
  - `python3 -m http.server`
- Start an installation on the target pc
- Two options:
  - Select **Advanced Options \> Automated Install**
    - Set the ip and location of the file when prompted. Eg:
    - `http://xxx.xxx.xxx.xx:8000/preseed.cfg`
  - Press \<key\>esc\</key\>
    - at the boot prompt:
    - `auto url=xxx.xxx.xxx.xx:8000/preseed.cfg`


{: .note }
> Make sure your firewall ports are open to allow
> access to port 8000 (or whatever port you have the http.server set to).
> You should see the GET request on the computer hosting the file if it
> all worked out.


------------------------------------------------------------------------

### Zero Interaction

You can configure the iso file so all you have to do is boot the machine
with the iso inserted.

It will automatically select the Automated Install option from the menu
and proceed with the install.

#### Steps


{: .note }
> This should be done before generating the md5sums
> in the [above steps](#add-it-to-the-iso) of adding the preseed to the
> iso.


- Change permissions to allow writing of these files:
      chmod +w isofiles/isolinux/{gtk.cfg, isolinux.cfg}
- Edit: `vim isofiles/isolinux/gtk.cfg`
      default auto
      label auto
          menu label ^Automated install
              menu default
          kernel /install.amd/vmlinuz
          append auto=true priority=critical vga=788 initrd=/install.amd/initrd.gz --- quiet
- Edit: `vim isofiles/isolinux/isolinux.cfg`
      # D-I config version 2.0
      # search path for the c32 support libraries (libcom32, libutil etc.)
      path
      include menu.cfg
      default vesamenu.c32
      prompt 0
      timeout 1
      autoselect auto
- Reset permissions:
  - `chmod -w isofiles/isolinux/{gtk.cfg, isolinux.cfg}`
- Continue with the [above steps](#add-it-to-the-iso) continuing from
  generating the md5sums.

------------------------------------------------------------------------

## Links

#### Debian Links

- <https://wiki.debian.org/DebianInstaller/Preseed>
- <https://www.debian.org/releases/stable/i386/apb.en.html>
- <https://wiki.debian.org/DebianInstaller/Preseed/EditIso>
- <https://preseed.debian.net/debian-preseed/>
- <https://hands.com/d-i/>
- <https://salsa.debian.org/installer-team/debian-installer/blob/master/doc/devel/partman-auto-recipe.txt>

------------------------------------------------------------------------

#### Other Links

- <http://ptomusk.blogspot.com/2012/09/ubuntu-preseedcfg-with-encrypted-lvm.html>
- <https://www.linuxjournal.com/content/preseeding-full-disk-encryption>
- <https://secopsmonkey.com/custom-partioning-using-preseed.html>
- <https://www.pitt-pladdy.com/blog/_20150712-141725_0100_Home_Lab_Project_Debian_Ubuntu_Preseed/>
- <https://superuser.com/questions/868596/trying-to-create-two-lvm-groups-using-preseed>
