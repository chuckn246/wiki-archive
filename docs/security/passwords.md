# Passwords

Password things.

------------------------------------------------------------------------

## Password Generation

### General Usage

- [diceware](../linux/security/password/password-generator/diceware.md) -
  Generates passwords using the diceware list.
- [makepasswd](../linux/security/password/password-generator/makepasswd.md) -
  Generates random alphanumeric passwords and/or encrypts a plaintext
  password of your choice.
- Generate password using `base64` and `/dev/urandom`:
  ``` bash
  head -c50 /dev/urandom | base64
  ```

------------------------------------------------------------------------

### Formatted for /etc/shadow

- [mkpasswd](../linux/security/password/mkpasswd.md)
  - sha-512:
    ``` bash
    mkpasswd --method=sha-512
    ```
  - yescrypt:
    ``` bash
    mkpasswd --method=yescrypt
    ```
- **openssl**:
  - sha-512:
    ``` bash
    openssl passwd -6
    ```
- **python3**:
  - sha-512:
    ``` bash
    python3 -c 'import crypt, getpass; print(crypt.crypt(getpass.getpass()))'
    ```

------------------------------------------------------------------------

## Password Managers

- [KeePassXC](../linux/security/password/password-manager/keepassxc.md) -
  Generates and stores random alphanumeric and diceware passwords.
- [pass](../linux/security/password/password-manager/pass.md) - Generates and
  stores random alphanumeric passwords.
- [Linux Keyring](../linux/security/keyring.md) - Stores passwords

------------------------------------------------------------------------
