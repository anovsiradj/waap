# httpd (Apache HTTP Server)

### persiapan

- unduh `httpd.zip` dari https://www.apachelounge.com/download/
- lalu ekstrak ke dalam folder `./httpd/`
- unduh `mod_fcgid.zip` dari https://www.apachelounge.com/download/
- lalu ekstrak `mod_fcgid.so` ke dalam folder ke `./httpd/modules/`

### kebutuhan module

- `access_compat_module` supaya bisa pake `[deny,allow]` di versi baru httpd, untuk kebutuhan legacy project.
- `rewrite_module`
- `expires_module`
- `headers_module`
- `cache_module`

### instalasi dengan service

berdasarkan [dokumentasi](https://httpd.apache.org/docs/current/platform/windows.html#winsvc),
ada beberapa perintah yang perlu dilakukan untuk memasang service:

```cmd
C:\waap\httpd\bin\httpd.exe -k install -n "waap_httpd"
C:\waap\httpd\bin\httpd.exe -n "waap_httpd" -t
C:\waap\httpd\bin\httpd.exe -k uninstall -n "waap_httpd"

C:\waap\httpd\bin\httpd.exe -k start -n "waap_httpd"
C:\waap\httpd\bin\httpd.exe -k restart -n "waap_httpd"
C:\waap\httpd\bin\httpd.exe -k stop -n "waap_httpd"
```

(untuk penamaan service `waap_httpd` bisa disesuaikan kebutuhan)

### catatan

penyedia binary disarankan menggunakan apachelounge, dikarenakan apachehaus sedang hiatus.

- https://forum.apachehaus.com/announcements/apache-haus-project-is-on-hold/msg4727/#msg4727
- https://forum.apachehaus.com/index.php?topic=1761.msg4799#msg4799
