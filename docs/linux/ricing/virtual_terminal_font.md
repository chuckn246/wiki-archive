# Virtual Terminal Font

Nothing too exciting yet..

------------------------------------------------------------------------

- Change the font & size interactively:
``` bash
sudo dpkg-reconfigure -plow console-setup
```
- Change the font & size manually:
``` bash
sudoedit /etc/default/console-setup
```
- VT font directory is:
``` bash
/usr/share/consolefonts
```
- Show current font. (Run in a tty):
``` bash
showconsolefont
```

------------------------------------------------------------------------

## References

### Fonts

- `man console-setup`

### General

- <http://blog.startaylor.net/2016/05/30/howto-console/>
