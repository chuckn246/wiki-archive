# keyring

------------------------------------------------------------------------

## Description

**keyring** provides a way to store, lookup and delete passwords in
various backends supported by Python-Keyring.

------------------------------------------------------------------------

## Install

### apt

- Install using apt:
  ``` bash
  sudo apt install python3-keyring
  ```

### pip

- Install using pip:
  ``` bash
  python3 -m pip install --user keyring
  ```

------------------------------------------------------------------------

## Usage

### Python

You can set/get entries from a Python script or from the Python terminal

- Add an entry:
  ``` python
  import keyring
  keyring.set_password("system", "username", "password")
  ```
- Add an entry but prompt for password:
  ``` python
  import keyring
  keyring.set_password('twitter', 'xkcd', getpass.getpass())
  ```
- Retrieve a password:
  ``` python
  import keyring
  keyring.get_password("system", "username")
  ```

------------------------------------------------------------------------

### CLI

You can set/get entries directly from the command line or from bash
scripts, etc.

- Set a password:
  ``` bash
  keyring set SERVICE USERNAME
  ```
- Retrieve a password:
  ``` bash
  keyring get SERVICE USERNAME
  ```
- Delete a password:
  ``` bash
  keyring del SERVICE USERNAME
  ```
- Show help:
  ``` bash
  keyring --help
  ```

------------------------------------------------------------------------

## Details

The commands above will set the following attributes on an entry:

- For example, set a twitter password:
  ``` bash
  keyring set twitter chuckn246
  ```
- Will create an entry with the Title:
  - Password for 'chuckn246' on 'twitter'
- Will set these attributes on the entry:
  - **application**: Python keyring library
  - **service**: twitter
  - **username**: chuckn246

##### Small Gotcha

- Note that the attribute username is different than the entry UserName
  (Note capitalization).
  ``` bash
  secret-tool search service twitter
  [/org/freedesktop/secrets/collection/TestDB/xxxxxxx]
  label = Password for 'chuckn246' on 'twitter'
  secret = twitterpassword
  created = 2020-05-08 22:17:06
  modified = 2020-05-08 22:17:06
  schema = (null)
  attribute.Path = /Password for 'chuckn246' on 'twitter'
  attribute.Uuid = 3174d145b5e74435ab15cf45a5d805cb
  attribute.UserName = chuck
  attribute.service = twitter
  attribute.URL = 
  attribute.Notes = 
  attribute.application = Python keyring library
  attribute.username = chuckn246
  attribute.Title = Password for 'chuckn246' on 'twitter'
  ```

------------------------------------------------------------------------

## Ansible

- Create entry for ansible:
  ``` bash
  keyring set ansible_vault ansible_user
  ```
- Create a python script to decrypt vault files
  `vim ~/.ansible/.vault_password`:
  ``` python
  #!/usr/bin/env python3
  import keyring
  vault_password=keyring.get_password("ansible_vault", "ansible_user")
  print(vault_password)
  ```
- Make script executable:
  ``` bash
  chmod 700 ~/.ansible/.vault_password
  ```
- Edit `ansible.cfg`:
  ``` ini
  vault_password_file = ~/.ansible/.vault_password
  ```

------------------------------------------------------------------------

## Links

- Python-Keyring command-line utility:
  <https://pypi.org/project/keyring/>
