# Virtual Terminal Color

The following notes apply to [virtual terminals]{.underline} such as
`/dev/tty1`, `/dev/tty2`, etc.

You use these terminals when you log in without a display manager (eg.
LightDM) or when you use a command such as `<ctrl>` + `<alt>` + `<F2>`.

These settings will *not* apply to a terminal emulator such as
**urxvt**, **st** or **xterm** etc. They will need to to be configured
separately.

------------------------------------------------------------------------

## Applying a VT Colorscheme at boot


{: .note }
> The following instructions were created on
> Debian 10 (buster).
>
> They *should* work on Ubuntu and other Debian based distributions as
> well.


### Setting Up

- If it's not already installed, install ''kbd'':
``` bash
sudo apt install kbd
```

------------------------------------------------------------------------

### Modify initramfs

Add the **setvtrgb** executable to the **initramfs** so that it's
available during boot.

- Create a shell script in the hooks directory:
``` bash
sudoedit /etc/initramfs-tools/hooks/setvtrgb_hook
```

- And add the contents:
``` sh
#!/bin/sh
PREREQ=""
prereqs()
{
    echo "$PREREQ"
}

case $1 in
prereqs)
    prereqs
    exit 0
    ;;
esac

. /usr/share/initramfs-tools/hook-functions

copy_exec /usr/bin/setvtrgb /bin
```

- Set the script to be executable:
``` bash
sudo chmod +x /etc/initramfs-tools/hooks/setvtrgb_hook
```

------------------------------------------------------------------------

### Choose a colorscheme


{: .tip }
> Test the colorscheme by running the script then clearing
> the terminal. This way you can see which one you like ahead of time.


- Copy one of the [Colorschemes](#vt-colorschemes) from below (or create
  your own) to:
  - `/etc/initramfs-tools/scripts/init-top/`
    - I chose the **init-top** directory because it gets called as early
      as possible into the boot process.
    - Refer to **man initramfs-tools** BOOT SCRIPTS section and change
      it to suit your needs.
- Set the script to be executable:
``` bash
sudo chmod +x /etc/initramfs-tools/scripts/init-top/my_colorscheme
```

------------------------------------------------------------------------

### Update initramfs

After completing the above steps, we will generate the new initramfs

- Update the initramfs:
  ``` bash
  sudo update-initramfs -u
  ```
- Verify that **setvtrgb** was added:
  ``` bash
  lsinitramfs -l /boot/initrd.img-4.19.0-9-amd64 | grep setvtrgb
  ```

  - *make sure to modify the above command to point to your initrd*
- Reboot

------------------------------------------------------------------------

## Applying a VT Colorscheme after boot

If you use Plymouth, a display manager or frankly just don't care if the
boot process terminal has custom colors, you can create a systemd
service to load the colors after login.

- Copy or create a [colorscheme](#vt-colorschemes) somewhere such as
  `/etc/custom-vt-colors`.
- Create a systemd service:
  ``` bash
  sudoedit /etc/systemd/system/custom-vt-colors.service
  ```
- Add the contents:
  ``` sh
  [Unit]
  Description=Load custom VT color palette

  [Service]
  Type=oneshot
  ExecStart=/usr/bin/setvtrgb /etc/custom-vt-colors

  [Install]
  WantedBy=multi-user.target
  ```
- Start and enable the service:
  ``` bash
  sudo systemctl enable --now custom-vt-colors.service
  ```

\

------------------------------------------------------------------------

## VT Colorschemes

For the colorschemes below (except default), I imported the Xresources
of each colorscheme to <https://terminal.sexy> to convert the hex values
to rgb quickly. Then I created the files using those rgb values.

#### Default

- [Default VT Colorscheme](colorscheme/default.md#default-vt-colorscheme)

#### Dracula

- [Dracula VT Colorscheme](colorscheme/dracula.md#dracula-vt-colorscheme)

#### Gruvbox

- [Gruvbox Dark VT Colorscheme](colorscheme/gruvbox_dark.md#gruvbox-dark-vt-colorscheme)
- [Gruvbox Light VT Colorscheme](colorscheme/gruvbox_light.md#gruvbox-light-vt-colorscheme)

#### Nord

- [Nord VT Colorscheme](colorscheme/nord.md#nord-vt-colorscheme)

#### Solarized

- [Solarized Dark Colorscheme](colorscheme/solarized_dark.md#solarized-dark-vt-colorscheme)
- [Solarized Light Colorscheme](colorscheme/solarized_light.md#solarized-light-vt-colorscheme)

------------------------------------------------------------------------

### VT Colorscheme Format

`setvtrgb` requires the input to be formatted properly for it to work.

Similar to Xresources, there are definable 16 colors ranging from
**color0** through **color15**. However, the colors need split into 3
lines with Red being the top line, Green being the middle line and Blue
being the bottom line. It should look like this (substituting the RGB
values of course):

    Red0,Red1,Red2,Red3,Red4,Red5,Red6,Red7,Red8,Red9,Red10,Red11,Red12,Red13,Rew14,Red15
    Green0,Green1,Green2,Green3,Green4,Green5,Green6,Green7,Green8,Green9,Green10,Green11,Green12,Green13,Rew14,Green15
    Blue0,Blue1,Blue2,Blue3,Blue4,Blue5,Blue6,Blue7,Blue8,Blue9,Blue10,Blue11,Blue12,Blue13,Rew14,Blue15

\
For a working example and/or to make a backup of the current settings:

- Save/view current vt colors in a **setvtrgb** usable format:
  ``` bash
  cat /sys/module/vt/parameters/default_{red,grn,blu} > ~/consolecolors
  ```

------------------------------------------------------------------------

#### Converting Hex Colors to RGB

- Convert hex values to rgb with each of r,g,b being on a newline:
  ``` bash
  #!/usr/bin/env bash

  hex_regex='^#?([[:xdigit:]]{6})$'

  # Check if input is valid hex
  if [[ "${1}" =~ ${hex_regex} ]]; then
    hexinput=$(echo "${1}" | tr '[:lower:]' '[:upper:]' | sed 's/#//g' )
  else
    printf '%s\n' "[ERROR] ${1} is not a valid hex color code" >&2 && exit 1
  fi

  # Print RGB output with each on it's own line
  printf '%d\n' "0x${hexinput:0:2}" "0x${hexinput:2:2}" "0x${hexinput:4:2}"

  # vim: ft=sh ts=2 sts=2 sw=2 sr et
  ```
- Run it:
  - `hexrgb.sh ff9900` or `hexrgb.sh \#ff9900` or `hexrgb.sh "#ff9900"`
  - Escaping or quoting the hex value starting with a \# is necessary
    else bash will think it's a comment.

------------------------------------------------------------------------

## References

### Colors

- `man initramfs-tools`
- `man setvtrgb`
- <https://superuser.com/a/1185870> - VT colors & systemd
- <https://stackoverflow.com/a/7254022> - Convert hex to rgb
- <https://serverfault.com/a/476699> - Adding executable to initramfs

### General

- <http://blog.startaylor.net/2016/05/30/howto-console/>
