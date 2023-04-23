
# instalasi

- cek isi zip httpd
- rename folder lama
- "zip extract here", tidak usah rename folder baru.

# konfigurasi fastcgi

- download di apachelounge
- copas `mod_fcgid.so` ke `httpd/modules/`

# instalasi service

```cmd
D:\server\httpd\bin\httpd.exe -k install -n "AnoopApache"
D:\server\httpd\bin\httpd.exe -n "AnoopApache" -t
D:\server\httpd\bin\httpd.exe -k uninstall -n "AnoopApache"

D:\server\httpd\bin\httpd.exe -k start -n "AnoopApache"
D:\server\httpd\bin\httpd.exe -k restart -n "AnoopApache"
D:\server\httpd\bin\httpd.exe -k stop -n "AnoopApache"
```
