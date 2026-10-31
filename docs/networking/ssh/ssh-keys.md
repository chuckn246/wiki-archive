# SSH Key Management

This page is meant to assist in setting up and maintaining SSH keys.

------------------------------------------------------------------------

## SSH Directory Permissions

``` bash
chmod 700 ~/.ssh
chmod 644 ~/.ssh/authorized_keys
chmod 644 ~/.ssh/known_hosts
chmod 644 ~/.ssh/config
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
```

------------------------------------------------------------------------

## Generating SSH Keys

### ED25519

- Change to `~/.ssh`:
  ``` bash
  cd ~/.ssh
  ```
- Generate an **Ed25519** ssh key:
  ``` bash
  ssh-keygen -t ed25519 -a 256
  ```
- Generate an **Ed25519** ssh key with a specific name:
  ``` bash
  ssh-keygen -f <keyname> -t ed25519 -a 256
  ```

------------------------------------------------------------------------

### RSA

- Change to `~/.ssh`:
  ``` bash
  cd ~/.ssh
  ```
- Generate a **RSA** ssh key:
  ``` bash
  ssh-keygen -t rsa -b 4096 -o -a 256
  ```
- Generate a **RSA** ssh key with a specific name:
  ``` bash
  ssh-keygen -f <keyname> -t rsa -b 4096 -o -a 256
  ```

------------------------------------------------------------------------

## Verifying SSH Keys

### Verify SSH Key Password

- Change to `~/.ssh`:
  ``` bash
  cd ~/.ssh
  ```
- Verify password:
  ``` bash
  ssh-keygen -y -f id_ed25519
  ```
- Upon entering successful passphrase, it prints the pubkey:
  ``` bash
  Enter passphrase: 
  ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJAZcdEIpPbJal7CEsIpaHzBEjs/8nedIvDA/sDlvqll chuck@gaming
  ```
- Enter the wrong passphrase:
  ``` bash
  ssh-keygen -y -f id_ed25519
  Enter passphrase: 
  Load key "id_ed25519": incorrect passphrase supplied to decrypt private key
  ```

------------------------------------------------------------------------

### Verify SSH Private Key Matches Public Key

- Change to `~/.ssh`:
  ``` bash
  cd ~/.ssh
  ```
- Verify ssh key matches it's private key:
  ``` bash
  ssh-keygen -l -f id_ed25519; ssh-keygen -l -f id_ed25519.pub
  ```
- Output should match:
  ``` bash
  256 SHA256:W5o5+DV3Jaba4txzQ58gZuIZvZD44McIU7tV9I4LZpw chuck@gaming (ED25519)
  256 SHA256:W5o5+DV3Jaba4txzQ58gZuIZvZD44McIU7tV9I4LZpw chuck@gaming (ED25519)
  ```

------------------------------------------------------------------------

## Modifying SSH Keys

### Change SSH Key Password

- Change to `~/.ssh`:
  ``` bash
  cd ~/.ssh
  ```
- Change password:
  ``` bash
  ssh-keygen -p -f id_ed25519
  ```

------------------------------------------------------------------------

### Change SSH Key Comment

- Change to `~/.ssh`:
  ``` bash
  cd ~/.ssh
  ```
- Change comment (email):
  ``` bash
  ssh-keygen -c -f id_ed25519
  Enter passphrase: 
  Key now has comment 'chuck@hostname'
  Enter new comment: user@newname
  The comment in your key file has been changed.
  ```

------------------------------------------------------------------------

## SSH-Agent

- Add the key to the ssh-agent.
  ``` bash
  ssh-add keyname
  ```
- Add the key to the server using the credentials from the config file.
  ``` bash
  ssh-copy-id -i keyname servername
  ```

------------------------------------------------------------------------

## Links

- <https://manpages.debian.org/stable/openssh-client/ssh.1.en.html>
- <https://manpages.debian.org/stable/openssh-client/ssh-keygen.1.en.html>
- <https://manpages.debian.org/stable/openssh-client/ssh-add.1.en.html>
- <https://manpages.debian.org/stable/openssh-client/ssh-copy-id.1.en.html>
