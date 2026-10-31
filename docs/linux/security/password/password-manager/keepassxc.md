# KeePassXC

------------------------------------------------------------------------

## Description

Awesome GUI Password Manager.

------------------------------------------------------------------------

## Install

### apt

- Install using apt:
  ``` bash
  sudo apt install keepassxc
  ```

------------------------------------------------------------------------

### AppImage

- Download the AppImage, GPG Key, and SHA Digest:
  <https://keepassxc.org/download/>
- Import KeePassXC's gpg signing key:
  ``` bash
  gpg --fetch-keys https://keepassxc.org/keepassxc_master_signing_key.asc
  ```
- GPG Verify the signature file:
  ``` bash
  gpg --verify KeePassXC-*.sig
  ```
- Verify integrity of the AppImage:
  ``` bash
  sha256sum -c KeePassXC-*.AppImage.DIGEST
  ```
- Move the AppImage to somewhere in your `$PATH`:
  ``` bash
  mv ~/Downloads/KeePassXC-*.AppImage ~/.local/bin/keepassxc
  ```
- Make the AppImage executable:
  ``` bash
  chmod u+x ~/.local/bin/keepassxc
  ```
- Create a `.desktop` file:
  ``` ini
  [Desktop Entry]
  Name=KeePassXC
  GenericName=Community Password Manager
  Exec="keepassxc" %U
  Icon=appimagekit-keepassxc
  Terminal=false
  Type=Application
  Categories=Qt;Utility;
  MimeType=application/x-keepass2;
  X-Desktop-File-Install-Version=0.22
  ```

------------------------------------------------------------------------

#### Script it!

- Here's a script I wrote to install/update the AppImage:
  ``` bash
  #!/usr/bin/env bash

  latest="https://api.github.com/repos/keepassxreboot/keepassxc/releases/latest"

  # Import keepassxc's gpg key
  if ! gpg --list-keys 0xCFB4C2166397D0D2; then
    gpg --fetch-keys https://keepassxc.org/keepassxc_master_signing_key.asc
  fi

  printf '\n%b\n\n' "\e[1;34mDownloading the files.\e[0m"

  # Download the files
  curl -s "$latest" | awk -F': ' '/browser_download_url/ && /\.AppImage/ && !/zsync/ {gsub(/"/, "", $(NF)); system("curl -LO " $(NF))}'

  # Verify and install the appimage
  printf '\n%b\n\n' "\e[1;34mVerifying the files.\e[0m"
  if shasum -c KeePassXC-*.AppImage.DIGEST; then
    if gpg --verify KeePassXC*.AppImage.sig KeePassXC*.AppImage; then
      mv -f KeePassXC*.AppImage ~/.local/bin/keepassxc && \
      chmod +x ~/.local/bin/keepassxc && \
      pkill -f keepassxc && \
      gtk-launch keepassxc.desktop && \
      rm -f KeePassXC*.AppImage*
    else
      printf '\n%b\n' "\e[1;31m[ERROR] Problem with signature!\e[0m"
    fi
  else
    printf '\n%b\n' "\e[1;31m[ERROR] Problem with checksum!\e[0m"
  fi
  ```

------------------------------------------------------------------------

## keepassxc-cli

There's a small difference in using the ''keepassxc-cli'' depending on
the method used to install. Note the hyphen `-` usage.

- Installed using the apt instructions above:
  ``` bash
  keepassxc-cli help
  ```
- Installed using the AppImage instructions above:
  ``` bash
  keepassxc cli help
  ```

------------------------------------------------------------------------

## Links

- <https://keepassxc.org>
- <https://keepassxc.org/verifying-signatures/>
- <https://keepassxc.org/docs/KeePassXC_UserGuide.html>
- <https://packages.debian.org/bullseye/keepassxc>
- <https://manpages.debian.org/testing/keepassxc/keepassxc.1.en.html>
- <https://manpages.debian.org/unstable/keepassxc/keepassxc-cli.1.en.html>
