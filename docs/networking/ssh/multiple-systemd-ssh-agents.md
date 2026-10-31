# Multiple systemd SSH Agents

------------------------------------------------------------------------


{: .note-title }
> This works great on my Debian Bullseye /
> i3wm system. I don't see why this wouldn't work on other distros / DEs
> but YMMV.

## Create a ssh-agent systemd service template

To enable agent creation for **all users**, create `/etc/systemd/user/ssh-agent@.service`:

- Create directory structure:
```bash
sudo mkdir -p /etc/systemd/user/
```

- Create the service file:
```ini
cat << EOF | sudo tee /etc/systemd/user/ssh-agent@.service
[Unit]
Description=SSH authentication agent for %I Before=default.target

[Service]
Type=simple Environment=SSH_AUTH_SOCK=%t/%i-agent.socket
ExecStart=/usr/bin/ssh-agent -D -a %t/%i-agent.socket
SuccessExitStatus=2

[Install]
WantedBy=default.target

# vim: ft=dosini ts=2 sts=2 sw=2 sr et EOF
```

To enable agent creation for **only you**, create `~/.config/systemd/user/ssh-agent@.service`:
- Create directory structure:
``` bash
mkdir -p ~/.config/systemd/user/
```

- Create the service file:
```bash
cat << EOF > ~/.config/systemd/user/ssh-agent@.service
[Unit]
Description=SSH authentication agent for %I
Before=default.target

[Service]
Type=simple
Environment=SSH_AUTH_SOCK=%t/%i-agent.socket
ExecStart=/usr/bin/ssh-agent -D -a %t/%i-agent.socket
SuccessExitStatus=2

[Install]
WantedBy=default.target

# vim: ft=dosini ts=2 sts=2 sw=2 sr et
EOF
```

Enabling creation for all users **does NOT** mean that all users can
access *your* agent, it just means that they can create *their own*
agents!

------------------------------------------------------------------------

## Administration

### Manage the ssh-agent service

- Start and enable the agent as your regular user (and similar for the other agent(s)):
``` bash
systemctl --user enable --now ssh-agent@<name>.service
```

- Check status of the ssh-agent service:
``` bash
systemctl --user status ssh-agent@<name>.service
```

- Stop the ssh-agent service:
``` bash
systemctl --user stop ssh-agent@<name>.service
```

#### Naming the ssh-agent services

- Whatever name you use for each service will be included in the name of
  the agent's socket. For example, if we named one ''foo'' and another `bar`:
``` bash
systemctl --user enable --now ssh-agent@foo.service
systemctl --user enable --now ssh-agent@bar.service
```

- We would have two new socket files:
``` bash
"$XDG_RUNTIME_DIR/foo-agent.socket"
"$XDG_RUNTIME_DIR/bar-agent.socket"
```

------------------------------------------------------------------------

## Set a default ssh-agent

- Create an environment variable in your preferred startup file (eg `~/.profile`, `~/.bash_profile`, etc):
```bash
socketpath="$XDG_RUNTIME_DIR/<name>-agent.socket"
if [ -S "$socketpath" ]; then
  export SSH_AUTH_SOCK="$socketpath"
fi
```

------------------------------------------------------------------------

## Configure SSH to use the agent

- Use the **IdentityAgent** directive and add the SSH agent socket in your `~/.ssh/config`:
```
Host myhost
    ...
    AddKeysToAgent yes
    IdentityAgent  "/run/user/%i/<name>-agent.socket"
    IdentitiesOnly yes
```

- **ForwardAgent** can be configured to forward the agent in `~/.ssh/config`:
```
Host myhost
    ...
    AddKeysToAgent yes
    ForwardAgent   "/run/user/%i/<name>-agent.socket"
    IdentityAgent  "/run/user/%i/<name>-agent.socket"
    IdentitiesOnly yes
```

- Leaving those unconfigured, the hosts will use whatever `$SSH_AUTH_SOCK` is set to by default.

------------------------------------------------------------------------

### Manage the keys in the ssh-agent

- For the default ssh-agent, running only the commands will work:
  - Add keys to the agent:
``` bash
ssh-add ~/.ssh/ed_25519
```

  - List keys in the ssh-agent:
``` bash
ssh-add -L
```

  - Clear keys from the agent:
``` bash
ssh-add -D
```

Prepend the command with the environment variable to access other
  ssh-agents:

* Add keys to the agent:
```bash
SSH_AUTH_SOCK="$XDG_RUNTIME_DIR/<name>-agent.socket" ssh-add ~/.ssh/work
```

* List keys in the ssh-agent:
```bash
SSH_AUTH_SOCK="$XDG_RUNTIME_DIR/<name>-agent.socket" ssh-add -L
```

* Clear keys from the agent:
```bash
SSH_AUTH_SOCK="$XDG_RUNTIME_DIR/<name>-agent.socket" ssh-add -D
```

{: .note-title }
> Configuring
> **IdentityAgent** and **AddKeysToAgent** in `~/.ssh/config` will
> automatically add the key to the correct agent when you use it.


------------------------------------------------------------------------

## Gotchas

Debian auto-starts a ssh-agent at login.

- Comment or remove the line in `/etc/X11/Xsession.options` to stop it from starting:
```bash
sudo sed -i 's/^use-ssh-agent$/# use-ssh-agent/g' /etc/X11/Xsession.options
```

- `ssh-add -L` will only list keys in `$SSH_AUTH_SOCK`.
  - Specify the ssh-agent by passing the variable:
``` bash
SSH_AUTH_SOCK="$XDG_RUNTIME_DIR/<name>-agent.socket" ssh-add -L
```

- If using ssh-askpass, add the following to the service file:
```
# DISPLAY required for ssh-askpass to work
Environment=DISPLAY=:0
```

`ssh-agent` exits with code 2 which results in 'failed' state on stop and I found 2 options to remedy this:

- Inform systemd that a successful exit status is `2`:
``` ini
SuccessExitStatus=2
```
- Prefix the ExecStart with a `-` to suppress this behavior:
``` ini
ExecStart=-/usr/bin/ssh-agent -D -a %t/%i-agent.socket
```
- *Currently untested*: Enable linger for users who need the agents to be active while not logged in:
``` bash
loginctl enable-linger <user>
```

- <https://manpages.debian.org/bullseye/systemd/loginctl.1.en.html#User_Commands>

------------------------------------------------------------------------

## Example

After following the steps above, as an example I'll create a "default"
agent for my everyday ssh keys and a "work" agent for my work ssh keys.

#### Create "Default" SSH Agent

- Start and enable the "default" ssh-agent:
``` bash
systemctl --user enable --now ssh-agent@ssh.service
```

- Check status:
``` bash
systemctl --user status ssh-agent@ssh.service
```

- Configure environment for the "default" agent:
``` bash
cat << EOF >> ~/.profile
socketpath="$XDG_RUNTIME_DIR/ssh-agent.socket"
if [ -S "$socketpath" ]; then
  export SSH_AUTH_SOCK="$socketpath"
fi
EOF
```

- Source the file to load the variable:
``` bash
source ~/.profile
```

- Add keys to "Default" agent:
``` bash
ssh-add ~/.ssh/key
```

- List keys in "Default" agent:
``` bash
ssh-add -L
```

#### Create "Work" Agent

- Start and enable a "work" agent:
``` bash
systemctl --user enable --now ssh-agent@work.service
```

- Check the status:
``` bash
systemctl --user status ssh-agent@work.service
```

- Add entries for work machines:
``` bash
Host work-workmachine-1
    HostName        XX.XX.XX.XX
    ForwardAgent    "/run/user/%i/work-agent.socket"
    ProxyJump       work-jump
```

- Add wildcard entry for work machines at **bottom** of `~/.ssh/config`:
``` bash
Host work-*
    User            username
    IdentityFile    "%d/.ssh/work"
    IdentityAgent   "/run/user/%i/work-agent.socket"
```

- Add keys to "Work" agent:
``` bash
SSH_AUTH_SOCK="XDG_RUNTIME_DIR/work-agent.socket" ssh-add ~/.ssh/work
```

- List keys in "Work" agent:
``` bash
SSH_AUTH_SOCK="XDG_RUNTIME_DIR/work-agent.socket" ssh-add -L
```


{: .note-title }
> Configuring
> **IdentityAgent** and **AddKeysToAgent** in `~/.ssh/config` will add the
> key to the correct agent when you first use it.


------------------------------------------------------------------------

## Bonus Tip

- You can create a `ssh` directory in your `$XDG_RUNTIME_DIR` to contain
  the agent socket files.
- This is a good opportunity to make use of systemd's ''tmpfiles.d'' to
  create the directory at boot.
- Create directory to hold the config files:
``` bash
mkdir -p ~/.local/share/user-tmpfiles.d
```

- Create a configuration file:
``` bash
cat << EOF > ~/.local/share/user-tmpfiles.d/ssh-config.conf
d %t/ssh 0700 - - -
EOF
```
- Create the directory:
``` bash
systemd-tmpfiles --user --create
```

- Enable the tmpfiles service so it creates the directory at boot:
``` bash
systemctl --user enable --now systemd-tmpfiles-setup.service
```

- Enable the cleanup timer:
``` bash
systemctl --user enable --now systemd-tmpfiles-clean.timer 
```

- Edit the paths in the files above to add the `ssh` dir. For example:
``` ini
Environment=SSH_AUTH_SOCK=%t/ssh/ssh-agent.socket
```


{: .note-title }
> For multi-user systems,
> make sure to add/configure files in `/etc/skel` so the agent
> dependencies are set up during user creation.


------------------------------------------------------------------------

## Conclusion

That's the general idea and should get your system set up with as many
ssh-agents as you would ever want to create. Enjoy!

------------------------------------------------------------------------

## Links

- <https://manpages.debian.org/stable/openssh-client/ssh-agent.1.en.html>
- <https://manpages.debian.org/stable/systemd/systemd.service.5.en.html#SERVICE_TEMPLATES>
- <https://manpages.debian.org/stable/systemd/systemd.unit.5.en.html#SPECIFIERS>
- <https://manpages.debian.org/stable/openssh-client/ssh-agent.1.en.html>
- <https://manpages.debian.org/stable/openssh-client/ssh_config.5.en.html>
- <https://manpages.debian.org/stable/openssh-client/ssh-add.1.en.html>
- <https://manpages.debian.org/stable/systemd/tmpfiles.d.5.en.html>
- <https://manpages.debian.org/stable/systemd/systemd-tmpfiles.8.en.html>
- <https://wikitech.wikimedia.org/wiki/Managing_multiple_SSH_agents>
- <https://unix.stackexchange.com/a/623559>
