# gnome-keyring

------------------------------------------------------------------------

## Description

The Gnome Keyring stores secrets, passwords, keys, certificates and
makes them available to applications. It is integrated with the user's
login so their secret storage can be unlocked when the user logins to
the session.

------------------------------------------------------------------------

## Manage

### seahorse

You can manage gnome-keyring entries by installing the `seahorse`
package.

- Install `seahorse`:
  ``` bash
  sudo apt install seahorse
  ```

------------------------------------------------------------------------

### secret-tool

See [secret-tool](secret-tool.md) for more info.

`{attribute} {value}` references key:value pairs stored under the
Advanced section of an Entry.

- Create entry:
  ``` bash
  secret-tool store --label='My Label' {attribute} {value} {attribute2} {value2} [...]
  ```
- Retrieve an entry:
  ``` bash
  secret-tool lookup {attribute} {value} {attribute2} {value2} [...]
  ```

------------------------------------------------------------------------

### keyring

See [keyring](keyring.md) for more info.

#### Python

- Create an entry:
  ``` python
  import keyring
  keyring.set_password("system", "username", "password")
  ```
- Retrieve a password:
  ``` python
  import keyring
  keyring.get_password("system", "username")
  ```

#### cli

- Create an entry:
  ``` bash
  keyring set SERVICE USERNAME
  ```
- Retrieve an entry:
  ``` bash
  keyring get SERVICE USERNAME
  ```
- Delete an entry:
  ``` bash
  keyring del SERVICE USERNAME
  ```

------------------------------------------------------------------------

## Reset

- Resetting everything (delete all passwords and start new keyring):
      rm ~/.local/share/keyrings/login.keyring

------------------------------------------------------------------------

## Reuse

Using the same keyring (resetting keyring password but keeping old
passwords in keyring):

- Change directories:
  ``` bash
  cd ~/.local/share/keyrings/
  ```
- Rename the existing keyring:
  ``` bash
  mv login.keyring login.keyring.backup
  ```
- Create a new keyring file from Gnome Keyring with the name `login`
- Replace the new keyring file with the backup of the old keyring file
      mv login.keyring.backup login.keyring      
- <https://askubuntu.com/a/65294>

------------------------------------------------------------------------

## Links

- <https://wiki.archlinux.org/index.php/GNOME/Keyring>
- <https://wiki.gnome.org/action/show/Projects/GnomeKeyring>
- <https://rtfm.co.ua/en/what-is-linux-keyring-gnome-keyring-secret-service-and-d-bus/>
