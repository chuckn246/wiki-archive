# mkpasswd

------------------------------------------------------------------------

## Description

Useful for generating passwords for `/etc/shadow` and for use in
[Ansible
playbooks](https://docs.ansible.com/ansible/latest/reference_appendices/faq.html#how-do-i-generate-encrypted-passwords-for-the-user-module).

------------------------------------------------------------------------

## Install

- Install `mkpasswd` which is included in the `whois` package:
  ``` bash
  sudo apt install whois
  ```

------------------------------------------------------------------------

## Use

- Encrypt a string as a SHA-512 password:
  ``` bash
  mkpasswd --method=sha-512
  ```
- Encrypt a string as a yescrypt password:
  ``` bash
  mkpasswd --method=yescrypt
  ```

------------------------------------------------------------------------

## Links

- <https://packages.debian.org/bullseye/whois>
- <https://manpages.debian.org/bullseye/whois/mkpasswd.1.en.html>
- <https://www.debian.org/releases/bullseye/amd64/release-notes/ch-information.en.html#pam-default-password>
