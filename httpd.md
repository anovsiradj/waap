# httpd (Apache HTTP Server)

### persiapan

- unduh `httpd.zip` dari https://www.apachelounge.com/download/
- lalu ekstrak ke dalam folder `./httpd/`
- unduh `mod_fcgid.zip` dari https://www.apachelounge.com/download/
- lalu ekstrak `mod_fcgid.so` ke dalam folder ke `./httpd/modules/`

### kebutuhan module

- `access_compat_module` supaya bisa pake `[deny,allow]` diversi terbaru httpd, untuk kebutuhan legacy project.
- `rewrite_module`
- `expires_module`
- `headers_module`
- `cache_module`

(untuk kebutuhan module bisa disesuaikan kasuka)

### konfigurasi `./httpd/conf/httpd.conf`

- awalan tambah `Include conf/httpd_envs.conf`
- cari dan ubah jadi `Define SRVROOT "${HTTPD_ROOT}"`
- cari dan ubah jadi `ServerAdmin "${SERVER_MAIL}"`
- cari dan ubah jadi `ServerName "${SERVER_HOST}"`
- cari dan ubah jadi `LogLevel notice`
- cari dan komen `Listen 80`
- cari dan tambah jadi `DirectoryIndex index.html index.php`
- akhiran tambah `Include conf/httpd_fcgi.conf`
- akhiran tambah `Include conf/httpd_hosts.conf`

### eksekusi console

httpd bisa dieksekusi langsung melalui console secara manual

```cmd
C:\waap\httpd\bin\httpd.exe -t
C:\waap\httpd\bin\httpd.exe
```

### instalasi service

beberapa perintah yang perlu dilakukan untuk instalasi service

```cmd
C:\waap\httpd\bin\httpd.exe -k install -n "waap_httpd"
C:\waap\httpd\bin\httpd.exe -n "waap_httpd" -t
C:\waap\httpd\bin\httpd.exe -k uninstall -n "waap_httpd"

C:\waap\httpd\bin\httpd.exe -k start -n "waap_httpd"
C:\waap\httpd\bin\httpd.exe -k restart -n "waap_httpd"
C:\waap\httpd\bin\httpd.exe -k stop -n "waap_httpd"
```

(untuk penamaan service `waap_httpd` bisa disesuaikan kasuka)

### catatan

penyedia binary disarankan menggunakan apachelounge, dikarenakan apachehaus sedang hiatus.

- https://forum.apachehaus.com/announcements/apache-haus-project-is-on-hold/msg4727/#msg4727
- https://forum.apachehaus.com/index.php?topic=1761.msg4799#msg4799

### referensi

- https://httpd.apache.org/docs/current/platform/windows.html#winsvc
