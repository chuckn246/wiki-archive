# Create LXC Templates

Every time inspiration struck or I saw a blog post with something I
wanted to try, it was frustrating and time consuming to get the base
operating system set up to the way I like it before proceeding with the
project.

Now I just update the template each point release or when I add
something substantial to my dotfiles so it's ready to go whenever I need
to spin up a fresh container.

It only takes a few minutes to set up or modify and can save lots of
time in the long run.

------------------------------------------------------------------------

## Select an Image

- SSH into Proxmox:
  ``` bash
  ssh proxmox
  ```
- List available system images (change sas-storage to wherever they are
  stored on your system eg. local):
  ``` bash
  sudo pveam list sas-storage
  ```

  - If what we want isn't there, update container template database:
    ``` bash
    sudo pveam update
    ```
  - List available images:
    ``` bash
    sudo pveam available
    ```
  - You can also filter the output:
    ``` bash
    sudo pveam available --section system
    ```
- Download the image:
  ``` bash
  sudo pveam download sas-storage debian-10.0-standard_10.0-1_amd64.tar.gz
  ```
- See `man pveam` for more details.

------------------------------------------------------------------------

## Create the Container

Now we need to create the container that we will be updating and adding
our programs to. Note that you will need to modify the following command
to match your system.

- Create a container:
  ``` bash
  sudo pct create 250 sas-storage:vztmpl/debian-10.0-standard_10.0-1_amd64.tar.gz \
    --storage sas-lvm --rootfs volume=sas-lvm:16 \
    --ostype debian --arch amd64 --password insecure --unprivileged 1 \
    --cores 1 --memory 1024 --swap 1024 \
    --hostname lxc-template --searchdomain local.lan --nameserver xxx.xxx.xxx.x \
    --net0 name=eth0,bridge=vmbrxx,ip=dhcp,gw=xxx.xxx.xx.x,type=veth \
    --start true
  ```
- See `man pct` for more information.

------------------------------------------------------------------------

## Modify the Container

Here's where we update/add programs/configure it to our liking.

- Enter the container:
  ``` bash
  sudo pct enter 250
  ```
- Do stuff:
  - Update the system:
    ``` bash
    apt update && apt upgrade
    ```
  - Install some packages:
    ``` bash
    apt install curl git screen stow unattended-upgrades vim
    ```
  - Set Vim as default editor:
    ``` bash
    update-alternatives --set editor /usr/bin/vim.basic
    ```
  - Create user:
    ``` bash
    adduser user
    ```
  - Switch to user:
    ``` bash
    su - user
    ```
  - Clone dotfiles:
    ``` bash
    git clone https://path.to/dotfiles ~/.dotfiles
    ```
  - Stow the dotfiles:
    ``` bash
    stow dotfiles
    ```
  - Create `~/.ssh` directory:
    ``` bash
    mkdir ~/.ssh
    ```
  - Create `~/.ssh/authorized_keys` file with your pubkey
  - And so on....
  - Bonus points if you have an Ansible playbook to run the commands!

------------------------------------------------------------------------

## Create the template

In order to turn the container into a template, we need to delete the
network interface then create a backup.

- From proxmox (not inside the container):
- Remove the network interface:
  ``` bash
  sudo pct set 250 --delete net0
  ```
- Create a backup:
  ``` bash
  vzdump 250 --mode stop --compress gzip --dumpdir /media/sas/data/template/cache/
  ```
- The new file will be located in:
  ``` bash
  /media/sas/data/template/cache
  ```
- You can leave it as is or rename it to something:
  - Change directories:
    ``` bash
    cd /media/sas/data/template/cache
    ```
  - Rename it:
    ``` bash
    sudo mv new_vz_dump.tar.gz custom_debian_10.4.tar.gz
    ```
- See `man vzdump` for info.

------------------------------------------------------------------------

## Cleaning up

Feel free to delete the container we used to make the template (250).

------------------------------------------------------------------------

## Modifying or Updating

It's really easy to modify the container when a new version of the OS is
released or you want to add something to your templates.

- Create a container with your custom file:
  ``` bash
  sudo pct create 250 sas-storage:vztmpl/custom_debian_10.4.tar.gz \
    --storage sas-lvm --rootfs volume=sas-lvm:16 \
    --ostype debian --arch amd64 --password insecure --unprivileged 1 \
    --cores 1 --memory 1024 --swap 1024 \
    --hostname lxc-template --searchdomain local.lan --nameserver xxx.xxx.xxx.x \
    --net0 name=eth0,bridge=vmbrxx,ip=dhcp,gw=xxx.xxx.xxx.x,type=veth \
    --start true
  ```
- Enter the container:
  ``` bash
  sudo pct enter 250
  ```
- Do stuff:
  - Update the system:
    ``` bash
    apt update && apt upgrade
    ```
  - Install some packages
  - Add new dotfiles
  - And so on..
- Exit back to Proxmox:
  ``` bash
  exit
  ```
- Remove the network device:
  ``` bash
  sudo pct set 250 --delete net0
  ```
- Create the backup:
  ``` bash
  vzdump 250 --mode stop --compress gzip --dumpdir /media/sas/data/template/cache/
  ```
- You can leave it as is or rename it to something:
  - Change directories:
    ``` bash
    cd /media/sas/data/template/cache
    ```
  - Rename it:
    ``` bash
    sudo mv new_vz_dump.tar.gz custom_debian_10.5.tar.gz
    ```

------------------------------------------------------------------------

## Conclusion

Now every time you want to create a lxc container to use, it will be
ready to go with things set just the way you like!

------------------------------------------------------------------------

## Links

- <https://pve.proxmox.com/wiki/Linux_Container>
- <https://pve.proxmox.com/pve-docs/pct.1.html>
- <https://pve.proxmox.com/pve-docs/pct-plain.html>
- <https://pve.proxmox.com/pve-docs/vzdump.1.html>
