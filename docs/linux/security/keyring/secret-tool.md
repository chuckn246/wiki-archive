# secret-tool

------------------------------------------------------------------------

## Description

Store and retrieve passwords from the keyring.

------------------------------------------------------------------------

## Install

### apt

- Install using apt:
  ``` bash
  sudo apt install libsecret-tools
  ```

------------------------------------------------------------------------

## Usage

- **Flags:**
  - `--label` = Mainly for GUI programs but can be used to retrieve a
    given secret.
  - `{attribute}` = Used by the secret-tool for retrieving or deleting a
    given secret.
  - `{value}` = Used by the secret-tool for retrieving or deleting a
    given secret.

<!-- -->

- Add an entry:
  ``` bash
  secret-tool store --label='My Label' {attribute} {value} {attribute2} {value2} [...]
  ```
- Retrieve a password:
  ``` bash
  secret-tool lookup {attribute} {value} {attribute2} {value2} [...]
  ```
- Show entries with similar key/values:
  ``` bash
  secret-tool search --all {attribute} {value} {attribute2} {value2} [...]
  ```
- Delete an entry:
  ``` bash
  secret-tool clear {attribute} {value} {attribute2} {value2} [...]
  ```

------------------------------------------------------------------------

### Searching

- Generic Formatting Example:
  ``` bash
  secret-tool search --all {attribute} {value} [...]
  ```
- Search `Title`:
  ``` bash
  secret-tool search --all Title name
  ```
- Search `UserName`:
  ``` bash
  secret-tool search --all UserName name
  ```
- Search `URL`:
  ``` bash
  secret-tool search --all URL https://www.url.com
  ```
- Search `Notes`:
  ``` bash
  secret-tool search --all Notes value
  ```

------------------------------------------------------------------------

## Tips

- Set an alias in `~/.bash_aliases`:
  ``` bash
  alias get_password1='secret-tool lookup {attribute} {value} {attribute2} {value2}'
  ```
- Use in docker:
  <https://www.marian-dan.ro/blog/storing-secrets-using-secret-tool/>

------------------------------------------------------------------------

### Use keyring for Ansible

- Create keyring entry:
  ``` bash
  secret-tool store --label='Ansible Playbook' service ansible_playbook username <username>
  ```
- Create variable in playbook:
  ``` yaml
  admin_user: "username"
  ansible_become_pass: "{{ lookup('community.general.keyring', 'ansible_playbook {{ admin_user }}') }}"
  ```
- <https://docs.ansible.com/ansible/latest/collections/community/general/keyring_lookup.html>

------------------------------------------------------------------------
