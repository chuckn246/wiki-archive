# Manage GPG Keys

------------------------------------------------------------------------

## GPG Directory Permissions

```bash
find ~/.gnupg -type f -execdir chmod 600 {} \; # Set 600 for files
find ~/.gnupg -type d -execdir chmod 700 {} \; # Set 700 for directories
```

------------------------------------------------------------------------

## Generate GPG Key

- Create a key pair:
```bash
gpg2 --expert --full-gen-key
```

For general use most people want:

- RSA (Sign Only) and RSA (Encrypt only) key
- Default 2048 Value Keysize. [^1]
- An expiration date. A year is good enough for the average user. Can be
  extended without having to re-issue a new key.
- Name and email address
- NO optional comment.
- A secure passphrase

------------------------------------------------------------------------

## List GPG Keys

### List Public Keys

- List keys in your public key ring:
```bash
gpg --list-keys
```

### List Private Keys

- List keys in your secret key ring:
```bash
gpg --list-secret-keys
```

------------------------------------------------------------------------

## Export GPG Keys

In order to send keys to other users or backup your keys, you need to
export them.

### Export Public Key

#### To stdout

- Generate an ASCII version of your public key (eg. to distribure it by
  email):
```bash
gpg --armor --export <user-id>
```

#### To a File

- Generate an ASCII version of your public key (eg. to distribure it by
  email):
```bash
gpg --output public.key --armor --export <user-id>
```

------------------------------------------------------------------------

### Export Private Key

If you want to import the key on another computer to encrypt/sign, you
will need the private key.

- List private keys:
```bash
gpg2 --list-secret-keys
```

#### To stdout

- Generate an ASCII version of your public key (eg. to distribute it by
  email):
```bash
gpg --armor --export-secret-key <user-id>
```

#### To a File

- Generate an ASCII version of your public key (eg. to distribute it by
  email):
```bash
gpg --output public.key --armor --export-secret-key <user-id>
```

------------------------------------------------------------------------

### Send GPG Keys to a Keyserver

- Or use a keyserver to share your key:
```bash
gpg --send-keys <user-id>
gpg --keyserver pgp.mit.edu --send-keys <user-id>
gpg --keyserver keyserver.ubuntu.com --send-keys <user-id>
gpg --keyserver keys.gnupg.net --send-keys <user-id>
gpg --keyserver pool.sks-keyservers.net --send-keys <user-id>
```

------------------------------------------------------------------------

## Import GPG Keys

In order to encrypt messages to others, as well as to verivy their
signatures, you need their public key.

### Import from a File

- Import a key:
```bash
gpg --import public.key
```

### Import from a Keyserver

- To find out details of a key on the keyserver without importing it:
```bash
gpg --search-keys <user-id>
```

- To import a key from a key server:
```bash
gpg --recv-keys <user-id>
```

### Import from a Smart Card

- Check card for keys:
```bash
gpg --card-status
```

- Export keys from card:
```bash
gpg --card-edit

# Then enter
fetch

# Then quit
quit
```

------------------------------------------------------------------------

## Trust GPG Keys

The ownertrust reflects the level of trust, which you put into how
thoroughly you think, the key owner acts when signing other keys.
Trust-levels are not set for keys but for the certain key owners.

> [!IMPORTANT] Adjusting the ownertrust will not affect the validity
> of the key you are setting it for. It only concerns third party keys,
> which then may be signed by your friends. Depending on the ownertrust
> you have set for your friends keys, their signatures on keys you have in
> GPG Keychain, will have different implications.

- Edit a key:
```bash
gpg --edit-key [key-id]
```

- Set trust level:
```
gpg> trust
Please decide how far you trust this user to correctly verify other users' keys
(by looking at passports, checking fingerprints from different sources, etc.)

1 = I don't know or won't say
2 = I do NOT trust
3 = I trust marginally
4 = I trust fully
5 = I trust ultimately
m = back to the main menu

Your decision?
```

#### Unknown (1)

Nothing is known about the owner's judgement in key signing. Keys on
your public keyring that you do not own initially have this trust level.

The default state. It means, no ownertrust has been set yet. The key is
not trusted.

#### Never/None (2)

The owner is known to improperly sign other keys.

Trust-level is identical to 'Unknown / Undefined' i.e. the key is not
trusted. But in this case, you actively state, to never trust the key in
question. That means, you know that the key owner is not accurately
verifying other keys before signing them.

#### Marginal (3)

The owner understands the implications of key signing and properly
validates keys before signing them.

Will make a key show as valid, if it has been signed by at least three
keys which you set to 'Marginal' trust-level. Example: If you set
Alice's, Bob's and Peter's key to 'Marginal' and they all sign Ed's key,
Ed's key will be valid. Due to the complexity of this status, we do not
recommend using it.

#### Full (4)

The owner has an excellent understanding of key signing, and his
signature on a key would be as good as your own.

Used for keys, which you trust to sign other keys. That means, if
Alice's key is signed by your Buddy Bob, whose key you set the
ownertrust to Full, Alice's key will be trusted. You should only be
using Full ownertrust after verifying and signing Bob's key.

#### Ultimate (5)

Only used for your own keys. You trust this key 'per se'. Any message
signed with that key, will be trusted. This is also the reason why any
key from a friend, that is signed by you, will also show as valid
(green), even though you did not change the ownertrust of the signed
key. The signed key will be valid due to the ultimate ownertrust of your
own key.

------------------------------------------------------------------------

## Renew GPG Keys

So, now after the year has passed, we need to renew the sub-keys so they
will not expire.

- Edit key:
  ```bash
  gpg2 --edit-key <user-id>
  ```
- Expire:
  ```bash
  gpg> expire
  ```
- Set expiration length of the **primary** key:
  ```bash
  Key is valid for? (0) 0
  ```
- Select all sub keys:
  ```bash
  gpg> key 1
  gpg> key 2
  gpg> key 3
  ```
- Expire the **sub** keys:
  ```bash
  gpg> expire
  ```
- Set expiration length of **sub** keys:
```bash
Key is valid for? (0) 1y
```

- Save changes:
```bash
gpg> save
```

#### Update the keys on keyserver

- Update the keys on keyservers:
```bash
gpg --keyserver pgp.mit.edu --send-keys <user-id>
gpg --keyserver keyserver.ubuntu.com --send-keys <user-id>
gpg --keyserver keys.gnupg.net --send-keys <user-id>
gpg --keyserver pool.sks-keyservers.net --send-keys <user-id>
```

------------------------------------------------------------------------

## Delete GPG Keys

- List keys:
```bash
gpg2 --list-keys
```

- Delete key:
```bash
gpg2 --delete-key <keyID> [<keyID> <keyID>...]
```

When you generate keys then both public and private keys are generated.

- Delete private key:
```bash
gpg --delete-secret-key <keyID>
```

- Then delete public key:
```bash
gpg2 --delete-key <keyID>
```

------------------------------------------------------------------------

## Links

[^1]: [External Link](https://www.gnupg.org/faq/gnupg-faq.html#no_default_of_rsa4096)
