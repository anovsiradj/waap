# php

### persiapan

- copas dari `./php.ini.stub` jadi `./php.ini`
- unduh setiap versi yang dibutuhkan
- ekstrak ke `./` dengan penamaan folder `php` atau dengan penamaan menggunakan prefix `php` (contoh `php5` atau `php7`).
- copas `/php/php.ini` dari `/php/php.ini-development` lalu atur setiap versinya
- hapus komen `extension_dir` setiap versinya

### kebutuhan extension

- `curl`
- `intl`
- `gd` atau `gd2`
- `exif`
- `fileinfo`
- `mbstring`
- `openssl`
- `odbc`
- `pgsql`
- `mysql`
- `mysqli`
- `sqlite3`
- `pdo`
- `pdo_odbc`
- `pdo_mysql`
- `pdo_pgsql`
- `pdo_sqlite`
- `zip`

### catatan

- pada `./php.ini` penulisan konfigurasi, jangan pake spasi sebelum dan sesudah "=" karena tidak jalan di php5.
- pada `./php.ini` awalan file jangan kasih komen, entah kenapa jadi gak jalan.

### referensi

- https://windows.php.net/download/
- https://windows.php.net/downloads/releases/archives/
- https://museum.php.net/
- https://mlocati.github.io/articles/php-windows-imagick.html
