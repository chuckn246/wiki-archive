# Speedy KVM Creation

I created a special [Debian 10 preseed](../../linux/distribution/debian/preseed/debian-10-preseed.md) iso just
for my Proxmox kvm machines. I can go from zero to ready to rock in
under 10 minutes!

------------------------------------------------------------------------

## Create the preseeded iso

The preseeded iso starts automatically, installs a few key packages,
sets vim as my default editor and copies my ssh public key to my
authorized_keys file so I can run the Ansible playbook right after
install.

- I created the preseed file then added it to the ISO using my [Zero Interaction](../../linux/distribution/debian/preseed/debian-10-preseed.md#zero-interaction)
  method.
- <https://gitlab.com/preseed/preseed-kvm/-/blob/da3402a1f9331fd23816703f62057091b7a36045/preseed.cfg>

------------------------------------------------------------------------

## Create the Ansible Playbook

I created a small playbook to configure the system for me so it's set up
the way I like.

- <https://gitlab.com/ansible9/ansible-kvm/-/blob/master/basic_kvm.yml>
- Run it like so:
      ansible-playbook -v -b --ask-become-pass -i xxx.xxx.xxx.xxx, basic_kvm.yml

------------------------------------------------------------------------

## Configure pfSense

If it's a VM that I plan on keeping around for a while, I'll give it a
static IP address in pfSense before installing Debian. The preseed will
use the hostname I assigned it in pfSense as the system hostname when
configuring the network via DHCP.

Otherwise, the system's hostname will be set as *hostname* and it will
be assigned an ip address outside of the 'reserved' addresses for the
vlan I added it to.

------------------------------------------------------------------------

## Create a VM

### GUI

- Open the Proxmox web interface
- Upload the newly created preseed-iso to your Proxmox storage
- Create a VM with whatever settings you want, using the preseed-iso for
  the CD/DVD disk image.
- Start the virtual machine.
- Wait for it to complete. It took roughly 7 minutes for mine.
- Run the ansible playbook.
- Enjoy!

------------------------------------------------------------------------

### CLI

- ssh into Proxmox:
      ssh user@proxmox
- The iso's on my system are located at
  ''/media/sas/data/template/iso''. Use your favorite file transfer
  method to get the iso file there (or the iso storage location on your
  system).
- List current VMs:
      sudo qm list
- Pick a free vmid and create a new VM with your preferred settings:
      sudo qm create 150 --cdrom sas-storage:iso/preseed-debian-10.4.iso \
        --name preseed --numa 0 --ostype l26 \
        --cpu cputype=host --cores 2 --sockets 2 \
        --memory 4096  \
        --net0 bridge=vmbr90,virtio \
        --bootdisk scsi0 --scsihw virtio-scsi-pci --scsi0 file=ssd-lvm:32 \
        --serial0 socket --vga qxl --audio0 device=ich9-intel-hda,driver=spice

      # I'll add macaddr=XX:XX:XX:XX:XX:XX to the --net0 section if I want to pre-configure the ip in pfSense beforehand.
- Start the vm:
      sudo qm start <vmid>
- Wait for it to complete.
- Run the ansible playbook.
- Enjoy!
- See `man qm` for more info

------------------------------------------------------------------------
