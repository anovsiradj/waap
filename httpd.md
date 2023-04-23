
# persiapan

- unduh `httpd.zip` dari https://www.apachelounge.com/download/
- lalu ekstrak ke dalam folder `./httpd/`

- unduh `mod_fcgid.zip` dari https://www.apachelounge.com/download/
- lalu taruh berkas `mod_fcgid.so` ke dalam folder `./httpd/modules/`

# kebutuhan modules

- `access_compat_module` supaya bisa pake `[Deny,Allow]` pada versi apache baru (karena legacy projects).
- `rewrite_module`
- `expires_module`
- `headers_module`

# pemasangan service

berdasarkan [dokumentasi](https://httpd.apache.org/docs/current/platform/windows.html#winsvc),
ada beberapa perintah yang perlu dilakukan untuk memasang service:

```cmd
D:\server\httpd\bin\httpd.exe -k install -n "AnoopApache"
D:\server\httpd\bin\httpd.exe -n "AnoopApache" -t
D:\server\httpd\bin\httpd.exe -k uninstall -n "AnoopApache"

D:\server\httpd\bin\httpd.exe -k start -n "AnoopApache"
D:\server\httpd\bin\httpd.exe -k restart -n "AnoopApache"
D:\server\httpd\bin\httpd.exe -k stop -n "AnoopApache"
```

(penamaan service disesuaikan kebutuhan pribadi)

# catatan

provider untuk binary disarankan dari apachelounge, dikarenakan [apachehaus sedang hiatus](https://forum.apachehaus.com/announcements/apache-haus-project-is-on-hold/msg4727/#msg4727).
