# KeepassXC as the System Keyring

------------------------------------------------------------------------

## Description

It is possible to use [KeePassXC](https://keepassxc.org/) as the system
keyring.


{: .note-title }
> The following information requires at least
> KeePassXC 2.5.0 installed.


------------------------------------------------------------------------

## Configure

- Stop gnome-keyring if it's installed. \* ''pgrep -l gnome''
  - `pkill pid`
- Create a new group in the database that will hold the passwords used
  for the keyring
- **Tools \> Settings \> Secret Service Integration \>**
  - Enable KeepassXC Freedesktop.org Secret Service integration
- **Database \> Database Settings \> Secret Service Integration \>
  Expose entries under this group**:
  - Select the new group

------------------------------------------------------------------------

### Disable gnome-keyring

Create 3 .desktop files and place them in `~/.config/autostart`:

- **gnome-keyring-pkcs11.desktop**:
  ``` ini
  [Desktop Entry]
  Hidden=true
  ```
- **gnome-keyring-secrets.desktop**:
  ``` ini
  [Desktop Entry]
  Hidden=true
  ```
- **gnome-keyring-ssh.desktop**:
  ``` ini
  [Desktop Entry]
  Hidden=true
  ```
- <https://unix.stackexchange.com/questions/271661/disable-gnome-keyring-daemon>

------------------------------------------------------------------------

## Accessing Entries

- Using [secret-tool](secret-tool.md)
- Using [keyring](keyring.md)

------------------------------------------------------------------------

## Entries

There are different fields that are stored in the **Advanced \>
Attributes** section of each entry.

You can create your own key:value pairs for easier access and searching
of specific entries.

Here's a couple examples:

### Nextcloud Desktop

##### General

    Title: Nextcloud Desktop
    Username: username
    Password: *******
    URL: https://path.to.nextcloud

##### Advanced

    Type: Password
    Use: Saved password or login
    server: Nextcloud
    type: plaintext
    user: username:https://path.to.nextcloud/:0

------------------------------------------------------------------------

### Thunar

You can configure access to remote filesystems for browsing in Thunar.

##### General

- The double `//` is not a typo.
- The password field should contain the password for the ssh key.

<!-- -->

    Title: username@hostname//home/username/.ssh/key
    Username: username
    Password: ********

##### Advanced

    authtype: publickey
    object: /home/username/.ssh/key
    protocol: sftp
    server: hostname
    user: username
    xdg:schema: org.gnome.keyring.NetworkPassword

------------------------------------------------------------------------

### keyring entries

Entries created with [keyring](keyring.md) have the
following attributes

##### General

    Title: Password for 'username' on 'service'
    Username: username
    Password: ********

##### Advanced

    application: Python keyring library
    service: twitter
    username: username

------------------------------------------------------------------------

## Suggestions

- I would recommend creating (at minimum) the following attributes every
  time for each entry:
  ``` bash
  secret-tool store --label='My Label' service <service> username <username>
  ```
- This way, it will be available to
  [python3-keyring](keyring.md) as well.

------------------------------------------------------------------------

## Links

- <https://www.cogitri.dev/posts/03-keepassxc-freedesktop-secret/>
- <https://www.reddit.com/r/linux/comments/ehfhud/keyring_alternative_access_keepassxc_entries_of/>
- <https://rtfm.co.ua/en/keepass-an-mfa-totp-codes-a-browsers-passwords-ssh-keys-passwords-storage-configuration-and-secret-service-integration/>
- <https://isamert.net/jekyll/update/2018/10/05/automatize-your-logins-with-gnome-keyring-and-keepassxc.html>
- <https://rtfm.co.ua/en/keepass-ssh-keys-passwords-storage-and-decryption-on-linux/>
