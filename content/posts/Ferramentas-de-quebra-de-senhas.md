---
title: "Ferramentas De Quebra De Senhas"
date: 2020-09-30T20:58:15-03:00
draft: true
---

Ferramentas de Quebra de Senhas

Hydra

O Hydra é uma ferramenta famosa que realiza ataque de dicionário a serviços. Seu uso é, basicamente, assim:

hydra -l <login> -p <senha> <IP> <serviço> -t <tasks>

Abaixo, um exemplo de uma tentativa única (-t 1) com o usuário root (-l root) e a senha 12345 (-p 12345) no endereço 10.0.2.2 no serviço ssh: 

>hydra -l root -p 12345 10.0.2.2 ssh -t 1 

Podemos passar um dicionário de logins e senhas com o parâmetro -L e -P: 

```
hydra -L <arquivo_login> -P <arquivo_senha> <IP> <serviço>

hydra -L login.txt -P senha.txt 10.0.2.2 ssh -t 4
```

O Hydra também possui uma interface gráfica que pode ser chamada com o comando:

xhydra 

Medusa

Assim como o Hydra, o Medusa realiza ataque de dicionário a serviços. Seu uso é basicamente:

Para listar os módulos

medusa -q | more

Comando: 


medusa -h <ip> -u <usuario> -p <senha> -M <modulo>

medusa -h 10.10.100.25 -u admin -p 1234 -M ftp

Lista de IP, usuários e senhas

medusa -H <ips> -U <usuarios> -P <senhas> -M <modulo>

medusa -H hosts.txt -U users.txt -P pass.txt -M smbnt

John the Ripper

O John the Ripper (o nome da ferramenta faz alusão a um famoso psicopata do século 19, Jack, o Estripador) é uma das ferramentas mais usadas em pentest, sendo ele um utilitário que faz quebra de senhas de três modos:

    WordList → Ele tenta por uma Wordlist, testando as combinaçõesde senha/usuário.

    Single Crack → Ele tenta quebrar a senha usando as informaçõesde login.

    Incremental → Sendo o modo mais robusto no John the Ripper,ele tentará cada caractere possível até achar a senha correta. Epor esse motivo, é indicado o uso de parâmetros com o intuito dereduzir o tempo de quebra.

No caso do modo incremental, é necessário ter o arquivo contendo o hash da senha do usuário (SAM no Windows ou /etc/shadow no Linux).

Seu uso é basicamente: 


john <arquivo> --wordlist=dicionario.txt

john <arquivo> --single

john <arquivo> --incremental

john <arquivo> --wordlist=dicionario.txt --format=NT

As senhas quebradas são armazenadas no arquivo:

<home_do_usuário)>/.john/john.pot

E assim como o Hydra, o JtR também tem uma Interface Gráfica, que pode ser chamada pelo comando:

johnny


OphCrack

O OphCrack é uma ferramenta nativa do Kali Linux e específica para uso com Rainbow Tables. Com uma interface gráfica bem intuitiva, o OphCrack é ideal para realizar ataques de Brute Force em sistemas Windows. 

Hashcat

Também nativo do Kali, o Hashcat é uma ferramenta específica para realizar ataques do tipo Password Cracking. Uma das features mais interessantes dela é a possibilidade de se utilizar o processador da placa de vídeo para dar mais performance ao ataque.

Seu uso é basicamente: 

hashcat -m <tipo do hash> -a <tipo do ataque> -o <arquivo de saída> <arquivo de hash> <dicionário> 

Exemplo:

hashcat -m 1800 -a 0 -o cracked.txt /etc/shadow /usr/share

/usr/share/wordlists/rockyou.txt

Caso os drivers da placa de vídeo não estejam instalados, é necessário utilizar a opção --force, desta forma:

hashcat -m 1800 -a 0 -o cracked.txt /etc/shadow /usr/share /usr/share/wordlists/rockyou.txt --force 


Metasploit Framework

O Metasploit (MSF) é um framework criado por H.D.Moore, que serve para elaboração e execução de um repositório de exploits. 

Apesar de não ser esse o objetivo da ferramenta, o MSF possui módulos de ataque Força Bruta para diversas aplicações, como, por exemplo, o SSH, que pode ser executado por meio da sequência de comandos abaixo: 

```
service postgresql start

msfconsole

use <auxiliar>

auxiliary/scanner/ssh/ssh_login

auxiliary/scanner/ftp/ftp_login

auxiliary/scanner/smb/smb_login

auxiliary/scanner/telnet/telnet_login

show options

set <parametros>

run

```